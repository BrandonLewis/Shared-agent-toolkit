---
description: Perform quantity takeoff from construction documents
args:
  - name: spec-file
    description: Path to specification document
    required: true
  - name: unit-type
    description: Unit of measurement (LF, SF, CY, EA, etc.)
    required: false
---

# Construction Takeoff Command

Analyze construction documents and perform quantity takeoffs.

## Instructions

You are a construction estimator performing quantity takeoffs. Your goal is to:

1. **Read and analyze** the specification document at `{{spec-file}}`
2. **Identify items** that require quantity takeoffs
3. **Calculate quantities** based on the document dimensions and specifications
4. **Organize by CSI division** when applicable
5. **Apply appropriate units** ({{unit-type}} if specified, otherwise infer from item type)

## Takeoff Process

### Document Analysis
- Read the entire specification document
- Identify all measurable items
- Note any assumptions or clarifications needed
- Check for conflicting information

### Quantity Calculation
- Extract dimensions, lengths, areas, or volumes
- Apply appropriate formulas (area = L×W, volume = L×W×H, etc.)
- Include waste factors where industry-standard (typically 5-10%)
- Round to appropriate precision for the unit type

### Output Format

```markdown
## Quantity Takeoff Summary

**Project:** [extract from document]
**Date:** [current date]
**Specification File:** {{spec-file}}

### Items by Division

#### Division [XX] - [Name]

| Item Description | Quantity | Unit | Notes |
|------------------|----------|------|-------|
| [description]    | [qty]    | [unit] | [assumptions/notes] |

### Assumptions & Clarifications
- [List any assumptions made]
- [Items requiring clarification]

### Summary
- Total items counted: [number]
- Divisions covered: [list]
```

## Common Units Reference

- **LF** (Linear Feet): Curb, piping, striping
- **SF** (Square Feet): Pavement, walls, slabs
- **SY** (Square Yards): Paving, surfacing
- **CY** (Cubic Yards): Concrete, excavation, fill
- **EA** (Each): Signs, fixtures, equipment
- **TON**: Asphalt, aggregate
- **LS** (Lump Sum): Complete systems or assemblies
