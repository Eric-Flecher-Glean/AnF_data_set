# Synthetic Conversational Data Generation Project

## Overview
This project provides comprehensive instructions and tooling for generating synthetic conversational datasets (meeting transcripts and Teams conversations) that integrate with structured retail store development data to improve AI agent cost estimation accuracy.

## Project Structure

```
store_build/
├── README.md (this file)
├── docs/
│   ├── 01_data_generation_plan.md
│   ├── 02_schema_specifications.md
│   ├── 03_integration_guide.md
│   └── 04_governance_framework.md
├── scripts/
│   ├── generate_meeting_transcripts.py
│   ├── generate_teams_conversations.py
│   ├── validate_data_quality.py
│   └── utils/
│       ├── persona_engine.py
│       ├── temporal_validator.py
│       └── cross_reference_mapper.py
├── templates/
│   ├── meeting_templates/
│   │   ├── site_visit_debrief.yaml
│   │   ├── vendor_negotiation.yaml
│   │   ├── lessons_learned.yaml
│   │   ├── design_review.yaml
│   │   └── weekly_dev_sync.yaml
│   └── teams_templates/
│       ├── general_discussion.yaml
│       ├── vendor_thread.yaml
│       └── decision_thread.yaml
├── config/
│   ├── personas.json
│   ├── temporal_rules.json
│   └── integration_mappings.json
├── output/
│   └── 07_Conversations/
│       ├── meeting_transcripts/
│       ├── teams_channels/
│       └── metadata/
└── tests/
    ├── test_schema_compliance.py
    ├── test_temporal_coherence.py
    └── test_cross_references.py
```

## Quick Start

1. Review the comprehensive plan: `docs/01_data_generation_plan.md`
2. Understand schemas: `docs/02_schema_specifications.md`
3. Configure personas and rules: `config/`
4. Run generation scripts: `scripts/`
5. Validate output: `tests/`

## Target Audience
Data engineers, ML engineers, and solutions architects implementing conversational AI for retail store development cost estimation systems.

## Prerequisites
- Python 3.9+
- Access to structured data folders (01-06)
- Understanding of retail store development workflows
