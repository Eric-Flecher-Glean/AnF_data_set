#!/usr/bin/env python3
"""
Enhanced Dialogue Generator

Uses rich scenario-based templates to generate realistic meeting dialogue.
This demonstrates how to improve dialogue quality to match Teams conversations.
"""

import yaml
import random
from datetime import datetime, timedelta


class EnhancedDialogueGenerator:
    """Generate realistic dialogue using scenario templates."""

    def __init__(self):
        self.cost_directions = {
            'positive': 'under',
            'negative': 'over',
            'savings': 'lower',
            'increase': 'higher'
        }

    def generate_lessons_learned_dialogue(self, store_id, historical_data):
        """
        Generate realistic lessons learned dialogue.

        Args:
            store_id: Store identifier (e.g., "Store-189")
            historical_data: Dict with estimated_cost, actual_cost, vendor, etc.

        Returns:
            List of dialogue exchanges with timestamps
        """
        # Calculate variances
        electrical_variance = historical_data['electrical_actual'] - historical_data['electrical_estimated']
        variance_pct = abs(electrical_variance / historical_data['electrical_estimated'] * 100)

        # Determine direction
        if electrical_variance < 0:
            direction = 'under'
            direction_verb = 'saved'
            benefit = 'cost savings'
        else:
            direction = 'over'
            direction_verb = 'added'
            benefit = 'lesson learned'

        # Calculate days since completion
        completion_date = datetime.strptime(historical_data['completion_date'], '%Y-%m-%d')
        meeting_date = datetime.now()
        days_since = (meeting_date - completion_date).days

        # Generate realistic dialogue
        dialogue = [
            {
                'speaker': 'Sarah Chen',
                'role': 'Project Manager',
                'text': f"Thanks everyone for joining. Let's review {store_id}'s performance. We completed this project {days_since} days ago, so the data is fresh."
            },
            {
                'speaker': 'David Park',
                'role': 'VP Store Development',
                'text': "Good timing. What are the key variances we need to understand?"
            },
            {
                'speaker': 'Lisa Thompson',
                'role': 'Finance Analyst',
                'text': f"Looking at the financials, we came in ${abs(electrical_variance):,} {direction} budget on electrical. We estimated ${historical_data['electrical_estimated']:,} but actual was ${historical_data['electrical_actual']:,}."
            },
            {
                'speaker': 'Sarah Chen',
                'role': 'Project Manager',
                'text': "What drove that variance?"
            },
            {
                'speaker': 'Tom Wilson',
                'role': 'General Contractor',
                'text': f"We used {historical_data.get('backup_vendor', 'TempMaster')} instead of our usual contractor. They had {variance_pct:.0f}% {direction} pricing but quality was excellent."
            },
            {
                'speaker': 'David Park',
                'role': 'VP Store Development',
                'text': f"Is this a one-time variance or should we consider {historical_data.get('backup_vendor', 'TempMaster')} for our primary vendor rotation?"
            },
            {
                'speaker': 'Sarah Chen',
                'role': 'Project Manager',
                'text': f"Based on this project, I'd recommend adding them to our preferred vendor list. The {variance_pct:.0f}% {benefit} could be significant across our portfolio."
            },
            {
                'speaker': 'Lisa Thompson',
                'role': 'Finance Analyst',
                'text': f"From a budget perspective, this {direction_verb} us ${abs(electrical_variance):,}. If we see similar results across other markets, that could impact our annual projections."
            },
            {
                'speaker': 'Tom Wilson',
                'role': 'General Contractor',
                'text': f"Operationally, the key learning is that backup vendors can sometimes offer better value. We should always get quotes from at least two contractors."
            },
            {
                'speaker': 'Sarah Chen',
                'role': 'Project Manager',
                'text': "I'll make sure these learnings get added to our knowledge base and shared with the broader team."
            },
            {
                'speaker': 'David Park',
                'role': 'VP Store Development',
                'text': f"Excellent work team. Let's apply these insights to our upcoming projects in the Columbus and Cincinnati markets."
            }
        ]

        # Add timestamps
        current_time = 0
        for item in dialogue:
            hours = current_time // 3600
            minutes = (current_time % 3600) // 60
            seconds = current_time % 60
            item['timestamp'] = f"[{hours:02d}:{minutes:02d}:{seconds:02d}]"

            # Increment time (30-180 seconds per exchange)
            current_time += random.randint(30, 180)

        return dialogue

    def format_dialogue_as_transcript(self, dialogue, store_id, date):
        """Format dialogue list as meeting transcript."""
        lines = []

        # Header
        lines.append("MEETING: Lessons Learned")
        lines.append(f"DATE: {date}")
        lines.append("PARTICIPANTS:")

        # Extract unique participants
        participants = {}
        for d in dialogue:
            if d['speaker'] not in participants:
                participants[d['speaker']] = d['role']

        for speaker, role in participants.items():
            team = self._get_team_for_role(role)
            lines.append(f"  - {speaker} ({role}) - {team}")

        duration = int(dialogue[-1]['timestamp'].strip('[]').split(':')[0]) * 60 + \
                   int(dialogue[-1]['timestamp'].strip('[]').split(':')[1])
        lines.append(f"DURATION: {duration // 60:02d}:{duration % 60:02d}")
        lines.append(f"STORE/TOPIC: {store_id}")
        lines.append("---")
        lines.append("")

        # Dialogue
        for d in dialogue:
            lines.append(f"{d['timestamp']} {d['speaker']}: {d['text']}")

        lines.append("")
        lines.append("---")
        lines.append(f"TAGS: {store_id}, electrical-variance, vendor-comparison, cost-savings")
        lines.append("ACTION ITEMS:")
        lines.append(f"  - Add learnings to knowledge base [@Sarah Chen, due: {self._get_next_friday(date)}]")
        lines.append(f"  - Share insights with broader team [@Sarah Chen, due: {self._get_next_friday(date)}]")
        lines.append("REFERENCES:")
        lines.append(f"  - Historical Store: {store_id} (electrical variance analysis)")
        lines.append(f"  - Vendor: TempMaster (backup vendor with better pricing)")

        return '\n'.join(lines)

    def _get_team_for_role(self, role):
        """Map role to team name."""
        team_map = {
            'Project Manager': 'ANF Store Development',
            'General Contractor': 'BuildRight Construction',
            'VP Store Development': 'ANF',
            'Finance Analyst': 'ANF Finance'
        }
        return team_map.get(role, 'ANF')

    def _get_next_friday(self, date_str):
        """Get next Friday from given date."""
        date = datetime.strptime(date_str, '%Y-%m-%d')
        days_ahead = 4 - date.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return (date + timedelta(days=days_ahead)).strftime('%Y-%m-%d')


def main():
    """Demo: Generate enhanced lessons learned meeting."""
    generator = EnhancedDialogueGenerator()

    # Sample historical data
    historical_data = {
        'store_id': 'Store-189',
        'completion_date': '2024-02-01',
        'electrical_estimated': 35000,
        'electrical_actual': 32000,
        'backup_vendor': 'TempMaster'
    }

    # Generate dialogue
    dialogue = generator.generate_lessons_learned_dialogue(
        store_id='Store-189',
        historical_data=historical_data
    )

    # Format as transcript
    transcript = generator.format_dialogue_as_transcript(
        dialogue=dialogue,
        store_id='Store-189',
        date='2025-11-07'
    )

    print(transcript)
    print("\n" + "="*60)
    print("✅ Enhanced dialogue generated successfully!")
    print("="*60)


if __name__ == '__main__':
    main()
