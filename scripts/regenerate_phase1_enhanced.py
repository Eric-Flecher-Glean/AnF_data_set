#!/usr/bin/env python3
"""
Regenerate Phase 1 with Enhanced Dialogue

Replaces original Phase 1 meetings with enhanced versions.
Teams conversations remain unchanged (already excellent).
"""

import os
import shutil
from datetime import datetime, timedelta
from generate_meeting_transcripts_v2 import EnhancedMeetingGenerator


def backup_original_data():
    """Backup original Phase 1 data."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = f'output/07_Conversations_backup_{timestamp}'

    if os.path.exists('output/07_Conversations/meeting_transcripts'):
        shutil.copytree(
            'output/07_Conversations/meeting_transcripts',
            f'{backup_dir}/meeting_transcripts'
        )
        print(f"✓ Backed up original meetings to {backup_dir}")

    return backup_dir


def regenerate_all_meetings():
    """Regenerate all Phase 1 meetings with enhanced dialogue."""
    generator = EnhancedMeetingGenerator()

    stats = {
        'generated': 0,
        'errors': []
    }

    print("\n" + "="*60)
    print("PHASE 1 ENHANCED REGENERATION")
    print("="*60 + "\n")

    # Generate 3 site visit debriefs
    print("[1/5] Generating site visit debriefs...")
    for i, store_id in enumerate(['Store-201', 'Store-202', 'Store-203']):
        try:
            config = {
                'meeting_type': 'site_visit_debrief',
                'store_id': store_id,
                'date': (datetime.now() - timedelta(days=30-i*5)).strftime('%Y-%m-%d'),
                'participants': 'Sarah Chen|Tom Wilson|Mike Rodriguez'
            }
            generator.generate_transcript('site_visit_debrief', config)
            stats['generated'] += 1
        except Exception as e:
            stats['errors'].append(f"Site visit {store_id}: {str(e)}")

    # Generate 3 vendor negotiations
    print("\n[2/5] Generating vendor negotiations...")
    for i in range(3):
        try:
            config = {
                'meeting_type': 'vendor_negotiation',
                'topic': f'hvac-vendors-q{i+1}',
                'date': (datetime.now() - timedelta(days=60-i*10)).strftime('%Y-%m-%d'),
                'participants': 'Jennifer Liu|Tom Wilson'
            }
            generator.generate_transcript('vendor_negotiation', config)
            stats['generated'] += 1
        except Exception as e:
            stats['errors'].append(f"Vendor negotiation Q{i+1}: {str(e)}")

    # Generate 5 lessons learned
    print("\n[3/5] Generating lessons learned meetings...")
    for i, store_id in enumerate([f'Store-{189+i}' for i in range(5)]):
        try:
            config = {
                'meeting_type': 'lessons_learned',
                'store_id': store_id,
                'date': (datetime.now() - timedelta(days=90-i*7)).strftime('%Y-%m-%d'),
                'participants': 'Sarah Chen|Tom Wilson|David Park|Lisa Thompson'
            }
            generator.generate_transcript('lessons_learned', config)
            stats['generated'] += 1
        except Exception as e:
            stats['errors'].append(f"Lessons learned {store_id}: {str(e)}")

    # Generate 2 design reviews
    print("\n[4/5] Generating design reviews...")
    for i, version in enumerate(['v2.3', 'v2.4']):
        try:
            config = {
                'meeting_type': 'design_review',
                'topic': f'template-{version}',
                'template_version': version,
                'date': (datetime.now() - timedelta(days=120-i*90)).strftime('%Y-%m-%d'),
                'participants': 'Carlos Martinez|Angela Wu|David Park'
            }
            generator.generate_transcript('design_review', config)
            stats['generated'] += 1
        except Exception as e:
            stats['errors'].append(f"Design review {version}: {str(e)}")

    # Generate 2 weekly syncs
    print("\n[5/5] Generating weekly dev syncs...")
    for i in range(2):
        try:
            config = {
                'meeting_type': 'weekly_dev_sync',
                'topic': 'Columbus-Market',
                'date': (datetime.now() - timedelta(days=14-i*7)).strftime('%Y-%m-%d'),
                'participants': 'Sarah Chen|Jennifer Liu'
            }
            generator.generate_transcript('weekly_dev_sync', config)
            stats['generated'] += 1
        except Exception as e:
            stats['errors'].append(f"Weekly sync {i+1}: {str(e)}")

    return stats


def main():
    """Main entry point."""
    print("\n" + "="*60)
    print("PHASE 1 ENHANCED REGENERATION")
    print("="*60)

    # Backup original
    print("\n[Step 1] Backing up original meetings...")
    backup_dir = backup_original_data()

    # Regenerate
    print("\n[Step 2] Regenerating with enhanced dialogue...")
    stats = regenerate_all_meetings()

    # Summary
    print("\n" + "="*60)
    print("REGENERATION COMPLETE")
    print("="*60)
    print(f"✓ Meetings generated: {stats['generated']}")

    if stats['errors']:
        print(f"\n⚠ Errors encountered: {len(stats['errors'])}")
        for error in stats['errors']:
            print(f"  - {error}")
    else:
        print("✓ No errors")

    print(f"\n✓ Original meetings backed up to: {backup_dir}")
    print("✓ Teams conversations unchanged (already excellent quality)")
    print("\n" + "="*60)


if __name__ == '__main__':
    main()
