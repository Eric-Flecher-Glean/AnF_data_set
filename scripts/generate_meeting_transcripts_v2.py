#!/usr/bin/env python3
"""
Enhanced Meeting Transcript Generator v2

Generates realistic meeting transcripts using scenario-based dialogue templates.
This version produces high-quality, contextual dialogue similar to Teams conversations.
"""

import argparse
import json
import os
import random
import yaml
from datetime import datetime, timedelta
from typing import Dict, List, Any
import pandas as pd


class EnhancedMeetingGenerator:
    """Generate realistic meeting transcripts with scenario-based dialogue."""

    def __init__(self, config_dir='config', templates_dir='templates', output_dir='output/07_Conversations'):
        self.config_dir = config_dir
        self.templates_dir = templates_dir
        self.output_dir = output_dir

        # Load configuration
        self.personas = self._load_json(f'{config_dir}/personas.json')
        self.vendors = self._load_json(f'{config_dir}/vendor_registry.json')

    def _load_json(self, path):
        """Load JSON file."""
        with open(path, 'r') as f:
            return json.load(f)

    def generate_transcript(self, meeting_type, config):
        """Generate enhanced meeting transcript."""
        # Load enhanced template
        template_path = f'{self.templates_dir}/meeting_templates/{meeting_type}_enhanced.yaml'

        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Enhanced template not found: {template_path}")

        with open(template_path, 'r') as f:
            template = yaml.safe_load(f)

        # Prepare context data
        context = self._prepare_context(meeting_type, config)

        # Generate dialogue
        dialogue = self._generate_dialogue_from_scenarios(
            template['dialogue_scenarios'],
            context,
            config
        )

        # Format transcript
        transcript = self._format_transcript(
            meeting_type=meeting_type,
            dialogue=dialogue,
            config=config,
            context=context
        )

        # Save
        filename = self._save_transcript(transcript, meeting_type, config)

        # Update index
        self._update_conversation_index(config, filename, context)

        return {'transcript': transcript, 'filename': filename}

    def _prepare_context(self, meeting_type, config):
        """Prepare context data for dialogue generation."""
        context = {}

        if meeting_type == 'site_visit_debrief':
            store_id = config.get('store_id', 'Store-201')
            context = {
                'store_id': store_id,
                'historical_store': f'Store-{int(store_id.split("-")[1]) - 12}',  # Reference store 12 earlier
                'cost': 35000,
                'historical_cost': 32000,
                'market': 'Cincinnati',
                'modifier': 1.08,
                'modifier_pct': 8,
                'modifier_reason': 'union contracts',
                'labor': 15000,
                'materials': 18000,
                'permits': 2000
            }

        elif meeting_type == 'vendor_negotiation':
            context = {
                'current_lead_time': 10,
                'old_lead_time': 6,
                'supply_chain_reason': 'Increased demand and shipping delays from overseas suppliers',
                'duration': '2-3 months',
                'unit_cost': 16500,
                'old_unit_cost': 15000,
                'price_increase_pct': 10,
                'discount_pct': 7,
                'higher_discount_pct': 12,
                'discounted_cost': 15345,  # After 7% discount
                'payment_terms': '50% deposit, 50% on delivery'
            }

        elif meeting_type == 'lessons_learned':
            store_id = config.get('store_id', 'Store-189')
            context = {
                'store_id': store_id,
                'electrical_estimated': 35000,
                'electrical_actual': 32000,
                'variance': -3000,
                'variance_pct': 9,
                'direction': 'under',
                'backup_vendor': 'TempMaster',
                'days_since_completion': 45,
                'timeline_status': 'finished 2 days ahead of schedule',
                'learning_financial': 'this saved us $3,000 and shows backup vendors can offer better value',
                'learning_operational': 'we should always get quotes from at least two contractors'
            }

        elif meeting_type == 'design_review':
            context = {
                'template_version': config.get('template_version', 'v2.3'),
                'old_spec': '200A panels',
                'new_spec': '400A panels',
                'problem_count': 3,
                'time_period': 'last quarter',
                'cost_increase': 5000,
                'cost_increase_pct': 15,
                'effective_date': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
                'technical_benefit': 'sufficient capacity for future electrical loads and equipment upgrades',
                'communication_date': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
            }

        elif meeting_type == 'weekly_dev_sync':
            context = {
                'active_project_count': 12,
                'lead_time': 10,
                'affected_store_count': 3,
                'cost_premium_pct': 15,
                'critical_store': 'Store-217',
                'budget_variance_pct': 3,
                'budget_direction': 'under',
                'variance_reason': 'favorable vendor pricing on recent contracts',
                'blocker_description': 'Waiting on permit approval for Store-215 - should be resolved by end of week',
                'upcoming_store_count': 4,
                'site_visit_count': 2
            }

        return context

    def _generate_dialogue_from_scenarios(self, scenarios, context, config):
        """Generate dialogue from scenario templates."""
        dialogue = []
        current_time = 0

        # Get participants for roles
        role_to_persona = self._map_roles_to_personas(scenarios)

        for scenario in scenarios:
            role = scenario['speaker_role']
            template_text = scenario['text']

            # Format text with context
            try:
                text = template_text.format(**context)
            except KeyError as e:
                # If key is missing, use template as-is
                text = template_text

            # Get persona for role
            persona = role_to_persona.get(role, {'name': 'Unknown', 'role': role})

            # Create dialogue entry
            dialogue.append({
                'timestamp': self._format_timestamp(current_time),
                'speaker': persona['name'],
                'role': persona['role'],
                'text': text
            })

            # Increment time (30-180 seconds)
            current_time += random.randint(30, 180)

        return dialogue

    def _map_roles_to_personas(self, scenarios):
        """Map role names to specific personas."""
        role_map = {
            'Project Manager': 'Sarah Chen',
            'General Contractor': 'Tom Wilson',
            'Procurement Manager': 'Jennifer Liu',
            'Store Manager': 'Mike Rodriguez',
            'VP Store Development': 'David Park',
            'Finance Analyst': 'Lisa Thompson',
            'Design Lead': 'Carlos Martinez',
            'Architect': 'Angela Wu'
        }

        result = {}
        for scenario in scenarios:
            role = scenario['speaker_role']
            if role in role_map:
                persona_name = role_map[role]
                # Find full persona
                for p in self.personas['participants']:
                    if p['name'] == persona_name:
                        result[role] = p
                        break

        return result

    def _format_timestamp(self, seconds):
        """Format seconds as [HH:MM:SS]."""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"[{hours:02d}:{minutes:02d}:{secs:02d}]"

    def _format_transcript(self, meeting_type, dialogue, config, context):
        """Format dialogue as meeting transcript."""
        lines = []

        # Header
        meeting_titles = {
            'site_visit_debrief': 'Site Visit Debrief',
            'vendor_negotiation': 'Vendor Negotiation',
            'lessons_learned': 'Lessons Learned',
            'design_review': 'Design Review',
            'weekly_dev_sync': 'Weekly Dev Sync'
        }

        lines.append(f"MEETING: {meeting_titles.get(meeting_type, meeting_type.title())}")
        lines.append(f"DATE: {config['date']}")
        lines.append("PARTICIPANTS:")

        # Extract unique participants
        participants = {}
        for d in dialogue:
            if d['speaker'] not in participants:
                participants[d['speaker']] = d['role']

        for speaker, role in participants.items():
            team = self._get_team_for_role(role)
            lines.append(f"  - {speaker} ({role}) - {team}")

        # Calculate duration
        last_timestamp = dialogue[-1]['timestamp'].strip('[]')
        hours, minutes, _ = map(int, last_timestamp.split(':'))
        total_minutes = hours * 60 + minutes
        lines.append(f"DURATION: {total_minutes // 60:02d}:{total_minutes % 60:02d}")
        lines.append(f"STORE/TOPIC: {config.get('store_id') or config.get('topic', 'General')}")
        lines.append("---")
        lines.append("")

        # Dialogue
        for d in dialogue:
            lines.append(f"{d['timestamp']} {d['speaker']}: {d['text']}")

        lines.append("")
        lines.append("---")

        # Tags
        tags = self._generate_tags(meeting_type, config, context)
        lines.append(f"TAGS: {', '.join(tags)}")

        # Action items
        action_items = self._generate_action_items(meeting_type, config, dialogue)
        if action_items:
            lines.append("ACTION ITEMS:")
            for item in action_items:
                due_str = f", due: {item['due']}" if item.get('due') else ""
                lines.append(f"  - {item['description']} [@{item['owner']}{due_str}]")

        # References
        references = self._generate_references(meeting_type, context)
        if references:
            lines.append("REFERENCES:")
            for ref in references:
                lines.append(f"  - {ref}")

        return '\n'.join(lines)

    def _get_team_for_role(self, role):
        """Get team name for role."""
        team_map = {
            'Project Manager': 'ANF Store Development',
            'General Contractor': 'BuildRight Construction',
            'Procurement Manager': 'ANF',
            'Store Manager': 'ANF',
            'VP Store Development': 'ANF',
            'Finance Analyst': 'ANF Finance',
            'Design Lead': 'ANF Design',
            'Architect': 'ANF Design'
        }
        return team_map.get(role, 'ANF')

    def _generate_tags(self, meeting_type, config, context):
        """Generate relevant tags."""
        tags = []

        if 'store_id' in config and config.get('store_id'):
            tags.append(config['store_id'])
        if 'store_id' in context and context.get('store_id'):
            tags.append(context['store_id'])
        if 'historical_store' in context and context.get('historical_store'):
            tags.append(context['historical_store'])

        # Meeting-specific tags
        if meeting_type == 'site_visit_debrief':
            tags.extend(['electrical-upgrade', 'site-constraints'])
        elif meeting_type == 'vendor_negotiation':
            tags.extend(['hvac-pricing', 'lead-times', 'vendor-contract'])
        elif meeting_type == 'lessons_learned':
            tags.extend(['cost-variance', 'lessons-learned'])
        elif meeting_type == 'design_review':
            tags.extend(['template-update', 'design-standards'])
        elif meeting_type == 'weekly_dev_sync':
            tags.extend(['project-status', 'weekly-sync'])

        return list(set(tags))  # Remove duplicates

    def _generate_action_items(self, meeting_type, config, dialogue):
        """Generate action items based on meeting type."""
        actions = []
        next_friday = self._get_next_friday(config['date'])

        if meeting_type == 'site_visit_debrief':
            actions = [
                {'description': 'Update cost estimate with electrical upgrade', 'owner': 'Sarah Chen', 'due': next_friday},
                {'description': 'Add landlord vendor constraint to constraints database', 'owner': 'Sarah Chen', 'due': next_friday}
            ]
        elif meeting_type == 'vendor_negotiation':
            actions = [
                {'description': 'Prepare formal quote based on discussion', 'owner': 'Tom Wilson', 'due': next_friday},
                {'description': 'Review volume commitment with project team', 'owner': 'Jennifer Liu', 'due': next_friday}
            ]
        elif meeting_type == 'lessons_learned':
            actions = [
                {'description': 'Add learnings to knowledge base', 'owner': 'Sarah Chen', 'due': next_friday},
                {'description': 'Share insights with broader team', 'owner': 'Sarah Chen', 'due': next_friday}
            ]
        elif meeting_type == 'design_review':
            actions = [
                {'description': 'Distribute updated template documentation', 'owner': 'Carlos Martinez', 'due': next_friday},
                {'description': 'Schedule training sessions for project teams', 'owner': 'Carlos Martinez', 'due': next_friday}
            ]
        elif meeting_type == 'weekly_dev_sync':
            actions = [
                {'description': 'Confirm vendor availability for site visits', 'owner': 'Jennifer Liu', 'due': next_friday}
            ]

        return actions

    def _generate_references(self, meeting_type, context):
        """Generate references based on context."""
        refs = []

        if meeting_type == 'site_visit_debrief' and 'historical_store' in context:
            refs.append(f"Historical Store: {context['historical_store']} (electrical: ${context.get('historical_cost', 0):,} actual)")
            refs.append(f"Regional Modifier: regional_modifiers.csv ({context.get('market', 'Market')} electrical: {context.get('modifier', 1.0)}x)")

        elif meeting_type == 'lessons_learned' and 'store_id' in context:
            refs.append(f"Historical Store: {context['store_id']} (electrical variance analysis)")
            refs.append(f"Vendor: {context.get('backup_vendor', 'TempMaster')} (backup vendor with better pricing)")

        elif meeting_type == 'design_review' and 'template_version' in context:
            refs.append(f"Template: base_template.json version {context['template_version']}")
            refs.append("Cost Model: Updated electrical panel specification")

        return refs

    def _get_next_friday(self, date_str):
        """Get next Friday from date."""
        date = datetime.strptime(date_str, '%Y-%m-%d')
        days_ahead = 4 - date.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return (date + timedelta(days=days_ahead)).strftime('%Y-%m-%d')

    def _save_transcript(self, transcript, meeting_type, config):
        """Save transcript to file."""
        store_topic = config.get('store_id') or config.get('topic', 'general')
        date = config['date']

        filename = f"{meeting_type}_{store_topic}_{date}.txt"
        filepath = os.path.join(
            self.output_dir,
            'meeting_transcripts',
            meeting_type,
            filename
        )

        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, 'w') as f:
            f.write(transcript)

        print(f"✓ Saved enhanced transcript: {filepath}")
        return filename

    def _update_conversation_index(self, config, filename, context):
        """Update conversation index."""
        index_path = f'{self.output_dir}/metadata/conversation_index.csv'

        store_id = config.get('store_id') or context.get('store_id', 'General')
        tags = self._generate_tags(config.get('meeting_type', 'meeting'), config, context)

        entry = {
            'store_id': store_id,
            'conversation_type': 'meeting',
            'filename': filename,
            'date': config['date'],
            'participants': config.get('participants', ''),
            'key_topics': '|'.join(tags),
            'cost_impact': 0,
            'timeline_impact': 0
        }

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
    parser = argparse.ArgumentParser(description='Generate enhanced meeting transcripts')
    parser.add_argument('--meeting-type', required=True, choices=[
        'site_visit_debrief', 'vendor_negotiation', 'lessons_learned',
        'design_review', 'weekly_dev_sync'
    ])
    parser.add_argument('--store-id', help='Store ID')
    parser.add_argument('--topic', help='Topic (for non-store meetings)')
    parser.add_argument('--date', help='Meeting date (YYYY-MM-DD)')

    args = parser.parse_args()

    config = {
        'meeting_type': args.meeting_type,
        'store_id': args.store_id,
        'topic': args.topic,
        'date': args.date or datetime.now().strftime('%Y-%m-%d'),
        'participants': ''
    }

    generator = EnhancedMeetingGenerator()
    result = generator.generate_transcript(args.meeting_type, config)

    print(f"\n✅ Enhanced transcript generated: {result['filename']}")


if __name__ == '__main__':
    main()
