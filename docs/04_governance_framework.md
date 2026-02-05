# Governance Framework

## Overview

This framework defines access control, data retention, privacy handling, and compliance requirements for synthetic conversational data.

## 1. Access Control

### Role-Based Access Control (RBAC)

#### Access Level Definitions

| Level | Access Scope | Data Types Accessible | Use Cases |
|-------|-------------|----------------------|-----------|
| **Full** | All conversations, all metadata | Meetings (all types), Teams (all channels), full metadata | Cost estimation, project planning, historical analysis |
| **Cost-Only** | Cost-related discussions with redactions | Lessons learned, vendor negotiations (redacted), cost-tagged Teams threads | Budgeting, financial analysis, variance reporting |
| **Summary** | High-level summaries and decisions | Meeting summaries, action items, decision threads | Strategic oversight, executive reporting |
| **Public** | Design standards and templates only | Design reviews, design-standards channel | Cross-functional alignment, operations |

#### Role Mappings

```json
{
  "access_levels": {
    "full": {
      "roles": [
        "Project Manager",
        "General Contractor",
        "Design Lead",
        "Architect",
        "Construction Manager"
      ],
      "description": "Need complete context for estimation and planning",
      "data_access": {
        "meeting_transcripts": "all",
        "teams_channels": "all",
        "metadata": "all"
      }
    },
    "cost_only": {
      "roles": [
        "Finance Analyst",
        "Budget Manager",
        "CFO",
        "Finance Director"
      ],
      "description": "Need cost data for budgeting, not operational details",
      "data_access": {
        "meeting_transcripts": ["lessons_learned", "vendor_negotiation"],
        "teams_channels": ["filtered_by_tags:cost,budget,variance"],
        "metadata": "conversation_index only",
        "redactions": ["vendor_negotiation_tactics", "pricing_strategies"]
      }
    },
    "summary": {
      "roles": [
        "VP Store Development",
        "C-Suite",
        "Executive Team"
      ],
      "description": "Strategic oversight, decision tracking",
      "data_access": {
        "meeting_transcripts": "summaries only",
        "teams_channels": ["filtered_by_tags:decision"],
        "metadata": "conversation_index with summaries"
      }
    },
    "public": {
      "roles": [
        "Store Operations",
        "Marketing",
        "IT Support",
        "HR"
      ],
      "description": "Design standards for cross-functional alignment",
      "data_access": {
        "meeting_transcripts": ["design_review"],
        "teams_channels": ["design-standards-updates"],
        "metadata": "none"
      }
    }
  }
}
```

### Implementation

#### Access Control Filter Function

```python
def filter_conversation_by_access_level(conversation, user_role):
    """Apply access control based on user role."""

    # Load access control rules
    with open('config/access_control_rules.json', 'r') as f:
        rules = json.load(f)

    # Determine user's access level
    user_access_level = None
    for level, config in rules['access_levels'].items():
        if user_role in config['roles']:
            user_access_level = level
            break

    if not user_access_level:
        raise PermissionError(f"Role '{user_role}' not defined in access control rules")

    access_config = rules['access_levels'][user_access_level]

    # Apply filters based on access level
    if user_access_level == 'full':
        return conversation  # No filtering

    elif user_access_level == 'cost_only':
        return _filter_cost_only(conversation, access_config)

    elif user_access_level == 'summary':
        return _filter_summary_only(conversation, access_config)

    elif user_access_level == 'public':
        return _filter_public_only(conversation, access_config)

    else:
        raise ValueError(f"Unknown access level: {user_access_level}")


def _filter_cost_only(conversation, config):
    """Filter to cost-related content only."""

    if conversation['type'] == 'meeting':
        # Only allow certain meeting types
        allowed_types = config['data_access']['meeting_transcripts']
        if conversation['meeting_type'] not in allowed_types:
            return None  # Hide this meeting

        # Apply redactions
        if 'vendor_negotiation_tactics' in config.get('redactions', []):
            conversation = _redact_negotiation_tactics(conversation)

    elif conversation['type'] == 'teams_thread':
        # Filter by tags
        required_tags = ['cost', 'budget', 'variance', 'pricing']
        if not any(tag in conversation['tags'] for tag in required_tags):
            return None  # Hide non-cost threads

    return conversation


def _filter_summary_only(conversation, config):
    """Return summary view only."""

    summary = {
        'type': conversation['type'],
        'date': conversation['date'],
        'participants': conversation['participants'],
        'key_topics': conversation.get('tags', []),
        'summary': conversation.get('summary', ''),
        'action_items': conversation.get('action_items', [])
    }

    # For meetings, include references but not dialogue
    if conversation['type'] == 'meeting':
        summary['references'] = conversation.get('references', [])

    return summary


def _filter_public_only(conversation, config):
    """Filter to design standards only."""

    if conversation['type'] == 'meeting':
        if conversation['meeting_type'] != 'design_review':
            return None

    elif conversation['type'] == 'teams_thread':
        if conversation['channel'] != 'design-standards-updates':
            return None

    return conversation


def _redact_negotiation_tactics(conversation):
    """Redact sensitive negotiation details."""

    # Patterns to redact
    redaction_patterns = [
        r'our (?:strategy|approach|tactic) (?:is|will be)',
        r'we(?:'ll| will) (?:leverage|use|exploit)',
        r'pricing strategy',
        r'negotiation leverage'
    ]

    text = conversation['text']
    for pattern in redaction_patterns:
        text = re.sub(pattern, '[REDACTED]', text, flags=re.IGNORECASE)

    conversation['text'] = text
    conversation['redacted'] = True

    return conversation
```

#### Query-Time Access Control

```python
def query_conversations_with_access_control(user_role, filters=None):
    """Query conversations with automatic access control."""

    # Load all conversations
    all_conversations = load_all_conversations()

    # Apply access control filter
    accessible_conversations = []
    for conv in all_conversations:
        filtered_conv = filter_conversation_by_access_level(conv, user_role)
        if filtered_conv:  # Not None (meaning accessible)
            accessible_conversations.append(filtered_conv)

    # Apply additional filters if provided
    if filters:
        accessible_conversations = apply_filters(accessible_conversations, filters)

    return accessible_conversations
```

---

## 2. Data Retention

### Retention Policy

#### Lifecycle Stages

| Stage | Timeframe | Storage | Indexing | Access |
|-------|-----------|---------|----------|--------|
| **Active** | Project start → +6 months post-completion | Primary storage | Full Glean index | Immediate, searchable |
| **Archived** | +6 months → +2 years post-completion | Archive storage | Summary index only | On-demand retrieval |
| **Historical Knowledge** | +2 years → Indefinite | Knowledge base | Sanitized lessons index | Search lessons only |
| **Deleted** | +2 years post-completion (non-significant projects) | Deleted | Not indexed | Not accessible |

#### Retention Rules

```python
RETENTION_RULES = {
    'active': {
        'criteria': 'project_status in ["in_progress", "recently_completed"]',
        'recently_completed_threshold_days': 180,
        'storage': 'primary',
        'indexing': 'full',
        'access': 'immediate'
    },
    'archived': {
        'criteria': '180 < days_since_completion <= 730',
        'storage': 'archive',
        'indexing': 'summary_only',
        'access': 'on_demand',
        'actions': [
            'move_full_transcripts_to_archive',
            'keep_conversation_index_entries',
            'keep_summaries_and_action_items',
            'remove_detailed_dialogue_from_search'
        ]
    },
    'historical_knowledge': {
        'criteria': 'days_since_completion > 730',
        'storage': 'knowledge_base',
        'indexing': 'lessons_only',
        'access': 'search_lessons',
        'actions': [
            'extract_lessons_to_knowledge_base',
            'anonymize_participant_names',
            'remove_store_specific_identifiers',
            'keep_cost_variance_patterns',
            'keep_constraint_types_and_impacts'
        ]
    },
    'deleted': {
        'criteria': 'days_since_completion > 730 AND not is_exceptional_project',
        'storage': 'deleted',
        'indexing': 'none',
        'access': 'none',
        'exceptions': [
            'projects with >20% cost variance',
            'projects with unique constraints',
            'projects flagged for legal/audit retention'
        ]
    }
}
```

### Implementation

#### Automated Retention Policy Application

```python
import datetime
from datetime import timedelta

def apply_retention_policy():
    """Apply retention policies to all conversations."""

    current_date = datetime.datetime.now()
    actions_taken = {
        'active': [],
        'archived': [],
        'historical_knowledge': [],
        'deleted': []
    }

    for conversation in load_all_conversations():
        store_id = conversation['store_id']

        # Get project completion date
        project = get_historical_project(store_id)
        if not project or not project.get('completion_date'):
            # Project not complete - keep as active
            conversation['retention_status'] = 'active'
            actions_taken['active'].append(conversation['filename'])
            continue

        completion_date = datetime.datetime.strptime(project['completion_date'], '%Y-%m-%d')
        days_since_completion = (current_date - completion_date).days

        # Determine retention stage
        if days_since_completion <= 180:
            # Active: Keep fully indexed
            conversation['retention_status'] = 'active'
            actions_taken['active'].append(conversation['filename'])

        elif days_since_completion <= 730:
            # Archived: Move details to archive, keep summaries
            archive_conversation_details(conversation)
            keep_conversation_summary(conversation)
            conversation['retention_status'] = 'archived'
            actions_taken['archived'].append(conversation['filename'])

        else:
            # Check if exceptional (>20% variance, unique constraints, etc.)
            if is_exceptional_project(store_id):
                # Keep as archived even after 2 years
                conversation['retention_status'] = 'archived'
                actions_taken['archived'].append(conversation['filename'])
            else:
                # Extract lessons and delete details
                extract_lessons_to_knowledge_base(conversation)
                delete_conversation_details(conversation)
                conversation['retention_status'] = 'deleted_details_only'
                actions_taken['deleted'].append(conversation['filename'])

    # Generate retention report
    report = generate_retention_report(actions_taken, current_date)
    save_retention_report(report)

    return actions_taken


def archive_conversation_details(conversation):
    """Move full conversation to archive storage."""

    # Move file to archive directory
    archive_path = f"07_Conversations/archive/{conversation['filename']}"
    os.makedirs(os.path.dirname(archive_path), exist_ok=True)
    shutil.move(conversation['filepath'], archive_path)

    # Remove from Glean full-text index (retain summary in index)
    # This would be integration-specific based on Glean API
    print(f"Archived: {conversation['filename']}")


def extract_lessons_to_knowledge_base(conversation):
    """Extract lessons learned and add to knowledge base."""

    lessons = {
        'source_conversation': conversation['filename'],
        'store_type': anonymize_store_id(conversation['store_id']),
        'market_region': get_region(conversation['store_id']),
        'extraction_date': datetime.datetime.now().isoformat(),
        'lessons': []
    }

    # Extract cost variance lessons
    if 'lessons_learned' in conversation.get('meeting_type', ''):
        cost_variances = extract_cost_variance_lessons(conversation)
        lessons['lessons'].extend(cost_variances)

    # Extract constraint lessons
    constraint_lessons = extract_constraint_lessons(conversation)
    lessons['lessons'].extend(constraint_lessons)

    # Anonymize and sanitize
    lessons = anonymize_lessons(lessons)

    # Add to knowledge base
    knowledge_base_path = '07_Conversations/knowledge_base/lessons_learned.json'
    append_to_knowledge_base(knowledge_base_path, lessons)

    print(f"Extracted lessons from: {conversation['filename']}")


def is_exceptional_project(store_id):
    """Determine if project should be retained longer than standard policy."""

    project = get_historical_project(store_id)

    # Check for significant cost variance
    total_variance_pct = calculate_total_variance_pct(project)
    if abs(total_variance_pct) > 20:
        return True

    # Check for unique constraints
    constraints = get_store_constraints(store_id)
    if any(c['constraint_type'] == 'unique' for c in constraints):
        return True

    # Check for legal/audit retention flags
    if project.get('legal_hold', False):
        return True

    return False
```

#### Scheduled Retention Job

```python
# Run retention policy monthly
def scheduled_retention_job():
    """Monthly job to apply retention policies."""

    print(f"[{datetime.datetime.now()}] Starting retention policy application...")

    try:
        actions = apply_retention_policy()

        summary = f"""
        Retention Policy Applied:
        - Active: {len(actions['active'])} conversations
        - Archived: {len(actions['archived'])} conversations
        - Lessons Extracted: {len(actions['historical_knowledge'])} conversations
        - Details Deleted: {len(actions['deleted'])} conversations
        """

        print(summary)
        send_retention_report_email(summary)

    except Exception as e:
        print(f"ERROR in retention job: {e}")
        send_error_alert(str(e))

# Schedule for first day of each month at 2 AM
# (Implementation depends on job scheduler: cron, Airflow, etc.)
```

---

## 3. Privacy & PII Handling

### PII Categories and Policies

| PII Category | Policy | Implementation |
|--------------|--------|----------------|
| **Participant Names** | Use fictional names only | Generate from name database; track in participant_roles.json |
| **Email Addresses** | No full emails; prefixes only (no @domain) | sarah.chen ✓, sarah.chen@anf.com ✗ |
| **Phone Numbers** | Prohibited | Validation regex rejects any phone patterns |
| **Physical Addresses** | Locations only (city/market) | "Columbus market" ✓, "123 Main St Columbus" ✗ |
| **Vendor Names** | Fictional or anonymized | Use vendor registry with canonical fictional names |
| **Landlord Identities** | Generic references only | "The landlord" ✓, "Easton Properties LLC" ✗ |
| **Financial Details** | Realistic ranges, not actual budgets | Generate from regional/category averages |

### PII Validation

```python
def validate_pii_compliance(conversation):
    """Scan conversation for PII violations."""

    violations = []
    text = extract_full_text(conversation)

    # Check for email addresses with domains
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)

    prohibited_domains = ['anf.com', 'abercrombie.com', 'company.com']
    for email in emails:
        domain = email.split('@')[1]
        if any(prohibited in domain for prohibited in prohibited_domains):
            violations.append({
                'type': 'prohibited_email_domain',
                'value': email,
                'location': find_location_in_text(text, email)
            })

    # Check for phone numbers
    phone_patterns = [
        r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',  # US phone
        r'\(\d{3}\)\s?\d{3}[-.\s]?\d{4}',       # (555) 123-4567
    ]

    for pattern in phone_patterns:
        phones = re.findall(pattern, text)
        if phones:
            violations.append({
                'type': 'phone_number',
                'value': phones,
                'location': find_location_in_text(text, phones[0])
            })

    # Check for physical addresses
    address_indicators = [
        r'\d+\s+[A-Z][a-z]+\s+(?:Street|St|Avenue|Ave|Boulevard|Blvd|Road|Rd)',
        r'Suite\s+\d+',
        r'Apt\.?\s+\d+',
        r'\bZIP:?\s*\d{5}'
    ]

    for pattern in address_indicators:
        if re.search(pattern, text):
            violations.append({
                'type': 'physical_address',
                'pattern': pattern,
                'location': 'See conversation text'
            })

    # Check participant names against real employee list (if available)
    if REAL_EMPLOYEE_LIST:
        for participant in conversation['participants']:
            if participant['name'] in REAL_EMPLOYEE_LIST:
                violations.append({
                    'type': 'real_employee_name',
                    'value': participant['name']
                })

    # Check vendor names against known real companies
    if REAL_VENDOR_LIST:
        vendors = extract_vendor_references(text)
        for vendor in vendors:
            if vendor in REAL_VENDOR_LIST:
                violations.append({
                    'type': 'real_vendor_name',
                    'value': vendor
                })

    return violations
```

### Anonymization Functions

```python
def anonymize_lessons(lessons):
    """Anonymize lessons learned data for long-term retention."""

    # Replace specific store IDs with generalized identifiers
    lessons['store_type'] = anonymize_store_id(lessons.get('store_id', ''))

    # Remove participant names, keep roles only
    if 'participants' in lessons:
        lessons['participants'] = [p['role'] for p in lessons['participants']]

    # Generalize market names if too specific
    if 'market' in lessons:
        lessons['market_region'] = generalize_market_name(lessons['market'])
        del lessons['market']

    # Remove specific dates, keep relative timings
    if 'date' in lessons:
        lessons['timeframe'] = get_quarter_year(lessons['date'])
        del lessons['date']

    return lessons


def anonymize_store_id(store_id):
    """Convert Store-217 to Type-A store in Midwest market."""

    store_profile = load_store_profile(store_id)

    return f"{store_profile['type']} store in {store_profile['region']} market"


def generalize_market_name(market):
    """Convert specific market to regional category."""

    market_regions = {
        'Columbus': 'Midwest',
        'Cincinnati': 'Midwest',
        'Cleveland': 'Midwest',
        'Atlanta': 'Southeast',
        'Miami': 'Southeast',
        # ... more mappings
    }

    return market_regions.get(market, 'Unknown Region')
```

---

## 4. Compliance & Auditing

### Audit Logging

#### Audit Events

| Event Type | Logged Information | Retention |
|------------|-------------------|-----------|
| **Conversation Access** | User, role, conversation ID, timestamp | 1 year |
| **Data Export** | User, role, conversations exported, timestamp | 2 years |
| **Retention Policy Execution** | Conversations affected, action taken, timestamp | Indefinite |
| **PII Violation Detected** | Violation type, conversation, timestamp | Indefinite |
| **Access Control Change** | Role, old access, new access, timestamp | Indefinite |

#### Audit Log Implementation

```python
import logging
import json

# Configure audit logger
audit_logger = logging.getLogger('conversation_audit')
audit_logger.setLevel(logging.INFO)

audit_handler = logging.FileHandler('07_Conversations/audit/audit.log')
audit_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
audit_logger.addHandler(audit_handler)


def log_conversation_access(user, role, conversation_id):
    """Log conversation access event."""

    audit_logger.info(json.dumps({
        'event_type': 'conversation_access',
        'user': user,
        'role': role,
        'conversation_id': conversation_id,
        'timestamp': datetime.datetime.now().isoformat()
    }))


def log_data_export(user, role, conversation_ids):
    """Log data export event."""

    audit_logger.info(json.dumps({
        'event_type': 'data_export',
        'user': user,
        'role': role,
        'conversation_count': len(conversation_ids),
        'conversation_ids': conversation_ids,
        'timestamp': datetime.datetime.now().isoformat()
    }))


def log_retention_execution(actions_taken):
    """Log retention policy execution."""

    audit_logger.info(json.dumps({
        'event_type': 'retention_policy_execution',
        'active_count': len(actions_taken['active']),
        'archived_count': len(actions_taken['archived']),
        'deleted_count': len(actions_taken['deleted']),
        'timestamp': datetime.datetime.now().isoformat()
    }))


def log_pii_violation(conversation_id, violations):
    """Log PII violation detection."""

    audit_logger.warning(json.dumps({
        'event_type': 'pii_violation_detected',
        'conversation_id': conversation_id,
        'violation_count': len(violations),
        'violation_types': [v['type'] for v in violations],
        'timestamp': datetime.datetime.now().isoformat()
    }))
```

### Compliance Reports

```python
def generate_compliance_report(start_date, end_date):
    """Generate compliance report for specified period."""

    report = {
        'report_period': {
            'start': start_date,
            'end': end_date
        },
        'access_summary': {},
        'retention_summary': {},
        'pii_compliance': {},
        'access_control_changes': []
    }

    # Parse audit log
    audit_entries = parse_audit_log(start_date, end_date)

    # Access summary
    access_events = [e for e in audit_entries if e['event_type'] == 'conversation_access']
    report['access_summary'] = {
        'total_accesses': len(access_events),
        'unique_users': len(set(e['user'] for e in access_events)),
        'by_role': count_by_field(access_events, 'role')
    }

    # Retention summary
    retention_events = [e for e in audit_entries if e['event_type'] == 'retention_policy_execution']
    if retention_events:
        latest = retention_events[-1]
        report['retention_summary'] = {
            'last_execution': latest['timestamp'],
            'conversations_archived': latest.get('archived_count', 0),
            'conversations_deleted': latest.get('deleted_count', 0)
        }

    # PII compliance
    pii_events = [e for e in audit_entries if e['event_type'] == 'pii_violation_detected']
    report['pii_compliance'] = {
        'violations_detected': len(pii_events),
        'violation_types': count_by_field(pii_events, 'violation_types'),
        'conversations_affected': list(set(e['conversation_id'] for e in pii_events))
    }

    # Access control changes
    acl_events = [e for e in audit_entries if e['event_type'] == 'access_control_change']
    report['access_control_changes'] = acl_events

    return report
```

---

## 5. Data Quality Governance

### Quality Metrics Dashboard

```python
def generate_quality_metrics():
    """Generate data quality metrics for governance dashboard."""

    metrics = {
        'schema_compliance': {},
        'cross_reference_integrity': {},
        'temporal_coherence': {},
        'participant_consistency': {},
        'coverage_metrics': {}
    }

    all_conversations = load_all_conversations()

    # Schema compliance
    schema_results = [validate_schema(c) for c in all_conversations]
    metrics['schema_compliance'] = {
        'total_conversations': len(all_conversations),
        'compliant': sum(1 for r in schema_results if r['compliant']),
        'compliance_rate': sum(1 for r in schema_results if r['compliant']) / len(schema_results),
        'violations': [r for r in schema_results if not r['compliant']]
    }

    # Cross-reference integrity
    xref_results = [validate_cross_references(c) for c in all_conversations]
    metrics['cross_reference_integrity'] = {
        'conversations_checked': len(xref_results),
        'no_errors': sum(1 for r in xref_results if len(r['errors']) == 0),
        'integrity_rate': sum(1 for r in xref_results if len(r['errors']) == 0) / len(xref_results),
        'error_summary': aggregate_errors(xref_results)
    }

    # Temporal coherence
    temporal_results = [validate_temporal_coherence(c) for c in all_conversations]
    metrics['temporal_coherence'] = {
        'conversations_checked': len(temporal_results),
        'no_violations': sum(1 for r in temporal_results if len(r['violations']) == 0),
        'coherence_rate': sum(1 for r in temporal_results if len(r['violations']) == 0) / len(temporal_results),
        'violation_summary': aggregate_violations(temporal_results)
    }

    # Coverage
    metrics['coverage_metrics'] = calculate_coverage_metrics()

    return metrics
```

---

## 6. Change Management

### Governance Policy Updates

```python
# Version control for governance policies
GOVERNANCE_VERSION = "1.0"
LAST_UPDATED = "2024-02-05"

def update_governance_policy(policy_section, changes, approval_info):
    """Update governance policy with change tracking."""

    # Load current policy
    with open('docs/04_governance_framework.md', 'r') as f:
        current_policy = f.read()

    # Create backup
    backup_path = f'docs/governance_versions/governance_v{GOVERNANCE_VERSION}_{LAST_UPDATED}.md'
    os.makedirs(os.path.dirname(backup_path), exist_ok=True)
    shutil.copy('docs/04_governance_framework.md', backup_path)

    # Apply changes
    # (Implementation specific to change type)

    # Log change
    change_log = {
        'version': GOVERNANCE_VERSION,
        'date': datetime.datetime.now().isoformat(),
        'section': policy_section,
        'changes': changes,
        'approved_by': approval_info['approver'],
        'approval_date': approval_info['date']
    }

    append_to_change_log('docs/governance_change_log.json', change_log)

    # Notify stakeholders
    notify_governance_change(change_log)
```

---

## Summary: Governance Enforcement Checklist

### Pre-Generation
- [ ] PII validation rules configured
- [ ] Access control roles defined
- [ ] Retention policies documented
- [ ] Audit logging enabled

### During Generation
- [ ] Validate PII compliance for each conversation
- [ ] Assign appropriate access level metadata
- [ ] Tag conversations with retention category

### Post-Generation
- [ ] Run PII compliance scan
- [ ] Verify access control filters work correctly
- [ ] Test retention policy application (dry run)
- [ ] Review audit logs for anomalies

### Ongoing
- [ ] Monthly retention policy execution
- [ ] Quarterly compliance report generation
- [ ] Annual governance policy review
- [ ] Continuous PII monitoring

---

**End of Governance Framework**
