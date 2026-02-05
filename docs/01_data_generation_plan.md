# Comprehensive Data Generation Plan

## 1. Overview & Objectives

### Primary Goal
Generate synthetic conversational datasets (meeting transcripts and Teams conversations) that integrate with existing structured retail store development data to improve AI agent cost estimation accuracy and stakeholder trust through transparent source attribution.

### Business Context
- **Current State**: AI agents use structured data (templates, historical projects, cost models) for store build/remodel estimates
- **Gap**: Critical context from conversations (constraints, vendor insights, lessons learned) is missing
- **Solution**: Add conversational signals layer to enable agents to surface contextual evidence

### Success Criteria
1. 500+ conversational artifacts across meeting transcripts and Teams channels
2. 100% cross-reference integrity with structured data (folders 01-06)
3. Temporal coherence across all conversations (no chronological violations)
4. Persona consistency (same participant maintains voice across all interactions)
5. Glean indexability (compatible with meeting transcript and Teams connectors)

---

## 2. Dataset Structure Specification

### Folder Hierarchy

```
07_Conversations/
├── meeting_transcripts/
│   ├── site_visit/
│   ├── vendor_negotiation/
│   ├── lessons_learned/
│   ├── design_review/
│   └── weekly_dev_sync/
├── teams_channels/
│   ├── store-development-general.json
│   ├── construction-vendors.json
│   ├── design-standards-updates.json
│   ├── columbus-market-planning.json
│   ├── cincinnati-market-planning.json
│   └── regional-compliance.json
└── metadata/
    ├── conversation_index.csv
    ├── participant_roles.json
    └── cross_reference_map.json
```

### File Naming Conventions

**Meeting Transcripts** (`.txt` format):
```
{meeting_type}_{store_id_or_topic}_{YYYY-MM-DD}.txt

Examples:
- site_visit_Store-217_2024-03-15.txt
- vendor_negotiation_electrical-vendors_2024-04-02.txt
- lessons_learned_Store-189_2024-02-20.txt
- design_review_StoreType-A_2024-03-10.txt
- weekly_dev_sync_Columbus-Market_2024-03-18.txt
```

**Teams Channels** (`.json` format):
```
{channel-name}.json

Examples:
- store-development-general.json
- construction-vendors.json
- columbus-market-planning.json
```

### Required Meeting Types

| Meeting Type | Purpose | Frequency | Typical Participants |
|--------------|---------|-----------|---------------------|
| site_visit_debrief | Post-visit findings, constraints, cost impacts | Per store, 2 weeks before estimate | PM, Contractor, Store Manager |
| vendor_negotiation | Pricing, timelines, supply chain constraints | Monthly, ad-hoc | Procurement, Contractors, Vendors |
| lessons_learned | Post-project review, cost variances, best practices | Per completed store | PM, Finance, Executives, Contractors |
| design_review | Template updates, design standard changes | Quarterly | Architects, Design Lead, Executives |
| weekly_dev_sync | Project status, blockers, resource allocation | Weekly | PM, Finance, Regional Managers |

### Required Teams Channels

| Channel Name | Purpose | Message Volume | Participants |
|--------------|---------|----------------|--------------|
| store-development-general | General updates, announcements | 10-15/week | All team members |
| construction-vendors | Vendor updates, lead times, pricing changes | 5-8/week | Procurement, Contractors |
| design-standards-updates | Template changes, standards updates | 2-3/month | Architects, Design Lead |
| {market}-market-planning | Market-specific planning (Columbus, Cincinnati, etc.) | 5-10/week | Regional PM, Local Managers |
| regional-compliance | Permit updates, code changes | 3-5/month | Legal, PM, Regional Managers |

---

## 3. Schema Definitions

### Meeting Transcript Schema (`.txt` format)

```
MEETING: {Meeting Type}
DATE: {YYYY-MM-DD}
PARTICIPANTS:
  - {Name} ({Role}) - {Company/Team}
  - {Name} ({Role}) - {Company/Team}
  ...
DURATION: {HH:MM}
STORE/TOPIC: {Store ID or Topic}
---

[00:00:00] {Speaker Name}: {Dialogue text}
[00:05:32] {Speaker Name}: {Dialogue text with specific cost figures, timeline impacts}
[00:12:15] {Speaker Name}: {Reference to historical stores, constraints, vendor names}
...

---
TAGS: {store-id}, {vendor-name}, {constraint-type}, {cost-category}
ACTION ITEMS:
  - {Action description} [@owner, due: YYYY-MM-DD]
REFERENCES:
  - Historical Store: {Store ID from historical_projects.csv}
  - Template: {base_template.json section}
  - Constraint: {constraints_rules.json rule ID}
```

**Example**:
```
MEETING: Site Visit Debrief
DATE: 2024-03-15
PARTICIPANTS:
  - Sarah Chen (Project Manager) - ANF Store Development
  - Tom Wilson (General Contractor) - BuildRight Construction
  - Mike Rodriguez (Store Manager) - Store #217
DURATION: 01:15
STORE/TOPIC: Store-217
---

[00:00:00] Sarah Chen: Thanks for joining. Tom, what did you find during the site visit yesterday?

[00:02:30] Tom Wilson: The electrical panel is undersized. We'll need a full upgrade to support the new HVAC and lighting load. Based on what we did at Store #189, I'm estimating $35,000 for the electrical work alone.

[00:05:45] Mike Rodriguez: That's going to push us over budget. Store #189 had similar issues, but their actual cost came in at $32K. Can we match that?

[00:08:12] Tom Wilson: Store #189 was Columbus market where labor rates are lower. Store #217 is Cincinnati - we're seeing 8-10% higher labor costs this year due to union contracts.

[00:11:20] Sarah Chen: Let me check the regional modifiers... Yes, Cincinnati shows 1.08x for electrical. Tom, does $35K account for that?

[00:13:45] Tom Wilson: Yes, that's with the regional adjustment. Also, the landlord requires all electrical work to use their approved vendor list, which limits our negotiation leverage.

---
TAGS: Store-217, Store-189, electrical-upgrade, cincinnati-market, landlord-constraint
ACTION ITEMS:
  - Update cost estimate with $35K electrical upgrade [@Sarah Chen, due: 2024-03-20]
  - Add landlord vendor restriction to constraints [@Sarah Chen, due: 2024-03-18]
REFERENCES:
  - Historical Store: Store-189 (electrical upgrade: $32K actual)
  - Template: base_template.json (electrical_panel section)
  - Constraint: Add to constraints_rules.json (landlord_approved_vendors)
```

### Teams Conversation Schema (`.json` format)

```json
{
  "channel": "{channel-name}",
  "threads": [
    {
      "thread_id": "{unique-id}",
      "date": "YYYY-MM-DD",
      "participants": [
        {
          "name": "{Full Name}",
          "role": "{Job Role}",
          "team": "{Team/Company}"
        }
      ],
      "messages": [
        {
          "timestamp": "YYYY-MM-DD HH:MM:SS",
          "author": "{Full Name}",
          "role": "{Job Role}",
          "text": "{Message content with @mentions, cost figures, references}",
          "reactions": [
            {"emoji": "👍", "count": 3}
          ],
          "tags": ["{store-id}", "{vendor}", "{topic}"]
        }
      ],
      "summary": "{AI-generated thread summary}",
      "action_items": [
        {
          "description": "{Action description}",
          "owner": "{Name}",
          "due_date": "YYYY-MM-DD",
          "status": "open|completed"
        }
      ],
      "references": {
        "stores": ["{Store-ID}"],
        "vendors": ["{Vendor Name}"],
        "meetings": ["{meeting filename}"],
        "structured_data": [
          {
            "source": "{folder name}",
            "file": "{filename}",
            "field": "{specific field/row}"
          }
        ]
      }
    }
  ]
}
```

**Example**:
```json
{
  "channel": "construction-vendors",
  "threads": [
    {
      "thread_id": "cv_2024_0315_001",
      "date": "2024-03-15",
      "participants": [
        {"name": "Jennifer Liu", "role": "Procurement Manager", "team": "ANF"},
        {"name": "Tom Wilson", "role": "General Contractor", "team": "BuildRight"},
        {"name": "Sarah Chen", "role": "Project Manager", "team": "ANF"}
      ],
      "messages": [
        {
          "timestamp": "2024-03-15 14:22:00",
          "author": "Jennifer Liu",
          "role": "Procurement Manager",
          "text": "Heads up team - our primary HVAC vendor (CoolAir Systems) just pushed lead times from 6 weeks to 10 weeks for all commercial units. This affects stores #215, #217, and #220.",
          "reactions": [{"emoji": "😬", "count": 5}],
          "tags": ["supply-chain", "hvac", "Store-215", "Store-217", "Store-220"]
        },
        {
          "timestamp": "2024-03-15 14:35:12",
          "author": "Tom Wilson",
          "role": "General Contractor",
          "text": "That's going to be a problem for Store #217 - we're already tight on schedule. @Sarah Chen can we explore the backup vendor we used for Store #189?",
          "reactions": [{"emoji": "👍", "count": 2}],
          "tags": ["Store-217", "Store-189", "schedule-risk"]
        },
        {
          "timestamp": "2024-03-15 15:01:43",
          "author": "Sarah Chen",
          "role": "Project Manager",
          "text": "Good idea Tom. Store #189's backup vendor (TempMaster) came in 15% higher but delivered on time. For Store #217, that would add ~$8K to HVAC costs but save us 4 weeks. Let me run the numbers.",
          "reactions": [{"emoji": "💡", "count": 3}],
          "tags": ["Store-217", "cost-tradeoff", "vendor-switch"]
        }
      ],
      "summary": "Primary HVAC vendor lead time increased from 6 to 10 weeks affecting 3 stores. Team discussing backup vendor option used for Store #189 (15% cost premium, faster delivery).",
      "action_items": [
        {
          "description": "Evaluate backup HVAC vendor cost impact for Store #217",
          "owner": "Sarah Chen",
          "due_date": "2024-03-18",
          "status": "open"
        }
      ],
      "references": {
        "stores": ["Store-217", "Store-189", "Store-215", "Store-220"],
        "vendors": ["CoolAir Systems", "TempMaster"],
        "meetings": ["site_visit_Store-217_2024-03-15.txt"],
        "structured_data": [
          {
            "source": "03_Historical_Projects",
            "file": "historical_projects.csv",
            "field": "Store-189 HVAC vendor"
          },
          {
            "source": "05_Cost_Models",
            "file": "material_costs.csv",
            "field": "HVAC_commercial_units"
          }
        ]
      }
    }
  ]
}
```

### Metadata Schemas

**conversation_index.csv**:
```csv
store_id,conversation_type,filename,date,participants,key_topics,cost_impact,timeline_impact
Store-217,meeting,site_visit_Store-217_2024-03-15.txt,2024-03-15,"Sarah Chen|Tom Wilson|Mike Rodriguez",electrical-upgrade|landlord-constraint,+35000,0
Store-217,teams_thread,construction-vendors.json#cv_2024_0315_001,2024-03-15,"Jennifer Liu|Tom Wilson|Sarah Chen",hvac-vendor|supply-chain,+8000,-28
Store-189,meeting,lessons_learned_Store-189_2024-02-20.txt,2024-02-20,"Sarah Chen|David Park|Tom Wilson",electrical-variance|schedule-delay,-3000,+14
```

**participant_roles.json**:
```json
{
  "participants": [
    {
      "name": "Sarah Chen",
      "role": "Project Manager",
      "team": "ANF Store Development",
      "authority_weight": 0.9,
      "expertise": ["scheduling", "budgeting", "vendor-management"],
      "voice_profile": "data-driven, collaborative, solution-focused"
    },
    {
      "name": "Tom Wilson",
      "role": "General Contractor",
      "team": "BuildRight Construction",
      "authority_weight": 0.85,
      "expertise": ["construction", "cost-estimation", "timelines"],
      "voice_profile": "cost-focused, risk-aware, detail-oriented"
    },
    {
      "name": "Jennifer Liu",
      "role": "Procurement Manager",
      "team": "ANF",
      "authority_weight": 0.8,
      "expertise": ["vendor-relations", "supply-chain", "pricing"],
      "voice_profile": "strategic, relationship-oriented, proactive"
    }
  ]
}
```

---

## 4. Generation Script Requirements

### Script 1: `generate_meeting_transcripts.py`

**Purpose**: Generate realistic meeting transcripts with proper formatting, persona-specific dialogue, and cross-references to structured data.

**Inputs**:
```python
{
  "meeting_type": "site_visit_debrief|vendor_negotiation|lessons_learned|design_review|weekly_dev_sync",
  "store_id_or_topic": "Store-217",  # or topic like "Columbus-Market"
  "date": "2024-03-15",
  "participants": [
    {"name": "Sarah Chen", "role": "Project Manager"},
    {"name": "Tom Wilson", "role": "General Contractor"}
  ],
  "context": {
    "historical_reference": "Store-189",  # For lessons learned
    "cost_focus": "electrical-upgrade",
    "constraint_type": "landlord-restriction"
  },
  "duration_minutes": 75
}
```

**Outputs**:
- Formatted `.txt` file saved to `07_Conversations/meeting_transcripts/{meeting_type}/`
- Entry in `conversation_index.csv`
- Cross-reference validation report

**Core Logic Requirements**:

1. **Template Selection & Loading**:
```python
# Load meeting type template
template = load_template(f"templates/meeting_templates/{meeting_type}.yaml")

# Template contains:
# - Dialogue flow structure (opening, key topics, action items, closing)
# - Topic-specific talking points per participant role
# - Cost/timeline data injection points
# - Cross-reference trigger phrases
```

2. **Persona Engine Integration**:
```python
# Load participant personas from config/personas.json
personas = load_personas(participants)

# Generate dialogue with persona-specific:
# - Vocabulary and phrasing patterns
# - Cost/timeline framing (contractor vs executive vs manager)
# - Decision-making authority level
# - Technical depth appropriate to role
```

3. **Cross-Reference Injection**:
```python
# Query structured data for relevant references
historical_data = query_historical_projects(context["historical_reference"])
template_data = query_build_templates(store_id)
constraint_data = query_constraints(context["constraint_type"])

# Inject references naturally into dialogue:
# - "Based on Store #189, we saw $32K actual cost..."
# - "The template calls for X, but the landlord requires Y..."
# - "Regional modifiers show 1.08x for Cincinnati electrical work..."
```

4. **Temporal Timestamp Generation**:
```python
# Generate realistic timestamps:
# - Start at [00:00:00]
# - Increment based on dialogue complexity (30-180 seconds per turn)
# - Add natural pauses for discussions (90-300 seconds)
# - Total duration matches input parameter
```

5. **Tags & Metadata Generation**:
```python
# Extract and format tags:
tags = extract_tags(dialogue_text, context)
# Tags include: store IDs, vendor names, constraint types, cost categories

# Generate action items:
action_items = extract_action_items(dialogue_text, participants)

# Map references to structured data:
references = map_structured_references(tags, dialogue_text)
```

6. **Variation Engine**:
```python
# Create 3-5 templates per meeting type with:
# - Different dialogue flows (e.g., smooth vs contentious negotiation)
# - Configurable parameters (cost ranges, timeline pressures, participants)
# - Randomized but realistic deviations from "script"
```

**Example Pseudo-Code**:
```python
def generate_meeting_transcript(config):
    # 1. Load template and personas
    template = load_template(config["meeting_type"])
    personas = load_personas(config["participants"])

    # 2. Query structured data for context
    context_data = gather_structured_context(
        store_id=config["store_id_or_topic"],
        historical_ref=config["context"]["historical_reference"]
    )

    # 3. Generate dialogue
    dialogue = []
    timestamp = 0
    for topic in template["topics"]:
        for turn in topic["dialogue_turns"]:
            speaker = get_speaker(turn["role"], personas)
            text = generate_dialogue_text(
                speaker=speaker,
                topic=topic,
                context_data=context_data,
                persona=personas[speaker]
            )
            dialogue.append({
                "timestamp": format_timestamp(timestamp),
                "speaker": speaker,
                "text": text
            })
            timestamp += calculate_turn_duration(text)

    # 4. Generate tags and metadata
    tags = extract_tags(dialogue, config["context"])
    action_items = extract_action_items(dialogue)
    references = map_references(tags, context_data)

    # 5. Format and save
    transcript = format_transcript(
        meeting_type=config["meeting_type"],
        date=config["date"],
        participants=config["participants"],
        dialogue=dialogue,
        tags=tags,
        action_items=action_items,
        references=references
    )

    save_transcript(transcript, config)
    update_conversation_index(config, tags, references)

    return transcript
```

**Validation Requirements**:
- Schema compliance check (header fields, timestamp format, tags format)
- Participant consistency (no undefined speakers)
- Cross-reference integrity (all referenced store IDs/vendors exist in structured data)
- Temporal coherence (timestamps monotonically increasing, total duration matches)
- Cost figure realism (within expected ranges for category/region)

---

### Script 2: `generate_teams_conversations.py`

**Purpose**: Generate realistic Teams channel conversations with threaded discussions, reactions, and temporal consistency with meeting transcripts.

**Inputs**:
```python
{
  "channel_name": "construction-vendors",
  "date_range": {
    "start": "2024-03-01",
    "end": "2024-03-31"
  },
  "conversation_themes": [
    {
      "theme": "supply-chain-delay",
      "stores_affected": ["Store-215", "Store-217", "Store-220"],
      "vendor": "CoolAir Systems",
      "date": "2024-03-15"
    }
  ],
  "participant_pool": ["Sarah Chen", "Tom Wilson", "Jennifer Liu", "David Park"],
  "message_density": "medium"  # low: 5-8/week, medium: 10-15/week, high: 20+/week
}
```

**Outputs**:
- Updated `.json` file for channel (appends new threads)
- Entries in `conversation_index.csv`
- Cross-reference validation report

**Core Logic Requirements**:

1. **Thread Generation**:
```python
# For each conversation theme:
# - Create thread with 3-8 messages
# - Assign participants based on theme relevance and roles
# - Generate multi-turn exchanges with natural flow
# - Include @mentions, reactions, and tags
```

2. **Message Composition**:
```python
# Generate messages with:
# - Persona-appropriate voice (use same persona engine as meetings)
# - Specific data points (costs, timelines, vendor names)
# - References to meetings (e.g., "Following up from today's site visit...")
# - Cross-references to structured data
# - Natural Teams formatting (@mentions, emoji reactions)
```

3. **Temporal Consistency**:
```python
# Ensure chronological coherence:
# - Thread dates fall within date_range
# - Messages within thread are chronologically ordered
# - Supply chain updates dated 2-4 weeks BEFORE related project estimates
# - Follow-up threads reference earlier threads with correct dates
# - Align with meeting transcript dates (e.g., Teams follow-up on meeting day or next day)
```

4. **Reaction & Engagement Simulation**:
```python
# Add realistic reactions:
# - Important updates: 3-5 reactions (👍, 😬, 💡)
# - Decision threads: Higher engagement from relevant roles
# - Routine updates: 0-2 reactions
# - Match reaction emoji to message sentiment
```

5. **Action Items & Summary Generation**:
```python
# For each thread:
# - Extract action items from message content
# - Generate concise thread summary (1-2 sentences)
# - Map to owners and due dates
# - Link to related meetings and structured data
```

6. **Cross-Channel Linking**:
```python
# Create references across channels:
# - General channel announces design review → design-standards channel discusses details
# - Vendor channel reports delay → market-specific channel discusses impact
# - Maintain consistency of facts across channels (same cost figures, dates)
```

**Example Pseudo-Code**:
```python
def generate_teams_conversations(config):
    channel = load_or_create_channel(config["channel_name"])

    for theme in config["conversation_themes"]:
        # 1. Determine participants
        participants = select_participants(
            pool=config["participant_pool"],
            theme=theme,
            required_roles=get_required_roles(theme)
        )

        # 2. Generate thread
        thread = {
            "thread_id": generate_thread_id(config["channel_name"], theme["date"]),
            "date": theme["date"],
            "participants": participants,
            "messages": []
        }

        # 3. Generate messages
        message_count = random.randint(3, 8)
        timestamp = parse_datetime(theme["date"] + " 09:00:00")

        for i in range(message_count):
            speaker = select_speaker(participants, i, theme)
            persona = load_persona(speaker)

            message_text = generate_message_text(
                speaker=speaker,
                persona=persona,
                theme=theme,
                previous_messages=thread["messages"],
                context_data=gather_structured_context(theme)
            )

            message = {
                "timestamp": timestamp.isoformat(),
                "author": speaker,
                "role": persona["role"],
                "text": message_text,
                "reactions": generate_reactions(message_text, participants),
                "tags": extract_tags(message_text, theme)
            }

            thread["messages"].append(message)
            timestamp += timedelta(minutes=random.randint(15, 180))

        # 4. Generate metadata
        thread["summary"] = generate_summary(thread["messages"])
        thread["action_items"] = extract_action_items(thread["messages"])
        thread["references"] = map_references(thread, theme)

        # 5. Add to channel
        channel["threads"].append(thread)

    # 6. Save and validate
    save_channel(channel, config["channel_name"])
    update_conversation_index(channel, config)
    validate_temporal_consistency(channel)

    return channel
```

**Validation Requirements**:
- Schema compliance (JSON structure matches specification)
- Temporal coherence (all timestamps within date_range, chronologically ordered)
- Participant consistency (all authors exist in participant_roles.json)
- Cross-reference integrity (stores, vendors, meetings exist)
- Thread coherence (messages form logical conversation flow)

---

## 5. Realism Implementation Guide

### Layer 1: Participant Personas

**Persona Dimensions**:
1. **Vocabulary & Phrasing**
2. **Data Framing** (how they discuss costs/timelines)
3. **Decision Authority**
4. **Technical Depth**
5. **Communication Style**

**Persona Definitions**:

#### Contractor Voice (e.g., Tom Wilson)
```yaml
name: Tom Wilson
role: General Contractor
company: BuildRight Construction
authority_weight: 0.85

vocabulary:
  - Technical construction terms (panel, load, HVAC tonnage)
  - Cost-specific language ("we're looking at $X", "that'll run you")
  - Risk framing ("that's going to be a problem", "we need to watch out for")

data_framing:
  costs: "Bottom-up estimation with labor/material breakdown"
  timelines: "Critical path focused, milestone-oriented"
  risks: "Proactive identification, mitigation-focused"

decision_authority:
  - Can commit to cost ranges
  - Cannot approve budget overruns without PM approval
  - Final say on construction methodology

technical_depth: High
  - Detailed knowledge of building systems
  - Cites code requirements, engineering specs
  - Explains technical constraints clearly

communication_style:
  - Direct and practical
  - Numbers-oriented (specific costs, not ranges)
  - Solution-focused (identifies problems but offers alternatives)

example_phrases:
  - "Based on what we did at Store #189..."
  - "That's going to run you about $35K with the regional adjustment"
  - "The landlord requires all electrical work to use their approved vendors"
  - "We're seeing 8-10% higher labor costs this year"
```

#### Executive Voice (e.g., David Park, VP Store Development)
```yaml
name: David Park
role: VP Store Development
company: ANF
authority_weight: 1.0

vocabulary:
  - Strategic terms (portfolio, ROI, resource allocation)
  - Financial language (budget variance, capital efficiency)
  - Decision-making language ("let's move forward with", "I'm approving")

data_framing:
  costs: "Portfolio-level impact, variance to budget"
  timelines: "Market entry timing, competitive positioning"
  risks: "Strategic implications, stakeholder impact"

decision_authority:
  - Final approval on budget variances >$50K
  - Can reallocate resources across projects
  - Sets strategic priorities

technical_depth: Medium
  - Understands high-level systems and processes
  - Defers to specialists for technical details
  - Focuses on implications rather than mechanics

communication_style:
  - Strategic and big-picture
  - Asks clarifying questions
  - Decisive when sufficient information provided

example_phrases:
  - "What's the portfolio impact if we see this across all Columbus stores?"
  - "Is this a one-time variance or a trend we need to address in templates?"
  - "I'm comfortable approving $40K if it keeps us on schedule"
  - "Sarah, work with Tom to explore the cost-timeline tradeoff"
```

#### Store Manager Voice (e.g., Mike Rodriguez)
```yaml
name: Mike Rodriguez
role: Store Manager
company: ANF Store #217
authority_weight: 0.6

vocabulary:
  - Operational terms (customer experience, store operations, staff)
  - Practical language (realistic, workable, makes sense)
  - Customer-impact framing

data_framing:
  costs: "Impact on store budget, operational constraints"
  timelines: "Customer disruption, staffing implications"
  risks: "Operational feasibility, customer experience"

decision_authority:
  - Input on operational constraints
  - Can highlight local market conditions
  - No budget approval authority

technical_depth: Low-Medium
  - Understands store systems operationally
  - Limited construction/engineering knowledge
  - Focuses on practical implications

communication_style:
  - Practical and operationally focused
  - Asks questions about feasibility
  - Advocates for customer experience

example_phrases:
  - "That's going to push us over budget - can we match Store #189's cost?"
  - "How long will this impact customer access to the store?"
  - "We've had issues with the current electrical panel during peak season"
  - "The local market is really competitive - timing matters"
```

#### Procurement Manager Voice (e.g., Jennifer Liu)
```yaml
name: Jennifer Liu
role: Procurement Manager
company: ANF
authority_weight: 0.8

vocabulary:
  - Vendor management terms (lead time, pricing, contracts)
  - Supply chain language (availability, sourcing, logistics)
  - Relationship language (partnership, negotiation, leverage)

data_framing:
  costs: "Vendor pricing, market rates, negotiation opportunities"
  timelines: "Lead times, supply chain constraints, vendor capacity"
  risks: "Vendor reliability, supply chain disruptions"

decision_authority:
  - Can negotiate vendor contracts
  - Approves vendor selection within budget
  - Escalates pricing exceptions

technical_depth: Medium
  - Understands products and specifications
  - Defers to technical experts on engineering
  - Expert in vendor capabilities and market conditions

communication_style:
  - Proactive and informative
  - Relationship-oriented
  - Data-backed (cites lead times, pricing trends)

example_phrases:
  - "Our primary HVAC vendor just pushed lead times from 6 to 10 weeks"
  - "The backup vendor we used for Store #189 came in 15% higher but delivered on time"
  - "I'm seeing steel prices up 12% across all vendors this quarter"
  - "Let me reach out to their rep and see if we can negotiate"
```

**Persona Consistency Rules**:
1. **Same participant = same voice** across all conversations
2. **Role-appropriate knowledge**: Don't have store managers quote engineering codes
3. **Authority boundaries**: Don't have contractors approve budget overruns
4. **Vocabulary consistency**: Track and reuse characteristic phrases per person
5. **Data style consistency**: Contractor gives specific costs, executive talks ranges/variance

---

### Layer 2: Temporal Coherence

**Temporal Rules & Logic**:

#### Rule 1: Meeting Sequence Logic
```python
# Site visit meetings occur 2 weeks BEFORE estimate deadline
estimate_deadline = parse_date("2024-04-01")
site_visit_date = estimate_deadline - timedelta(days=14)  # 2024-03-18

# Lessons learned meetings occur 1-2 months AFTER project completion
project_completion = parse_date("2024-02-01")
lessons_learned_date = project_completion + timedelta(days=45)  # 2024-03-18

# Design reviews occur quarterly
design_review_dates = ["2024-01-15", "2024-04-15", "2024-07-15", "2024-10-15"]

# Vendor negotiations occur monthly or ad-hoc before material orders
material_order_date = parse_date("2024-03-25")
vendor_negotiation_date = material_order_date - timedelta(days=10)  # 2024-03-15
```

#### Rule 2: Teams Thread Timing
```python
# Teams threads follow meetings on same day or next day
meeting_date = parse_date("2024-03-15")
teams_followup_date = meeting_date + timedelta(days=random.randint(0, 1))

# Supply chain update threads dated 2-4 weeks BEFORE impacted project estimates
project_estimate_date = parse_date("2024-04-01")
supply_chain_update = project_estimate_date - timedelta(days=random.randint(14, 28))

# Decision threads span 2-5 days with multiple check-ins
thread_start = parse_date("2024-03-15")
thread_messages = [
    thread_start,
    thread_start + timedelta(hours=4),
    thread_start + timedelta(days=1),
    thread_start + timedelta(days=2)
]
```

#### Rule 3: Historical Project References
```python
# Lessons learned can only reference COMPLETED projects (past dates)
current_date = parse_date("2024-03-15")
historical_projects = get_projects_completed_before(current_date)
# Can reference Store #189 (completed 2024-02-01) but NOT Store #220 (completes 2024-05-01)

# Cost comparisons reference projects with similar timeline
# "Store #189 cost $32K" is valid if Store #189 completed within last 12 months
reference_project_completion = parse_date("2024-02-01")
if (current_date - reference_project_completion).days <= 365:
    allow_cost_reference = True
```

#### Rule 4: Supply Chain Lead Time Logic
```python
# Supply chain updates reflect realistic lead time changes
# Lead times are forward-looking from update date
update_date = parse_date("2024-03-15")
new_lead_time_weeks = 10
material_available_date = update_date + timedelta(weeks=new_lead_time_weeks)  # 2024-05-24

# Projects requiring material must be scheduled after availability
project_start_date = material_available_date + timedelta(days=7)  # 2024-05-31
```

#### Rule 5: Constraint Discovery Timing
```python
# Site-specific constraints discovered during site visits
# Cannot reference constraint before site visit date
site_visit_date = parse_date("2024-03-15")
# Landlord restriction can be mentioned in conversations AFTER 2024-03-15 only

# Template constraints exist from template creation date
template_version_date = parse_date("2024-01-15")
# Can reference template requirement in any conversation after 2024-01-15
```

**Temporal Validation Decision Tree**:
```
For any conversation with date D:
│
├─ Does it reference a historical project?
│  ├─ YES: Is project completion date < D?
│  │  ├─ YES: Is completion within 12 months of D?
│  │  │  ├─ YES: ✓ Valid reference
│  │  │  └─ NO: ⚠ Flag as stale reference
│  │  └─ NO: ✗ INVALID (future reference)
│  └─ NO: Continue
│
├─ Does it reference a meeting?
│  ├─ YES: Is meeting date ≤ D?
│  │  ├─ YES: ✓ Valid reference
│  │  └─ NO: ✗ INVALID (future reference)
│  └─ NO: Continue
│
├─ Does it mention lead times or material availability?
│  ├─ YES: Is availability date = D + lead_time?
│  │  ├─ YES: ✓ Valid
│  │  └─ NO: ✗ INVALID (incorrect calculation)
│  └─ NO: Continue
│
└─ Does it reference a constraint?
   ├─ YES: Is constraint discovery date ≤ D?
   │  ├─ YES: ✓ Valid reference
   │  └─ NO: ✗ INVALID (premature knowledge)
   └─ NO: ✓ No temporal issues
```

---

### Layer 3: Cross-Referencing

**Cross-Reference Types & Implementation**:

#### Type 1: Meeting ↔ Historical Projects
```python
# Meeting mentions Store #189 electrical issue
meeting_text = "Based on Store #189, we saw $32K actual cost for electrical upgrade"

# Must link to historical_projects.csv entry
historical_entry = {
    "store_id": "Store-189",
    "completion_date": "2024-02-01",
    "electrical_actual_cost": 32000,
    "electrical_estimated_cost": 35000,
    "variance": -3000
}

# Validation:
assert "Store-189" in meeting_text
assert historical_entry["electrical_actual_cost"] == 32000  # Matches mentioned cost
assert parse_date(meeting_date) > parse_date(historical_entry["completion_date"])  # Temporal valid
```

#### Type 2: Teams Threads ↔ Build Templates
```python
# Teams discussion about template update
teams_message = "The new base template now requires upgraded electrical panels for all Type-A stores"

# Must link to base_template.json revision
template_entry = {
    "template_id": "base_template_v2.3",
    "effective_date": "2024-03-01",
    "changes": {
        "electrical_panel": {
          "previous": "200A standard",
          "new": "400A upgraded",
          "reason": "Increased HVAC and lighting load requirements"
        }
    }
}

# Validation:
assert parse_date(teams_message_date) >= parse_date(template_entry["effective_date"])
assert "upgraded electrical panels" in teams_message.lower()
```

#### Type 3: Both ↔ Constraints Rules
```python
# Meeting discovers landlord restriction
meeting_text = "The landlord requires all electrical work to use their approved vendor list"

# Teams follow-up
teams_text = "@Sarah Chen - can you add the Store #217 landlord vendor restriction to our constraints database?"

# Both link to constraints_rules.json NEW entry
constraint_entry = {
    "constraint_id": "CNS-217-001",
    "store_id": "Store-217",
    "constraint_type": "landlord_vendor_restriction",
    "category": "electrical",
    "discovered_date": "2024-03-15",
    "source": "site_visit_Store-217_2024-03-15.txt",
    "impact": {
        "cost_modifier": 1.05,
        "timeline_days": 0,
        "vendor_options": "landlord_approved_list_only"
    }
}

# Validation:
assert constraint_entry["discovered_date"] == meeting_date
assert constraint_entry["source"] == meeting_filename
assert constraint_entry["store_id"] in teams_text
```

#### Type 4: Cross-Conversation Consistency
```python
# Same fact appears in multiple conversations with consistent details
meeting_1_text = "Store #189 electrical upgrade came in at $32K actual cost"
meeting_2_text = "Remember Store #189's electrical work? We estimated $35K but actual was $32K"
teams_text = "Store #189 saved $3K on electrical by using backup vendor"

# All must reference same underlying fact:
fact = {
    "store_id": "Store-189",
    "category": "electrical_upgrade",
    "estimated_cost": 35000,
    "actual_cost": 32000,
    "variance": -3000,
    "variance_reason": "Used backup vendor with better pricing"
}

# Validation:
# All conversations mentioning Store-189 electrical must cite consistent costs
assert extract_cost(meeting_1_text, "Store-189", "electrical") == 32000
assert extract_cost(meeting_2_text, "Store-189", "electrical") == 32000
assert extract_variance(teams_text, "Store-189", "electrical") == -3000
```

#### Type 5: Vendor Name Consistency
```python
# Vendor names must be consistent across all conversations and structured data
vendor_refs = [
    "CoolAir Systems",  # Teams channel
    "CoolAir Systems",  # Vendor negotiation meeting
    "CoolAir Systems"   # Historical projects CSV
]

# NOT valid:
vendor_refs_bad = [
    "CoolAir Systems",
    "Cool Air Systems",  # Different spacing
    "CoolAir"            # Abbreviation
]

# Maintain vendor registry
vendor_registry = {
    "vendors": [
        {
            "canonical_name": "CoolAir Systems",
            "aliases": [],  # Only if explicitly defined
            "category": "HVAC",
            "appears_in": [
                "construction-vendors.json#cv_2024_0315_001",
                "vendor_negotiation_hvac-vendors_2024-02-10.txt",
                "historical_projects.csv:Store-189:hvac_vendor"
            ]
        }
    ]
}
```

#### Type 6: Regional Modifiers Alignment
```python
# Conversation mentions regional cost adjustment
meeting_text = "Cincinnati shows 1.08x for electrical work this year"

# Must align with regional_modifiers.csv
regional_data = {
    "market": "Cincinnati",
    "category": "electrical",
    "year": 2024,
    "modifier": 1.08,
    "reason": "Union contract increases"
}

# Validation:
assert extract_region(meeting_text) == regional_data["market"]
assert extract_modifier(meeting_text) == regional_data["modifier"]
assert meeting_year == regional_data["year"]
```

**Cross-Reference Mapping Table**:

| Conversational Element | Structured Data Source | Validation Rule |
|------------------------|------------------------|-----------------|
| Store ID mention | historical_projects.csv, build_templates/ | Store exists in dataset |
| Historical cost figure | historical_projects.csv:actual_cost | Cost matches within ±5% |
| Template requirement | base_template.json sections | Requirement exists in template version |
| Landlord constraint | constraints_rules.json | Constraint added with discovery date |
| Regional modifier | regional_modifiers.csv | Modifier value matches |
| Vendor name | material_costs.csv, labor_rates.csv | Vendor in registry |
| Lead time | material_costs.csv:lead_time_weeks | Lead time matches current data |
| Completion date | historical_projects.csv:completion_date | Date valid and in past |

---

## 6. Integration Mapping

### Meeting Transcripts → Historical Projects

**Linkage Pattern**: Lessons learned meetings reference completed stores with actual cost/timeline data.

**Implementation**:
```python
# For lessons_learned meeting type:
def link_to_historical_projects(meeting_config):
    store_id = meeting_config["store_id"]

    # Query historical data
    historical = query_csv(
        file="03_Historical_Projects/historical_projects.csv",
        filter={"store_id": store_id, "status": "completed"}
    )

    if not historical:
        raise ValueError(f"Store {store_id} not found or not completed")

    # Inject actual costs and variances into dialogue
    cost_variances = {
        "electrical": historical["electrical_actual"] - historical["electrical_estimate"],
        "hvac": historical["hvac_actual"] - historical["hvac_estimate"],
        "interior": historical["interior_actual"] - historical["interior_estimate"]
    }

    # Generate dialogue discussing variances
    dialogue_points = []
    for category, variance in cost_variances.items():
        if abs(variance) > 1000:  # Only discuss significant variances
            dialogue_points.append({
                "category": category,
                "estimated": historical[f"{category}_estimate"],
                "actual": historical[f"{category}_actual"],
                "variance": variance,
                "reason": historical[f"{category}_variance_reason"]
            })

    return dialogue_points
```

**Example Integration**:
```
Meeting: lessons_learned_Store-189_2024-02-20.txt

[00:15:30] Sarah Chen: Let's review the electrical costs. We estimated $35K but came in at $32K - what drove that $3K savings?

[00:16:45] Tom Wilson: We used the backup vendor TempMaster instead of our primary. They had better pricing on the panel upgrade but same quality.

Historical Projects CSV Entry:
Store-189,2024-02-01,electrical,35000,32000,-3000,"Used backup vendor TempMaster"
```

---

### Teams Conversations → Build Templates

**Linkage Pattern**: Template update discussions in Teams channels link to base_template.json revisions.

**Implementation**:
```python
# For design-standards-updates channel:
def link_to_template_changes(thread_config):
    template_version = thread_config["template_version"]

    # Query template changes
    template = load_json("02_Build_Templates/base_template.json")
    version_history = load_json("02_Build_Templates/template_version_history.json")

    changes = version_history[template_version]["changes"]

    # Generate Teams discussion about changes
    discussion_points = []
    for section, change in changes.items():
        discussion_points.append({
            "section": section,
            "previous_value": change["previous"],
            "new_value": change["new"],
            "rationale": change["reason"],
            "effective_date": version_history[template_version]["effective_date"]
        })

    return discussion_points
```

**Example Integration**:
```
Teams Thread: design-standards-updates.json

Message 1: "Heads up team - base template v2.3 is live as of March 1. All new stores now require 400A electrical panels instead of 200A."

Message 2: "What's driving this change?"

Message 3: "Increased HVAC and lighting load requirements. We saw undersized panels in 3 stores last quarter."

Template File: base_template.json v2.3
{
  "version": "2.3",
  "effective_date": "2024-03-01",
  "electrical": {
    "panel_amperage": 400,
    "previous": 200,
    "change_reason": "Increased HVAC and lighting load requirements"
  }
}
```

---

### Both → Constraints Rules

**Linkage Pattern**: Constraints discovered in conversations get added to constraints_rules.json.

**Implementation**:
```python
# Constraint discovery workflow:
def create_constraint_from_conversation(conversation_data):
    # Extract constraint details from meeting/Teams
    constraint = {
        "constraint_id": generate_constraint_id(conversation_data["store_id"]),
        "store_id": conversation_data["store_id"],
        "constraint_type": conversation_data["constraint_type"],
        "category": conversation_data["category"],
        "discovered_date": conversation_data["date"],
        "source": conversation_data["filename"],
        "impact": calculate_impact(conversation_data["constraint_details"])
    }

    # Add to constraints_rules.json
    constraints = load_json("06_Constraints_Rules/constraints_rules.json")
    constraints["store_specific"].append(constraint)
    save_json("06_Constraints_Rules/constraints_rules.json", constraints)

    # Update conversation to reference new constraint ID
    conversation_data["references"]["constraints"] = [constraint["constraint_id"]]

    return constraint
```

**Example Integration**:
```
Meeting: site_visit_Store-217_2024-03-15.txt
[00:13:45] Tom Wilson: "The landlord requires all electrical work to use their approved vendor list."

↓ Creates constraint ↓

Constraints Rules: constraints_rules.json
{
  "constraint_id": "CNS-217-001",
  "store_id": "Store-217",
  "constraint_type": "landlord_vendor_restriction",
  "category": "electrical",
  "discovered_date": "2024-03-15",
  "source": "site_visit_Store-217_2024-03-15.txt",
  "impact": {
    "cost_modifier": 1.05,
    "timeline_days": 0,
    "vendor_options": "landlord_approved_list_only"
  }
}

↓ Referenced in Teams ↓

Teams Thread: construction-vendors.json
"@Sarah Chen - FYI, Store #217 has a landlord vendor restriction (CNS-217-001) for electrical work. This limits our negotiation leverage."
```

---

### Metadata Cross-Index: conversation_index.csv

**Purpose**: Enable fast lookup of all conversations related to a store, vendor, or topic.

**Schema & Population**:
```python
def build_conversation_index():
    index_entries = []

    # Index all meeting transcripts
    for meeting_file in glob("07_Conversations/meeting_transcripts/**/*.txt"):
        metadata = parse_meeting_metadata(meeting_file)
        index_entries.append({
            "store_id": metadata["store_id"],
            "conversation_type": "meeting",
            "filename": meeting_file,
            "date": metadata["date"],
            "participants": "|".join(metadata["participants"]),
            "key_topics": "|".join(metadata["tags"]),
            "cost_impact": calculate_cost_impact(metadata),
            "timeline_impact": calculate_timeline_impact(metadata)
        })

    # Index all Teams threads
    for channel_file in glob("07_Conversations/teams_channels/*.json"):
        channel = load_json(channel_file)
        for thread in channel["threads"]:
            for store_id in thread["references"]["stores"]:
                index_entries.append({
                    "store_id": store_id,
                    "conversation_type": "teams_thread",
                    "filename": f"{channel_file}#{thread['thread_id']}",
                    "date": thread["date"],
                    "participants": "|".join([p["name"] for p in thread["participants"]]),
                    "key_topics": "|".join(set([tag for msg in thread["messages"] for tag in msg["tags"]])),
                    "cost_impact": calculate_cost_impact_from_thread(thread),
                    "timeline_impact": calculate_timeline_impact_from_thread(thread)
                })

    # Save to CSV
    save_csv("07_Conversations/metadata/conversation_index.csv", index_entries)
```

**Usage Example**:
```python
# Query: "Find all conversations about Store #217"
results = query_csv(
    file="07_Conversations/metadata/conversation_index.csv",
    filter={"store_id": "Store-217"}
)

# Returns:
# - site_visit_Store-217_2024-03-15.txt
# - construction-vendors.json#cv_2024_0315_001
# - columbus-market-planning.json#cmp_2024_0318_005
```

---

### participant_roles.json: Authority Weighting

**Purpose**: Enable AI agents to rank source credibility based on participant authority and expertise.

**Schema & Usage**:
```python
# Load participant roles
participants = load_json("07_Conversations/metadata/participant_roles.json")

# When agent evaluates a cost estimate from a conversation:
def calculate_source_credibility(conversation_data):
    speaker = conversation_data["speaker"]
    topic = conversation_data["topic"]

    participant = next(p for p in participants if p["name"] == speaker)

    # Base credibility from authority weight
    credibility = participant["authority_weight"]

    # Boost if topic matches expertise
    if topic in participant["expertise"]:
        credibility *= 1.2

    # Boost for role-appropriate topics
    role_topic_match = {
        "General Contractor": ["construction", "cost-estimation", "timelines"],
        "Procurement Manager": ["vendor-relations", "supply-chain", "pricing"],
        "Project Manager": ["scheduling", "budgeting", "vendor-management"]
    }

    if topic in role_topic_match.get(participant["role"], []):
        credibility *= 1.15

    return min(credibility, 1.0)  # Cap at 1.0

# Example:
# Tom Wilson (Contractor, authority_weight=0.85) discussing "cost-estimation"
# Credibility = 0.85 * 1.2 (expertise match) * 1.15 (role match) = 1.17 → capped at 1.0

# Sarah Chen (PM, authority_weight=0.9) discussing "cost-estimation" (not in expertise)
# Credibility = 0.9 * 1.15 (role match) = 1.035 → capped at 1.0

# Mike Rodriguez (Store Manager, authority_weight=0.6) discussing "cost-estimation"
# Credibility = 0.6 (no boosts) = 0.6
```

---

## 7. Quality Validation Checklist

### Automated Validation (Script-Based)

#### Schema Compliance Checks
```python
def validate_meeting_transcript_schema(transcript_file):
    """Validate meeting transcript against schema specification."""
    checks = {
        "has_header": False,
        "has_required_fields": False,
        "has_dialogue": False,
        "has_tags": False,
        "timestamp_format": False,
        "participant_consistency": False
    }

    content = read_file(transcript_file)

    # Check header
    required_fields = ["MEETING:", "DATE:", "PARTICIPANTS:", "DURATION:", "STORE/TOPIC:"]
    checks["has_header"] = all(field in content for field in required_fields)
    checks["has_required_fields"] = len([f for f in required_fields if f in content]) >= 4

    # Check dialogue format
    dialogue_pattern = r'\[\d{2}:\d{2}:\d{2}\] \w+.*?:'
    checks["has_dialogue"] = bool(re.search(dialogue_pattern, content))
    checks["timestamp_format"] = all(re.match(r'\d{2}:\d{2}:\d{2}', ts) for ts in re.findall(r'\[(\d{2}:\d{2}:\d{2})\]', content))

    # Check tags
    checks["has_tags"] = "TAGS:" in content

    # Check participant consistency
    participant_names = extract_participants(content)
    dialogue_speakers = extract_speakers(content)
    checks["participant_consistency"] = all(speaker in participant_names for speaker in dialogue_speakers)

    return checks

def validate_teams_conversation_schema(channel_file):
    """Validate Teams conversation against JSON schema."""
    checks = {
        "valid_json": False,
        "has_required_fields": False,
        "thread_structure": False,
        "message_structure": False,
        "references_complete": False
    }

    try:
        data = load_json(channel_file)
        checks["valid_json"] = True
    except:
        return checks

    # Check required top-level fields
    required_fields = ["channel", "threads"]
    checks["has_required_fields"] = all(field in data for field in required_fields)

    # Check thread structure
    if "threads" in data:
        thread_fields = ["thread_id", "date", "participants", "messages", "summary", "action_items", "references"]
        checks["thread_structure"] = all(
            all(field in thread for field in thread_fields)
            for thread in data["threads"]
        )

        # Check message structure
        message_fields = ["timestamp", "author", "role", "text", "reactions", "tags"]
        checks["message_structure"] = all(
            all(field in message for field in message_fields)
            for thread in data["threads"]
            for message in thread["messages"]
        )

        # Check references
        reference_fields = ["stores", "vendors", "meetings", "structured_data"]
        checks["references_complete"] = all(
            all(field in thread["references"] for field in reference_fields)
            for thread in data["threads"]
        )

    return checks
```

#### Temporal Consistency Checks
```python
def validate_temporal_consistency(conversation_file):
    """Check for temporal violations."""
    violations = []

    metadata = extract_metadata(conversation_file)
    conversation_date = parse_date(metadata["date"])

    # Check historical project references
    historical_refs = extract_historical_references(conversation_file)
    for ref in historical_refs:
        project = query_historical_project(ref["store_id"])
        if project["completion_date"] > conversation_date:
            violations.append({
                "type": "future_historical_reference",
                "details": f"References {ref['store_id']} (completes {project['completion_date']}) before completion"
            })

    # Check meeting references
    meeting_refs = extract_meeting_references(conversation_file)
    for ref in meeting_refs:
        meeting_date = extract_meeting_date(ref["meeting_file"])
        if meeting_date > conversation_date:
            violations.append({
                "type": "future_meeting_reference",
                "details": f"References meeting from {meeting_date} in conversation dated {conversation_date}"
            })

    # Check timestamp monotonicity (for meeting transcripts)
    if conversation_file.endswith(".txt"):
        timestamps = extract_timestamps(conversation_file)
        for i in range(len(timestamps) - 1):
            if timestamps[i] >= timestamps[i+1]:
                violations.append({
                    "type": "non_monotonic_timestamps",
                    "details": f"Timestamp {timestamps[i]} >= {timestamps[i+1]}"
                })

    # Check lead time calculations
    lead_time_refs = extract_lead_time_references(conversation_file)
    for ref in lead_time_refs:
        expected_date = conversation_date + timedelta(weeks=ref["weeks"])
        if ref["mentioned_date"] != expected_date:
            violations.append({
                "type": "incorrect_lead_time",
                "details": f"Lead time calculation error: {ref['weeks']} weeks from {conversation_date} should be {expected_date}, not {ref['mentioned_date']}"
            })

    return violations
```

#### Cross-Reference Integrity Checks
```python
def validate_cross_references(conversation_file):
    """Validate all cross-references to structured data."""
    errors = []

    # Check store ID references
    store_refs = extract_store_references(conversation_file)
    for store_id in store_refs:
        if not store_exists_in_historical_data(store_id):
            errors.append({
                "type": "invalid_store_reference",
                "store_id": store_id,
                "message": f"Store {store_id} not found in historical_projects.csv"
            })

    # Check vendor name consistency
    vendor_refs = extract_vendor_references(conversation_file)
    vendor_registry = load_json("config/vendor_registry.json")
    for vendor in vendor_refs:
        if vendor not in [v["canonical_name"] for v in vendor_registry["vendors"]]:
            errors.append({
                "type": "invalid_vendor_name",
                "vendor": vendor,
                "message": f"Vendor '{vendor}' not in registry. Did you mean: {suggest_vendor(vendor, vendor_registry)}"
            })

    # Check cost figure alignment
    cost_refs = extract_cost_references(conversation_file)
    for cost_ref in cost_refs:
        if cost_ref["store_id"] and cost_ref["category"]:
            historical_cost = get_historical_cost(cost_ref["store_id"], cost_ref["category"])
            if historical_cost:
                variance = abs(cost_ref["amount"] - historical_cost) / historical_cost
                if variance > 0.05:  # More than 5% variance
                    errors.append({
                        "type": "cost_mismatch",
                        "details": f"Mentioned cost ${cost_ref['amount']} for {cost_ref['store_id']} {cost_ref['category']} differs from historical ${historical_cost}"
                    })

    # Check constraint references
    constraint_refs = extract_constraint_references(conversation_file)
    constraints = load_json("06_Constraints_Rules/constraints_rules.json")
    for constraint_id in constraint_refs:
        if not constraint_exists(constraint_id, constraints):
            errors.append({
                "type": "invalid_constraint_reference",
                "constraint_id": constraint_id,
                "message": f"Constraint {constraint_id} not found in constraints_rules.json"
            })

    return errors
```

#### Participant Consistency Checks
```python
def validate_participant_consistency(participant_name):
    """Check if participant maintains consistent voice across all conversations."""
    issues = []

    # Get all conversations with this participant
    conversations = find_conversations_with_participant(participant_name)

    # Load persona
    personas = load_json("config/personas.json")
    persona = next((p for p in personas["participants"] if p["name"] == participant_name), None)

    if not persona:
        return [{"type": "undefined_participant", "name": participant_name}]

    # Check vocabulary consistency
    expected_phrases = persona.get("example_phrases", [])
    for conv in conversations:
        participant_text = extract_participant_dialogue(conv, participant_name)

        # Check if characteristic phrases appear
        phrase_usage = sum(1 for phrase in expected_phrases if phrase.lower() in participant_text.lower())
        if phrase_usage == 0 and len(expected_phrases) > 0:
            issues.append({
                "type": "missing_characteristic_phrases",
                "conversation": conv,
                "expected": expected_phrases
            })

        # Check role-appropriate knowledge
        if persona["role"] == "Store Manager" and any(term in participant_text.lower() for term in ["engineering spec", "building code section", "electrical panel amperage calculation"]):
            issues.append({
                "type": "inappropriate_technical_depth",
                "conversation": conv,
                "details": "Store Manager using contractor-level technical language"
            })

    return issues
```

### Manual Validation (Human Review)

#### Realism Review Checklist

**Dialogue Naturalness** (Sample 10% of transcripts):
- [ ] Conversations flow naturally (not scripted/robotic)
- [ ] Participants interrupt, ask clarifying questions, show personality
- [ ] Technical jargon used appropriately for roles
- [ ] Informal language mixed with formal when appropriate

**Cost Figure Realism** (Review all cost mentions):
- [ ] Costs fall within expected ranges for category/region
- [ ] Cost breakdowns add up correctly (labor + material = total)
- [ ] Variance explanations are logical and specific
- [ ] Historical cost references align with inflation/market trends

**Timeline Plausibility** (Review timeline discussions):
- [ ] Lead times realistic for materials/vendors
- [ ] Project durations align with scope
- [ ] Schedule pressure discussions reference actual constraints
- [ ] Delay explanations are specific and credible

**Vendor Behavior** (Review vendor-related conversations):
- [ ] Pricing changes have realistic drivers (supply chain, market conditions)
- [ ] Vendor capabilities match industry standards
- [ ] Negotiation dynamics feel authentic
- [ ] Vendor responsiveness varies realistically

**Decision Logic** (Review decision threads):
- [ ] Decisions consider appropriate tradeoffs (cost vs timeline vs quality)
- [ ] Authority levels respected (PMs don't override executives)
- [ ] Escalation patterns make sense
- [ ] Action items assigned to appropriate roles

---

### Data Coverage Validation

```python
def validate_data_coverage():
    """Ensure comprehensive coverage across dataset."""
    coverage_metrics = {
        "stores_with_conversations": 0,
        "stores_without_conversations": [],
        "meeting_types_coverage": {},
        "constraint_types_coverage": {},
        "vendor_coverage": {},
        "temporal_distribution": {}
    }

    # Check store coverage
    all_stores = get_all_store_ids_from_historical_data()
    stores_in_conversations = get_stores_referenced_in_conversations()

    coverage_metrics["stores_with_conversations"] = len(stores_in_conversations)
    coverage_metrics["stores_without_conversations"] = list(set(all_stores) - set(stores_in_conversations))

    # Require: Each store has 2-3 related conversations
    for store in all_stores:
        conv_count = count_conversations_for_store(store)
        if conv_count < 2:
            coverage_metrics["low_coverage_stores"].append({"store": store, "count": conv_count})

    # Check meeting type distribution
    for meeting_type in ["site_visit", "vendor_negotiation", "lessons_learned", "design_review", "weekly_dev_sync"]:
        count = count_meetings_of_type(meeting_type)
        coverage_metrics["meeting_types_coverage"][meeting_type] = count
        if count < 10:  # Minimum 10 of each type
            coverage_metrics["warnings"].append(f"Low coverage for {meeting_type}: only {count} meetings")

    # Check constraint type representation
    constraint_types = ["landlord_restriction", "permit_requirement", "union_labor", "supply_chain", "design_standard"]
    for constraint_type in constraint_types:
        count = count_conversations_mentioning_constraint_type(constraint_type)
        coverage_metrics["constraint_types_coverage"][constraint_type] = count

    # Check vendor coverage
    vendors = get_all_vendors_from_material_costs()
    for vendor in vendors:
        mention_count = count_vendor_mentions_in_conversations(vendor)
        coverage_metrics["vendor_coverage"][vendor] = mention_count

    # Check temporal distribution (conversations spread across 6-12 months)
    conversation_dates = get_all_conversation_dates()
    coverage_metrics["temporal_distribution"] = {
        "earliest": min(conversation_dates),
        "latest": max(conversation_dates),
        "span_months": (max(conversation_dates) - min(conversation_dates)).days / 30,
        "by_month": count_by_month(conversation_dates)
    }

    return coverage_metrics
```

**Coverage Requirements**:
| Metric | Minimum Threshold | Target |
|--------|------------------|--------|
| Stores with ≥2 conversations | 80% | 100% |
| Meeting types (each) | 10 | 20+ |
| Constraint types mentioned | 5 | All |
| Vendors mentioned | 70% | 90% |
| Temporal span | 6 months | 12 months |
| Monthly conversation distribution | At least 1/month | Even distribution |

---

## 8. Governance Framework

### Access Control

**Principle**: Conversational data access aligns with role-based data sensitivity.

#### Access Levels

**Level 1: Full Conversational Access**
- **Roles**: Store Development Team (PMs, Architects, Design Leads)
- **Access**: All meeting transcripts, all Teams channels, full metadata
- **Rationale**: Need complete context for cost estimation and planning

**Level 2: Cost Discussions Only**
- **Roles**: Finance Team, Budget Analysts
- **Access**:
  - ✓ Lessons learned meetings (cost variance discussions)
  - ✓ Vendor negotiation meetings (pricing)
  - ✗ Site visit debriefs (redact vendor negotiation details)
  - ✓ Cost-related Teams threads (filtered by tags)
- **Redactions**: Specific vendor pricing strategies, negotiation tactics
- **Rationale**: Need cost data for budgeting but not competitive vendor intelligence

**Level 3: Summary Views**
- **Roles**: Executive Team (VPs, C-suite)
- **Access**:
  - ✓ Meeting summaries (from action_items and summary fields)
  - ✓ Decision threads (Teams threads tagged "decision")
  - ✗ Detailed transcripts (too granular)
  - ✓ Conversation index (what was discussed, when, by whom)
- **Rationale**: Need strategic context and decision history, not verbatim details

**Level 4: Public/Cross-Functional**
- **Roles**: Store Operations, Marketing, IT
- **Access**:
  - ✓ Design review meetings (standards and templates)
  - ✓ Design-standards-updates Teams channel
  - ✗ Cost discussions, vendor negotiations
- **Rationale**: Need design standards for operations but not financial details

**Implementation**:
```python
def filter_conversation_by_access_level(conversation, user_role):
    """Apply access control filters based on user role."""
    access_rules = load_json("config/access_control_rules.json")
    user_access = access_rules[user_role]

    if user_access["level"] == "full":
        return conversation  # No filtering

    elif user_access["level"] == "cost_only":
        # Filter to cost-related content
        if conversation["type"] == "meeting":
            if conversation["meeting_type"] not in ["lessons_learned", "vendor_negotiation"]:
                return None  # Hide non-cost meetings
            # Redact vendor negotiation tactics
            conversation = redact_negotiation_details(conversation)

        elif conversation["type"] == "teams_thread":
            if "cost" not in conversation["tags"] and "budget" not in conversation["tags"]:
                return None  # Hide non-cost threads

    elif user_access["level"] == "summary":
        # Return summary only
        return {
            "date": conversation["date"],
            "type": conversation["type"],
            "participants": conversation["participants"],
            "summary": conversation["summary"],
            "action_items": conversation["action_items"],
            "key_topics": conversation["tags"]
        }

    elif user_access["level"] == "public":
        # Filter to design/standards only
        if conversation["type"] == "meeting" and conversation["meeting_type"] != "design_review":
            return None
        if conversation["type"] == "teams_thread" and conversation["channel"] != "design-standards-updates":
            return None

    return conversation
```

---

### Data Retention

**Principle**: Balance data utility with storage efficiency and compliance.

#### Retention Policies

**Active Projects** (In-progress stores):
- **Retention**: Full conversational history indexed and searchable
- **Duration**: From project kickoff until 6 months post-completion
- **Storage**: Primary Glean index, full search enabled
- **Rationale**: Need complete context for ongoing cost estimation and decision-making

**Completed Projects** (6 months - 2 years post-completion):
- **Retention**: Archive detailed conversations, maintain summaries
- **Actions**:
  - Move full transcripts/threads to archive storage (not Glean-indexed)
  - Keep conversation_index.csv entries (for discovery)
  - Keep action_items and summaries (for quick reference)
  - Remove detailed dialogue from search index
- **Access**: Available on-demand via archive retrieval (slower)
- **Rationale**: Reduce index bloat while preserving retrievability

**Historical Lessons Learned** (Indefinite):
- **Retention**: Sanitized versions retained permanently
- **Actions**:
  - Extract key lessons into structured knowledge base
  - Anonymize participant names (keep roles only)
  - Remove store-specific identifiers (keep "Type-A store in Columbus market")
  - Keep cost variance patterns and root causes
- **Storage**: Lessons learned database (separate from raw conversations)
- **Rationale**: Preserve institutional knowledge without PII or outdated project details

**Deletion** (2+ years post-completion):
- **Scope**: Raw transcript/thread details for non-significant projects
- **Exceptions**: Projects with major variances (>20%) or unique constraints retained
- **Process**:
  1. Verify lessons extracted
  2. Confirm no ongoing legal/audit requirements
  3. Delete detailed dialogue, keep metadata
- **Rationale**: Compliance and storage efficiency

**Implementation**:
```python
def apply_retention_policy():
    """Apply retention policies based on project completion dates."""
    current_date = datetime.now()

    for conversation in get_all_conversations():
        store_id = conversation["store_id"]
        project_completion = get_project_completion_date(store_id)

        if not project_completion:
            # Active project - keep fully indexed
            conversation["retention_status"] = "active"
            continue

        days_since_completion = (current_date - project_completion).days

        if days_since_completion <= 180:  # 6 months
            # Recently completed - keep fully indexed
            conversation["retention_status"] = "active"

        elif days_since_completion <= 730:  # 2 years
            # Archive detailed dialogue
            archive_conversation_details(conversation)
            keep_conversation_summary(conversation)
            conversation["retention_status"] = "archived"

        else:  # 2+ years
            # Extract lessons and delete details (unless exceptional)
            if is_exceptional_project(store_id):
                conversation["retention_status"] = "archived"
            else:
                extract_lessons_to_knowledge_base(conversation)
                delete_conversation_details(conversation)
                conversation["retention_status"] = "deleted_details_only"
```

---

### PII Handling

**Principle**: Use realistic but fictional data to avoid real PII exposure.

#### PII Categories & Handling

**Participant Names**:
- **Approach**: Use realistic but fictional names
- **Implementation**: Generate diverse names from name database
- **Consistency**: Same fictional person across all conversations (tracked in participant_roles.json)
- **Avoid**: Real employee names, even if publicly known

**Vendor Names**:
- **Approach**: Use fictional vendor names OR anonymize real vendors
- **Implementation**:
  - Option 1: Create fictional vendor registry (e.g., "BuildRight Construction", "CoolAir Systems")
  - Option 2: If referencing real vendors, use category + ID (e.g., "HVAC-Vendor-A")
- **Rationale**: Avoid disclosing real vendor relationships or pricing

**Store Locations**:
- **Approach**: Use generic market names (Columbus, Cincinnati) but avoid specific addresses
- **Implementation**:
  - ✓ "Columbus market", "Cincinnati downtown"
  - ✗ "123 Main Street, Columbus OH 43215"
- **Rationale**: Market-level data useful for regional modifiers, but specific addresses are PII

**Lease Terms & Landlord Details**:
- **Approach**: Discuss constraints generically, avoid landlord names
- **Implementation**:
  - ✓ "The landlord requires approved vendor list"
  - ✗ "Easton Properties LLC requires..."
- **Rationale**: Landlord relationships are commercially sensitive

**Contact Information**:
- **Approach**: No phone numbers, emails, or addresses in synthetic data
- **Exception**: Can use fictional emails in Teams @mentions if realistic (e.g., @sarah.chen, not @sarah.chen@anf.com)

**Financial Details**:
- **Approach**: Use realistic cost ranges but not real project budgets
- **Implementation**: Generate costs based on regional/category averages ± variation
- **Rationale**: Protect actual project financials while maintaining realism

**Implementation Checklist**:
```python
def validate_pii_compliance(conversation):
    """Check for PII violations in synthetic data."""
    violations = []

    # Check for email addresses
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, conversation["text"])
    if any("@" + domain in email for email in emails for domain in ["anf.com", "company.com"]):
        violations.append({"type": "real_email", "details": emails})

    # Check for phone numbers
    phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
    if re.search(phone_pattern, conversation["text"]):
        violations.append({"type": "phone_number"})

    # Check for specific addresses
    address_indicators = ["street", "avenue", "boulevard", "suite", "apt", "zip"]
    if any(indicator in conversation["text"].lower() for indicator in address_indicators):
        violations.append({"type": "potential_address"})

    # Check participant names against real employee list (if available)
    if real_employee_list:
        for participant in conversation["participants"]:
            if participant["name"] in real_employee_list:
                violations.append({"type": "real_employee_name", "name": participant["name"]})

    return violations
```

---

## 9. Phased Implementation Roadmap

### Phase 1: MVP (20 Stores)

**Objectives**:
- Validate data generation approach
- Test cross-reference integrity
- Confirm Glean indexability
- Establish quality baselines

**Deliverables**:

| Component | Target | Details |
|-----------|--------|---------|
| Meeting Transcripts | 15 | 3 site visits, 3 vendor negotiations, 5 lessons learned, 2 design reviews, 2 weekly syncs |
| Teams Threads | 50 messages | Across 4 channels (general, vendors, design, 1 market-specific) |
| Stores Covered | 20 | Mix of completed and in-progress |
| Participants | 8-10 | Core team (PMs, contractors, procurement, 1-2 executives) |
| Metadata Files | 3 | conversation_index.csv, participant_roles.json, cross_reference_map.json |

**Timeline**: 2 weeks

**Activities**:
1. **Week 1: Setup & Initial Generation**
   - Configure personas.json with 8-10 core participants
   - Create 5 meeting templates (one per type)
   - Generate 5 meeting transcripts (one per type)
   - Generate 20 Teams messages across 4 channels
   - Run schema validation

2. **Week 2: Iteration & Validation**
   - Generate remaining 10 meeting transcripts
   - Generate remaining 30 Teams messages
   - Build conversation_index.csv
   - Run cross-reference validation
   - Manual review for realism (sample 20%)
   - Test Glean indexing (if available)

**Success Criteria**:
- ✓ 100% schema compliance
- ✓ Zero cross-reference integrity errors
- ✓ Zero temporal consistency violations
- ✓ Positive manual realism review (4/5 rating)
- ✓ Successfully indexed in Glean (if tested)

**Estimated Output**: ~30 conversational artifacts, ~15,000 words

---

### Phase 2: Scaling (100 Stores)

**Objectives**:
- Scale generation process
- Add market-specific conversations
- Implement temporal progression (6-month history)
- Expand participant pool

**Deliverables**:

| Component | Target | Details |
|-----------|--------|---------|
| Meeting Transcripts | 75 | 15 site visits, 12 vendor negotiations, 25 lessons learned, 10 design reviews, 13 weekly syncs |
| Teams Threads | 200 messages | Across 6 channels (add 2 market-specific: Columbus, Cincinnati) |
| Stores Covered | 100 | Comprehensive coverage of dataset |
| Participants | 20-25 | Add regional managers, architects, finance analysts |
| Temporal Span | 6 months | Conversations dated across Jan-Jun 2024 |

**Timeline**: 4 weeks

**Activities**:
1. **Week 1: Expand Configuration**
   - Add 12-15 new participants to personas.json
   - Create market-specific conversation themes
   - Add temporal progression logic to scripts
   - Refine meeting templates based on Phase 1 learnings

2. **Week 2-3: Batch Generation**
   - Generate 60 additional meeting transcripts
   - Generate 150 additional Teams messages
   - Implement temporal consistency across 6-month span
   - Link conversations to 100 stores

3. **Week 4: Validation & Refinement**
   - Run full validation suite
   - Manual realism review (sample 10%)
   - Coverage analysis (ensure all stores have 2-3 conversations)
   - Glean indexing test

**Success Criteria**:
- ✓ 100% stores have ≥2 related conversations
- ✓ All meeting types have ≥10 examples
- ✓ Temporal span = 6 months with even distribution
- ✓ <5% cross-reference errors (with remediation plan)
- ✓ Positive manual realism review (4/5 rating)

**Estimated Output**: ~150 conversational artifacts, ~75,000 words

---

### Phase 3: Production (Full Dataset)

**Objectives**:
- Generate conversations for all stores in dataset
- Add quarterly/annual patterns (budget cycles, template reviews)
- Implement dynamic update capability
- Production-ready quality and governance

**Deliverables**:

| Component | Target | Details |
|-----------|--------|---------|
| Meeting Transcripts | 250 | Full coverage across all meeting types and stores |
| Teams Threads | 300 messages | Dense channel activity across 12-month period |
| Stores Covered | All (250+) | Every store has relevant conversational context |
| Participants | 30-40 | Full organizational representation |
| Temporal Span | 12 months | Full year of conversational history |
| Quarterly Events | 4 | Budget reviews, template updates, strategic planning |

**Timeline**: 6 weeks

**Activities**:
1. **Week 1-2: Full-Scale Generation**
   - Generate remaining 175 meeting transcripts
   - Generate remaining 100 Teams messages
   - Implement quarterly event patterns:
     - Q1: Budget planning, template v2.2 review
     - Q2: Mid-year review, template v2.3 release
     - Q3: Portfolio analysis, vendor contract renewals
     - Q4: Year-end review, template v2.4 planning

2. **Week 3: Temporal Coherence & Linking**
   - Ensure all quarterly events linked to relevant monthly/weekly conversations
   - Validate temporal progression (budget discussions precede approvals, etc.)
   - Cross-reference all conversations to structured data

3. **Week 4: Quality Assurance**
   - Full validation suite on complete dataset
   - Manual review (sample 5%, stratified by meeting type and date)
   - Persona consistency check across all participants
   - Coverage analysis

4. **Week 5: Governance Implementation**
   - Implement access control filters
   - Set up retention policy automation
   - PII compliance final check
   - Create user documentation

5. **Week 6: Production Readiness**
   - Glean indexing of full dataset
   - Performance testing (search latency, retrieval accuracy)
   - Stakeholder demo and feedback
   - Production deployment

**Success Criteria**:
- ✓ 100% stores have ≥2 conversations
- ✓ All meeting types have ≥20 examples
- ✓ Zero critical validation errors
- ✓ Temporal coherence across 12-month span
- ✓ Positive manual realism review (4.5/5 rating)
- ✓ Glean search returns relevant results (<2s latency)
- ✓ Access control tested and functional

**Estimated Output**: ~500+ conversational artifacts, ~250,000 words

---

### Dynamic Update Capability (Post-Production)

**Purpose**: Enable ongoing conversation generation as new stores are added.

**Implementation**:
```python
def generate_conversations_for_new_store(store_id):
    """Generate conversations for a newly added store."""
    # 1. Determine project timeline
    project_timeline = get_project_timeline(store_id)

    # 2. Generate site visit debrief (2 weeks before estimate)
    site_visit_date = project_timeline["estimate_date"] - timedelta(days=14)
    generate_meeting_transcript({
        "meeting_type": "site_visit_debrief",
        "store_id": store_id,
        "date": site_visit_date,
        "participants": select_participants(["PM", "Contractor", "Store Manager"])
    })

    # 3. Generate vendor negotiation (if applicable)
    if has_special_vendor_requirements(store_id):
        vendor_negotiation_date = project_timeline["material_order_date"] - timedelta(days=10)
        generate_meeting_transcript({
            "meeting_type": "vendor_negotiation",
            "store_id": store_id,
            "date": vendor_negotiation_date,
            "participants": select_participants(["Procurement", "Contractor", "Vendor"])
        })

    # 4. Generate Teams threads (2-3 related discussions)
    generate_teams_conversations({
        "channel_name": determine_market_channel(store_id),
        "conversation_themes": [
            {"theme": "project-kickoff", "store_id": store_id, "date": project_timeline["kickoff"]},
            {"theme": "constraint-discussion", "store_id": store_id, "date": site_visit_date + timedelta(days=1)}
        ]
    })

    # 5. If completed: generate lessons learned
    if project_timeline["status"] == "completed":
        lessons_learned_date = project_timeline["completion_date"] + timedelta(days=45)
        generate_meeting_transcript({
            "meeting_type": "lessons_learned",
            "store_id": store_id,
            "date": lessons_learned_date,
            "participants": select_participants(["PM", "Finance", "Contractor", "Executive"])
        })
```

---

## 10. Success Criteria & Metrics

### Quantitative Metrics

**Volume Metrics**:
| Metric | Phase 1 Target | Phase 2 Target | Phase 3 Target |
|--------|---------------|----------------|----------------|
| Total Conversations | 30 | 150 | 500+ |
| Stores with ≥2 Conversations | 20 (100%) | 100 (100%) | 250+ (100%) |
| Meeting Transcripts | 15 | 75 | 250 |
| Teams Messages | 50 | 200 | 300 |
| Unique Participants | 10 | 25 | 40 |
| Temporal Span (months) | 1 | 6 | 12 |

**Quality Metrics**:
| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Schema Compliance | 100% | Automated validation |
| Cross-Reference Integrity | 100% | Automated validation (zero broken links) |
| Temporal Consistency | 100% | Automated validation (zero violations) |
| Participant Consistency | ≥95% | Automated + Manual review |
| Cost Figure Realism | ≥90% | Manual review (within expected ranges) |
| Realism Score | ≥4/5 | Manual review by domain experts |

**Coverage Metrics**:
| Category | Target | Phase 3 Goal |
|----------|--------|-------------|
| Meeting Types (each) | ≥10 | ≥20 |
| Constraint Types Mentioned | 5 | All (8+) |
| Vendors Mentioned | ≥70% of registry | ≥90% |
| Markets Covered | 3 | All (6+) |
| Monthly Distribution | ≥1/month | Even spread |

---

### Qualitative Success Indicators

**Conversational Realism**:
- [ ] Domain experts confirm dialogues sound authentic
- [ ] Personas are distinct and consistent
- [ ] Decisions and constraints feel credible
- [ ] Cost/timeline discussions align with industry practices

**Integration Quality**:
- [ ] AI agents successfully retrieve relevant conversational context
- [ ] Cross-references enable traceability to source conversations
- [ ] Conversations add non-redundant value beyond structured data
- [ ] Source attribution improves stakeholder trust in estimates

**Glean Indexability**:
- [ ] All conversations indexed without errors
- [ ] Search queries return relevant conversations
- [ ] Meeting transcript connector extracts metadata correctly
- [ ] Teams connector threads conversations properly

**Governance Effectiveness**:
- [ ] Access control filters work as intended
- [ ] Retention policies automate archival correctly
- [ ] No PII violations in synthetic data
- [ ] Documentation enables self-service data generation

---

### Acceptance Testing

**Test 1: End-to-End AI Agent Workflow**
```
Scenario: AI agent estimates cost for Store #225 (new Cincinnati store)

Steps:
1. Agent queries for relevant conversational context
2. Retrieves:
   - Site visit debrief mentioning electrical constraints
   - Teams thread about Cincinnati market labor rates
   - Lessons learned from Store #189 (similar constraints)
3. Agent cites specific conversations in estimate rationale
4. Stakeholder reviews estimate and can trace claims to source conversations

Success Criteria:
✓ Agent retrieves 2-3 relevant conversations
✓ Conversations contain specific, actionable insights
✓ Source attribution is accurate and verifiable
✓ Stakeholder trusts estimate more due to transparent sourcing
```

**Test 2: Cross-Reference Integrity**
```
Scenario: Validate all store ID references resolve correctly

Steps:
1. Extract all store IDs mentioned in conversations
2. Check each against historical_projects.csv
3. Verify completion dates precede conversation dates
4. Confirm cost figures align (within 5%)

Success Criteria:
✓ 100% of store references resolve to valid entries
✓ Zero temporal violations (future references)
✓ ≥95% cost figure alignment
```

**Test 3: Temporal Coherence**
```
Scenario: Follow a store's conversation timeline from kickoff to completion

Steps:
1. Select completed Store #189
2. Retrieve all conversations mentioning Store #189
3. Order chronologically
4. Validate sequence: kickoff → site visit → vendor negotiation → weekly syncs → completion → lessons learned

Success Criteria:
✓ Conversations appear in logical chronological order
✓ No references to events before they occurred
✓ Lead times and timelines calculate correctly
✓ Lessons learned only references completed aspects
```

**Test 4: Persona Consistency**
```
Scenario: Validate Tom Wilson (Contractor) maintains consistent voice

Steps:
1. Extract all dialogue/messages from Tom Wilson
2. Check for characteristic phrases from persona definition
3. Validate technical depth appropriate to role
4. Confirm cost-framing style matches persona

Success Criteria:
✓ ≥60% of conversations include characteristic phrases
✓ No instances of inappropriate knowledge (e.g., executive-level strategy)
✓ Consistent cost-oriented, risk-aware communication style
```

**Test 5: Glean Search Effectiveness**
```
Scenario: Search for conversations about "electrical upgrades Cincinnati"

Steps:
1. Execute Glean search query
2. Review top 5 results
3. Verify relevance (actually discuss electrical work in Cincinnati market)
4. Check result diversity (different conversation types)

Success Criteria:
✓ ≥4/5 results are relevant
✓ Results include both meetings and Teams threads
✓ Search latency <2 seconds
✓ Results ranked by relevance (not just date)
```

---

## Appendices

### Appendix A: Sample Conversation Templates

*See `templates/meeting_templates/` for full templates*

**Site Visit Debrief Template (Abbreviated)**:
```yaml
meeting_type: site_visit_debrief
duration_minutes: 60-90
required_participants:
  - role: Project Manager
  - role: General Contractor
  - role: Store Manager (optional)

dialogue_flow:
  - section: opening
    topics: [agenda, site visit recap]
  - section: findings
    topics: [structural observations, constraint discoveries, cost implications]
  - section: cost_discussion
    topics: [cost estimates, historical comparisons, variance drivers]
  - section: action_items
    topics: [next steps, owner assignments, deadlines]

injection_points:
  - type: historical_cost_reference
    template: "Based on {historical_store}, we saw ${historical_cost} for {category}"
  - type: constraint_discovery
    template: "The landlord requires {constraint_detail}"
  - type: regional_modifier
    template: "{market} shows {modifier}x for {category} due to {reason}"
```

### Appendix B: Vendor Registry

*See `config/vendor_registry.json`*

**Sample Vendors**:
```json
{
  "vendors": [
    {
      "canonical_name": "BuildRight Construction",
      "category": "General Contractor",
      "specialties": ["store-builds", "remodels"],
      "markets_served": ["Columbus", "Cincinnati", "Cleveland"]
    },
    {
      "canonical_name": "CoolAir Systems",
      "category": "HVAC",
      "specialties": ["commercial-units", "installation"],
      "typical_lead_time_weeks": 8
    }
  ]
}
```

### Appendix C: Regional Modifiers Reference

*Alignment with `04_Regional_Factors/regional_modifiers.csv`*

| Market | Category | Modifier | Reason |
|--------|----------|----------|--------|
| Cincinnati | Electrical | 1.08 | Union contracts |
| Columbus | HVAC | 1.05 | Higher demand |
| Cleveland | Interior | 0.95 | Lower labor costs |

### Appendix D: Temporal Rules Reference

**Meeting Timing Rules**:
- Site Visit: Estimate Date - 14 days
- Vendor Negotiation: Material Order - 10 days
- Lessons Learned: Completion + 45 days
- Design Review: Quarterly (Jan 15, Apr 15, Jul 15, Oct 15)
- Weekly Sync: Every Monday

**Teams Thread Timing**:
- Meeting Follow-up: Same day or next day
- Supply Chain Update: 2-4 weeks before impact
- Decision Thread: 2-5 day span

---

## Document Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2024-02-05 | Initial comprehensive plan | Data Generation Team |

---

**End of Data Generation Plan**
