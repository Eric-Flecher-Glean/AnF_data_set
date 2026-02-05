#!/usr/bin/env python3
"""
Teams Conversation Generator

Generates realistic Teams channel conversations with threaded discussions, reactions,
and temporal consistency with meeting transcripts.

Usage:
    python generate_teams_conversations.py --channel construction-vendors --theme supply-chain-delay
    python generate_teams_conversations.py --config teams_config.json
"""

import argparse
import json
import os
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
import pandas as pd


class TeamsConversationGenerator:
    """Generate realistic Teams conversations."""

    def __init__(self, config_dir='config', output_dir='output/07_Conversations'):
        self.config_dir = config_dir
        self.output_dir = output_dir

        # Load configuration
        self.personas = self._load_personas()
        self.conversation_themes = self._load_conversation_themes()

    def _load_personas(self) -> Dict:
        """Load participant personas."""
        with open(f'{self.config_dir}/personas.json', 'r') as f:
            return json.load(f)

    def _load_conversation_themes(self) -> Dict:
        """Load conversation theme templates."""
        # Could load from config or define inline
        return {
            'supply-chain-delay': {
                'required_roles': ['Procurement Manager', 'Project Manager', 'General Contractor'],
                'message_count': (3, 6),
                'topics': ['lead_time_increase', 'vendor_alternatives', 'cost_impact']
            },
            'site-visit-followup': {
                'required_roles': ['Project Manager', 'General Contractor'],
                'message_count': (2, 4),
                'topics': ['findings_recap', 'action_items']
            },
            'template-update': {
                'required_roles': ['Design Lead', 'Project Manager', 'Architect'],
                'message_count': (3, 5),
                'topics': ['change_announcement', 'rationale', 'impact']
            },
            'cost-variance-discussion': {
                'required_roles': ['Finance', 'Project Manager', 'General Contractor'],
                'message_count': (4, 7),
                'topics': ['variance_identification', 'root_cause', 'mitigation']
            }
        }

    def generate_conversations(self, config: Dict) -> Dict:
        """
        Generate Teams conversations for a channel.

        Args:
            config: Dictionary with:
                - channel_name: str
                - date_range: Dict with start, end
                - conversation_themes: List[Dict] with theme, store_id, date
                - participant_pool: List[str] of names
                - message_density: str (low/medium/high)

        Returns:
            Dictionary with channel data
        """
        channel_file = self._get_channel_file(config['channel_name'])

        # Load existing channel or create new
        if os.path.exists(channel_file):
            with open(channel_file, 'r') as f:
                channel_data = json.load(f)
        else:
            channel_data = {
                'channel': config['channel_name'],
                'threads': []
            }

        # Generate threads for each theme
        for theme_config in config.get('conversation_themes', []):
            thread = self._generate_thread(
                channel_name=config['channel_name'],
                theme_config=theme_config,
                participant_pool=config.get('participant_pool', [])
            )

            channel_data['threads'].append(thread)

        # Save channel
        self._save_channel(channel_data, config['channel_name'])

        # Update conversation index
        self._update_conversation_index(channel_data, config)

        return channel_data

    def _get_channel_file(self, channel_name: str) -> str:
        """Get path to channel JSON file."""
        return os.path.join(
            self.output_dir,
            'teams_channels',
            f'{channel_name}.json'
        )

    def _generate_thread(self, channel_name: str, theme_config: Dict,
                         participant_pool: List[str]) -> Dict:
        """Generate a single conversation thread."""
        theme = theme_config['theme']
        theme_template = self.conversation_themes.get(theme, {})

        # Generate thread ID
        thread_id = self._generate_thread_id(channel_name, theme_config['date'])

        # Select participants
        participants = self._select_participants(
            theme_template.get('required_roles', []),
            participant_pool
        )

        # Generate messages
        messages = self._generate_messages(
            theme=theme,
            theme_config=theme_config,
            participants=participants,
            message_count=random.randint(*theme_template.get('message_count', (3, 5)))
        )

        # Generate thread metadata
        summary = self._generate_summary(messages, theme)
        action_items = self._extract_action_items_from_messages(messages)
        references = self._generate_references(messages, theme_config)

        thread = {
            'thread_id': thread_id,
            'date': theme_config['date'],
            'participants': participants,
            'messages': messages,
            'summary': summary,
            'action_items': action_items,
            'references': references
        }

        return thread

    def _generate_thread_id(self, channel_name: str, date: str) -> str:
        """Generate unique thread ID."""
        # Format: {channel_prefix}_{YYYYMMDD}_{###}
        prefix = ''.join([word[0] for word in channel_name.split('-')])
        date_str = date.replace('-', '')
        counter = random.randint(1, 999)
        return f"{prefix}_{date_str}_{counter:03d}"

    def _select_participants(self, required_roles: List[str],
                              participant_pool: List[str]) -> List[Dict]:
        """Select participants for thread."""
        participants = []

        # If participant pool specified, use those
        if participant_pool:
            for name in participant_pool[:4]:  # Max 4 participants per thread
                persona = self._get_persona(name)
                participants.append({
                    'name': persona['name'],
                    'role': persona['role'],
                    'team': persona.get('team', '')
                })
        else:
            # Auto-select based on required roles
            for role in required_roles:
                persona = self._get_persona_by_role(role)
                if persona:
                    participants.append({
                        'name': persona['name'],
                        'role': persona['role'],
                        'team': persona.get('team', '')
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

    def _generate_messages(self, theme: str, theme_config: Dict,
                            participants: List[Dict], message_count: int) -> List[Dict]:
        """Generate messages for thread."""
        messages = []

        # Start timestamp
        base_date = datetime.strptime(theme_config['date'], '%Y-%m-%d')
        current_time = base_date.replace(hour=9, minute=0)  # Start at 9 AM

        # Generate message templates based on theme
        message_templates = self._get_message_templates_for_theme(theme, theme_config)

        for i in range(min(message_count, len(message_templates))):
            # Select author (rotate through participants)
            author = participants[i % len(participants)]

            # Generate message text
            text = message_templates[i].format(
                **theme_config,
                author=author['name']
            )

            # Generate reactions (more for important messages)
            reactions = self._generate_reactions(i, message_count)

            # Extract tags
            tags = self._extract_tags_from_message(text, theme_config)

            message = {
                'timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
                'author': author['name'],
                'role': author['role'],
                'text': text,
                'reactions': reactions,
                'tags': tags
            }

            messages.append(message)

            # Increment time (15 minutes to 3 hours between messages)
            current_time += timedelta(minutes=random.randint(15, 180))

        return messages

    def _get_message_templates_for_theme(self, theme: str, config: Dict) -> List[str]:
        """Get message templates for a theme."""
        templates = {
            'supply-chain-delay': [
                "Heads up team - our primary HVAC vendor (CoolAir Systems) just notified me they're pushing lead times from 6 weeks to 10 weeks for all commercial units. This affects stores #{store_id} and others in our pipeline.",
                "That's going to be a problem for {store_id} - we're already on a tight schedule. Can we explore the backup vendor we used for Store #189?",
                "Good idea. Store #189's backup vendor (TempMaster) came in about 15% higher on cost but delivered on time with good quality. For {store_id}, that would add roughly $8K to our HVAC budget but save us 4 weeks. Let me run the numbers.",
                "I can reach out to TempMaster today to confirm they can meet our timeline. The 15% premium might be worth it to avoid schedule delays.",
                "After running the numbers: 4-week delay would cost us ~$12K in extended fees and lost revenue. The $8K vendor premium is actually the cheaper option. Let's move forward with TempMaster."
            ],
            'site-visit-followup': [
                "Following up from today's site visit for {store_id} - the electrical panel issue Tom identified is going to need immediate attention in our cost estimate.",
                "Agreed. I'm updating the estimate now with the $35K electrical upgrade. Also documenting the landlord vendor restriction we discovered.",
                "Thanks Sarah. Mike, can you send over the store traffic data so we can schedule the electrical work during lowest impact periods?",
                "Will do - sending that over by end of day."
            ],
            'template-update': [
                "Heads up team - base template v2.3 is live as of {date}. All new stores now require 400A electrical panels instead of 200A.",
                "What's driving this change?",
                "Increased HVAC and lighting load requirements. We saw undersized panels causing issues in 3 stores last quarter.",
                "Makes sense. This will add about $5-8K to electrical costs per store, but better to spec it correctly upfront.",
                "Exactly. I've updated the cost model templates to reflect the new 400A standard."
            ],
            'cost-variance-discussion': [
                "FYI - Store #{store_id} came in $15K under budget on electrical work. Worth understanding what drove that variance.",
                "We used the backup vendor TempMaster who had better pricing than our usual contractor. Quality was good, no issues.",
                "Interesting. Is TempMaster someone we should add to our primary vendor rotation?",
                "I'd recommend it. They were responsive, delivered on time, and pricing was 12% lower than our standard rate.",
                "Let me reach out to them about establishing a preferred vendor relationship. Could generate savings across our portfolio."
            ]
        }

        return templates.get(theme, [
            "Update on {store_id}.",
            "Thanks for the info.",
            "Let me follow up on that."
        ])

    def _generate_reactions(self, message_index: int, total_messages: int) -> List[Dict]:
        """Generate reactions for a message."""
        # First and last messages get more reactions
        if message_index == 0 or message_index == total_messages - 1:
            reaction_count = random.randint(3, 5)
        else:
            reaction_count = random.randint(0, 3)

        emojis = ['👍', '👏', '💡', '😬', '✅', '🙏']

        reactions = []
        for _ in range(reaction_count):
            reactions.append({
                'emoji': random.choice(emojis),
                'count': random.randint(1, 4)
            })

        return reactions

    def _extract_tags_from_message(self, text: str, theme_config: Dict) -> List[str]:
        """Extract tags from message text."""
        tags = []

        # Add theme-specific tags
        if 'supply-chain' in text.lower() or 'lead time' in text.lower():
            tags.append('supply-chain')

        if 'hvac' in text.lower():
            tags.append('hvac')

        if 'cost' in text.lower() or 'budget' in text.lower() or '$' in text:
            tags.append('cost')

        if 'schedule' in text.lower() or 'timeline' in text.lower():
            tags.append('schedule')

        # Add store IDs from config
        if 'store_id' in theme_config:
            tags.append(theme_config['store_id'])

        return tags

    def _generate_summary(self, messages: List[Dict], theme: str) -> str:
        """Generate thread summary."""
        summaries = {
            'supply-chain-delay': "Primary HVAC vendor extended lead times from 6 to 10 weeks. Team decided to switch to backup vendor despite 15% cost premium to avoid schedule delays.",
            'site-visit-followup': "Follow-up on site visit findings. Cost estimate updated with electrical upgrade and landlord constraint documented.",
            'template-update': "Base template v2.3 released with updated electrical panel requirements (200A → 400A) to address load issues.",
            'cost-variance-discussion': "Discussed cost variance on completed store. Identified backup vendor with better pricing for potential preferred vendor status."
        }

        return summaries.get(theme, f"Discussion with {len(messages)} messages.")

    def _extract_action_items_from_messages(self, messages: List[Dict]) -> List[Dict]:
        """Extract action items from message text."""
        action_items = []

        for msg in messages:
            text = msg['text']

            # Look for action-oriented language
            if any(phrase in text.lower() for phrase in ['i can', 'i\'ll', 'let me', 'will send']):
                action_items.append({
                    'description': text[:100],  # First 100 chars
                    'owner': msg['author'],
                    'due_date': None,
                    'status': 'open'
                })

        return action_items[:3]  # Max 3 action items

    def _generate_references(self, messages: List[Dict], theme_config: Dict) -> Dict:
        """Generate references object."""
        # Extract mentioned stores, vendors, etc. from messages
        full_text = ' '.join([m['text'] for m in messages])

        references = {
            'stores': [],
            'vendors': [],
            'meetings': [],
            'structured_data': []
        }

        # Extract store IDs
        import re
        store_pattern = r'Store[- ]#?(\d+)'
        stores = re.findall(store_pattern, full_text)
        references['stores'] = [f"Store-{s}" for s in stores]

        # Extract vendor names
        vendor_pattern = r'([A-Z][a-zA-Z]+ (?:Systems|Solutions|Construction|Master))'
        vendors = re.findall(vendor_pattern, full_text)
        references['vendors'] = list(set(vendors))

        # Add meeting references if theme is followup
        if theme_config.get('theme') == 'site-visit-followup' and theme_config.get('store_id'):
            meeting_file = f"site_visit_{theme_config['store_id']}_{theme_config['date']}.txt"
            references['meetings'].append(meeting_file)

        # Add structured data references
        if theme_config.get('store_id'):
            references['structured_data'].append({
                'source': '03_Historical_Projects',
                'file': 'historical_projects.csv',
                'field': f"{theme_config['store_id']}"
            })

        return references

    def _save_channel(self, channel_data: Dict, channel_name: str):
        """Save channel to JSON file."""
        filepath = self._get_channel_file(channel_name)

        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, 'w') as f:
            json.dump(channel_data, f, indent=2)

        print(f"✓ Saved channel: {filepath}")
        print(f"  Threads: {len(channel_data['threads'])}")

    def _update_conversation_index(self, channel_data: Dict, config: Dict):
        """Update conversation index with Teams threads."""
        index_path = f'{self.output_dir}/metadata/conversation_index.csv'

        entries = []

        for thread in channel_data['threads']:
            # Extract stores from references
            stores = thread['references'].get('stores', [])

            for store_id in stores:
                entry = {
                    'store_id': store_id,
                    'conversation_type': 'teams_thread',
                    'filename': f"{channel_data['channel']}.json#{thread['thread_id']}",
                    'date': thread['date'],
                    'participants': '|'.join([p['name'] for p in thread['participants']]),
                    'key_topics': '|'.join(set([tag for msg in thread['messages'] for tag in msg['tags']])),
                    'cost_impact': 0,
                    'timeline_impact': 0
                }
                entries.append(entry)

        if entries:
            # Append to CSV
            if os.path.exists(index_path):
                df = pd.read_csv(index_path)
                df = pd.concat([df, pd.DataFrame(entries)], ignore_index=True)
            else:
                df = pd.DataFrame(entries)

            os.makedirs(os.path.dirname(index_path), exist_ok=True)
            df.to_csv(index_path, index=False)

            print(f"✓ Updated conversation index ({len(entries)} entries)")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Generate Teams conversations')
    parser.add_argument('--config', help='Path to config JSON file')
    parser.add_argument('--channel', help='Channel name')
    parser.add_argument('--theme', help='Conversation theme')
    parser.add_argument('--store-id', help='Store ID')
    parser.add_argument('--date', help='Conversation date (YYYY-MM-DD)')

    args = parser.parse_args()

    # Load config
    if args.config:
        with open(args.config, 'r') as f:
            config = json.load(f)
    else:
        # Build config from args
        config = {
            'channel_name': args.channel or 'construction-vendors',
            'conversation_themes': [
                {
                    'theme': args.theme or 'supply-chain-delay',
                    'store_id': args.store_id or 'Store-217',
                    'date': args.date or datetime.now().strftime('%Y-%m-%d')
                }
            ]
        }

    # Generate conversations
    generator = TeamsConversationGenerator()
    result = generator.generate_conversations(config)

    print(f"\n✓ Generated {len(result['threads'])} threads for channel: {result['channel']}")


if __name__ == '__main__':
    main()
