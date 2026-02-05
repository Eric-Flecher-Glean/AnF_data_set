#!/usr/bin/env python3
"""
Phase 2 Enhanced Data Generation - Scaling to 100 Stores

Generates:
- 75 meeting transcripts (60 additional beyond Phase 1)
- 250+ Teams messages
- 100 stores total (Store-201 to Store-300)
- 6 channels with varied themes
"""

import os
import random
from datetime import datetime, timedelta
from generate_meeting_transcripts_v2 import EnhancedMeetingGenerator
from generate_teams_conversations import TeamsConversationGenerator


class Phase2Generator:
    """Generate Phase 2 scaled dataset."""

    def __init__(self):
        self.meeting_gen = EnhancedMeetingGenerator()
        self.teams_gen = TeamsConversationGenerator()
        self.stores = [f'Store-{200+i}' for i in range(1, 101)]  # Store-201 to Store-300
        self.stats = {
            'meetings_generated': 0,
            'teams_threads_generated': 0,
            'stores_covered': set(),
            'errors': []
        }

    def generate_meetings(self):
        """Generate 75 meeting transcripts across 100 stores."""
        print("\n" + "="*60)
        print("PHASE 2: MEETING TRANSCRIPT GENERATION")
        print("="*60 + "\n")

        # 1. Site Visit Debriefs (15 total)
        print("[1/5] Generating 15 site visit debriefs...")
        for i in range(15):
            store_id = self.stores[i]
            try:
                config = {
                    'meeting_type': 'site_visit_debrief',
                    'store_id': store_id,
                    'date': (datetime.now() - timedelta(days=180-i*10)).strftime('%Y-%m-%d'),
                    'participants': 'Sarah Chen|Tom Wilson|Mike Rodriguez'
                }
                self.meeting_gen.generate_transcript('site_visit_debrief', config)
                self.stats['meetings_generated'] += 1
                self.stats['stores_covered'].add(store_id)
            except Exception as e:
                self.stats['errors'].append(f"Site visit {store_id}: {str(e)}")

        # 2. Vendor Negotiations (15 total)
        print("\n[2/5] Generating 15 vendor negotiations...")
        vendor_topics = [
            'hvac-vendors-q1', 'hvac-vendors-q2', 'hvac-vendors-q3', 'hvac-vendors-q4',
            'electrical-contractors-spring', 'electrical-contractors-summer',
            'plumbing-vendors-q1', 'plumbing-vendors-q2',
            'general-contractors-northeast', 'general-contractors-midwest',
            'hvac-volume-pricing', 'lighting-suppliers-annual',
            'flooring-vendors-q3', 'signage-vendors-q2', 'security-systems-annual'
        ]

        for i, topic in enumerate(vendor_topics):
            try:
                config = {
                    'meeting_type': 'vendor_negotiation',
                    'topic': topic,
                    'date': (datetime.now() - timedelta(days=200-i*12)).strftime('%Y-%m-%d'),
                    'participants': 'Jennifer Liu|Tom Wilson'
                }
                self.meeting_gen.generate_transcript('vendor_negotiation', config)
                self.stats['meetings_generated'] += 1
            except Exception as e:
                self.stats['errors'].append(f"Vendor negotiation {topic}: {str(e)}")

        # 3. Lessons Learned (25 total)
        print("\n[3/5] Generating 25 lessons learned meetings...")
        for i in range(25):
            store_id = f'Store-{170+i}'  # Historical stores
            try:
                config = {
                    'meeting_type': 'lessons_learned',
                    'store_id': store_id,
                    'date': (datetime.now() - timedelta(days=220-i*7)).strftime('%Y-%m-%d'),
                    'participants': 'Sarah Chen|Tom Wilson|David Park|Lisa Thompson'
                }
                self.meeting_gen.generate_transcript('lessons_learned', config)
                self.stats['meetings_generated'] += 1
                self.stats['stores_covered'].add(store_id)
            except Exception as e:
                self.stats['errors'].append(f"Lessons learned {store_id}: {str(e)}")

        # 4. Design Reviews (10 total)
        print("\n[4/5] Generating 10 design reviews...")
        template_versions = [
            'v2.3', 'v2.4', 'v2.5', 'v2.6', 'v2.7',
            'v3.0', 'v3.1', 'v3.2', 'v3.3', 'v3.4'
        ]

        for i, version in enumerate(template_versions):
            try:
                config = {
                    'meeting_type': 'design_review',
                    'topic': f'template-{version}',
                    'template_version': version,
                    'date': (datetime.now() - timedelta(days=240-i*20)).strftime('%Y-%m-%d'),
                    'participants': 'Carlos Martinez|Angela Wu|David Park'
                }
                self.meeting_gen.generate_transcript('design_review', config)
                self.stats['meetings_generated'] += 1
            except Exception as e:
                self.stats['errors'].append(f"Design review {version}: {str(e)}")

        # 5. Weekly Dev Syncs (10 total)
        print("\n[5/5] Generating 10 weekly dev syncs...")
        markets = [
            'Columbus-Market', 'Cincinnati-Market', 'Cleveland-Market',
            'Pittsburgh-Market', 'Indianapolis-Market', 'Louisville-Market',
            'Detroit-Market', 'Nashville-Market', 'Charlotte-Market', 'Atlanta-Market'
        ]

        for i, market in enumerate(markets):
            try:
                config = {
                    'meeting_type': 'weekly_dev_sync',
                    'topic': market,
                    'date': (datetime.now() - timedelta(days=70-i*7)).strftime('%Y-%m-%d'),
                    'participants': 'Sarah Chen|Jennifer Liu'
                }
                self.meeting_gen.generate_transcript('weekly_dev_sync', config)
                self.stats['meetings_generated'] += 1
            except Exception as e:
                self.stats['errors'].append(f"Weekly sync {market}: {str(e)}")

        print(f"\n✓ Meetings generated: {self.stats['meetings_generated']}/75")

    def generate_teams_conversations(self):
        """Generate 250+ Teams messages across 6 channels."""
        print("\n" + "="*60)
        print("PHASE 2: TEAMS CONVERSATION GENERATION")
        print("="*60 + "\n")

        channels_config = [
            {
                'channel': 'store-development-general',
                'threads': 15,
                'themes': [
                    'site-visit-followup', 'cost-variance-discussion',
                    'schedule-update', 'vendor-question'
                ]
            },
            {
                'channel': 'construction-vendors',
                'threads': 20,
                'themes': [
                    'supply-chain-delay', 'pricing-negotiation',
                    'vendor-performance-issue', 'emergency-procurement'
                ]
            },
            {
                'channel': 'design-standards-updates',
                'threads': 12,
                'themes': [
                    'template-update', 'design-standard-change',
                    'material-specification', 'compliance-question'
                ]
            },
            {
                'channel': 'columbus-market-planning',
                'threads': 10,
                'themes': [
                    'market-specific-constraint', 'regional-vendor-discussion',
                    'permitting-timeline', 'market-expansion-plan'
                ]
            },
            {
                'channel': 'cincinnati-market-planning',
                'threads': 10,
                'themes': [
                    'labor-rate-discussion', 'union-requirement',
                    'market-specific-constraint', 'landlord-negotiation'
                ]
            },
            {
                'channel': 'finance-cost-tracking',
                'threads': 12,
                'themes': [
                    'budget-variance-alert', 'cost-model-update',
                    'financial-reporting', 'savings-opportunity'
                ]
            }
        ]

        total_threads = 0

        for channel_cfg in channels_config:
            channel = channel_cfg['channel']
            thread_count = channel_cfg['threads']
            themes = channel_cfg['themes']

            print(f"\nGenerating {thread_count} threads for '{channel}'...")

            for i in range(thread_count):
                theme = random.choice(themes)
                store_id = random.choice(self.stores[:50])  # Use first 50 stores

                try:
                    config = {
                        'channel_name': channel,
                        'conversation_themes': [
                            {
                                'theme': theme,
                                'store_id': store_id,
                                'date': (datetime.now() - timedelta(days=random.randint(5, 150))).strftime('%Y-%m-%d')
                            }
                        ],
                        'participant_pool': ['Sarah Chen', 'Tom Wilson', 'Jennifer Liu', 'Mike Rodriguez', 'David Park']
                    }

                    result = self.teams_gen.generate_conversations(config)
                    total_threads += len(result['threads'])
                    self.stats['teams_threads_generated'] += len(result['threads'])

                except Exception as e:
                    self.stats['errors'].append(f"Teams thread {channel}/{theme}: {str(e)}")

        print(f"\n✓ Teams threads generated: {total_threads}")

    def print_summary(self):
        """Print generation summary."""
        print("\n" + "="*60)
        print("PHASE 2 GENERATION COMPLETE")
        print("="*60)
        print(f"\nMeetings Generated:         {self.stats['meetings_generated']}/75")
        print(f"Teams Threads Generated:    {self.stats['teams_threads_generated']}")
        print(f"Stores Covered:             {len(self.stats['stores_covered'])}")

        if self.stats['errors']:
            print(f"\n⚠ Errors encountered:       {len(self.stats['errors'])}")
            for error in self.stats['errors'][:5]:  # Show first 5 errors
                print(f"  - {error}")
            if len(self.stats['errors']) > 5:
                print(f"  ... and {len(self.stats['errors']) - 5} more")
        else:
            print("\n✓ No errors encountered")

        print("\n" + "="*60)

    def run(self):
        """Run full Phase 2 generation."""
        print("\n" + "="*60)
        print("PHASE 2: SCALING TO 100 STORES")
        print("="*60)
        print("\nTargets:")
        print("  - 100 stores (Store-201 to Store-300)")
        print("  - 75 meeting transcripts")
        print("  - 250+ Teams messages")
        print("  - 6 channels")
        print("\n" + "="*60)

        # Generate meetings
        self.generate_meetings()

        # Generate Teams conversations
        self.generate_teams_conversations()

        # Print summary
        self.print_summary()


def main():
    """Main entry point."""
    generator = Phase2Generator()
    generator.run()


if __name__ == '__main__':
    main()
