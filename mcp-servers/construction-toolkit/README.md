# Construction Toolkit MCP Server

A specialized MCP server providing construction industry tools for estimating, bid analysis, specification lookup, and project data management.

## Features

### Tools

#### Bid Analysis
- `analyze_bid` - Analyze bid completeness and competitiveness
- `compare_bids` - Compare multiple bids side-by-side
- `check_bid_balance` - Identify unbalanced bid items

#### Quantity Takeoff
- `calculate_takeoff` - Calculate quantities from specifications
- `apply_waste_factor` - Apply industry-standard waste factors
- `convert_units` - Convert between construction units (SF, SY, CY, etc.)

#### Specification Lookup
- `query_caltrans_spec` - Look up CALTRANS standard specifications
- `search_specs` - Search specification documents for keywords
- `get_csi_division` - Get CSI MasterFormat division information

#### Historical Data
- `query_historical_pricing` - Get historical unit prices for items
- `get_market_trends` - Analyze current material and labor market trends
- `compare_to_estimate` - Compare bid prices to historical estimates

#### Compliance & DBE
- `check_dbe_requirements` - Verify DBE (Disadvantaged Business Enterprise) compliance
- `calculate_dbe_participation` - Calculate DBE participation percentage
- `verify_prevailing_wage` - Check prevailing wage requirements

## Installation

```bash
cd mcp-servers/construction-toolkit
pip install -e .
```

## Configuration

### Claude Code (~/.claude/mcp_settings.json)
```json
{
  "mcpServers": {
    "construction": {
      "command": "python",
      "args": ["-m", "construction_toolkit"],
      "env": {
        "HEAVYBID_DB_PATH": "/path/to/heavybid/database",
        "CALTRANS_SPECS_PATH": "/path/to/caltrans/specs"
      }
    }
  }
}
```

### Environment Variables

- `HEAVYBID_DB_PATH` - Path to HeavyBid database (optional)
- `PROCORE_API_KEY` - Procore API key (optional)
- `CALTRANS_SPECS_PATH` - Path to CALTRANS specifications directory
- `HISTORICAL_DATA_PATH` - Path to historical pricing data

## Usage Examples

### Analyze a Bid

```python
# AI can call this tool
result = await analyze_bid(
    project_id="SR-99-12345",
    bid_file="path/to/bid_tab.pdf",
    comparison_basis="engineer_estimate"
)
```

### Calculate Quantity Takeoff

```python
result = await calculate_takeoff(
    spec_file="path/to/specs.pdf",
    item_description="Asphalt Concrete Paving",
    dimensions={"length": 250, "width": 12, "depth": 3},
    unit="TON"
)
```

### Query CALTRANS Specifications

```python
result = await query_caltrans_spec(
    section="40-1.03",
    topic="Hot Mix Asphalt"
)
```

## Integration with External Systems

### HeavyBid Integration
If `HEAVYBID_DB_PATH` is configured, the server can:
- Query historical job costs
- Access item libraries
- Retrieve productivity rates
- Compare current bids to past jobs

### Procore Integration
If `PROCORE_API_KEY` is configured, the server can:
- Fetch project information
- Access RFIs and submittals
- Retrieve budget data
- Track change orders

### CALTRANS Specification Access
If `CALTRANS_SPECS_PATH` is configured, the server provides:
- Standard specification lookup
- Special provisions search
- Standard plan references
- Material specifications

## Data Sources

The server can connect to various data sources:

1. **Local databases** - SQLite, PostgreSQL
2. **File-based data** - JSON, CSV, Excel
3. **External APIs** - HeavyBid, Procore, B2W
4. **Document repositories** - Specifications, plans, drawings
5. **Market data services** - Material pricing, labor rates

## Security Considerations

- **API keys** - Store securely in environment variables
- **Database access** - Use read-only credentials when possible
- **File access** - Restrict to designated directories
- **Data validation** - Validate all inputs before processing
- **Audit logging** - Log all data access and modifications

## Development

### Adding New Tools

```python
@server.tool()
async def your_new_tool(param: str) -> dict:
    """
    Tool description for AI

    Args:
        param: Parameter description

    Returns:
        Result dictionary
    """
    # Implementation
    return {"result": "success"}
```

### Testing

```bash
# Run tests
pytest tests/

# Test with MCP inspector
mcp-inspector python -m construction_toolkit
```

## Example Prompts

The server includes specialized prompts for construction tasks:

- `estimate_review` - Review an estimate for completeness
- `bid_day_workflow` - Guide through bid day procedures
- `specification_analysis` - Analyze specification requirements
- `subcontractor_qualification` - Evaluate subcontractor qualifications

## Resources

- [CALTRANS Specifications](https://dot.ca.gov/programs/engineering-services/manuals)
- [CSI MasterFormat](https://www.csiresources.org/standards/masterformat)
- [RS Means Data](https://www.rsmeans.com/)
- [HeavyBid Documentation](https://www.hcss.com/products/heavybid/)

## Support

For issues or questions:
1. Check the documentation
2. Review example code in `examples/`
3. Open an issue on GitHub
4. Contact support team

## License

MIT License - See LICENSE file for details
