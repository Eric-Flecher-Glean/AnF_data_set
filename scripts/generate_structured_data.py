#!/usr/bin/env python3
"""
Generate Structured Data (Folders 01-06)

Creates foundational structured data that supports the conversational dataset
and enables budget planning artifact generation.
"""

import os
import json
import csv
from datetime import datetime

# Create output directories
base_dir = 'output'
folders = [
    '01_Build_Templates',
    '02_Constraints',
    '03_Historical_Projects',
    '04_Regional_Modifiers',
    '05_Cost_Models',
    '06_Vendor_Data'
]

for folder in folders:
    os.makedirs(f'{base_dir}/{folder}', exist_ok=True)

print("Creating structured data files...")

# ============================================================================
# 01_BUILD_TEMPLATES
# ============================================================================
print("\n[1/6] Creating build templates...")

# Store type configurations
store_types = {
    "store_types": [
        {
            "type_id": "urban_flagship",
            "name": "Urban Flagship",
            "typical_sqft": 5000,
            "sqft_range": [4500, 6000],
            "target_markets": ["New York", "Chicago", "San Francisco", "Boston"],
            "typical_use_cases": ["High-traffic urban locations", "Brand showcases", "Market entry"],
            "key_features": [
                "Premium finishes and fixtures",
                "Advanced technology package",
                "Enhanced lighting design",
                "Digital experience zones"
            ],
            "cost_drivers": ["Premium materials", "Urban labor rates", "Complex permitting"]
        },
        {
            "type_id": "suburban_standard",
            "name": "Suburban Standard",
            "typical_sqft": 3500,
            "sqft_range": [3000, 4000],
            "target_markets": ["Columbus", "Cincinnati", "Indianapolis", "Louisville"],
            "typical_use_cases": ["Mall locations", "Shopping centers", "Standard rollout"],
            "key_features": [
                "Standard fixtures and finishes",
                "Base technology package",
                "Standard lighting",
                "Traditional layout"
            ],
            "cost_drivers": ["Material costs", "Standard labor", "Landlord requirements"]
        },
        {
            "type_id": "express_compact",
            "name": "Express/Compact",
            "typical_sqft": 2000,
            "sqft_range": [1500, 2500],
            "target_markets": ["Secondary markets", "Airport locations", "Outlet centers"],
            "typical_use_cases": ["Quick market entry", "Test markets", "Cost-optimized"],
            "key_features": [
                "Essential fixtures only",
                "Minimal technology",
                "Cost-effective finishes",
                "Simplified layout"
            ],
            "cost_drivers": ["Efficiency", "Material minimization", "Fast construction"]
        },
        {
            "type_id": "remodel_refresh",
            "name": "Remodel/Refresh",
            "typical_sqft": 3500,
            "sqft_range": [2000, 5000],
            "target_markets": ["All markets"],
            "typical_use_cases": ["Store updates", "Brand refresh", "Technology upgrade"],
            "key_features": [
                "Selective category updates",
                "Existing infrastructure reuse",
                "Phased construction",
                "Minimal disruption"
            ],
            "cost_drivers": ["Demolition", "Working around existing", "Phasing complexity"]
        },
        {
            "type_id": "prototype_innovation",
            "name": "Prototype/Innovation",
            "typical_sqft": 4000,
            "sqft_range": [3500, 5000],
            "target_markets": ["Select test markets"],
            "typical_use_cases": ["New concept testing", "Format innovation", "Future rollout development"],
            "key_features": [
                "Custom fixtures",
                "Advanced technology",
                "Experimental layouts",
                "Premium everything"
            ],
            "cost_drivers": ["Custom design", "R&D costs", "Trial and error", "Documentation"]
        }
    ]
}

with open(f'{base_dir}/01_Build_Templates/store_types.json', 'w') as f:
    json.dump(store_types, f, indent=2)

# Base configuration template
base_config = {
    "template_id": "base_template_v2.3",
    "version": "2.3",
    "effective_date": "2025-03-01",
    "categories": [
        {
            "category": "Construction",
            "subcategories": [
                "Demolition",
                "Structural",
                "Framing",
                "Drywall",
                "Flooring",
                "Ceiling",
                "Paint"
            ]
        },
        {
            "category": "Electrical",
            "subcategories": [
                "Electrical panel (400A standard)",
                "LED lighting system",
                "Outlets and switches",
                "Emergency lighting",
                "Technology wiring"
            ]
        },
        {
            "category": "HVAC",
            "subcategories": [
                "Commercial HVAC unit",
                "Ductwork",
                "Controls",
                "Maintenance"
            ]
        },
        {
            "category": "Plumbing",
            "subcategories": [
                "Fixtures",
                "Water lines",
                "Drainage",
                "Backflow prevention"
            ]
        },
        {
            "category": "Fixtures",
            "subcategories": [
                "Display fixtures",
                "Shelving",
                "Mannequins",
                "Signage",
                "Checkout counter"
            ]
        },
        {
            "category": "Technology",
            "subcategories": [
                "POS systems",
                "Security cameras",
                "WiFi infrastructure",
                "Digital displays"
            ]
        },
        {
            "category": "Soft Costs",
            "subcategories": [
                "Design fees",
                "Permits",
                "Insurance",
                "Project management",
                "Contingency (10%)"
            ]
        }
    ],
    "specifications": {
        "electrical_panel": "400A (updated from 200A as of v2.3)",
        "lighting": "LED throughout",
        "flooring": "Luxury vinyl tile (LVT)",
        "ceiling": "9ft minimum height",
        "hvac": "Variable refrigerant flow (VRF)"
    }
}

with open(f'{base_dir}/01_Build_Templates/base_template.json', 'w') as f:
    json.dump(base_config, f, indent=2)

print(f"  ✓ Created 2 build template files")

# ============================================================================
# 02_CONSTRAINTS
# ============================================================================
print("\n[2/6] Creating constraint definitions...")

constraints = {
    "constraint_types": [
        {
            "type": "landlord",
            "description": "Requirements imposed by property owner",
            "examples": [
                {
                    "constraint": "Approved vendor list only",
                    "impact": "May increase costs 5-15% if preferred vendors not approved",
                    "mitigation": "Negotiate vendor approval, use approved subs, price accordingly"
                },
                {
                    "constraint": "No structural modifications",
                    "impact": "Limits layout options, may require creative workarounds",
                    "mitigation": "Design within existing footprint, use non-structural solutions"
                },
                {
                    "constraint": "After-hours work required",
                    "impact": "Labor rates increase 20-30% for night/weekend shifts",
                    "mitigation": "Optimize work scheduling, frontload daytime tasks"
                },
                {
                    "constraint": "Noise restrictions during mall hours",
                    "impact": "Extends timeline by 15-25%, phasing complexity",
                    "mitigation": "Schedule noisy work appropriately, sound dampening"
                }
            ]
        },
        {
            "type": "budget",
            "description": "Financial limitations on project",
            "examples": [
                {
                    "constraint": "Budget cap below market rate",
                    "impact": "Requires value engineering, material substitutions",
                    "mitigation": "Phased approach, specification downgrades, vendor negotiation"
                },
                {
                    "constraint": "Cash flow limitations",
                    "impact": "Payment schedule affects vendor pricing",
                    "mitigation": "Negotiate extended terms, progress payments"
                }
            ]
        },
        {
            "type": "timeline",
            "description": "Schedule constraints and deadlines",
            "examples": [
                {
                    "constraint": "Accelerated schedule (8 weeks vs. 12 weeks)",
                    "impact": "Labor premium 15%, material expedite fees, overlap inefficiencies",
                    "mitigation": "Parallel work streams, premium scheduling, night shifts"
                },
                {
                    "constraint": "Holiday deadline",
                    "impact": "Premium labor during holiday season, reduced productivity",
                    "mitigation": "Buffer time, incentive payments, backup resources"
                }
            ]
        },
        {
            "type": "regional",
            "description": "Local market conditions and requirements",
            "examples": [
                {
                    "constraint": "Union labor required",
                    "impact": "Labor rates 8-12% higher than non-union markets",
                    "mitigation": "Build into baseline, negotiate scope efficiently"
                },
                {
                    "constraint": "Complex permitting jurisdiction",
                    "impact": "Extended timeline (4-6 weeks), additional fees",
                    "mitigation": "Early permit application, expediter services"
                },
                {
                    "constraint": "Limited local vendor pool",
                    "impact": "Reduced competition, potentially higher pricing",
                    "mitigation": "Develop regional vendor relationships, incentivize new entrants"
                }
            ]
        },
        {
            "type": "operational",
            "description": "Store operation requirements",
            "examples": [
                {
                    "constraint": "Store must remain open during remodel",
                    "impact": "Phasing required, productivity loss 20-30%",
                    "mitigation": "Night work, temporary barriers, dust control"
                },
                {
                    "constraint": "Minimize closure days",
                    "impact": "Compressed schedule, premium labor costs",
                    "mitigation": "Prefabrication, parallel work, extended hours"
                }
            ]
        }
    ]
}

with open(f'{base_dir}/02_Constraints/constraint_catalog.json', 'w') as f:
    json.dump(constraints, f, indent=2)

print(f"  ✓ Created constraint catalog")

# ============================================================================
# 03_HISTORICAL_PROJECTS
# ============================================================================
print("\n[3/6] Creating historical projects data...")

# Generate historical project data
historical_projects = []

# Define store type distribution
store_type_examples = [
    ("suburban_standard", 3500, 80),  # Most common
    ("urban_flagship", 5000, 20),
    ("express_compact", 2000, 30),
    ("remodel_refresh", 3500, 25),
    ("prototype_innovation", 4000, 5)
]

project_id = 50  # Start from Store-50

for store_type, sqft, count in store_type_examples:
    for i in range(count):
        store_id = f"Store-{project_id}"

        # Base costs per sqft by store type
        base_cost_psf = {
            "suburban_standard": 185,
            "urban_flagship": 285,
            "express_compact": 145,
            "remodel_refresh": 95,
            "prototype_innovation": 325
        }

        # Add variation (+/- 15%)
        import random
        random.seed(project_id)
        variation = random.uniform(0.85, 1.15)

        total_cost = int(base_cost_psf[store_type] * sqft * variation)

        # Break down by category (percentages)
        construction_pct = 0.35
        electrical_pct = 0.12
        hvac_pct = 0.08
        plumbing_pct = 0.05
        fixtures_pct = 0.25
        technology_pct = 0.08
        soft_costs_pct = 0.07

        project = {
            "store_id": store_id,
            "store_type": store_type,
            "square_footage": sqft,
            "market": random.choice(["Columbus", "Cincinnati", "Cleveland", "Indianapolis", "Louisville", "Pittsburgh", "Detroit"]),
            "completion_date": f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
            "total_cost": total_cost,
            "cost_per_sqft": round(total_cost / sqft, 2),
            "categories": {
                "construction": int(total_cost * construction_pct),
                "electrical": int(total_cost * electrical_pct),
                "hvac": int(total_cost * hvac_pct),
                "plumbing": int(total_cost * plumbing_pct),
                "fixtures": int(total_cost * fixtures_pct),
                "technology": int(total_cost * technology_pct),
                "soft_costs": int(total_cost * soft_costs_pct)
            },
            "timeline_days": random.randint(60, 120),
            "variance_from_budget": random.randint(-5, 10),  # percentage
            "lessons_learned": [
                "Completed on schedule" if random.random() > 0.3 else "Delayed by permit issues",
                "Vendor performance good" if random.random() > 0.2 else "Vendor substitution required"
            ]
        }

        historical_projects.append(project)
        project_id += 1

# Save as CSV for easy analysis
with open(f'{base_dir}/03_Historical_Projects/historical_projects.csv', 'w', newline='') as f:
    fieldnames = ['store_id', 'store_type', 'square_footage', 'market', 'completion_date',
                  'total_cost', 'cost_per_sqft', 'construction', 'electrical', 'hvac', 'plumbing',
                  'fixtures', 'technology', 'soft_costs', 'timeline_days', 'variance_from_budget']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for project in historical_projects:
        row = {
            'store_id': project['store_id'],
            'store_type': project['store_type'],
            'square_footage': project['square_footage'],
            'market': project['market'],
            'completion_date': project['completion_date'],
            'total_cost': project['total_cost'],
            'cost_per_sqft': project['cost_per_sqft'],
            'construction': project['categories']['construction'],
            'electrical': project['categories']['electrical'],
            'hvac': project['categories']['hvac'],
            'plumbing': project['categories']['plumbing'],
            'fixtures': project['categories']['fixtures'],
            'technology': project['categories']['technology'],
            'soft_costs': project['categories']['soft_costs'],
            'timeline_days': project['timeline_days'],
            'variance_from_budget': project['variance_from_budget']
        }
        writer.writerow(row)

# Also save as JSON
with open(f'{base_dir}/03_Historical_Projects/historical_projects.json', 'w') as f:
    json.dump({"projects": historical_projects}, f, indent=2)

print(f"  ✓ Created {len(historical_projects)} historical project records")

# ============================================================================
# 04_REGIONAL_MODIFIERS
# ============================================================================
print("\n[4/6] Creating regional modifier data...")

regional_modifiers = {
    "markets": [
        {
            "market": "Columbus",
            "state": "OH",
            "tier": "secondary",
            "modifiers": {
                "construction": 1.00,  # Baseline
                "electrical": 1.03,
                "hvac": 1.02,
                "plumbing": 1.01,
                "fixtures": 1.00,
                "technology": 1.00,
                "soft_costs": 1.02
            },
            "notes": "Baseline market, good vendor competition"
        },
        {
            "market": "Cincinnati",
            "state": "OH",
            "tier": "secondary",
            "modifiers": {
                "construction": 1.05,
                "electrical": 1.08,  # Union market
                "hvac": 1.04,
                "plumbing": 1.03,
                "fixtures": 1.00,
                "technology": 1.00,
                "soft_costs": 1.03
            },
            "notes": "Union labor requirements increase electrical costs"
        },
        {
            "market": "Cleveland",
            "state": "OH",
            "tier": "secondary",
            "modifiers": {
                "construction": 1.04,
                "electrical": 1.06,
                "hvac": 1.03,
                "plumbing": 1.02,
                "fixtures": 1.00,
                "technology": 1.00,
                "soft_costs": 1.03
            },
            "notes": "Moderate cost market"
        },
        {
            "market": "Pittsburgh",
            "state": "PA",
            "tier": "secondary",
            "modifiers": {
                "construction": 1.07,
                "electrical": 1.09,
                "hvac": 1.05,
                "plumbing": 1.04,
                "fixtures": 1.02,
                "technology": 1.00,
                "soft_costs": 1.05
            },
            "notes": "Higher labor costs, union presence"
        },
        {
            "market": "Indianapolis",
            "state": "IN",
            "tier": "secondary",
            "modifiers": {
                "construction": 0.97,
                "electrical": 0.99,
                "hvac": 0.98,
                "plumbing": 0.98,
                "fixtures": 1.00,
                "technology": 1.00,
                "soft_costs": 1.00
            },
            "notes": "Cost-effective market, good vendor availability"
        },
        {
            "market": "Louisville",
            "state": "KY",
            "tier": "tertiary",
            "modifiers": {
                "construction": 0.94,
                "electrical": 0.96,
                "hvac": 0.95,
                "plumbing": 0.95,
                "fixtures": 1.00,
                "technology": 1.00,
                "soft_costs": 0.98
            },
            "notes": "Lower cost market"
        },
        {
            "market": "Detroit",
            "state": "MI",
            "tier": "secondary",
            "modifiers": {
                "construction": 1.08,
                "electrical": 1.12,
                "hvac": 1.06,
                "plumbing": 1.05,
                "fixtures": 1.00,
                "technology": 1.00,
                "soft_costs": 1.06
            },
            "notes": "High union presence, regulatory complexity"
        },
        {
            "market": "Chicago",
            "state": "IL",
            "tier": "primary",
            "modifiers": {
                "construction": 1.25,
                "electrical": 1.35,
                "hvac": 1.22,
                "plumbing": 1.20,
                "fixtures": 1.05,
                "technology": 1.00,
                "soft_costs": 1.15
            },
            "notes": "Major urban market, high labor costs, complex permitting"
        },
        {
            "market": "New York",
            "state": "NY",
            "tier": "primary",
            "modifiers": {
                "construction": 1.45,
                "electrical": 1.55,
                "hvac": 1.40,
                "plumbing": 1.38,
                "fixtures": 1.10,
                "technology": 1.05,
                "soft_costs": 1.25
            },
            "notes": "Highest cost market, union mandates, complex logistics"
        },
        {
            "market": "San Francisco",
            "state": "CA",
            "tier": "primary",
            "modifiers": {
                "construction": 1.50,
                "electrical": 1.52,
                "hvac": 1.45,
                "plumbing": 1.42,
                "fixtures": 1.08,
                "technology": 1.03,
                "soft_costs": 1.28
            },
            "notes": "Extreme high cost, seismic requirements, permit complexity"
        }
    ]
}

with open(f'{base_dir}/04_Regional_Modifiers/regional_modifiers.json', 'w') as f:
    json.dump(regional_modifiers, f, indent=2)

# CSV version
with open(f'{base_dir}/04_Regional_Modifiers/regional_modifiers.csv', 'w', newline='') as f:
    fieldnames = ['market', 'state', 'tier', 'construction', 'electrical', 'hvac',
                  'plumbing', 'fixtures', 'technology', 'soft_costs', 'notes']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for market in regional_modifiers['markets']:
        row = {
            'market': market['market'],
            'state': market['state'],
            'tier': market['tier'],
            **market['modifiers'],
            'notes': market['notes']
        }
        writer.writerow(row)

print(f"  ✓ Created regional modifiers for {len(regional_modifiers['markets'])} markets")

# ============================================================================
# 05_COST_MODELS
# ============================================================================
print("\n[5/6] Creating cost models...")

cost_models = {
    "model_version": "2.3",
    "last_updated": "2025-03-01",
    "base_costs": {
        "suburban_standard_3500sqft": {
            "store_type": "suburban_standard",
            "square_footage": 3500,
            "total_base_cost": 647500,
            "cost_per_sqft": 185,
            "breakdown": {
                "construction": {
                    "total": 226625,
                    "per_sqft": 64.75,
                    "line_items": [
                        {"item": "Demolition", "unit": "sqft", "quantity": 3500, "unit_cost": 5.50, "total": 19250},
                        {"item": "Framing", "unit": "sqft", "quantity": 3500, "unit_cost": 12.00, "total": 42000},
                        {"item": "Drywall", "unit": "sqft", "quantity": 7000, "unit_cost": 8.50, "total": 59500},
                        {"item": "Flooring (LVT)", "unit": "sqft", "quantity": 3500, "unit_cost": 18.00, "total": 63000},
                        {"item": "Ceiling", "unit": "sqft", "quantity": 3500, "unit_cost": 7.50, "total": 26250},
                        {"item": "Paint", "unit": "sqft", "quantity": 7000, "unit_cost": 2.25, "total": 15750}
                    ]
                },
                "electrical": {
                    "total": 77700,
                    "per_sqft": 22.20,
                    "line_items": [
                        {"item": "400A electrical panel", "unit": "each", "quantity": 1, "unit_cost": 8500, "total": 8500},
                        {"item": "LED lighting fixtures", "unit": "each", "quantity": 65, "unit_cost": 412, "total": 26780},
                        {"item": "Outlets and switches", "unit": "each", "quantity": 85, "unit_cost": 125, "total": 10625},
                        {"item": "Emergency lighting", "unit": "each", "quantity": 12, "unit_cost": 385, "total": 4620},
                        {"item": "Electrical rough-in", "unit": "sqft", "quantity": 3500, "unit_cost": 7.50, "total": 26250}
                    ]
                },
                "hvac": {
                    "total": 51800,
                    "per_sqft": 14.80,
                    "line_items": [
                        {"item": "Commercial HVAC unit (VRF)", "unit": "each", "quantity": 1, "unit_cost": 16500, "total": 16500},
                        {"item": "Ductwork", "unit": "sqft", "quantity": 3500, "unit_cost": 8.50, "total": 29750},
                        {"item": "HVAC controls", "unit": "system", "quantity": 1, "unit_cost": 3250, "total": 3250},
                        {"item": "Installation labor", "unit": "system", "quantity": 1, "unit_cost": 2300, "total": 2300}
                    ]
                },
                "plumbing": {
                    "total": 32375,
                    "per_sqft": 9.25,
                    "line_items": [
                        {"item": "Bathroom fixtures", "unit": "set", "quantity": 2, "unit_cost": 2850, "total": 5700},
                        {"item": "Water heater", "unit": "each", "quantity": 1, "unit_cost": 1250, "total": 1250},
                        {"item": "Water lines", "unit": "lf", "quantity": 280, "unit_cost": 22, "total": 6160},
                        {"item": "Drainage", "unit": "lf", "quantity": 280, "unit_cost": 28, "total": 7840},
                        {"item": "Plumbing labor", "unit": "sqft", "quantity": 3500, "unit_cost": 3.25, "total": 11375}
                    ]
                },
                "fixtures": {
                    "total": 161875,
                    "per_sqft": 46.25,
                    "line_items": [
                        {"item": "Wall display fixtures", "unit": "lf", "quantity": 320, "unit_cost": 185, "total": 59200},
                        {"item": "Floor fixtures", "unit": "each", "quantity": 45, "unit_cost": 725, "total": 32625},
                        {"item": "Mannequins", "unit": "each", "quantity": 18, "unit_cost": 385, "total": 6930},
                        {"item": "Signage package", "unit": "package", "quantity": 1, "unit_cost": 12500, "total": 12500},
                        {"item": "Checkout counter", "unit": "lf", "quantity": 24, "unit_cost": 425, "total": 10200},
                        {"item": "Dressing rooms", "unit": "each", "quantity": 8, "unit_cost": 1850, "total": 14800},
                        {"item": "Mirrors and accessories", "unit": "package", "quantity": 1, "unit_cost": 8500, "total": 8500}
                    ]
                },
                "technology": {
                    "total": 51800,
                    "per_sqft": 14.80,
                    "line_items": [
                        {"item": "POS system (3 terminals)", "unit": "system", "quantity": 1, "unit_cost": 12500, "total": 12500},
                        {"item": "Security cameras", "unit": "each", "quantity": 16, "unit_cost": 875, "total": 14000},
                        {"item": "WiFi infrastructure", "unit": "system", "quantity": 1, "unit_cost": 4250, "total": 4250},
                        {"item": "Digital displays", "unit": "each", "quantity": 4, "unit_cost": 2150, "total": 8600},
                        {"item": "Sound system", "unit": "system", "quantity": 1, "unit_cost": 3850, "total": 3850},
                        {"item": "Technology wiring", "unit": "sqft", "quantity": 3500, "unit_cost": 2.50, "total": 8750}
                    ]
                },
                "soft_costs": {
                    "total": 45325,
                    "per_sqft": 12.95,
                    "line_items": [
                        {"item": "Architectural design", "unit": "project", "quantity": 1, "unit_cost": 15000, "total": 15000},
                        {"item": "Engineering", "unit": "project", "quantity": 1, "unit_cost": 8500, "total": 8500},
                        {"item": "Permits and fees", "unit": "project", "quantity": 1, "unit_cost": 6250, "total": 6250},
                        {"item": "Project management", "unit": "project", "quantity": 1, "unit_cost": 8500, "total": 8500},
                        {"item": "Contingency (10%)", "unit": "percent", "quantity": 1, "unit_cost": 7075, "total": 7075}
                    ]
                }
            }
        }
    },
    "formulas": {
        "regional_adjustment": "base_cost * regional_modifier",
        "timeline_premium": "base_cost * (1 + premium_rate) where premium_rate = 0.15 for accelerated",
        "total_cost": "sum(categories) * regional_modifier * timeline_factor"
    }
}

with open(f'{base_dir}/05_Cost_Models/cost_model_suburban_standard.json', 'w') as f:
    json.dump(cost_models, f, indent=2)

print(f"  ✓ Created detailed cost model")

# ============================================================================
# 06_VENDOR_DATA
# ============================================================================
print("\n[6/6] Creating vendor pricing data...")

vendor_data = {
    "vendors": [
        {
            "vendor_id": "V001",
            "name": "BuildRight Construction",
            "category": "General Contractor",
            "markets": ["Columbus", "Cincinnati", "Cleveland", "Indianapolis"],
            "specialties": ["Full store builds", "Remodels", "Project management"],
            "pricing": {
                "typical_margin": "12-15%",
                "payment_terms": "Progress payments: 30% deposit, 40% at roughin, 30% at completion",
                "typical_lead_time_days": 90
            },
            "performance": {
                "projects_completed": 85,
                "on_time_rate": 0.87,
                "on_budget_rate": 0.82,
                "quality_rating": 4.3
            }
        },
        {
            "vendor_id": "V002",
            "name": "CoolAir Systems",
            "category": "HVAC",
            "markets": ["All OH, IN, KY markets"],
            "specialties": ["Commercial HVAC", "VRF systems", "Controls"],
            "pricing": {
                "commercial_unit_3500sqft": 16500,
                "volume_discount_5_units": "7%",
                "volume_discount_10_units": "12%",
                "payment_terms": "50% deposit, 50% on delivery",
                "typical_lead_time_weeks": 10
            },
            "performance": {
                "projects_completed": 120,
                "on_time_rate": 0.75,
                "on_budget_rate": 0.88,
                "quality_rating": 4.5
            }
        },
        {
            "vendor_id": "V003",
            "name": "TempMaster",
            "category": "HVAC",
            "markets": ["Columbus", "Cincinnati"],
            "specialties": ["Backup vendor", "Competitive pricing"],
            "pricing": {
                "commercial_unit_3500sqft": 15000,
                "typical_discount": "9% under primary vendor",
                "payment_terms": "Standard net 30",
                "typical_lead_time_weeks": 8
            },
            "performance": {
                "projects_completed": 35,
                "on_time_rate": 0.91,
                "on_budget_rate": 0.95,
                "quality_rating": 4.4
            },
            "notes": "Emerging preferred vendor based on Store-112 performance"
        },
        {
            "vendor_id": "V004",
            "name": "PowerTech Solutions",
            "category": "Electrical",
            "markets": ["All Midwest"],
            "specialties": ["Commercial electrical", "LED lighting", "Technology infrastructure"],
            "pricing": {
                "panel_400A": 8500,
                "led_fixture": 412,
                "hourly_rate": 95,
                "typical_lead_time_weeks": 6
            },
            "performance": {
                "projects_completed": 95,
                "on_time_rate": 0.89,
                "on_budget_rate": 0.84,
                "quality_rating": 4.6
            }
        },
        {
            "vendor_id": "V005",
            "name": "FlowMaster Plumbing",
            "category": "Plumbing",
            "markets": ["OH, IN, PA"],
            "specialties": ["Commercial plumbing", "Fixture installation"],
            "pricing": {
                "hourly_rate": 85,
                "fixture_set": 2850,
                "typical_lead_time_weeks": 4
            },
            "performance": {
                "projects_completed": 78,
                "on_time_rate": 0.92,
                "on_budget_rate": 0.90,
                "quality_rating": 4.4
            }
        },
        {
            "vendor_id": "V006",
            "name": "RetailFixtures Pro",
            "category": "Fixtures",
            "markets": ["National"],
            "specialties": ["Custom retail fixtures", "Display systems", "Millwork"],
            "pricing": {
                "wall_system_per_lf": 185,
                "floor_fixture": 725,
                "mannequin": 385,
                "typical_lead_time_weeks": 8
            },
            "performance": {
                "projects_completed": 145,
                "on_time_rate": 0.83,
                "on_budget_rate": 0.87,
                "quality_rating": 4.7
            }
        },
        {
            "vendor_id": "V007",
            "name": "SmartStore Tech",
            "category": "Technology",
            "markets": ["National"],
            "specialties": ["POS systems", "Security", "Digital displays"],
            "pricing": {
                "pos_3_terminal_system": 12500,
                "security_camera": 875,
                "digital_display": 2150,
                "typical_lead_time_weeks": 6
            },
            "performance": {
                "projects_completed": 110,
                "on_time_rate": 0.88,
                "on_budget_rate": 0.91,
                "quality_rating": 4.5
            }
        },
        {
            "vendor_id": "V008",
            "name": "BuildSmart Design",
            "category": "Design/Architecture",
            "markets": ["National"],
            "specialties": ["Retail design", "Store planning", "Engineering"],
            "pricing": {
                "design_fee_3500sqft": 15000,
                "engineering_fee": 8500,
                "typical_lead_time_weeks": 4
            },
            "performance": {
                "projects_completed": 125,
                "on_time_rate": 0.90,
                "on_budget_rate": 0.93,
                "quality_rating": 4.8
            }
        }
    ]
}

with open(f'{base_dir}/06_Vendor_Data/vendor_catalog.json', 'w') as f:
    json.dump(vendor_data, f, indent=2)

# CSV version
with open(f'{base_dir}/06_Vendor_Data/vendor_pricing.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Vendor', 'Category', 'Item', 'Price', 'Unit', 'Lead Time', 'Notes'])

    pricing_rows = [
        ['CoolAir Systems', 'HVAC', 'Commercial unit 3500sqft', 16500, 'each', '10 weeks', 'Volume discounts available'],
        ['TempMaster', 'HVAC', 'Commercial unit 3500sqft', 15000, 'each', '8 weeks', '9% under primary vendor'],
        ['PowerTech Solutions', 'Electrical', '400A panel', 8500, 'each', '6 weeks', ''],
        ['PowerTech Solutions', 'Electrical', 'LED fixture', 412, 'each', '6 weeks', ''],
        ['FlowMaster Plumbing', 'Plumbing', 'Fixture set', 2850, 'set', '4 weeks', ''],
        ['RetailFixtures Pro', 'Fixtures', 'Wall system', 185, 'lf', '8 weeks', ''],
        ['RetailFixtures Pro', 'Fixtures', 'Floor fixture', 725, 'each', '8 weeks', ''],
        ['RetailFixtures Pro', 'Fixtures', 'Mannequin', 385, 'each', '8 weeks', ''],
        ['SmartStore Tech', 'Technology', 'POS system (3 terminals)', 12500, 'system', '6 weeks', ''],
        ['SmartStore Tech', 'Technology', 'Security camera', 875, 'each', '6 weeks', ''],
        ['SmartStore Tech', 'Technology', 'Digital display', 2150, 'each', '6 weeks', ''],
        ['BuildSmart Design', 'Design', 'Design fee 3500sqft', 15000, 'project', '4 weeks', ''],
        ['BuildSmart Design', 'Design', 'Engineering fee', 8500, 'project', '4 weeks', '']
    ]

    writer.writerows(pricing_rows)

print(f"  ✓ Created vendor catalog with {len(vendor_data['vendors'])} vendors")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*60)
print("STRUCTURED DATA GENERATION COMPLETE")
print("="*60)
print(f"\n01_Build_Templates: 2 files (store types, base template)")
print(f"02_Constraints: 1 file (constraint catalog)")
print(f"03_Historical_Projects: 2 files ({len(historical_projects)} projects)")
print(f"04_Regional_Modifiers: 2 files ({len(regional_modifiers['markets'])} markets)")
print(f"05_Cost_Models: 1 file (detailed cost model)")
print(f"06_Vendor_Data: 2 files ({len(vendor_data['vendors'])} vendors)")
print(f"\nReady for budget artifact generation!")
print("="*60 + "\n")
