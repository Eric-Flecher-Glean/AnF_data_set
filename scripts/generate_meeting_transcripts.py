#!/usr/bin/env python3
"""
Meeting Transcript Generator

Generates realistic meeting transcripts with proper formatting, persona-specific dialogue,
and cross-references to structured data.

Usage:
    python generate_meeting_transcripts.py --config config.json
    python generate_meeting_transcripts.py --meeting-type site_visit --store-id Store-217 --date 2024-03-15
"""

import argparse
import json
import os
import re
import yaml
from datetime import datetime, timedelta
from typing import Dict, List, Any
import pandas as pd
import random


class MeetingTranscriptGenerator:
    """Generate realistic meeting transcripts."""

    def __init__(self, config_dir='config', templates_dir='templates', output_dir='output/07_Conversations'):
        self.config_dir = config_dir
        self.templates_dir = templates_dir
        self.output_dir = output_dir

        # Load configuration
        self.personas = self._load_personas()
        self.temporal_rules = self._load_temporal_rules()
        self.vendor_registry = self._load_vendor_registry()

    def _load_personas(self) -> Dict:
        """Load participant personas from config."""
        with open(f'{self.config_dir}/personas.json', 'r') as f:
            return json.load(f)

    def _load_temporal_rules(self) -> Dict:
        """Load temporal rules from config."""
        with open(f'{self.config_dir}/temporal_rules.json', 'r') as f:
            return json.load(f)

    def _load_vendor_registry(self) -> Dict:
        """Load vendor registry from config."""
        with open(f'{self.config_dir}/vendor_registry.json', 'r') as f:
            return json.load(f)

    def generate_transcript(self, config: Dict) -> Dict:
        """
        Generate a meeting transcript based on configuration.

        Args:
            config: Dictionary with:
                - meeting_type: str
                - store_id_or_topic: str
                - date: str (YYYY-MM-DD)
                - participants: List[Dict] with name, role
                - context: Dict with historical_reference, cost_focus, etc.
                - duration_minutes: int

        Returns:
            Dictionary with transcript data and metadata
        """
        # Load meeting template
        template = self._load_template(config['meeting_type'])

        # Load structured data context
        context_data = self._gather_structured_context(config)

        # Select participants
        participants = self._select_participants(config, template)

        # Generate dialogue
        dialogue = self._generate_dialogue(template, participants, context_data, config)

        # Generate tags and metadata
        tags = self._extract_tags(dialogue, config)
        action_items = self._extract_action_items(dialogue, participants)
        references = self._map_references(tags, context_data)

        # Format transcript
        transcript = self._format_transcript(
            meeting_type=config['meeting_type'],
            date=config['date'],
            participants=participants,
            dialogue=dialogue,
            duration=config.get('duration_minutes', 60),
            store_topic=config['store_id_or_topic'],
            tags=tags,
            action_items=action_items,
            references=references
        )

        # Save transcript
        filename = self._save_transcript(transcript, config)

        # Update conversation index
        self._update_conversation_index(config, tags, references, filename)

        return {
            'transcript': transcript,
            'filename': filename,
            'metadata': {
                'participants': participants,
                'tags': tags,
                'action_items': action_items,
                'references': references
            }
        }

    def _load_template(self, meeting_type: str) -> Dict:
        """Load meeting template YAML."""
        template_path = f'{self.templates_dir}/meeting_templates/{meeting_type}.yaml'

        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template not found: {template_path}")

        with open(template_path, 'r') as f:
            return yaml.safe_load(f)

    def _gather_structured_context(self, config: Dict) -> Dict:
        """Query structured data for context."""
        context = {}

        # Load historical project data if referenced
        if config.get('context', {}).get('historical_reference'):
            hist_ref = config['context']['historical_reference']
            context['historical_project'] = self._load_historical_project(hist_ref)

        # Load store profile if store-specific meeting
        if config['store_id_or_topic'].startswith('Store-'):
            context['store_profile'] = self._load_store_profile(config['store_id_or_topic'])

        # Load relevant templates
        if config.get('context', {}).get('template_reference'):
            context['template'] = self._load_build_template(
                config['context']['template_reference']
            )

        # Load regional modifiers
        if context.get('store_profile'):
            market = context['store_profile'].get('market')
            if market:
                context['regional_modifiers'] = self._load_regional_modifiers(market)

        return context

    def _load_historical_project(self, store_id: str) -> Dict:
        """Load historical project data from CSV."""
        try:
            df = pd.read_csv('03_Historical_Projects/historical_projects.csv')
            row = df[df['store_id'] == store_id]

            if row.empty:
                raise ValueError(f"Store {store_id} not found in historical projects")

            return row.iloc[0].to_dict()
        except FileNotFoundError:
            # If structured data doesn't exist yet, return mock data
            return {
                'store_id': store_id,
                'electrical_estimated_cost': 35000,
                'electrical_actual_cost': 32000,
                'completion_date': '2024-02-01'
            }

    def _load_store_profile(self, store_id: str) -> Dict:
        """Load store profile data."""
        # Mock implementation - replace with actual data loading
        return {
            'store_id': store_id,
            'market': 'Cincinnati',
            'type': 'Type-A',
            'status': 'in_progress'
        }

    def _load_build_template(self, template_name: str) -> Dict:
        """Load build template data."""
        # Mock implementation
        return {
            'template': 'base_template.json',
            'electrical_panel': '400A'
        }

    def _load_regional_modifiers(self, market: str) -> Dict:
        """Load regional modifiers for market."""
        # Mock implementation
        modifiers = {
            'Cincinnati': {'electrical': 1.08, 'hvac': 1.05},
            'Columbus': {'electrical': 1.00, 'hvac': 1.02}
        }
        return modifiers.get(market, {})

    def _select_participants(self, config: Dict, template: Dict) -> List[Dict]:
        """Select and configure participants based on meeting type."""
        required_roles = template.get('required_participants', [])
        participants = []

        # If participants specified in config, use those
        if 'participants' in config:
            for p in config['participants']:
                persona = self._get_persona(p['name'])
                participants.append({
                    'name': p['name'],
                    'role': p.get('role', persona['role']),
                    'team': persona.get('team', ''),
                    'persona': persona
                })
        else:
            # Auto-select participants based on required roles
            for role_config in required_roles:
                role = role_config['role']
                persona = self._get_persona_by_role(role)
                if persona:
                    participants.append({
                        'name': persona['name'],
                        'role': persona['role'],
                        'team': persona['team'],
                        'persona': persona
                    })

        return participants

    def _get_persona(self, name: str) -> Dict:
        """Get persona by name."""
        for p in self.personas.get('participants', []):
            if p['name'] == name:
                return p

        raise ValueError(f"Persona not found: {name}")

    def _get_persona_by_role(self, role: str) -> Dict:
        """Get first persona matching role."""
        for p in self.personas.get('participants', []):
            if p['role'] == role:
                return p

        return None

    def _generate_dialogue(self, template: Dict, participants: List[Dict],
                           context_data: Dict, config: Dict) -> List[Dict]:
        """Generate dialogue based on template and context."""
        dialogue = []
        current_timestamp = 0  # seconds

        # Process each topic section from template
        for topic_section in template.get('dialogue_flow', []):
            section_name = topic_section['section']
            topics = topic_section['topics']

            # Generate dialogue turns for this section
            for topic in topics:
                # Determine speakers based on topic and participant roles
                speakers = self._select_speakers_for_topic(topic, participants)

                # Generate 2-4 dialogue turns per topic
                num_turns = random.randint(2, 4)

                for i in range(num_turns):
                    speaker = speakers[i % len(speakers)]

                    # Generate dialogue text
                    text = self._generate_dialogue_text(
                        speaker=speaker,
                        topic=topic,
                        context_data=context_data,
                        config=config,
                        turn_index=i
                    )

                    dialogue.append({
                        'timestamp': self._format_timestamp(current_timestamp),
                        'speaker': speaker['name'],
                        'text': text
                    })

                    # Increment timestamp (30-180 seconds per turn)
                    current_timestamp += random.randint(30, 180)

        return dialogue

    def _select_speakers_for_topic(self, topic: str, participants: List[Dict]) -> List[Dict]:
        """Select appropriate speakers for a topic."""
        # Topic-to-role mapping
        topic_roles = {
            'cost': ['General Contractor', 'Project Manager', 'Finance'],
            'timeline': ['Project Manager', 'General Contractor'],
            'constraints': ['General Contractor', 'Store Manager', 'Project Manager'],
            'vendor': ['Procurement Manager', 'General Contractor'],
            'design': ['Architect', 'Design Lead', 'Project Manager']
        }

        # Find matching roles for topic
        relevant_roles = []
        for key, roles in topic_roles.items():
            if key in topic.lower():
                relevant_roles.extend(roles)

        if not relevant_roles:
            # Default to all participants
            return participants

        # Filter participants by relevant roles
        speakers = [p for p in participants if p['role'] in relevant_roles]

        return speakers if speakers else participants

    def _generate_dialogue_text(self, speaker: Dict, topic: str, context_data: Dict,
                                 config: Dict, turn_index: int) -> str:
        """Generate dialogue text for a speaker."""
        persona = speaker['persona']

        # Get characteristic phrases
        phrases = persona.get('characteristic_phrases', [])

        # Build dialogue based on topic and turn
        if 'cost' in topic.lower() and turn_index == 0:
            # First turn on cost topic - provide cost estimate
            if context_data.get('historical_project'):
                hist = context_data['historical_project']
                cost = hist.get('electrical_actual_cost', 35000)
                text = f"Based on what we did at {hist['store_id']}, we saw ${cost:,} for electrical work. "
                text += random.choice(phrases) if phrases else ""
                return text
            else:
                return f"We're looking at around $35,000 for the electrical upgrade. {random.choice(phrases) if phrases else ''}"

        elif 'constraint' in topic.lower():
            # Discuss constraints
            return "The landlord requires all electrical work to use their approved vendor list. This limits our negotiation flexibility."

        elif 'regional' in topic.lower() or 'modifier' in topic.lower():
            # Discuss regional modifiers
            if context_data.get('regional_modifiers'):
                modifiers = context_data['regional_modifiers']
                if 'electrical' in modifiers:
                    return f"Cincinnati shows {modifiers['electrical']}x for electrical work this year due to union contracts."

        else:
            # Generic dialogue
            templates = [
                "Let me check the numbers on that.",
                "That aligns with what we've seen in similar projects.",
                "We should validate that against the historical data.",
                "I'll follow up with more details by end of week."
            ]
            return random.choice(templates)

    def _format_timestamp(self, seconds: int) -> str:
        """Format timestamp as [HH:MM:SS]."""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"[{hours:02d}:{minutes:02d}:{secs:02d}]"

    def _extract_tags(self, dialogue: List[Dict], config: Dict) -> List[str]:
        """Extract tags from dialogue and config."""
        tags = set()

        # Add store ID if present
        if config['store_id_or_topic'].startswith('Store-'):
            tags.add(config['store_id_or_topic'])

        # Extract from context
        if config.get('context'):
            if config['context'].get('historical_reference'):
                tags.add(config['context']['historical_reference'])
            if config['context'].get('cost_focus'):
                tags.add(config['context']['cost_focus'])
            if config['context'].get('constraint_type'):
                tags.add(config['context']['constraint_type'])

        # Extract from dialogue (store IDs, vendors, etc.)
        full_text = ' '.join([d['text'] for d in dialogue])

        # Extract store IDs
        store_pattern = r'Store-\d+'
        tags.update(re.findall(store_pattern, full_text))

        # Extract vendor names
        for vendor in self.vendor_registry.get('vendors', []):
            if vendor['canonical_name'] in full_text:
                tags.add(vendor['canonical_name'])

        return sorted(list(tags))

    def _extract_action_items(self, dialogue: List[Dict], participants: List[Dict]) -> List[Dict]:
        """Extract action items from dialogue."""
        action_items = []

        # Look for action-oriented language
        action_patterns = [
            r"I'?ll ([\w\s]+) by (\w+ \d+)",
            r"(@[\w\s]+) (?:will|should) ([\w\s]+)",
            r"(?:Need to|Must|Should) ([\w\s]+)"
        ]

        full_text = ' '.join([d['text'] for d in dialogue])

        for pattern in action_patterns:
            matches = re.finditer(pattern, full_text, re.IGNORECASE)
            for match in matches:
                action_items.append({
                    'description': match.group(0),
                    'owner': participants[0]['name'],  # Default to first participant
                    'due_date': None  # Could extract from text
                })

        return action_items[:5]  # Limit to 5

    def _map_references(self, tags: List[str], context_data: Dict) -> List[str]:
        """Map tags to structured data references."""
        references = []

        # Historical projects
        if context_data.get('historical_project'):
            hist = context_data['historical_project']
            references.append(
                f"Historical Store: {hist['store_id']} (electrical: ${hist.get('electrical_actual_cost', 0):,} actual)"
            )

        # Templates
        if context_data.get('template'):
            template = context_data['template']
            references.append(f"Template: {template['template']} (electrical_panel section)")

        # Regional modifiers
        if context_data.get('regional_modifiers'):
            for category, modifier in context_data['regional_modifiers'].items():
                references.append(f"Regional Modifier: regional_modifiers.csv ({category}: {modifier}x)")

        return references

    def _format_transcript(self, meeting_type: str, date: str, participants: List[Dict],
                           dialogue: List[Dict], duration: int, store_topic: str,
                           tags: List[str], action_items: List[Dict], references: List[str]) -> str:
        """Format transcript as text."""
        lines = []

        # Header
        lines.append(f"MEETING: {meeting_type.replace('_', ' ').title()}")
        lines.append(f"DATE: {date}")
        lines.append("PARTICIPANTS:")
        for p in participants:
            lines.append(f"  - {p['name']} ({p['role']}) - {p['team']}")
        lines.append(f"DURATION: {duration // 60:02d}:{duration % 60:02d}")
        lines.append(f"STORE/TOPIC: {store_topic}")
        lines.append("---")
        lines.append("")

        # Dialogue
        for d in dialogue:
            lines.append(f"{d['timestamp']} {d['speaker']}: {d['text']}")

        lines.append("")
        lines.append("---")

        # Tags
        lines.append(f"TAGS: {', '.join(tags)}")

        # Action items
        if action_items:
            lines.append("ACTION ITEMS:")
            for item in action_items:
                due = f", due: {item['due_date']}" if item.get('due_date') else ""
                lines.append(f"  - {item['description']} [@{item['owner']}{due}]")

        # References
        if references:
            lines.append("REFERENCES:")
            for ref in references:
                lines.append(f"  - {ref}")

        return '\n'.join(lines)

    def _save_transcript(self, transcript: str, config: Dict) -> str:
        """Save transcript to file."""
        # Generate filename
        meeting_type = config['meeting_type']
        store_topic = config['store_id_or_topic']
        date = config['date']

        filename = f"{meeting_type}_{store_topic}_{date}.txt"
        filepath = os.path.join(
            self.output_dir,
            'meeting_transcripts',
            meeting_type,
            filename
        )

        # Create directory if needed
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # Write file
        with open(filepath, 'w') as f:
            f.write(transcript)

        print(f"✓ Saved transcript: {filepath}")

        return filename

    def _update_conversation_index(self, config: Dict, tags: List[str],
                                    references: List[str], filename: str):
        """Update conversation index CSV."""
        index_path = f'{self.output_dir}/metadata/conversation_index.csv'

        # Create entry
        entry = {
            'store_id': config['store_id_or_topic'],
            'conversation_type': 'meeting',
            'filename': filename,
            'date': config['date'],
            'participants': '|'.join([p['name'] for p in config.get('participants', [])]),
            'key_topics': '|'.join(tags),
            'cost_impact': 0,  # Could extract from dialogue
            'timeline_impact': 0
        }

        # Append to CSV
        if os.path.exists(index_path):
            df = pd.read_csv(index_path)
            df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
        else:
            df = pd.DataFrame([entry])

        os.makedirs(os.path.dirname(index_path), exist_ok=True)
        df.to_csv(index_path, index=False)

        print(f"✓ Updated conversation index")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Generate meeting transcripts')
    parser.add_argument('--config', help='Path to config JSON file')
    parser.add_argument('--meeting-type', choices=[
        'site_visit_debrief', 'vendor_negotiation', 'lessons_learned',
        'design_review', 'weekly_dev_sync'
    ])
    parser.add_argument('--store-id', help='Store ID or topic')
    parser.add_argument('--date', help='Meeting date (YYYY-MM-DD)')
    parser.add_argument('--duration', type=int, default=60, help='Duration in minutes')

    args = parser.parse_args()

    # Load config
    if args.config:
        with open(args.config, 'r') as f:
            config = json.load(f)
    else:
        # Build config from args
        config = {
            'meeting_type': args.meeting_type,
            'store_id_or_topic': args.store_id,
            'date': args.date or datetime.now().strftime('%Y-%m-%d'),
            'duration_minutes': args.duration,
            'context': {}
        }

    # Generate transcript
    generator = MeetingTranscriptGenerator()
    result = generator.generate_transcript(config)

    print(f"\n✓ Generated transcript: {result['filename']}")
    print(f"  Tags: {', '.join(result['metadata']['tags'])}")
    print(f"  Action Items: {len(result['metadata']['action_items'])}")


if __name__ == '__main__':
    main()
