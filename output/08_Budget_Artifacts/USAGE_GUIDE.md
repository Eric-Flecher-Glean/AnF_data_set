# Budget Artifacts Usage Guide

## Overview

This folder contains Excel-based budget planning tools designed to enable AI agents and human analysts to rapidly generate accurate store build cost estimates based on historical project data, regional variations, and proven build strategies.

**Total Artifacts**: 11 Excel files across 4 categories

---

## Directory Structure

```
08_Budget_Artifacts/
├── budget_plans/               (5 files) - Complete budget examples by store type
├── templates/                  (2 files) - Reusable configuration templates
├── strategy_worksheets/        (2 files) - Build strategy cost models
├── agent_tools/                (2 files) - Master index and workflow demos
└── USAGE_GUIDE.md             (this file)
```

---

## 1. Budget Plans (5 Files)

Complete, historically-grounded budget examples for each major store configuration type.

### Files

| File | Store Type | Size | Avg Cost | Use Cases |
|------|------------|------|----------|-----------|
| `Budget_Plan_urban_flagship_5000sqft.xlsx` | Urban Flagship | 5,000 sqft | ~$1,425,000 | High-traffic urban, brand showcases |
| `Budget_Plan_suburban_standard_3500sqft.xlsx` | Suburban Standard | 3,500 sqft | ~$647,500 | Mall locations, standard rollout |
| `Budget_Plan_express_compact_2000sqft.xlsx` | Express/Compact | 2,000 sqft | ~$290,000 | Quick market entry, cost-optimized |
| `Budget_Plan_remodel_refresh_3500sqft.xlsx` | Remodel/Refresh | 3,500 sqft | ~$332,500 | Store updates, selective categories |
| `Budget_Plan_prototype_innovation_4000sqft.xlsx` | Prototype/Innovation | 4,000 sqft | ~$1,300,000 | New concepts, R&D |

### Worksheet Structure

Each budget plan file contains **5 worksheets**:

#### 1. Executive Summary
- Store configuration overview
- High-level cost breakdown by category
- Total project cost and cost/sqft
- Comparison to historical average
- Key assumptions

**Example**: Total cost $647,500 for suburban_standard (3,500 sqft)
- Construction: $226,625 (35%)
- Electrical: $77,700 (12%)
- HVAC: $51,800 (8%)
- Plumbing: $32,375 (5%)
- Fixtures: $161,875 (25%)
- Technology: $51,800 (8%)
- Soft Costs: $45,325 (7%)

#### 2. Detailed Line Items
- Category-by-category breakdown
- Item descriptions with quantities and unit costs
- Extended costs calculated
- Source references (which cost model/historical project)
- Regional modifiers noted

**Example Line Item**:
```
Category: Electrical
Item: LED lighting fixtures
Quantity: 65 fixtures
Unit Cost: $412/each
Total: $26,780
Source: Cost Model suburban_standard
```

#### 3. Scenario Comparisons
- Base case vs. adjusted scenarios
- Cost impacts of common variations:
  - Cincinnati market (+6% due to union labor)
  - Accelerated schedule (+15% timeline premium)
  - Premium finishes (+22% upgrade cost)
  - Value engineering (-12% cost reduction)
- Side-by-side comparison table

#### 4. Data Sources
- References to source data files
- Links to:
  - `01_Build_Templates/store_types.json`
  - `03_Historical_Projects/historical_projects.csv`
  - `05_Cost_Models/cost_model_*.json`
  - `06_Vendor_Data/vendor_pricing.csv`
  - `07_Conversations/meeting_transcripts/*`
- Calculation formulas documented

#### 5. Agent Instructions
- How to use this budget plan as reference
- Which parameters to adjust for new projects
- Validation checkpoints
- Source attribution guidelines
- Named ranges for programmatic access

### When to Use Budget Plans

**Selection Criteria**:
1. Identify store type from user request
2. Match square footage to closest typical size
3. Use as baseline for adjustments

**Example**:
- Request: "Budget for 3,200 sqft suburban store"
- Select: `Budget_Plan_suburban_standard_3500sqft.xlsx`
- Adjust: Scale costs proportionally (3,200 / 3,500 = 0.914)

---

## 2. Configuration Templates (2 Files)

Reusable templates with input zones for agents to populate with project-specific data.

### Files

#### `Template_Config_Store_Configuration.xlsx`

**Purpose**: Universal store configuration input template for generating custom budgets

**Features**:
- **Agent Input Zone** (blue highlighted cells):
  - Store Type (dropdown: 5 options)
  - Square Footage (numeric entry)
  - Region/Market (dropdown: 10 markets)
  - Timeline (dropdown: Standard/Accelerated/Extended)
  - Special Constraints (text entry)

- **Auto-Calculation Zone** (gray cells):
  - Base costs pulled from cost models
  - Regional multipliers applied via VLOOKUP
  - Timeline premiums calculated
  - Final adjusted costs computed

- **Output Zone** (green cells):
  - Total project cost by category
  - Overall cost summary
  - Cost per square foot

**Agent Workflow**:
1. Agent populates input zone with project parameters
2. Formulas auto-calculate adjusted budget
3. Agent reads output zone for cost estimate
4. Agent cites template in response

#### `Template_Config_Constraint_Response.xlsx`

**Purpose**: Calculate cost impacts of project constraints

**Features**:
- Constraint type selector (dropdown):
  - Landlord (approved vendor list, no structural changes, etc.)
  - Budget (cost caps, cash flow limitations)
  - Timeline (accelerated, holiday deadlines)
  - Regional (union labor, permitting complexity)
  - Operational (store open during remodel)

- Impact calculation by constraint type:
  - Affected cost categories identified
  - Multipliers applied (e.g., 1.20x for after-hours labor)
  - Mitigation strategies listed
  - Alternative approaches suggested

**Example Use**:
- Constraint: "Landlord requires approved vendor list"
- Impact: +5% to +15% across all categories
- Mitigation: "Negotiate vendor approval, price accordingly"

### How to Use Templates

1. **For Agents**:
   - Read input requirements from blue zone
   - Populate cells with project data
   - Reference output zone for results
   - Use named ranges for programmatic access

2. **For Humans**:
   - Enter parameters manually
   - Review auto-calculated results
   - Validate against comparable projects
   - Export or print for stakeholder review

---

## 3. Build Strategy Worksheets (2 Files)

Proven build strategies with documented cost impacts and applicability criteria.

### Files

#### `Strategy_Fast_Track.xlsx`

**Purpose**: Timeline compression cost model

**Contents**:
- **Strategy Overview**:
  - Objective: Reduce 12-week timeline to 8 weeks
  - Cost Impact: +15% to +20% total project cost
  - Success Rate: 78% on-time completion

- **Cost Impact by Category**:
  - Construction: +18% (overtime labor, weekend shifts)
  - Electrical: +15% (premium rates, expedited materials)
  - HVAC: +12% (expedited delivery)
  - Plumbing: +15% (premium labor for compressed schedule)
  - Fixtures: +8% (air freight, rush orders)
  - Technology: +5% (minimal timeline impact)
  - Soft Costs: +10% (expedited permitting)

- **When to Use**:
  - ✓ Critical market entry timing
  - ✓ Lease penalty clauses for delays
  - ✓ Budget can absorb 15-20% premium
  - ✗ Complex site conditions
  - ✗ Landlord restrictions on after-hours work
  - ✗ Tight budget constraints

- **Historical Examples**:
  - Store-147 (Columbus): 8.5 weeks, +17%, Success
  - Store-162 (Cincinnati): 9 weeks, +19%, Delayed 1 week
  - Store-183 (Cleveland): 8 weeks, +16%, Success

#### `Strategy_Value_Engineering.xlsx`

**Purpose**: Cost reduction opportunities

**Contents**:
- **Cost Reduction Opportunities**:

| Category | Standard Cost | VE Approach | Savings | Quality Impact |
|----------|---------------|-------------|---------|----------------|
| Flooring | $63,000 | LVT → Laminate | 22% | Minimal (3yr vs 5yr lifespan) |
| Lighting Fixtures | $26,780 | Reduce fixture count 15% | 15% | Minor (adequate illumination) |
| Mannequins | $6,930 | Reduce from 18 to 12 | 33% | Minimal (display flexibility) |
| Digital Displays | $8,600 | Reduce from 4 to 2 units | 50% | Moderate (less dynamic content) |
| Paint Finish | $15,750 | Standard vs premium | 18% | Minimal (appearance) |
| Dressing Rooms | $14,800 | Reduce from 8 to 6 units | 25% | Minimal (adequate capacity) |

- **Total Savings Potential**: $35,575 (12-18% reduction)

- **When to Use**:
  - Budget cap constraints
  - Value-oriented market entry
  - Test market/pilot locations
  - Cost-optimized rollout strategy

### How to Use Strategy Worksheets

1. **Identify Applicable Strategy**:
   - Fast-Track: Timeline is critical constraint
   - Value Engineering: Budget is critical constraint

2. **Review Cost Impacts**:
   - Understand category-specific premiums or savings
   - Evaluate quality trade-offs

3. **Apply to Budget Estimate**:
   - Start with appropriate budget plan
   - Layer strategy multipliers on top
   - Cite strategy worksheet in agent response

4. **Reference Historical Performance**:
   - Check success rates
   - Review similar historical projects
   - Set realistic expectations

---

## 4. Agent Tools (2 Files)

Master catalog and workflow demonstrations for AI agent integration.

### Files

#### `Master_Index_Budget_Artifacts.xlsx`

**Purpose**: Complete catalog of all budget artifacts with use case mapping

**Worksheets**:

1. **Master Catalog**:
   - Lists all 11 Excel files
   - Descriptions and use cases for each
   - Average costs where applicable
   - Quick reference for file selection

2. **Recommendation Matrix**:
   - IF/THEN rules for selecting artifacts
   - Example scenarios mapped to recommended files
   - Constraint-driven selection logic

**Example Recommendations**:
- IF: "New urban flagship" + "Premium finish requirement"
  - THEN: Use `Budget_Plan_urban_flagship_5000sqft.xlsx`
  - PLUS: None

- IF: "Any store type" + "Tight timeline (< 10 weeks)"
  - THEN: Use appropriate budget plan
  - PLUS: `Strategy_Fast_Track.xlsx`

- IF: "Any store type" + "Budget cap constraint"
  - THEN: Use appropriate budget plan
  - PLUS: `Strategy_Value_Engineering.xlsx`

#### `Sample_Workflow_Demo.xlsx`

**Purpose**: Step-by-step demonstration of agent using budget artifacts

**Scenario**: Create budget for 3,200 sqft suburban store in Cincinnati with 10-week timeline

**Workflow Steps**:

1. **Receive Request**:
   - User: "Create budget estimate for 3,200 sqft suburban store in Cincinnati with 10-week timeline"

2. **Identify Parameters**:
   - Store Type: suburban_standard (closest match)
   - Region: Cincinnati
   - Timeline: Accelerated (10 weeks vs standard 12)
   - Square Footage: 3,200 sqft

3. **Select Budget Artifacts**:
   - Primary: `Budget_Plan_suburban_standard_3500sqft.xlsx`
   - Regional: `regional_modifiers.csv` (Cincinnati 1.06x)
   - Timeline: `Strategy_Fast_Track.xlsx` (+15% premium)

4. **Calculate Adjusted Budget**:
   - Base Cost (3500 sqft): $647,500
   - Size Adjustment (3200/3500): $592,914
   - Cincinnati Multiplier (1.06): $628,489
   - Timeline Premium (1.15): $722,762
   - **FINAL ESTIMATED COST**: **$722,762**

5. **Cite Sources**:
   - "Based on Budget_Plan_suburban_standard_3500sqft.xlsx"
   - "adjusted for Cincinnati market (1.06x regional modifier)"
   - "and 10-week accelerated timeline (+15% premium)"
   - "per Strategy_Fast_Track.xlsx"

6. **Provide Breakdown**:
   - Construction: $296,423 (41%)
   - Electrical: $101,484 (14%)
   - HVAC: $53,795 (7.4%)
   - Plumbing: $33,621 (4.7%)
   - Fixtures: $168,064 (23.2%)
   - Technology: $53,795 (7.4%)
   - Soft Costs: $47,076 (6.5%)

---

## Agent Integration Features

### Named Ranges

All Excel files use named ranges for programmatic access:

- **InputParameters**: Input zone cells (blue)
- **BudgetOutput**: Output zone cells (green)
- **CostSummary**: Executive summary tables
- **LineItemsData**: Detailed cost breakdown
- **ScenarioCompare**: Scenario comparison tables

### Data Validation

Input cells include:
- Dropdown menus for categorical inputs
- Data validation rules for numeric inputs
- Clear error messages for invalid entries
- Embedded instructions in cell comments

### Metadata Sheets

Each file includes metadata:
- File purpose and version
- Generation date
- Dependencies on source data files
- Update procedures

### Color Coding Standard

Consistent across all files:
- **Blue cells**: Agent/human input zones
- **Green cells**: Calculated outputs
- **Gray cells**: Formula cells (intermediate calculations)
- **Headers**: Dark blue background, white text

---

## Data Source References

All budget artifacts derive from and reference:

### Structured Data (Folders 01-06)

- **01_Build_Templates**: Store type definitions, base configurations
- **02_Constraints**: Constraint catalog and cost impacts
- **03_Historical_Projects**: 160 completed projects with actual costs
- **04_Regional_Modifiers**: Market-specific multipliers for 10 markets
- **05_Cost_Models**: Detailed line item costs and formulas
- **06_Vendor_Data**: Current vendor pricing from 8 major vendors

### Conversational Data (Folder 07)

- **Meeting Transcripts**: 341 meetings with vendor negotiations, lessons learned
- **Teams Conversations**: 8,098 threads with cost discussions and decisions

### Traceability

Every budget line item includes:
- Source file reference (e.g., "Cost Model: suburban_standard")
- Historical project citations (e.g., "Based on Store-189 actual: $32,000")
- Meeting transcript references (e.g., "Vendor negotiation 2025-12-07")
- Regional modifier documentation (e.g., "Cincinnati electrical: 1.08x")

---

## Example Agent Prompts

### Generate New Budget Estimate

```
Prompt: "Generate a budget estimate for a 4,200 sqft suburban store
in Indianapolis with standard timeline."

Agent Response:
1. Select Budget_Plan_suburban_standard_3500sqft.xlsx as baseline
2. Apply size adjustment: (4,200 / 3,500) = 1.20x
3. Apply Indianapolis regional modifier: 0.99x (slightly lower cost)
4. Calculate: $647,500 × 1.20 × 0.99 = $769,470
5. Cite: "Based on Budget_Plan_suburban_standard_3500sqft.xlsx,
   scaled to 4,200 sqft with Indianapolis regional adjustment (0.99x)"
6. Provide category breakdown from detailed line items
```

### Evaluate Constraint Impact

```
Prompt: "How much would landlord-mandated approved vendor list
add to a $650,000 project?"

Agent Response:
1. Open Template_Config_Constraint_Response.xlsx
2. Select constraint type: "landlord" / "approved vendor list"
3. Review impact: +5% to +15% across all categories
4. Calculate: $650,000 × 1.10 (midpoint) = $715,000
5. Additional cost: $65,000 (+10%)
6. Cite: "Per Template_Config_Constraint_Response.xlsx, landlord
   vendor restrictions typically add 5-15% to project costs"
7. Suggest mitigation: "Negotiate vendor approval, price accordingly"
```

### Compare Build Strategies

```
Prompt: "Should we fast-track or value engineer a suburban store
with $600K budget and tight timeline?"

Agent Response:
1. Review Strategy_Fast_Track.xlsx:
   - Timeline reduction: 12 weeks → 8 weeks
   - Cost impact: +15% = $690K (over budget)
2. Review Strategy_Value_Engineering.xlsx:
   - Cost reduction: -12% = $528K (under budget, but slower)
3. Recommendation: "Fast-track exceeds $600K budget. Consider:
   - Option A: Value engineer to reduce costs, maintain timeline
   - Option B: Request budget increase to $690K for fast-track
   - Option C: Hybrid: selective value engineering + moderate acceleration"
4. Cite both strategy worksheets with specific cost impacts
```

---

## Update Procedures

### When to Regenerate Budget Artifacts

1. **Quarterly** (recommended):
   - New historical projects complete
   - Vendor pricing updates from negotiations
   - Regional market trends shift

2. **As Needed**:
   - Template specifications change (e.g., v2.3 → v3.0)
   - New store types introduced
   - Major vendor contract renegotiations
   - Significant cost model adjustments

### How to Update

1. Update source data (folders 01-07):
   - Add new historical projects to `03_Historical_Projects/`
   - Update vendor pricing in `06_Vendor_Data/`
   - Adjust regional modifiers in `04_Regional_Modifiers/`

2. Regenerate budget artifacts:
   ```bash
   python3 scripts/generate_budget_artifacts.py
   ```

3. Review changes:
   - Compare cost summaries to previous versions
   - Validate formula integrity
   - Test agent workflows with updated files

4. Document updates:
   - Note version in file metadata
   - Log significant changes in USAGE_GUIDE.md
   - Communicate updates to agent teams

---

## Validation Checklist

Before using budget artifacts in production:

### Data Accuracy
- ✓ All costs trace back to source data files
- ✓ Regional modifiers correctly applied
- ✓ Formulas produce mathematically correct results
- ✓ Historical comparisons use actual data

### Completeness
- ✓ Every major store type has budget plan
- ✓ All common constraint scenarios covered
- ✓ Configuration templates address primary use cases
- ✓ Build strategies reference real historical projects

### Usability
- ✓ Clear instructions on every worksheet
- ✓ No broken formulas or circular references
- ✓ Print-friendly formatting
- ✓ Accessible to both humans and AI agents

### Consistency
- ✓ Uniform category hierarchies across files
- ✓ Standardized naming conventions
- ✓ Consistent use of units (sqft, dollars, days)
- ✓ Cross-file references validated

---

## Support & Questions

For questions about budget artifacts:

1. **Review This Guide**: Complete usage instructions above
2. **Check Master Index**: `agent_tools/Master_Index_Budget_Artifacts.xlsx`
3. **Review Sample Workflow**: `agent_tools/Sample_Workflow_Demo.xlsx`
4. **Examine Source Data**: Folders 01-07 contain foundational data
5. **Regenerate if Needed**: Run `scripts/generate_budget_artifacts.py`

---

**Last Updated**: 2026-02-05
**Total Budget Artifacts**: 11 Excel files
**Ready for**: AI agent integration, human analysis, stakeholder reporting
