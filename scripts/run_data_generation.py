#!/usr/bin/env python3
"""
Orchestration script for generating complete conversational dataset.

This script coordinates the generation of meeting transcripts and Teams conversations
according to a phased implementation plan.

Usage:
    python run_data_generation.py --phase 1
    python run_data_generation.py --phase 2
    python run_data_generation.py --phase 3 --full
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
import random

# Import generators
from generate_meeting_transcripts import MeetingTranscriptGenerator
from generate_teams_conversations import TeamsConversationGenerator


class DataGenerationOrchestrator:
    """Orchestrate full data generation workflow."""

    def __init__(self):
        self.meeting_generator = MeetingTranscriptGenerator()
        self.teams_generator = TeamsConversationGenerator()

        # Load store list (or generate mock stores)
        self.stores = self._load_or_generate_stores()

    def _load_or_generate_stores(self):
        """Load store list or generate for MVP."""
        # For MVP, generate sample store IDs
        return [f"Store-{200+i}" for i in range(1, 21)]  # Store-201 to Store-220

    def run_phase_1_mvp(self):
        """
        Phase 1: MVP (20 stores)
        - 15 meeting transcripts
        - 50 Teams messages
        - 4 channels
        """
        print("\n" + "="*60)
        print("PHASE 1: MVP DATA GENERATION")
        print("="*60 + "\n")

        stats = {
            'meetings_generated': 0,
            'teams_threads_generated': 0,
            'stores_covered': set()
        }

        # Generate 3 site visit debriefs
        print("\n[1/5] Generating site visit debriefs...")
        for i, store_id in enumerate(self.stores[:3]):
            config = {
                'meeting_type': 'site_visit_debrief',
                'store_id_or_topic': store_id,
                'date': (datetime.now() - timedelta(days=30-i*5)).strftime('%Y-%m-%d'),
                'participants': [
                    {'name': 'Sarah Chen'},
                    {'name': 'Tom Wilson'},
                    {'name': 'Mike Rodriguez'}
                ],
                'context': {
                    'historical_reference': f'Store-{189+i}',
                    'cost_focus': 'electrical-upgrade'
                },
                'duration_minutes': 75
            }

            result = self.meeting_generator.generate_transcript(config)
            stats['meetings_generated'] += 1
            stats['stores_covered'].add(store_id)

        # Generate 3 vendor negotiations
        print("\n[2/5] Generating vendor negotiations...")
        for i in range(3):
            config = {
                'meeting_type': 'vendor_negotiation',
                'store_id_or_topic': f'hvac-vendors-q{i+1}',
                'date': (datetime.now() - timedelta(days=60-i*10)).strftime('%Y-%m-%d'),
                'participants': [
                    {'name': 'Jennifer Liu'},
                    {'name': 'Tom Wilson'}
                ],
                'context': {},
                'duration_minutes': 45
            }

            result = self.meeting_generator.generate_transcript(config)
            stats['meetings_generated'] += 1

        # Generate 5 lessons learned
        print("\n[3/5] Generating lessons learned meetings...")
        for i, store_id in enumerate([f'Store-{189+i}' for i in range(5)]):
            config = {
                'meeting_type': 'lessons_learned',
                'store_id_or_topic': store_id,
                'date': (datetime.now() - timedelta(days=90-i*7)).strftime('%Y-%m-%d'),
                'participants': [
                    {'name': 'Sarah Chen'},
                    {'name': 'Tom Wilson'},
                    {'name': 'David Park'},
                    {'name': 'Lisa Thompson'}
                ],
                'context': {
                    'historical_reference': store_id
                },
                'duration_minutes': 90
            }

            result = self.meeting_generator.generate_transcript(config)
            stats['meetings_generated'] += 1
            stats['stores_covered'].add(store_id)

        # Generate 2 design reviews
        print("\n[4/5] Generating design reviews...")
        for i in range(2):
            config = {
                'meeting_type': 'design_review',
                'store_id_or_topic': f'template-v2.{3+i}',
                'date': (datetime.now() - timedelta(days=120-i*90)).strftime('%Y-%m-%d'),
                'participants': [
                    {'name': 'Carlos Martinez'},
                    {'name': 'Angela Wu'},
                    {'name': 'David Park'}
                ],
                'context': {},
                'duration_minutes': 60
            }

            result = self.meeting_generator.generate_transcript(config)
            stats['meetings_generated'] += 1

        # Generate 2 weekly syncs
        print("\n[5/5] Generating weekly dev syncs...")
        for i in range(2):
            config = {
                'meeting_type': 'weekly_dev_sync',
                'store_id_or_topic': 'Columbus-Market',
                'date': (datetime.now() - timedelta(days=14-i*7)).strftime('%Y-%m-%d'),
                'participants': [
                    {'name': 'Sarah Chen'},
                    {'name': 'Jennifer Liu'}
                ],
                'context': {},
                'duration_minutes': 30
            }

            result = self.meeting_generator.generate_transcript(config)
            stats['meetings_generated'] += 1

        # Generate Teams threads
        print("\n[6/6] Generating Teams conversations...")

        channels_and_themes = [
            ('store-development-general', 'site-visit-followup'),
            ('construction-vendors', 'supply-chain-delay'),
            ('design-standards-updates', 'template-update'),
            ('columbus-market-planning', 'cost-variance-discussion')
        ]

        for channel, theme in channels_and_themes:
            # Generate 2-3 threads per channel
            for i in range(random.randint(2, 3)):
                store_id = random.choice(list(stats['stores_covered']))

                config = {
                    'channel_name': channel,
                    'conversation_themes': [
                        {
                            'theme': theme,
                            'store_id': store_id,
                            'date': (datetime.now() - timedelta(days=random.randint(5, 60))).strftime('%Y-%m-%d')
                        }
                    ],
                    'participant_pool': ['Sarah Chen', 'Tom Wilson', 'Jennifer Liu']
                }

                result = self.teams_generator.generate_conversations(config)
                stats['teams_threads_generated'] += len(result['threads'])

        # Print summary
        print("\n" + "="*60)
        print("PHASE 1 COMPLETE")
        print("="*60)
        print(f"Meetings Generated: {stats['meetings_generated']}")
        print(f"Teams Threads Generated: {stats['teams_threads_generated']}")
        print(f"Stores Covered: {len(stats['stores_covered'])}")
        print(f"Conversation Index Updated: Yes")
        print("="*60 + "\n")

        return stats

    def run_phase_2_scaling(self):
        """
        Phase 2: Scaling (100 stores)
        - 75 meeting transcripts total (60 additional)
        - 200 Teams messages total (150 additional)
        - 6 channels
        """
        print("\n" + "="*60)
        print("PHASE 2: SCALING DATA GENERATION")
        print("="*60 + "\n")
        print("This would generate 60 additional meetings and 150 Teams messages...")
        print("(Implementation similar to Phase 1 with larger scale)")
        print("\nTo implement: Extend Phase 1 logic with more stores and variation.")

    def run_phase_3_production(self):
        """
        Phase 3: Production (Full dataset)
        - 250 meeting transcripts total
        - 300 Teams messages total
        - 12-month temporal span
        """
        print("\n" + "="*60)
        print("PHASE 3: PRODUCTION DATA GENERATION")
        print("="*60 + "\n")
        print("This would generate full production dataset...")
        print("(Implementation with quarterly events, full temporal progression)")
        print("\nTo implement: Extend Phase 2 with quarterly patterns and full coverage.")

    def validate_generated_data(self):
        """Run validation on generated data."""
        print("\n" + "="*60)
        print("VALIDATION")
        print("="*60 + "\n")

        from validate_data_quality import DataValidator

        validator = DataValidator()

        print("[1/4] Validating schema compliance...")
        schema_results = validator.validate_all_schemas()

        print("[2/4] Validating cross-reference integrity...")
        xref_results = validator.validate_cross_references()

        print("[3/4] Validating temporal coherence...")
        temporal_results = validator.validate_temporal_coherence()

        print("[4/4] Validating coverage...")
        coverage_results = validator.validate_coverage()

        # Print summary
        print("\nValidation Summary:")
        print(f"  Schema Compliance: {schema_results.get('compliance_rate', 0)*100:.1f}%")
        print(f"  Cross-Reference Integrity: {xref_results.get('integrity_rate', 0)*100:.1f}%")
        print(f"  Temporal Coherence: {temporal_results.get('coherence_rate', 0)*100:.1f}%")
        print(f"  Coverage: {coverage_results.get('stores_with_2plus_conversations', 0)} stores")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Run data generation orchestration')
    parser.add_argument('--phase', type=int, choices=[1, 2, 3], required=True,
                        help='Generation phase (1=MVP, 2=Scaling, 3=Production)')
    parser.add_argument('--validate', action='store_true',
                        help='Run validation after generation')

    args = parser.parse_args()

    orchestrator = DataGenerationOrchestrator()

    # Run selected phase
    if args.phase == 1:
        stats = orchestrator.run_phase_1_mvp()
    elif args.phase == 2:
        stats = orchestrator.run_phase_2_scaling()
    elif args.phase == 3:
        stats = orchestrator.run_phase_3_production()

    # Run validation if requested
    if args.validate:
        orchestrator.validate_generated_data()


if __name__ == '__main__':
    main()
