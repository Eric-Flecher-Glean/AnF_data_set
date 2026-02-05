#!/usr/bin/env python3
"""
Phase 3 Production Data Generation - Full Scale

Generates:
- 250 meeting transcripts (160 additional beyond Phase 2)
- 750+ Teams messages
- 300 stores total (Store-101 to Store-400)
- 12-month temporal span with quarterly patterns
- 8 channels with comprehensive themes
"""

import os
import random
from datetime import datetime, timedelta
from generate_meeting_transcripts_v2 import EnhancedMeetingGenerator
from generate_teams_conversations import TeamsConversationGenerator


class Phase3Generator:
    """Generate Phase 3 production dataset."""

    def __init__(self):
        self.meeting_gen = EnhancedMeetingGenerator()
        self.teams_gen = TeamsConversationGenerator()
        # Expanded store range: Store-101 to Store-400 (300 stores)
        self.stores = [f'Store-{100+i}' for i in range(1, 301)]
        self.base_date = datetime.now() - timedelta(days=365)  # 12 months ago
        self.stats = {
            'meetings_generated': 0,
            'teams_threads_generated': 0,
            'stores_covered': set(),
            'errors': []
        }

    def generate_meetings(self):
        """Generate 250 meeting transcripts across 300 stores with 12-month span."""
        print("\n" + "="*60)
        print("PHASE 3: PRODUCTION MEETING GENERATION")
        print("="*60 + "\n")

        # 1. Site Visit Debriefs (50 total)
        print("[1/5] Generating 50 site visit debriefs...")
        for i in range(50):
            store_id = self.stores[i * 6]  # Spread across store range
            days_offset = 30 + (i * 7)  # Weekly cadence over year
            try:
                config = {
                    'meeting_type': 'site_visit_debrief',
                    'store_id': store_id,
                    'date': (self.base_date + timedelta(days=days_offset)).strftime('%Y-%m-%d'),
                    'participants': 'Sarah Chen|Tom Wilson|Mike Rodriguez'
                }
                self.meeting_gen.generate_transcript('site_visit_debrief', config)
                self.stats['meetings_generated'] += 1
                self.stats['stores_covered'].add(store_id)
            except Exception as e:
                self.stats['errors'].append(f"Site visit {store_id}: {str(e)}")

        # 2. Vendor Negotiations (50 total - quarterly patterns)
        print("\n[2/5] Generating 50 vendor negotiations...")
        vendor_topics = [
            # Q1 topics
            'hvac-vendors-q1-2025', 'electrical-contractors-q1', 'plumbing-vendors-q1',
            'general-contractors-northeast-q1', 'lighting-suppliers-q1', 'flooring-vendors-q1',
            'signage-vendors-q1', 'security-systems-q1', 'hvac-maintenance-q1', 'fire-suppression-q1',
            'hvac-parts-q1', 'hvac-service-q1', 'electrical-parts-q1',
            # Q2 topics
            'hvac-vendors-q2-2025', 'electrical-contractors-q2', 'plumbing-vendors-q2',
            'general-contractors-midwest-q2', 'lighting-suppliers-q2', 'flooring-vendors-q2',
            'signage-vendors-q2', 'security-systems-q2', 'hvac-maintenance-q2', 'fire-suppression-q2',
            'hvac-parts-q2', 'hvac-service-q2', 'electrical-parts-q2',
            # Q3 topics
            'hvac-vendors-q3-2025', 'electrical-contractors-q3', 'plumbing-vendors-q3',
            'general-contractors-south-q3', 'lighting-suppliers-q3', 'flooring-vendors-q3',
            'signage-vendors-q3', 'security-systems-q3', 'hvac-maintenance-q3', 'fire-suppression-q3',
            'hvac-parts-q3', 'hvac-service-q3', 'electrical-parts-q3',
            # Q4 topics
            'hvac-vendors-q4-2025', 'electrical-contractors-q4', 'plumbing-vendors-q4',
            'general-contractors-west-q4', 'lighting-suppliers-q4', 'flooring-vendors-q4',
            'signage-vendors-q4', 'security-systems-q4', 'hvac-maintenance-q4', 'fire-suppression-q4',
            'hvac-annual-review', 'electrical-annual-review'
        ]

        for i, topic in enumerate(vendor_topics[:50]):
            quarter = (i // 13) + 1  # Roughly 13 per quarter
            days_offset = (quarter - 1) * 90 + (i % 13) * 7
            try:
                config = {
                    'meeting_type': 'vendor_negotiation',
                    'topic': topic,
                    'date': (self.base_date + timedelta(days=days_offset)).strftime('%Y-%m-%d'),
                    'participants': 'Jennifer Liu|Tom Wilson'
                }
                self.meeting_gen.generate_transcript('vendor_negotiation', config)
                self.stats['meetings_generated'] += 1
            except Exception as e:
                self.stats['errors'].append(f"Vendor negotiation {topic}: {str(e)}")

        # 3. Lessons Learned (80 total)
        print("\n[3/5] Generating 80 lessons learned meetings...")
        for i in range(80):
            # Reference historical stores (Store-50 to Store-129)
            store_id = f'Store-{50 + i}'
            days_offset = 60 + (i * 4)  # Every 4 days over the year
            try:
                config = {
                    'meeting_type': 'lessons_learned',
                    'store_id': store_id,
                    'date': (self.base_date + timedelta(days=days_offset)).strftime('%Y-%m-%d'),
                    'participants': 'Sarah Chen|Tom Wilson|David Park|Lisa Thompson'
                }
                self.meeting_gen.generate_transcript('lessons_learned', config)
                self.stats['meetings_generated'] += 1
                self.stats['stores_covered'].add(store_id)
            except Exception as e:
                self.stats['errors'].append(f"Lessons learned {store_id}: {str(e)}")

        # 4. Design Reviews (40 total - monthly cadence)
        print("\n[4/5] Generating 40 design reviews...")
        template_versions = []
        # Generate version numbers v2.0 to v5.9
        for major in [2, 3, 4, 5]:
            for minor in range(10):
                template_versions.append(f'v{major}.{minor}')
                if len(template_versions) >= 40:
                    break
            if len(template_versions) >= 40:
                break

        for i, version in enumerate(template_versions[:40]):
            days_offset = 15 + (i * 9)  # Roughly every 9 days
            try:
                config = {
                    'meeting_type': 'design_review',
                    'topic': f'template-{version}',
                    'template_version': version,
                    'date': (self.base_date + timedelta(days=days_offset)).strftime('%Y-%m-%d'),
                    'participants': 'Carlos Martinez|Angela Wu|David Park'
                }
                self.meeting_gen.generate_transcript('design_review', config)
                self.stats['meetings_generated'] += 1
            except Exception as e:
                self.stats['errors'].append(f"Design review {version}: {str(e)}")

        # 5. Weekly Dev Syncs (30 total - weekly cadence across markets)
        print("\n[5/5] Generating 30 weekly dev syncs...")
        markets = [
            'Columbus-Market', 'Cincinnati-Market', 'Cleveland-Market',
            'Pittsburgh-Market', 'Indianapolis-Market', 'Louisville-Market',
            'Detroit-Market', 'Nashville-Market', 'Charlotte-Market', 'Atlanta-Market',
            'Chicago-Market', 'Milwaukee-Market', 'Minneapolis-Market', 'St-Louis-Market',
            'Kansas-City-Market', 'Dallas-Market', 'Houston-Market', 'San-Antonio-Market',
            'Phoenix-Market', 'Denver-Market', 'Seattle-Market', 'Portland-Market',
            'San-Francisco-Market', 'Los-Angeles-Market', 'San-Diego-Market',
            'Boston-Market', 'Philadelphia-Market', 'New-York-Market', 'Baltimore-Market', 'DC-Market'
        ]

        for i in range(30):
            market = markets[i]
            days_offset = 7 + (i * 12)  # Every 12 days (just under weekly)
            try:
                config = {
                    'meeting_type': 'weekly_dev_sync',
                    'topic': market,
                    'date': (self.base_date + timedelta(days=days_offset)).strftime('%Y-%m-%d'),
                    'participants': 'Sarah Chen|Jennifer Liu'
                }
                self.meeting_gen.generate_transcript('weekly_dev_sync', config)
                self.stats['meetings_generated'] += 1
            except Exception as e:
                self.stats['errors'].append(f"Weekly sync {market}: {str(e)}")

        print(f"\n✓ Meetings generated: {self.stats['meetings_generated']}/250")

    def generate_teams_conversations(self):
        """Generate 750+ Teams messages across 8 channels with quarterly patterns."""
        print("\n" + "="*60)
        print("PHASE 3: TEAMS CONVERSATION GENERATION")
        print("="*60 + "\n")

        channels_config = [
            {
                'channel': 'store-development-general',
                'threads': 40,
                'themes': [
                    'site-visit-followup', 'cost-variance-discussion',
                    'schedule-update', 'vendor-question', 'permit-status',
                    'construction-milestone', 'inspection-result'
                ]
            },
            {
                'channel': 'construction-vendors',
                'threads': 50,
                'themes': [
                    'supply-chain-delay', 'pricing-negotiation',
                    'vendor-performance-issue', 'emergency-procurement',
                    'quality-concern', 'delivery-coordination',
                    'vendor-substitution', 'warranty-question'
                ]
            },
            {
                'channel': 'design-standards-updates',
                'threads': 30,
                'themes': [
                    'template-update', 'design-standard-change',
                    'material-specification', 'compliance-question',
                    'sustainability-requirement', 'accessibility-standard',
                    'brand-guideline-update'
                ]
            },
            {
                'channel': 'columbus-market-planning',
                'threads': 25,
                'themes': [
                    'market-specific-constraint', 'regional-vendor-discussion',
                    'permitting-timeline', 'market-expansion-plan',
                    'local-regulation-update', 'competitor-activity'
                ]
            },
            {
                'channel': 'cincinnati-market-planning',
                'threads': 25,
                'themes': [
                    'labor-rate-discussion', 'union-requirement',
                    'market-specific-constraint', 'landlord-negotiation',
                    'local-incentive-program', 'market-trend-analysis'
                ]
            },
            {
                'channel': 'finance-cost-tracking',
                'threads': 30,
                'themes': [
                    'budget-variance-alert', 'cost-model-update',
                    'financial-reporting', 'savings-opportunity',
                    'portfolio-performance', 'roi-analysis',
                    'capital-planning'
                ]
            },
            {
                'channel': 'project-management-tools',
                'threads': 25,
                'themes': [
                    'schedule-optimization', 'resource-allocation',
                    'risk-mitigation', 'stakeholder-communication',
                    'milestone-tracking', 'process-improvement'
                ]
            },
            {
                'channel': 'quality-and-compliance',
                'threads': 25,
                'themes': [
                    'safety-incident-report', 'code-compliance-check',
                    'quality-inspection-finding', 'warranty-claim',
                    'lessons-learned-share', 'best-practice-discussion'
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
                # Use broader store range for Teams conversations
                store_id = random.choice(self.stores[:150])
                # Spread across 12 months
                days_offset = random.randint(0, 365)

                try:
                    config = {
                        'channel_name': channel,
                        'conversation_themes': [
                            {
                                'theme': theme,
                                'store_id': store_id,
                                'date': (self.base_date + timedelta(days=days_offset)).strftime('%Y-%m-%d')
                            }
                        ],
                        'participant_pool': [
                            'Sarah Chen', 'Tom Wilson', 'Jennifer Liu',
                            'Mike Rodriguez', 'David Park', 'Lisa Thompson',
                            'Carlos Martinez', 'Angela Wu'
                        ]
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
        print("PHASE 3 PRODUCTION GENERATION COMPLETE")
        print("="*60)
        print(f"\nMeetings Generated:         {self.stats['meetings_generated']}/250")
        print(f"Teams Threads Generated:    {self.stats['teams_threads_generated']}")
        print(f"Stores Covered:             {len(self.stats['stores_covered'])}")

        if self.stats['errors']:
            print(f"\n⚠ Errors encountered:       {len(self.stats['errors'])}")
            for error in self.stats['errors'][:10]:  # Show first 10 errors
                print(f"  - {error}")
            if len(self.stats['errors']) > 10:
                print(f"  ... and {len(self.stats['errors']) - 10} more")
        else:
            print("\n✓ No errors encountered")

        print("\n" + "="*60)

    def run(self):
        """Run full Phase 3 generation."""
        print("\n" + "="*60)
        print("PHASE 3: PRODUCTION SCALE - 300 STORES")
        print("="*60)
        print("\nTargets:")
        print("  - 300 stores (Store-101 to Store-400)")
        print("  - 250 meeting transcripts")
        print("  - 750+ Teams messages")
        print("  - 8 channels")
        print("  - 12-month temporal span")
        print("\n" + "="*60)

        # Generate meetings
        self.generate_meetings()

        # Generate Teams conversations
        self.generate_teams_conversations()

        # Print summary
        self.print_summary()


def main():
    """Main entry point."""
    generator = Phase3Generator()
    generator.run()


if __name__ == '__main__':
    main()
