# Quick Start Guide

## Overview

This project generates synthetic conversational data (meeting transcripts and Teams conversations) for retail store development cost estimation.

## Prerequisites

```bash
# Python 3.9+
python --version

# Install dependencies
pip install -r requirements.txt
```

## Directory Structure

```
store_build/
├── README.md                 # Project overview
├── QUICKSTART.md            # This file
├── docs/                    # Comprehensive documentation
│   ├── 01_data_generation_plan.md
│   ├── 02_schema_specifications.md
│   ├── 03_integration_guide.md
│   └── 04_governance_framework.md
├── scripts/                 # Generation scripts
│   ├── generate_meeting_transcripts.py
│   ├── generate_teams_conversations.py
│   └── run_data_generation.py
├── config/                  # Configuration files
│   ├── personas.json
│   ├── vendor_registry.json
│   └── temporal_rules.json
├── templates/              # Meeting templates
│   └── meeting_templates/
│       └── site_visit_debrief.yaml
└── output/                 # Generated data (created by scripts)
    └── 07_Conversations/
        ├── meeting_transcripts/
        ├── teams_channels/
        └── metadata/
```

## Quick Start: Generate MVP Dataset (Phase 1)

### Step 1: Review Configuration

Check the personas and vendors:

```bash
cat config/personas.json
cat config/vendor_registry.json
```

### Step 2: Generate Sample Meeting Transcript

```bash
cd scripts

# Generate a site visit debrief
python generate_meeting_transcripts.py \
  --meeting-type site_visit_debrief \
  --store-id Store-217 \
  --date 2024-03-15 \
  --duration 75
```

Output will be saved to: `output/07_Conversations/meeting_transcripts/site_visit_debrief/`

### Step 3: Generate Sample Teams Conversation

```bash
# Generate a Teams thread about supply chain delays
python generate_teams_conversations.py \
  --channel construction-vendors \
  --theme supply-chain-delay \
  --store-id Store-217 \
  --date 2024-03-16
```

Output will be saved to: `output/07_Conversations/teams_channels/construction-vendors.json`

### Step 4: Run Full Phase 1 Generation

```bash
# Generate complete Phase 1 dataset (15 meetings, 50+ Teams messages)
python run_data_generation.py --phase 1
```

This will generate:
- 15 meeting transcripts across 5 types
- 8-12 Teams threads across 4 channels
- Metadata files (conversation_index.csv)
- Cross-references to historical stores

### Step 5: Validate Generated Data

```bash
# Run validation (requires implementation of validate_data_quality.py)
python run_data_generation.py --phase 1 --validate
```

## Understanding the Output

### Meeting Transcript Format

```
MEETING: Site Visit Debrief
DATE: 2024-03-15
PARTICIPANTS:
  - Sarah Chen (Project Manager) - ANF Store Development
  - Tom Wilson (General Contractor) - BuildRight Construction
DURATION: 01:15
STORE/TOPIC: Store-217
---

[00:00:00] Sarah Chen: Thanks for joining...
[00:02:30] Tom Wilson: The electrical panel is undersized...
...

---
TAGS: Store-217, electrical-upgrade, cincinnati-market
ACTION ITEMS:
  - Update cost estimate [@Sarah Chen, due: 2024-03-20]
REFERENCES:
  - Historical Store: Store-189 (electrical: $32K actual)
```

### Teams Conversation Format

```json
{
  "channel": "construction-vendors",
  "threads": [
    {
      "thread_id": "cv_20240315_001",
      "date": "2024-03-15",
      "participants": [...],
      "messages": [
        {
          "timestamp": "2024-03-15 14:22:00",
          "author": "Jennifer Liu",
          "text": "Heads up team - lead times extended...",
          "reactions": [{"emoji": "😬", "count": 5}],
          "tags": ["supply-chain", "hvac"]
        }
      ],
      "summary": "Primary HVAC vendor extended lead times...",
      "action_items": [...],
      "references": {
        "stores": ["Store-217"],
        "vendors": ["CoolAir Systems"],
        "meetings": ["site_visit_Store-217_2024-03-15.txt"]
      }
    }
  ]
}
```

## Customization

### Add New Personas

Edit `config/personas.json`:

```json
{
  "participants": [
    {
      "name": "Your Name",
      "role": "Your Role",
      "team": "Your Team",
      "authority_weight": 0.8,
      "expertise": ["expertise1", "expertise2"],
      "characteristic_phrases": ["phrase1", "phrase2"]
    }
  ]
}
```

### Add New Vendors

Edit `config/vendor_registry.json`:

```json
{
  "vendors": [
    {
      "canonical_name": "Vendor Name",
      "category": "HVAC|Electrical|etc",
      "specialties": ["specialty1"],
      "markets_served": ["Columbus"],
      "typical_lead_time_weeks": 6
    }
  ]
}
```

### Create New Meeting Template

Create `templates/meeting_templates/your_meeting_type.yaml`:

```yaml
meeting_type: your_meeting_type
duration_minutes: 60-90
required_participants:
  - role: Project Manager
  - role: Contractor

dialogue_flow:
  - section: opening
    topics: [topic1, topic2]
  - section: main_discussion
    topics: [topic3, topic4]
```

## Phased Implementation

### Phase 1: MVP (Current Quick Start)
- 20 stores
- 15 meeting transcripts
- 50+ Teams messages
- **Estimated time**: 5-10 minutes runtime

### Phase 2: Scaling (100 stores)
```bash
python run_data_generation.py --phase 2
```
- 100 stores
- 75 meeting transcripts
- 200 Teams messages
- **Estimated time**: 30-45 minutes runtime

### Phase 3: Production (Full dataset)
```bash
python run_data_generation.py --phase 3
```
- 250+ stores
- 250 meeting transcripts
- 300+ Teams messages
- 12-month temporal span
- **Estimated time**: 2-3 hours runtime

## Integration with Glean

Once data is generated, the conversations can be indexed by Glean:

1. **Meeting Transcripts**: Use Glean's meeting transcript connector
2. **Teams Conversations**: Use Glean's Teams connector (or simulate via JSON files)
3. **Search Testing**: Query for stores, vendors, constraints to verify indexing

## Troubleshooting

### Missing Dependencies

```bash
pip install pandas pyyaml
```

### Permission Errors

```bash
chmod +x scripts/*.py
```

### Output Directory Not Created

The scripts will automatically create the `output/` directory structure. If issues persist:

```bash
mkdir -p output/07_Conversations/meeting_transcripts
mkdir -p output/07_Conversations/teams_channels
mkdir -p output/07_Conversations/metadata
```

## Next Steps

1. **Review Generated Data**: Check `output/07_Conversations/` for generated files
2. **Read Full Documentation**: See `docs/01_data_generation_plan.md` for comprehensive guidance
3. **Customize**: Modify personas, vendors, and templates to match your use case
4. **Validate**: Ensure cross-references and temporal coherence
5. **Index in Glean**: Set up connectors to make data searchable

## Support

For detailed instructions on:
- **Schema specifications**: See `docs/02_schema_specifications.md`
- **Integration with structured data**: See `docs/03_integration_guide.md`
- **Governance and access control**: See `docs/04_governance_framework.md`

## Example Workflow

```bash
# 1. Generate Phase 1 MVP dataset
cd scripts
python run_data_generation.py --phase 1

# 2. Check generated files
ls -la ../output/07_Conversations/meeting_transcripts/
ls -la ../output/07_Conversations/teams_channels/

# 3. View conversation index
cat ../output/07_Conversations/metadata/conversation_index.csv

# 4. Generate single custom meeting
python generate_meeting_transcripts.py \
  --meeting-type lessons_learned \
  --store-id Store-189 \
  --date 2024-02-20

# 5. Generate custom Teams thread
python generate_teams_conversations.py \
  --channel design-standards-updates \
  --theme template-update \
  --date 2024-03-01

# Done! Data is ready for use.
```

---

**You're ready to generate synthetic conversational data!**

Start with Phase 1 to validate the approach, then scale to Phase 2 and Phase 3 as needed.
