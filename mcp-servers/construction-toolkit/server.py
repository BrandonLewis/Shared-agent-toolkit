#!/usr/bin/env python3
"""
Construction Toolkit MCP Server
Provides construction industry tools for estimating, bid analysis, and project management
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from mcp.server import Server
    from mcp.types import Tool, Resource, TextContent
except ImportError:
    print("Error: mcp package not installed. Install with: pip install mcp")
    exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("construction-toolkit")

# Initialize server
server = Server("construction-toolkit")

# Configuration from environment
HEAVYBID_DB_PATH = os.getenv("HEAVYBID_DB_PATH")
PROCORE_API_KEY = os.getenv("PROCORE_API_KEY")
CALTRANS_SPECS_PATH = os.getenv("CALTRANS_SPECS_PATH")
HISTORICAL_DATA_PATH = os.getenv("HISTORICAL_DATA_PATH", "./data/historical")

# Unit conversion factors
UNIT_CONVERSIONS = {
    "SF_to_SY": 1 / 9,  # Square feet to square yards
    "SY_to_SF": 9,      # Square yards to square feet
    "CF_to_CY": 1 / 27, # Cubic feet to cubic yards
    "CY_to_CF": 27,     # Cubic yards to cubic feet
    "TON_to_CY_asphalt": 1 / 2.4,  # Tons to CY for asphalt (typical density)
    "CY_to_TON_asphalt": 2.4,      # CY to tons for asphalt
}

# Waste factors by material type
WASTE_FACTORS = {
    "concrete": 1.05,    # 5% waste
    "asphalt": 1.03,     # 3% waste
    "aggregate": 1.10,   # 10% waste
    "rebar": 1.08,       # 8% waste
    "lumber": 1.15,      # 15% waste
    "pipe": 1.05,        # 5% waste
    "default": 1.05,     # 5% waste
}


# ============================================================================
# BID ANALYSIS TOOLS
# ============================================================================

@server.tool()
async def analyze_bid(
    project_id: str,
    bid_file: str,
    comparison_basis: str = "engineer_estimate"
) -> Dict[str, Any]:
    """
    Analyze a bid for completeness and competitiveness

    Args:
        project_id: Project identifier
        bid_file: Path to bid tabulation file
        comparison_basis: What to compare against (engineer_estimate, market_average, historical)

    Returns:
        Bid analysis results with recommendations
    """
    logger.info(f"Analyzing bid for project {project_id}")

    # In a real implementation, this would:
    # 1. Parse the bid file (PDF, Excel, etc.)
    # 2. Extract bid items and prices
    # 3. Compare to the specified basis
    # 4. Calculate variances
    # 5. Identify unbalanced items

    return {
        "project_id": project_id,
        "bid_file": bid_file,
        "analysis_date": datetime.now().isoformat(),
        "status": "analyzed",
        "summary": {
            "total_bid": 1250000.00,
            "comparison_total": 1300000.00,
            "variance_percent": -3.85,
            "competitiveness": "very competitive"
        },
        "flags": [
            {
                "severity": "warning",
                "item": "Item 5: Asphalt Paving",
                "issue": "Price 25% below estimate",
                "recommendation": "Verify subcontractor quote and scope understanding"
            },
            {
                "severity": "info",
                "item": "Item 12: Traffic Control",
                "issue": "Price 15% above estimate",
                "recommendation": "Within acceptable range for current market"
            }
        ],
        "recommendation": "Bid appears competitive with minor flags to investigate"
    }


@server.tool()
async def check_bid_balance(bid_items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Check if bid items are unbalanced (front-loaded or back-loaded)

    Args:
        bid_items: List of bid items with quantities, unit prices, and timing

    Returns:
        Analysis of bid balance
    """
    logger.info(f"Checking balance of {len(bid_items)} bid items")

    # In real implementation:
    # 1. Calculate cash flow timing
    # 2. Compare early vs late items
    # 3. Identify front-loading or back-loading
    # 4. Calculate weighted average timing

    return {
        "balance_status": "balanced",
        "front_loaded_percentage": 15.2,
        "back_loaded_percentage": 12.8,
        "analysis": "Bid shows slight front-loading within acceptable limits",
        "risk_level": "low"
    }


# ============================================================================
# QUANTITY TAKEOFF TOOLS
# ============================================================================

@server.tool()
async def calculate_takeoff(
    item_description: str,
    dimensions: Dict[str, float],
    unit: str,
    material_type: Optional[str] = None
) -> Dict[str, Any]:
    """
    Calculate quantity takeoff with waste factor

    Args:
        item_description: Description of the item
        dimensions: Dictionary with length, width, depth/height as applicable
        unit: Target unit (LF, SF, SY, CF, CY, TON, EA)
        material_type: Type of material for waste factor (optional)

    Returns:
        Calculated quantities with and without waste
    """
    logger.info(f"Calculating takeoff for: {item_description}")

    # Calculate base quantity
    base_qty = 1.0

    if unit in ["LF"]:  # Linear
        base_qty = dimensions.get("length", 0)
    elif unit in ["SF"]:  # Area
        base_qty = dimensions.get("length", 0) * dimensions.get("width", 0)
    elif unit in ["SY"]:  # Area in yards
        sf = dimensions.get("length", 0) * dimensions.get("width", 0)
        base_qty = sf / 9
    elif unit in ["CF"]:  # Volume
        base_qty = (dimensions.get("length", 0) *
                    dimensions.get("width", 0) *
                    dimensions.get("depth", dimensions.get("height", 0)))
    elif unit in ["CY"]:  # Volume in yards
        cf = (dimensions.get("length", 0) *
              dimensions.get("width", 0) *
              dimensions.get("depth", dimensions.get("height", 0)))
        base_qty = cf / 27
    elif unit in ["EA"]:  # Each
        base_qty = dimensions.get("quantity", 1)

    # Apply waste factor
    waste_factor = WASTE_FACTORS.get(material_type, WASTE_FACTORS["default"])
    qty_with_waste = base_qty * waste_factor

    return {
        "item": item_description,
        "dimensions": dimensions,
        "base_quantity": round(base_qty, 2),
        "unit": unit,
        "waste_factor": waste_factor,
        "quantity_with_waste": round(qty_with_waste, 2),
        "waste_amount": round(qty_with_waste - base_qty, 2),
        "calculation_notes": f"Calculated from dimensions, applied {int((waste_factor-1)*100)}% waste factor"
    }


@server.tool()
async def convert_units(
    quantity: float,
    from_unit: str,
    to_unit: str,
    material_type: str = "general"
) -> Dict[str, Any]:
    """
    Convert between construction units

    Args:
        quantity: Quantity to convert
        from_unit: Source unit (LF, SF, SY, CF, CY, TON)
        to_unit: Target unit
        material_type: Material type for density conversions

    Returns:
        Converted quantity with conversion factor
    """
    conversion_key = f"{from_unit}_to_{to_unit}"
    if material_type != "general":
        conversion_key = f"{conversion_key}_{material_type}"

    conversion_factor = UNIT_CONVERSIONS.get(
        conversion_key,
        UNIT_CONVERSIONS.get(f"{from_unit}_to_{to_unit}", 1.0)
    )

    converted_qty = quantity * conversion_factor

    return {
        "original_quantity": quantity,
        "original_unit": from_unit,
        "converted_quantity": round(converted_qty, 2),
        "converted_unit": to_unit,
        "conversion_factor": conversion_factor,
        "material_type": material_type
    }


# ============================================================================
# SPECIFICATION LOOKUP TOOLS
# ============================================================================

@server.tool()
async def query_caltrans_spec(section: str, topic: Optional[str] = None) -> Dict[str, Any]:
    """
    Look up CALTRANS standard specification

    Args:
        section: Specification section number (e.g., "40-1.03")
        topic: Optional topic or keyword to search within section

    Returns:
        Specification text and requirements
    """
    logger.info(f"Looking up CALTRANS spec section {section}")

    # In real implementation:
    # 1. Access CALTRANS specs database or files
    # 2. Parse section number
    # 3. Extract relevant text
    # 4. Return formatted specification

    return {
        "section": section,
        "title": "Hot Mix Asphalt",
        "division": "40 - Asphalt Concrete",
        "content": "Specification content would be extracted from CALTRANS database",
        "requirements": [
            "Material shall conform to Section 39",
            "Minimum compaction: 95% of laboratory density",
            "Temperature range: 275°F - 325°F"
        ],
        "references": ["Section 39-2", "CT 125", "CT 304"],
        "source": "CALTRANS Standard Specifications 2024"
    }


@server.tool()
async def get_csi_division(division_number: int) -> Dict[str, Any]:
    """
    Get information about a CSI MasterFormat division

    Args:
        division_number: CSI division number (1-50)

    Returns:
        Division information and common sections
    """
    # CSI MasterFormat divisions reference
    divisions = {
        1: {"title": "General Requirements", "description": "Project management, temporary facilities, quality"},
        2: {"title": "Existing Conditions", "description": "Demolition, site remediation, structure moving"},
        3: {"title": "Concrete", "description": "Concrete forming, reinforcement, cast-in-place"},
        31: {"title": "Earthwork", "description": "Excavation, fill, grading, soil treatment"},
        32: {"title": "Exterior Improvements", "description": "Paving, sidewalks, site utilities"},
        33: {"title": "Utilities", "description": "Water, sewer, storm drainage systems"},
    }

    division_info = divisions.get(division_number, {"title": f"Division {division_number}", "description": "Not in reference"})

    return {
        "division_number": division_number,
        "title": division_info["title"],
        "description": division_info["description"],
        "format": "CSI MasterFormat 2024"
    }


# ============================================================================
# HISTORICAL DATA TOOLS
# ============================================================================

@server.tool()
async def query_historical_pricing(
    item_code: str,
    project_type: Optional[str] = None,
    date_range_months: int = 12
) -> Dict[str, Any]:
    """
    Query historical unit pricing for bid items

    Args:
        item_code: Item code or description
        project_type: Type of project for filtering
        date_range_months: How many months of history to retrieve

    Returns:
        Historical pricing data and statistics
    """
    logger.info(f"Querying historical pricing for item: {item_code}")

    # In real implementation:
    # 1. Query HeavyBid database or historical data store
    # 2. Filter by project type and date range
    # 3. Calculate statistics
    # 4. Return formatted results

    return {
        "item_code": item_code,
        "item_description": "Asphalt Concrete Paving (Type A)",
        "unit": "TON",
        "date_range_months": date_range_months,
        "statistics": {
            "count": 15,
            "average": 145.50,
            "median": 142.00,
            "min": 125.00,
            "max": 168.00,
            "std_dev": 12.30
        },
        "recent_trend": "stable",
        "market_note": "Prices stable over past 6 months",
        "projects": [
            {"project": "SR-99 Overlay", "date": "2024-11-15", "price": 142.00},
            {"project": "I-5 Resurfacing", "date": "2024-10-20", "price": 148.50},
            {"project": "Local Street Rehab", "date": "2024-09-10", "price": 138.00}
        ]
    }


# ============================================================================
# COMPLIANCE TOOLS
# ============================================================================

@server.tool()
async def check_dbe_requirements(
    project_id: str,
    project_value: float,
    dbe_goal_percent: float
) -> Dict[str, Any]:
    """
    Check DBE (Disadvantaged Business Enterprise) requirements

    Args:
        project_id: Project identifier
        project_value: Total project value
        dbe_goal_percent: Required DBE participation percentage

    Returns:
        DBE requirement information and checklist
    """
    dbe_goal_amount = project_value * (dbe_goal_percent / 100)

    return {
        "project_id": project_id,
        "project_value": project_value,
        "dbe_goal_percent": dbe_goal_percent,
        "dbe_goal_amount": round(dbe_goal_amount, 2),
        "requirements": [
            "Submit DBE commitment letters with bid",
            "Use Caltrans-certified DBE firms",
            "Document good faith efforts if goal not met",
            "Report DBE payments monthly"
        ],
        "resources": [
            "DBE Directory: https://dot.ca.gov/programs/civil-rights/dbe",
            "Certification requirements",
            "Good faith effort documentation"
        ]
    }


# ============================================================================
# SERVER LIFECYCLE
# ============================================================================

@server.on_initialize()
async def on_initialize():
    """Called when server initializes"""
    logger.info("Construction Toolkit MCP server initialized")
    logger.info(f"HeavyBid integration: {'enabled' if HEAVYBID_DB_PATH else 'disabled'}")
    logger.info(f"Procore integration: {'enabled' if PROCORE_API_KEY else 'disabled'}")


@server.on_shutdown()
async def on_shutdown():
    """Called when server shuts down"""
    logger.info("Construction Toolkit MCP server shutting down")


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Run the MCP server"""
    import asyncio
    from mcp.server.stdio import stdio_server

    logger.info("Starting Construction Toolkit MCP Server...")

    async def run():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options()
            )

    asyncio.run(run())


if __name__ == "__main__":
    main()
