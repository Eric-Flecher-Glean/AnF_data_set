# Schema Specifications

## Overview

This document provides detailed schema specifications for all conversational data artifacts, including meeting transcripts, Teams conversations, and metadata files.

## 1. Meeting Transcript Schema

### File Format: Plain Text (`.txt`)

### Structure

```
MEETING: {Meeting Type}
DATE: {YYYY-MM-DD}
PARTICIPANTS:
  - {Name} ({Role}) - {Company/Team}
  - {Name} ({Role}) - {Company/Team}
DURATION: {HH:MM}
STORE/TOPIC: {Store ID or Topic}
---

[HH:MM:SS] {Speaker Name}: {Dialogue text}
[HH:MM:SS] {Speaker Name}: {Dialogue text}
...

---
TAGS: {tag1}, {tag2}, {tag3}
ACTION ITEMS:
  - {Description} [@owner, due: YYYY-MM-DD]
REFERENCES:
  - Historical Store: {Store-ID}
  - Template: {template_file.json section}
  - Constraint: {constraint_id}
```

### Field Specifications

#### Header Section

| Field | Type | Required | Format | Example |
|-------|------|----------|--------|---------|
| MEETING | String | Yes | Meeting type from enum | Site Visit Debrief |
| DATE | Date | Yes | YYYY-MM-DD | 2024-03-15 |
| PARTICIPANTS | List | Yes | Name (Role) - Company | Sarah Chen (Project Manager) - ANF |
| DURATION | Time | Yes | HH:MM | 01:15 |
| STORE/TOPIC | String | Yes | Store-### or topic | Store-217 |

**Meeting Type Enum**:
- Site Visit Debrief
- Vendor Negotiation
- Lessons Learned
- Design Review
- Weekly Dev Sync

#### Dialogue Section

| Element | Format | Example |
|---------|--------|---------|
| Timestamp | [HH:MM:SS] | [00:15:30] |
| Speaker Name | Full name matching participants | Sarah Chen |
| Dialogue Text | Natural language | We need to address the electrical panel issue |

**Dialogue Rules**:
- Timestamps start at [00:00:00]
- Timestamps must be monotonically increasing
- Total span should match DURATION ± 5 minutes
- Speaker names must match PARTICIPANTS exactly
- Dialogue should include specific data points (costs, dates, references)

#### Footer Section

**TAGS Format**:
```
TAGS: Store-217, electrical-upgrade, cincinnati-market, landlord-constraint
```
- Comma-separated
- Include: store IDs, vendor names, constraint types, cost categories, market names

**ACTION ITEMS Format**:
```
ACTION ITEMS:
  - Update cost estimate with $35K electrical upgrade [@Sarah Chen, due: 2024-03-20]
  - Add landlord vendor restriction to constraints [@Sarah Chen, due: 2024-03-18]
```
- One per line with indent
- Include: description, owner (@Name), due date

**REFERENCES Format**:
```
REFERENCES:
  - Historical Store: Store-189 (electrical upgrade: $32K actual)
  - Template: base_template.json (electrical_panel section)
  - Constraint: CNS-217-001 (landlord_approved_vendors)
```
- Link to structured data sources
- Include context in parentheses

### Validation Rules

1. **Required Fields**: All header fields must be present
2. **Date Format**: DATE must be YYYY-MM-DD
3. **Timestamp Format**: [HH:MM:SS] with leading zeros
4. **Participant Consistency**: All speakers in dialogue appear in PARTICIPANTS
5. **Temporal Coherence**: Timestamps monotonically increasing
6. **Tag Format**: Comma-separated, no leading/trailing spaces
7. **Duration Match**: Total dialogue span ≈ DURATION

---

## 2. Teams Conversation Schema

### File Format: JSON (`.json`)

### Structure

```json
{
  "channel": "channel-name",
  "threads": [
    {
      "thread_id": "unique-thread-id",
      "date": "YYYY-MM-DD",
      "participants": [
        {
          "name": "Full Name",
          "role": "Job Title",
          "team": "Company/Department"
        }
      ],
      "messages": [
        {
          "timestamp": "YYYY-MM-DD HH:MM:SS",
          "author": "Full Name",
          "role": "Job Title",
          "text": "Message content",
          "reactions": [
            {"emoji": "👍", "count": 3}
          ],
          "tags": ["tag1", "tag2"]
        }
      ],
      "summary": "Thread summary text",
      "action_items": [
        {
          "description": "Action description",
          "owner": "Full Name",
          "due_date": "YYYY-MM-DD",
          "status": "open"
        }
      ],
      "references": {
        "stores": ["Store-ID"],
        "vendors": ["Vendor Name"],
        "meetings": ["meeting_filename.txt"],
        "structured_data": [
          {
            "source": "folder_name",
            "file": "filename",
            "field": "specific_field"
          }
        ]
      }
    }
  ]
}
```

### Field Specifications

#### Top-Level Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| channel | String | Yes | Channel name (lowercase-hyphenated) |
| threads | Array | Yes | Array of thread objects |

#### Thread Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| thread_id | String | Yes | Unique ID: {channel}_{YYYYMMDD}_{###} |
| date | String | Yes | Thread start date (YYYY-MM-DD) |
| participants | Array | Yes | Array of participant objects |
| messages | Array | Yes | Array of message objects (min 1) |
| summary | String | Yes | 1-2 sentence thread summary |
| action_items | Array | No | Array of action item objects |
| references | Object | Yes | References to other data |

#### Participant Object

| Field | Type | Required | Example |
|-------|------|----------|---------|
| name | String | Yes | Sarah Chen |
| role | String | Yes | Project Manager |
| team | String | Yes | ANF Store Development |

#### Message Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| timestamp | String | Yes | YYYY-MM-DD HH:MM:SS |
| author | String | Yes | Must match participant name |
| role | String | Yes | Must match participant role |
| text | String | Yes | Message content (supports @mentions) |
| reactions | Array | No | Array of reaction objects |
| tags | Array | Yes | Array of tags (can be empty) |

#### Reaction Object

| Field | Type | Required | Example |
|-------|------|----------|---------|
| emoji | String | Yes | 👍 |
| count | Integer | Yes | 3 |

#### Action Item Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| description | String | Yes | What needs to be done |
| owner | String | Yes | Full name (must be participant) |
| due_date | String | No | YYYY-MM-DD |
| status | String | Yes | "open" or "completed" |

#### References Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| stores | Array[String] | Yes | Store IDs mentioned (can be empty) |
| vendors | Array[String] | Yes | Vendor names mentioned (can be empty) |
| meetings | Array[String] | Yes | Meeting filenames referenced (can be empty) |
| structured_data | Array[Object] | Yes | Links to structured data (can be empty) |

**Structured Data Reference Object**:
```json
{
  "source": "03_Historical_Projects",
  "file": "historical_projects.csv",
  "field": "Store-189 HVAC vendor"
}
```

### Validation Rules

1. **JSON Validity**: Must parse as valid JSON
2. **Required Fields**: All required fields present
3. **Date/Time Format**: Strict ISO format
4. **Author Consistency**: All message authors in participants
5. **Timestamp Order**: Messages chronologically ordered within thread
6. **Tag Format**: Lowercase-hyphenated strings
7. **Reference Integrity**: Referenced stores/vendors/meetings exist
8. **Action Item Owner**: Owner must be thread participant

---

## 3. Conversation Index Schema

### File Format: CSV

### Structure

```csv
store_id,conversation_type,filename,date,participants,key_topics,cost_impact,timeline_impact
Store-217,meeting,site_visit_Store-217_2024-03-15.txt,2024-03-15,"Sarah Chen|Tom Wilson|Mike Rodriguez",electrical-upgrade|landlord-constraint,35000,0
Store-217,teams_thread,construction-vendors.json#cv_2024_0315_001,2024-03-15,"Jennifer Liu|Tom Wilson|Sarah Chen",hvac-vendor|supply-chain,8000,-28
```

### Field Specifications

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| store_id | String | Store identifier | Store-217 |
| conversation_type | Enum | "meeting" or "teams_thread" | meeting |
| filename | String | File path (with #thread_id for Teams) | site_visit_Store-217_2024-03-15.txt |
| date | Date | Conversation date (YYYY-MM-DD) | 2024-03-15 |
| participants | String | Pipe-separated names | Sarah Chen\|Tom Wilson |
| key_topics | String | Pipe-separated topic tags | electrical-upgrade\|constraint |
| cost_impact | Integer | Cost impact in dollars (+/-) | 35000 |
| timeline_impact | Integer | Timeline impact in days (+/-) | -28 |

### Usage

**Query Examples**:
```python
# Find all conversations about Store-217
df[df['store_id'] == 'Store-217']

# Find all conversations with cost impact >$10K
df[df['cost_impact'] > 10000]

# Find all conversations from March 2024
df[df['date'].str.startswith('2024-03')]

# Find conversations with specific participant
df[df['participants'].str.contains('Sarah Chen')]
```

---

## 4. Participant Roles Schema

### File Format: JSON

### Structure

```json
{
  "participants": [
    {
      "name": "Sarah Chen",
      "role": "Project Manager",
      "team": "ANF Store Development",
      "authority_weight": 0.9,
      "expertise": ["scheduling", "budgeting", "vendor-management"],
      "voice_profile": "data-driven, collaborative, solution-focused",
      "email": "sarah.chen",
      "characteristic_phrases": [
        "Let me check the numbers",
        "What does the data show",
        "We need to validate that against"
      ]
    }
  ]
}
```

### Field Specifications

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | String | Yes | Full name (unique) |
| role | String | Yes | Job title |
| team | String | Yes | Company/department |
| authority_weight | Float | Yes | 0.0-1.0, decision-making weight |
| expertise | Array[String] | Yes | Areas of expertise |
| voice_profile | String | Yes | Communication style descriptors |
| email | String | No | Email prefix (no domain) |
| characteristic_phrases | Array[String] | No | Typical phrases this person uses |

### Authority Weight Guidelines

| Range | Description | Examples |
|-------|-------------|----------|
| 0.9-1.0 | Executive decision makers | VP, C-suite |
| 0.8-0.9 | Senior managers, key specialists | PM, Senior Contractor, Procurement Manager |
| 0.6-0.8 | Mid-level contributors | Architects, Analysts |
| 0.4-0.6 | Operational staff, advisors | Store Managers, Junior staff |

### Expertise Categories

- **Technical**: construction, electrical, hvac, plumbing, structural
- **Financial**: budgeting, cost-estimation, financial-analysis
- **Project Management**: scheduling, resource-allocation, vendor-management
- **Procurement**: vendor-relations, supply-chain, pricing, contracts
- **Design**: architecture, interior-design, design-standards
- **Operations**: store-operations, customer-experience, staffing
- **Legal/Compliance**: permits, regulatory, landlord-relations

---

## 5. Cross-Reference Map Schema

### File Format: JSON

### Structure

```json
{
  "store_references": {
    "Store-217": {
      "conversations": [
        "site_visit_Store-217_2024-03-15.txt",
        "construction-vendors.json#cv_2024_0315_001"
      ],
      "structured_data": {
        "historical_projects": "historical_projects.csv:row-217",
        "constraints": ["CNS-217-001"],
        "templates": ["base_template.json:electrical"]
      }
    }
  },
  "vendor_references": {
    "CoolAir Systems": {
      "conversations": [
        "vendor_negotiation_hvac-vendors_2024-02-10.txt",
        "construction-vendors.json#cv_2024_0315_001"
      ],
      "structured_data": {
        "material_costs": "material_costs.csv:hvac-vendor"
      }
    }
  },
  "constraint_references": {
    "CNS-217-001": {
      "discovered_in": "site_visit_Store-217_2024-03-15.txt",
      "mentioned_in": [
        "construction-vendors.json#cv_2024_0318_002"
      ],
      "constraint_file": "constraints_rules.json:store_specific[0]"
    }
  }
}
```

### Purpose

Enable bidirectional lookups:
- Given a store ID → find all related conversations
- Given a conversation → find all structured data references
- Given a vendor → find all mentions across conversations
- Given a constraint → trace from discovery to application

---

## 6. Temporal Coherence Rules

### Meeting Timing Rules

| Meeting Type | Timing Relative To | Offset | Example |
|--------------|-------------------|--------|---------|
| Site Visit Debrief | Estimate Deadline | -14 days | Estimate 2024-04-01 → Visit 2024-03-18 |
| Vendor Negotiation | Material Order Date | -10 days | Order 2024-03-25 → Negotiation 2024-03-15 |
| Lessons Learned | Project Completion | +45 days | Complete 2024-02-01 → Lesson 2024-03-18 |
| Design Review | Fixed Quarterly | Q dates | 2024-01-15, 2024-04-15, 2024-07-15, 2024-10-15 |
| Weekly Dev Sync | Fixed Weekly | Mondays | Every Monday |

### Teams Thread Timing Rules

| Thread Type | Timing Relative To | Offset | Example |
|-------------|-------------------|--------|---------|
| Meeting Follow-up | Meeting Date | +0 to +1 day | Meeting 2024-03-15 → Thread 2024-03-15 or 2024-03-16 |
| Supply Chain Update | Project Estimate | -14 to -28 days | Estimate 2024-04-01 → Update 2024-03-04 to 2024-03-18 |
| Decision Thread | Thread Start | +2 to +5 days span | Start 2024-03-15 → End 2024-03-17 to 2024-03-20 |

### Validation Rules

1. **No Future References**: Conversation date ≥ all referenced event dates
2. **Historical Project References**: Project completion < conversation date
3. **Meeting References**: Meeting date ≤ conversation date
4. **Constraint Discovery**: Constraint mentioned only after discovery date
5. **Lead Time Calculations**: Availability = Update Date + Lead Time

---

## 7. Data Quality Requirements

### Meeting Transcripts

| Metric | Target | Measurement |
|--------|--------|-------------|
| Min Duration | 30 minutes | DURATION field |
| Max Duration | 120 minutes | DURATION field |
| Min Speakers | 2 | Unique names in dialogue |
| Max Speakers | 6 | Unique names in dialogue |
| Min Dialogue Turns | 10 | Count of timestamp lines |
| Cost References | ≥1 per cost-related meeting | Regex for $### pattern |
| Store References | ≥1 per store-specific meeting | Regex for Store-### |
| Tags | 3-8 | Count of tags |
| Action Items | 1-5 | Count of action items |

### Teams Conversations

| Metric | Target | Measurement |
|--------|--------|-------------|
| Messages per Thread | 3-8 | Length of messages array |
| Thread Span | 0-5 days | Max timestamp - min timestamp |
| Reactions per Message | 0-5 | Count of reactions |
| Tags per Message | 1-5 | Length of tags array |
| Action Items per Thread | 0-3 | Length of action_items array |
| Summary Length | 100-200 chars | Length of summary field |

### Cross-Reference Integrity

| Check | Requirement |
|-------|-------------|
| Store ID Resolution | 100% of mentioned stores exist in historical_projects.csv |
| Vendor Name Consistency | 100% of vendors in vendor registry |
| Meeting References | 100% of referenced meetings exist as files |
| Constraint IDs | 100% of constraint IDs in constraints_rules.json |
| Cost Alignment | ≥95% of historical cost references within ±5% |

---

## 8. Example Artifacts

### Example 1: Complete Meeting Transcript

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

[00:00:00] Sarah Chen: Thanks for joining, everyone. Let's dive into yesterday's site visit findings. Tom, what did you discover?

[00:02:30] Tom Wilson: The electrical panel is significantly undersized for the new HVAC and lighting requirements. We're looking at a full panel upgrade to 400A. Based on what we did at Store #189, I'm estimating around $35,000 for the electrical work.

[00:05:45] Mike Rodriguez: That's going to push us over our initial budget. Store #189 came in at $32K for similar work, right? Can we match that?

[00:08:12] Tom Wilson: Store #189 was in the Columbus market where labor rates are lower. We're in Cincinnati here, and we're seeing 8-10% higher labor costs this year due to the new union contracts. The $35K accounts for that regional difference.

[00:11:20] Sarah Chen: Let me verify that against our regional modifiers... Yes, I'm seeing Cincinnati at 1.08x for electrical work. Tom, does your $35K estimate include that adjustment?

[00:13:45] Tom Wilson: Correct, that's with the 1.08x modifier applied. Also, I should mention the landlord has a requirement that all electrical work must use vendors from their approved list. That limits our negotiation flexibility.

[00:16:30] Sarah Chen: That's a new constraint I wasn't aware of. Mike, did you know about this landlord requirement?

[00:18:00] Mike Rodriguez: Yes, it came up during lease negotiations. They had issues with a previous tenant using unlicensed contractors, so now they maintain an approved vendor list for all major systems work.

[00:21:15] Tom Wilson: The good news is that our usual electrical subcontractor, PowerTech Solutions, is on their approved list. But we can't shop around for better pricing like we normally would.

[00:24:30] Sarah Chen: Understood. I'll need to document this as a store-specific constraint. Tom, can you provide a detailed breakdown of the $35K estimate?

[00:26:45] Tom Wilson: Sure. We're looking at $18K for the panel and materials, $15K for labor at Cincinnati rates, and $2K for permits and inspections.

[00:30:00] Sarah Chen: That breakdown helps. Given the constraint and the regional factors, I think $35K is reasonable. Mike, from an operational perspective, how disruptive will this work be?

[00:32:15] Mike Rodriguez: We'll need to close the store for at least two days for the panel swap. Can we schedule that during our lowest traffic period?

[00:35:00] Tom Wilson: Typically we'd do electrical work mid-week. I'd recommend Tuesday-Wednesday to minimize customer impact.

[00:37:30] Sarah Chen: I'll coordinate with scheduling. Let me capture the action items: I'll update the cost estimate to include the $35K electrical upgrade, add the landlord vendor constraint to our constraints database, and work with Mike on scheduling the downtime.

[00:40:00] Tom Wilson: I'll get you that detailed cost breakdown by end of day tomorrow.

[00:41:30] Mike Rodriguez: And I can provide our traffic data to help optimize the closure timing.

[00:43:00] Sarah Chen: Perfect. Anything else we need to address from the site visit?

[00:45:15] Tom Wilson: The HVAC placement looks good, interior walls are in better shape than expected, so no surprises there. Electrical was the main issue.

[00:47:00] Sarah Chen: Great, that's good news on the other fronts. Thanks for your time, everyone.

---
TAGS: Store-217, Store-189, electrical-upgrade, cincinnati-market, landlord-constraint, regional-modifier
ACTION ITEMS:
  - Update cost estimate with $35K electrical upgrade [@Sarah Chen, due: 2024-03-20]
  - Add landlord vendor restriction to constraints database [@Sarah Chen, due: 2024-03-18]
  - Provide detailed electrical cost breakdown [@Tom Wilson, due: 2024-03-16]
  - Share store traffic data for closure scheduling [@Mike Rodriguez, due: 2024-03-18]
REFERENCES:
  - Historical Store: Store-189 (electrical upgrade: $32K actual, Columbus market)
  - Template: base_template.json (electrical_panel: 400A requirement)
  - Regional Modifier: regional_modifiers.csv (Cincinnati electrical: 1.08x)
  - Constraint: To be created - CNS-217-001 (landlord approved vendor list)
```

### Example 2: Complete Teams Thread

```json
{
  "channel": "construction-vendors",
  "threads": [
    {
      "thread_id": "cv_2024_0315_001",
      "date": "2024-03-15",
      "participants": [
        {
          "name": "Jennifer Liu",
          "role": "Procurement Manager",
          "team": "ANF"
        },
        {
          "name": "Tom Wilson",
          "role": "General Contractor",
          "team": "BuildRight Construction"
        },
        {
          "name": "Sarah Chen",
          "role": "Project Manager",
          "team": "ANF Store Development"
        }
      ],
      "messages": [
        {
          "timestamp": "2024-03-15 14:22:00",
          "author": "Jennifer Liu",
          "role": "Procurement Manager",
          "text": "Heads up team - our primary HVAC vendor (CoolAir Systems) just notified me they're pushing lead times from 6 weeks to 10 weeks for all commercial units. This affects stores #215, #217, and #220 currently in our pipeline.",
          "reactions": [
            {"emoji": "😬", "count": 5},
            {"emoji": "👍", "count": 2}
          ],
          "tags": ["supply-chain", "hvac", "Store-215", "Store-217", "Store-220", "lead-time"]
        },
        {
          "timestamp": "2024-03-15 14:35:12",
          "author": "Tom Wilson",
          "role": "General Contractor",
          "text": "That's going to be a problem for Store #217 - we're already on a tight schedule with the electrical upgrade work we discussed this morning. @Sarah Chen can we explore the backup vendor we used for Store #189 last quarter?",
          "reactions": [
            {"emoji": "👍", "count": 2}
          ],
          "tags": ["Store-217", "Store-189", "schedule-risk", "backup-vendor"]
        },
        {
          "timestamp": "2024-03-15 15:01:43",
          "author": "Sarah Chen",
          "role": "Project Manager",
          "text": "Good idea Tom. Store #189's backup vendor (TempMaster) came in about 15% higher on cost but delivered on time with good quality. For Store #217, that would add roughly $8K to our HVAC budget but save us 4 weeks on the schedule. Let me run the cost-benefit analysis.",
          "reactions": [
            {"emoji": "💡", "count": 3},
            {"emoji": "👍", "count": 4}
          ],
          "tags": ["Store-217", "cost-tradeoff", "vendor-switch", "TempMaster"]
        },
        {
          "timestamp": "2024-03-15 15:28:19",
          "author": "Jennifer Liu",
          "role": "Procurement Manager",
          "text": "I can reach out to TempMaster today to confirm they can meet our timeline. Last time we worked with them they had great turnaround. The 15% premium might be worth it to avoid schedule delays.",
          "reactions": [
            {"emoji": "🙏", "count": 2}
          ],
          "tags": ["vendor-outreach", "TempMaster"]
        },
        {
          "timestamp": "2024-03-15 16:45:55",
          "author": "Sarah Chen",
          "role": "Project Manager",
          "text": "Thanks Jennifer. After running the numbers: 4-week delay would cost us ~$12K in extended contractor fees and lost opening revenue. The $8K vendor premium is actually the cheaper option. Let's move forward with TempMaster for Store #217.",
          "reactions": [
            {"emoji": "✅", "count": 5}
          ],
          "tags": ["Store-217", "decision", "vendor-switch", "cost-analysis"]
        }
      ],
      "summary": "Primary HVAC vendor (CoolAir Systems) extended lead times from 6 to 10 weeks, affecting 3 stores. Team decided to switch to backup vendor (TempMaster) for Store #217 despite 15% cost premium ($8K) to avoid 4-week schedule delay.",
      "action_items": [
        {
          "description": "Contact TempMaster to confirm timeline availability for Store #217",
          "owner": "Jennifer Liu",
          "due_date": "2024-03-18",
          "status": "open"
        },
        {
          "description": "Complete cost-benefit analysis for vendor switch",
          "owner": "Sarah Chen",
          "due_date": "2024-03-18",
          "status": "completed"
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
            "field": "Store-189:hvac_vendor"
          },
          {
            "source": "05_Cost_Models",
            "file": "material_costs.csv",
            "field": "HVAC_commercial_units:lead_time_weeks"
          }
        ]
      }
    }
  ]
}
```

---

## Schema Compliance Testing

### Automated Tests

```python
def test_meeting_transcript_schema(file_path):
    """Test meeting transcript against schema."""
    with open(file_path, 'r') as f:
        content = f.read()

    # Test header fields
    assert 'MEETING:' in content
    assert 'DATE:' in content
    assert 'PARTICIPANTS:' in content
    assert 'DURATION:' in content
    assert 'STORE/TOPIC:' in content

    # Test dialogue format
    dialogue_pattern = r'\[\d{2}:\d{2}:\d{2}\] [\w\s]+:'
    assert re.search(dialogue_pattern, content)

    # Test footer
    assert 'TAGS:' in content
    assert 'ACTION ITEMS:' in content
    assert 'REFERENCES:' in content

def test_teams_conversation_schema(file_path):
    """Test Teams conversation against schema."""
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Test required top-level fields
    assert 'channel' in data
    assert 'threads' in data
    assert isinstance(data['threads'], list)

    # Test thread structure
    for thread in data['threads']:
        assert 'thread_id' in thread
        assert 'date' in thread
        assert 'participants' in thread
        assert 'messages' in thread
        assert 'summary' in thread
        assert 'references' in thread

        # Test message structure
        for message in thread['messages']:
            assert 'timestamp' in message
            assert 'author' in message
            assert 'role' in message
            assert 'text' in message
            assert 'reactions' in message
            assert 'tags' in message
```

---

**End of Schema Specifications**
