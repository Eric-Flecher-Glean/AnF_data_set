# Integration Guide

## Overview

This guide explains how conversational data integrates with existing structured data (folders 01-06) and how to maintain cross-reference integrity.

## Integration Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 Structured Data Layer                        │
│  ┌────────────┬────────────┬────────────┬────────────┐      │
│  │ 01_Store   │ 02_Build   │ 03_Histor  │ 04_Region  │      │
│  │  Profiles  │  Templates │  Projects  │  Factors   │      │
│  └─────┬──────┴─────┬──────┴─────┬──────┴─────┬──────┘      │
│        │            │            │            │             │
│  ┌─────┴──────┬─────┴──────┬─────┴──────┬─────┴──────┐      │
│  │ 05_Cost    │ 06_Constr  │            │            │      │
│  │  Models    │  Rules     │            │            │      │
│  └─────┬──────┴─────┬──────┘            │            │      │
└────────┼────────────┼───────────────────┼────────────┼──────┘
         │            │                   │            │
         ▼            ▼                   ▼            ▼
┌─────────────────────────────────────────────────────────────┐
│          Conversational Data Layer (07_Conversations)        │
│  ┌──────────────────┬───────────────────┬────────────────┐  │
│  │ Meeting          │ Teams             │ Metadata       │  │
│  │ Transcripts      │ Conversations     │                │  │
│  │                  │                   │                │  │
│  │ • Site Visits    │ • General Channel │ • Index        │  │
│  │ • Vendor Neg     │ • Vendor Channel  │ • Participants │  │
│  │ • Lessons        │ • Design Channel  │ • Cross-Refs   │  │
│  │ • Design Review  │ • Market Channels │                │  │
│  │ • Weekly Syncs   │                   │                │  │
│  └──────────────────┴───────────────────┴────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Integration Patterns

### Pattern 1: Historical Project References

**Flow**: Meeting Transcripts / Teams → Historical Projects CSV

**Use Case**: Lessons learned discussions reference completed store costs/timelines

**Implementation**:

```python
def link_conversation_to_historical_project(conversation, store_id):
    """Create bidirectional link between conversation and historical data."""

    # Load historical data
    historical_df = pd.read_csv('03_Historical_Projects/historical_projects.csv')
    store_row = historical_df[historical_df['store_id'] == store_id]

    if store_row.empty:
        raise ValueError(f"Store {store_id} not found in historical projects")

    # Extract relevant cost data
    historical_data = {
        'store_id': store_id,
        'completion_date': store_row['completion_date'].values[0],
        'categories': {}
    }

    # Get cost categories
    for category in ['electrical', 'hvac', 'interior', 'exterior']:
        estimated = store_row[f'{category}_estimated_cost'].values[0]
        actual = store_row[f'{category}_actual_cost'].values[0]
        variance = actual - estimated

        historical_data['categories'][category] = {
            'estimated': estimated,
            'actual': actual,
            'variance': variance,
            'variance_pct': (variance / estimated) * 100 if estimated > 0 else 0
        }

    # Validate temporal coherence
    conversation_date = pd.to_datetime(conversation['date'])
    completion_date = pd.to_datetime(historical_data['completion_date'])

    if conversation_date < completion_date:
        raise ValueError(
            f"Temporal violation: Conversation dated {conversation_date} "
            f"references Store {store_id} which completes {completion_date}"
        )

    return historical_data
```

**Example Integration**:

```
# Lessons Learned Meeting
MEETING: Lessons Learned
STORE/TOPIC: Store-189
DATE: 2024-02-20

[00:15:30] Sarah Chen: Let's review the electrical costs. We estimated $35K but came in at $32K.

↓ Links to ↓

# Historical Projects CSV
store_id,completion_date,electrical_estimated_cost,electrical_actual_cost
Store-189,2024-02-01,35000,32000

↓ Creates Reference ↓

REFERENCES:
  - Historical Store: Store-189 (electrical: $32K actual vs $35K estimate, -$3K variance)
```

---

### Pattern 2: Template Updates

**Flow**: Teams Design Channel → Build Templates JSON

**Use Case**: Template changes discussed in Teams are reflected in template versioning

**Implementation**:

```python
def link_template_discussion_to_template_file(thread, template_version):
    """Link Teams discussion about template changes to actual template file."""

    # Load template version history
    with open('02_Build_Templates/template_version_history.json', 'r') as f:
        version_history = json.load(f)

    if template_version not in version_history:
        raise ValueError(f"Template version {template_version} not found")

    version_info = version_history[template_version]

    # Extract changes
    changes = []
    for section, change_detail in version_info['changes'].items():
        changes.append({
            'section': section,
            'previous_value': change_detail['previous'],
            'new_value': change_detail['new'],
            'rationale': change_detail['reason'],
            'effective_date': version_info['effective_date']
        })

    # Validate thread date aligns with effective date
    thread_date = pd.to_datetime(thread['date'])
    effective_date = pd.to_datetime(version_info['effective_date'])

    # Thread should be within 7 days before/after effective date
    days_diff = abs((thread_date - effective_date).days)
    if days_diff > 7:
        warnings.warn(
            f"Thread date {thread_date} is {days_diff} days from "
            f"template effective date {effective_date}"
        )

    return changes
```

**Example Integration**:

```json
// Teams Thread
{
  "channel": "design-standards-updates",
  "messages": [
    {
      "text": "Base template v2.3 is live as of March 1. All new stores require 400A electrical panels instead of 200A.",
      "date": "2024-03-01"
    }
  ]
}

↓ Links to ↓

// base_template.json
{
  "version": "2.3",
  "effective_date": "2024-03-01",
  "electrical": {
    "panel_amperage": 400
  }
}

↓ References ↓

// template_version_history.json
{
  "2.3": {
    "effective_date": "2024-03-01",
    "changes": {
      "electrical": {
        "previous": 200,
        "new": 400,
        "reason": "Increased HVAC and lighting load requirements"
      }
    }
  }
}
```

---

### Pattern 3: Constraint Discovery

**Flow**: Site Visit Meetings → Constraints Rules JSON

**Use Case**: New constraints discovered during site visits are added to constraints database

**Implementation**:

```python
def create_constraint_from_meeting(meeting_file, constraint_details):
    """Extract constraint from meeting and add to constraints_rules.json."""

    # Parse meeting metadata
    with open(meeting_file, 'r') as f:
        content = f.read()

    meeting_meta = parse_meeting_header(content)
    store_id = meeting_meta['store_topic']
    discovery_date = meeting_meta['date']

    # Generate constraint ID
    constraint_count = count_existing_constraints(store_id)
    constraint_id = f"CNS-{store_id.split('-')[1]}-{constraint_count + 1:03d}"

    # Create constraint object
    constraint = {
        'constraint_id': constraint_id,
        'store_id': store_id,
        'constraint_type': constraint_details['type'],
        'category': constraint_details['category'],
        'discovered_date': discovery_date,
        'source': os.path.basename(meeting_file),
        'description': constraint_details['description'],
        'impact': {
            'cost_modifier': constraint_details.get('cost_modifier', 1.0),
            'timeline_days': constraint_details.get('timeline_days', 0),
            'notes': constraint_details.get('impact_notes', '')
        }
    }

    # Add to constraints_rules.json
    with open('06_Constraints_Rules/constraints_rules.json', 'r') as f:
        constraints_data = json.load(f)

    if 'store_specific' not in constraints_data:
        constraints_data['store_specific'] = []

    constraints_data['store_specific'].append(constraint)

    with open('06_Constraints_Rules/constraints_rules.json', 'w') as f:
        json.dump(constraints_data, f, indent=2)

    return constraint_id
```

**Example Integration**:

```
# Site Visit Meeting
[00:13:45] Tom Wilson: "The landlord requires all electrical work to use their approved vendor list."

↓ Triggers Constraint Creation ↓

# constraints_rules.json (NEW ENTRY)
{
  "store_specific": [
    {
      "constraint_id": "CNS-217-001",
      "store_id": "Store-217",
      "constraint_type": "landlord_vendor_restriction",
      "category": "electrical",
      "discovered_date": "2024-03-15",
      "source": "site_visit_Store-217_2024-03-15.txt",
      "description": "Landlord requires use of approved vendor list for electrical work",
      "impact": {
        "cost_modifier": 1.05,
        "timeline_days": 0,
        "notes": "Limits negotiation leverage, may increase costs"
      }
    }
  ]
}

↓ Referenced in Meeting ↓

REFERENCES:
  - Constraint: CNS-217-001 (landlord_approved_vendors)
```

---

### Pattern 4: Regional Modifier Validation

**Flow**: Meetings/Teams → Regional Modifiers CSV (validation)

**Use Case**: Cost discussions reference regional modifiers; ensure consistency

**Implementation**:

```python
def validate_regional_modifier_reference(conversation_text, market, category):
    """Validate that regional modifier mentioned matches actual data."""

    # Load regional modifiers
    modifiers_df = pd.read_csv('04_Regional_Factors/regional_modifiers.csv')

    # Find modifier
    modifier_row = modifiers_df[
        (modifiers_df['market'] == market) &
        (modifiers_df['category'] == category)
    ]

    if modifier_row.empty:
        raise ValueError(f"No regional modifier found for {market}/{category}")

    actual_modifier = modifier_row['modifier'].values[0]
    reason = modifier_row['reason'].values[0]

    # Extract mentioned modifier from conversation
    # Pattern: "1.08x" or "8%" or "108%"
    mentioned_patterns = [
        r'(\d+\.\d+)x',
        r'(\d+)%\s+higher',
        r'(\d+\.\d+)%\s+higher'
    ]

    mentioned_modifier = None
    for pattern in mentioned_patterns:
        match = re.search(pattern, conversation_text)
        if match:
            value = float(match.group(1))
            # Convert percentage to multiplier if needed
            if '%' in pattern:
                mentioned_modifier = 1 + (value / 100)
            else:
                mentioned_modifier = value
            break

    if mentioned_modifier is None:
        warnings.warn(f"Could not extract modifier value from conversation")
        return None

    # Validate match
    if abs(mentioned_modifier - actual_modifier) > 0.01:
        raise ValueError(
            f"Modifier mismatch: Conversation mentions {mentioned_modifier}, "
            f"but regional_modifiers.csv shows {actual_modifier} for {market}/{category}"
        )

    return {
        'market': market,
        'category': category,
        'modifier': actual_modifier,
        'reason': reason,
        'validated': True
    }
```

**Example Integration**:

```
# Meeting Dialogue
[00:08:12] Tom Wilson: "Cincinnati shows 1.08x for electrical work this year due to union contracts."

↓ Validates Against ↓

# regional_modifiers.csv
market,category,modifier,reason,year
Cincinnati,electrical,1.08,"Union contract increases",2024

↓ Validation Result ↓

✓ Match confirmed: 1.08x electrical modifier for Cincinnati
✓ Reason aligned: Union contracts
✓ Year current: 2024
```

---

### Pattern 5: Vendor Registry Consistency

**Flow**: Conversations → Material Costs CSV (vendor validation)

**Use Case**: Ensure vendor names used in conversations match vendor registry

**Implementation**:

```python
def validate_and_normalize_vendor_name(mentioned_vendor, category=None):
    """Validate vendor name against registry and return canonical name."""

    # Load vendor registry
    with open('config/vendor_registry.json', 'r') as f:
        vendor_registry = json.load(f)

    # Exact match
    for vendor in vendor_registry['vendors']:
        if vendor['canonical_name'].lower() == mentioned_vendor.lower():
            return vendor['canonical_name']

        # Check aliases
        if 'aliases' in vendor:
            for alias in vendor['aliases']:
                if alias.lower() == mentioned_vendor.lower():
                    return vendor['canonical_name']

    # Fuzzy match
    from difflib import get_close_matches
    canonical_names = [v['canonical_name'] for v in vendor_registry['vendors']]

    matches = get_close_matches(mentioned_vendor, canonical_names, n=1, cutoff=0.8)
    if matches:
        warnings.warn(
            f"Vendor name '{mentioned_vendor}' matched to '{matches[0]}' (fuzzy match). "
            f"Consider using canonical name."
        )
        return matches[0]

    # Category-specific fallback
    if category:
        category_vendors = [
            v['canonical_name'] for v in vendor_registry['vendors']
            if v.get('category') == category
        ]
        matches = get_close_matches(mentioned_vendor, category_vendors, n=1, cutoff=0.7)
        if matches:
            warnings.warn(
                f"Vendor '{mentioned_vendor}' matched to '{matches[0]}' in category {category}"
            )
            return matches[0]

    raise ValueError(
        f"Vendor '{mentioned_vendor}' not found in registry. "
        f"Add to config/vendor_registry.json or check spelling."
    )
```

**Example Integration**:

```
# Teams Message
"Our primary HVAC vendor (CoolAir Systems) just pushed lead times..."

↓ Validates Against ↓

# vendor_registry.json
{
  "vendors": [
    {
      "canonical_name": "CoolAir Systems",
      "category": "HVAC",
      "typical_lead_time_weeks": 8
    }
  ]
}

↓ Cross-References to ↓

# material_costs.csv
vendor,category,lead_time_weeks,cost_per_unit
CoolAir Systems,HVAC_commercial_units,8,15000

✓ Vendor name consistent across all sources
```

---

## Integration Workflows

### Workflow 1: Generating Conversations for New Store

```python
def generate_full_conversation_set_for_store(store_id):
    """Generate complete set of conversations for a new store."""

    # Step 1: Load store data
    store_profile = load_store_profile(store_id)
    historical_data = load_historical_data(store_id)

    # Step 2: Determine conversation timeline
    timeline = calculate_conversation_timeline(store_profile)
    # Returns: {'site_visit': date, 'vendor_neg': date, 'lessons': date, ...}

    # Step 3: Select participants based on store type and location
    participants = select_participants_for_store(
        store_type=store_profile['type'],
        market=store_profile['market'],
        project_stage=store_profile['status']
    )

    # Step 4: Generate site visit debrief
    site_visit_context = {
        'constraints': extract_store_constraints(store_id),
        'historical_reference': find_similar_completed_store(store_id),
        'cost_focus_areas': identify_cost_drivers(store_profile)
    }

    site_visit_meeting = generate_meeting_transcript({
        'meeting_type': 'site_visit_debrief',
        'store_id': store_id,
        'date': timeline['site_visit'],
        'participants': participants['site_visit'],
        'context': site_visit_context
    })

    # Step 5: Generate Teams follow-up thread
    teams_thread = generate_teams_conversation({
        'channel': determine_market_channel(store_profile['market']),
        'date': timeline['site_visit'] + timedelta(days=1),
        'theme': 'site-visit-followup',
        'store_id': store_id,
        'meeting_reference': site_visit_meeting['filename']
    })

    # Step 6: If store is completed, generate lessons learned
    if store_profile['status'] == 'completed':
        lessons_context = {
            'cost_variances': calculate_cost_variances(historical_data),
            'timeline_variances': calculate_timeline_variances(historical_data),
            'key_learnings': extract_key_learnings(historical_data)
        }

        lessons_meeting = generate_meeting_transcript({
            'meeting_type': 'lessons_learned',
            'store_id': store_id,
            'date': timeline['lessons'],
            'participants': participants['lessons'],
            'context': lessons_context
        })

    # Step 7: Update conversation index
    update_conversation_index([site_visit_meeting, teams_thread, lessons_meeting])

    # Step 8: Validate cross-references
    validate_all_cross_references(store_id)

    return {
        'site_visit': site_visit_meeting,
        'teams_threads': [teams_thread],
        'lessons_learned': lessons_meeting if store_profile['status'] == 'completed' else None
    }
```

### Workflow 2: Adding Template Discussion After Template Update

```python
def generate_template_discussion_thread(template_version, effective_date):
    """Generate Teams thread discussing template update."""

    # Step 1: Load template changes
    version_history = load_json('02_Build_Templates/template_version_history.json')
    changes = version_history[template_version]['changes']

    # Step 2: Determine impacted stakeholders
    participants = []
    if 'electrical' in changes or 'hvac' in changes:
        participants.append('Contractor')
    if any(changes.keys()):
        participants.extend(['Project Manager', 'Design Lead'])

    # Step 3: Generate discussion
    thread = generate_teams_conversation({
        'channel': 'design-standards-updates',
        'date': effective_date,
        'theme': 'template-update',
        'template_version': template_version,
        'participants': select_participants(participants),
        'context': {
            'changes': changes,
            'rationale': version_history[template_version].get('rationale', '')
        }
    })

    # Step 4: Link to template file
    thread['references']['structured_data'].append({
        'source': '02_Build_Templates',
        'file': 'base_template.json',
        'field': f'version {template_version}'
    })

    return thread
```

### Workflow 3: Extracting Constraints from Conversations

```python
def extract_and_create_constraints_from_conversations(conversation_file):
    """Scan conversation for constraint mentions and create constraint entries."""

    # Load conversation
    if conversation_file.endswith('.txt'):
        conversation = parse_meeting_transcript(conversation_file)
    else:
        conversation = parse_teams_thread(conversation_file)

    # Constraint detection patterns
    constraint_patterns = {
        'landlord_restriction': r'landlord (?:requires|restricts|mandates)',
        'permit_requirement': r'permit (?:requires|needed|mandatory)',
        'union_labor': r'union (?:requirement|contract|must use)',
        'supply_chain': r'(?:lead time|availability|supply) (?:issue|constraint|delay)',
        'code_requirement': r'(?:building code|code requires|code mandates)'
    }

    detected_constraints = []

    # Scan dialogue/messages for constraint mentions
    text = extract_full_text(conversation)

    for constraint_type, pattern in constraint_patterns.items():
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            # Extract context (surrounding sentences)
            context = extract_context_around_match(text, match.start(), match.end())

            detected_constraints.append({
                'type': constraint_type,
                'mention': match.group(),
                'context': context,
                'store_id': conversation.get('store_id'),
                'source_file': conversation_file,
                'discovery_date': conversation['date']
            })

    # Create constraint entries
    created_constraints = []
    for detected in detected_constraints:
        # Extract impact details from context
        impact = extract_impact_from_context(detected['context'])

        constraint_id = create_constraint_from_meeting(
            meeting_file=detected['source_file'],
            constraint_details={
                'type': detected['type'],
                'category': determine_category(detected['context']),
                'description': detected['context'],
                **impact
            }
        )

        created_constraints.append(constraint_id)

    return created_constraints
```

---

## Data Synchronization

### Keeping Conversations Current with Structured Data Changes

**Scenario**: Regional modifiers update (e.g., Cincinnati electrical modifier changes from 1.08 to 1.10)

**Impact**: Existing conversations referencing old modifier become stale

**Options**:

**Option 1: Append Update Conversations** (Recommended)
```python
def generate_modifier_update_conversation(market, category, old_modifier, new_modifier, effective_date):
    """Generate Teams thread announcing modifier change."""

    thread = generate_teams_conversation({
        'channel': 'regional-compliance',
        'date': effective_date,
        'theme': 'modifier-update',
        'participants': select_participants(['Finance', 'Project Manager']),
        'messages': [
            {
                'author': 'Finance Analyst',
                'text': f'Updated regional modifier for {market} {category}: {old_modifier}x → {new_modifier}x effective {effective_date}. All new estimates should use updated rate.'
            },
            {
                'author': 'Project Manager',
                'text': f'Thanks for the heads up. Will update cost models and notify contractors.'
            }
        ]
    })

    return thread
```

**Option 2: Version Flag Conversations**
```python
# Add metadata to existing conversations indicating they reference historical data
def flag_conversation_as_historical(conversation_file, reference_date):
    """Mark conversation as referencing point-in-time data."""

    metadata = {
        'data_valid_as_of': reference_date,
        'note': 'Regional modifiers referenced may differ from current values'
    }

    # Append to conversation index
    update_conversation_index_metadata(conversation_file, metadata)
```

---

## Integration Testing

### Test 1: Cross-Reference Integrity

```python
def test_cross_reference_integrity():
    """Validate all cross-references resolve correctly."""

    errors = []

    # Test store ID references
    all_conversations = load_all_conversations()
    all_store_ids = get_all_store_ids_from_historical_data()

    for conv in all_conversations:
        mentioned_stores = extract_store_references(conv)
        for store_id in mentioned_stores:
            if store_id not in all_store_ids:
                errors.append({
                    'type': 'invalid_store_reference',
                    'conversation': conv['filename'],
                    'store_id': store_id
                })

    # Test vendor name consistency
    vendor_registry = load_vendor_registry()
    canonical_vendors = [v['canonical_name'] for v in vendor_registry['vendors']]

    for conv in all_conversations:
        mentioned_vendors = extract_vendor_references(conv)
        for vendor in mentioned_vendors:
            if vendor not in canonical_vendors:
                errors.append({
                    'type': 'invalid_vendor_reference',
                    'conversation': conv['filename'],
                    'vendor': vendor
                })

    # Test constraint ID resolution
    constraints_data = load_json('06_Constraints_Rules/constraints_rules.json')
    all_constraint_ids = extract_all_constraint_ids(constraints_data)

    for conv in all_conversations:
        mentioned_constraints = extract_constraint_references(conv)
        for constraint_id in mentioned_constraints:
            if constraint_id not in all_constraint_ids:
                errors.append({
                    'type': 'invalid_constraint_reference',
                    'conversation': conv['filename'],
                    'constraint_id': constraint_id
                })

    return errors
```

### Test 2: Temporal Coherence Across Integrations

```python
def test_temporal_coherence_across_data():
    """Validate temporal relationships between conversations and structured data."""

    violations = []

    for conv in load_all_conversations():
        conv_date = pd.to_datetime(conv['date'])

        # Test historical project references
        historical_refs = extract_historical_references(conv)
        for ref in historical_refs:
            project = get_historical_project(ref['store_id'])
            project_completion = pd.to_datetime(project['completion_date'])

            if conv_date < project_completion:
                violations.append({
                    'type': 'premature_historical_reference',
                    'conversation': conv['filename'],
                    'conversation_date': conv_date,
                    'project_completion': project_completion,
                    'store_id': ref['store_id']
                })

        # Test template version references
        template_refs = extract_template_references(conv)
        for ref in template_refs:
            version_info = get_template_version_info(ref['version'])
            effective_date = pd.to_datetime(version_info['effective_date'])

            if conv_date < effective_date:
                violations.append({
                    'type': 'premature_template_reference',
                    'conversation': conv['filename'],
                    'conversation_date': conv_date,
                    'template_effective': effective_date,
                    'version': ref['version']
                })

        # Test constraint discovery dates
        constraint_refs = extract_constraint_references(conv)
        for constraint_id in constraint_refs:
            constraint = get_constraint_by_id(constraint_id)
            discovery_date = pd.to_datetime(constraint['discovered_date'])

            if conv_date < discovery_date:
                violations.append({
                    'type': 'premature_constraint_reference',
                    'conversation': conv['filename'],
                    'conversation_date': conv_date,
                    'constraint_discovered': discovery_date,
                    'constraint_id': constraint_id
                })

    return violations
```

---

## Best Practices

### 1. Maintain Bidirectional Links

Always create links from both directions:
- Conversation → Structured Data (in REFERENCES section)
- Structured Data → Conversation (in metadata/cross_reference_map.json)

### 2. Validate on Creation

Run validation immediately after generating new conversations:
```python
new_conversation = generate_meeting_transcript(config)
validate_cross_references(new_conversation)
validate_temporal_coherence(new_conversation)
```

### 3. Use Canonical Names

Always use canonical names from registries:
- Store IDs: Exactly as in historical_projects.csv
- Vendor names: From vendor_registry.json
- Constraint IDs: From constraints_rules.json

### 4. Document Integration Points

When adding new structured data, document conversation implications:
```python
# When adding new regional modifier:
# 1. Update regional_modifiers.csv
# 2. Generate announcement thread in regional-compliance channel
# 3. Reference in next cost estimation meeting for that market
```

### 5. Version Awareness

Track which version of structured data conversations reference:
```json
{
  "conversation": "site_visit_Store-217_2024-03-15.txt",
  "data_references": {
    "regional_modifiers": {"version": "2024-Q1", "as_of": "2024-03-15"},
    "base_template": {"version": "2.3", "effective": "2024-03-01"}
  }
}
```

---

**End of Integration Guide**
