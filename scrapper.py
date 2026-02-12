import csv
import re
from html_scrapper import rows_out

rows = rows_out

def split_commodity_and_unit(raw):
    """
    Example:
    'Crude OilUSD/Bbl' -> ('Crude Oil', 'USD/Bbl')
    'GoldUSD/t.oz'     -> ('Gold', 'USD/t.oz')
    """
    match = re.search(r'(USD|USd|EUR|CNY|INR|GBP|AUD|CAD|BRL|NOK|MYR)(.*)', raw)
    if match:
        commodity = raw[:match.start()].strip()
        unit = match.group().strip()
    else:
        commodity = raw.strip()
        unit = ""
    return commodity, unit

# Define the 10 commodities we want to keep - UPDATED with Rhodium instead of Iron Ore
selected_commodities = {
    # Metals
    'Gold': 'Metal',
    'Silver': 'Metal',
    'Copper': 'Metal',
    'Lithium': 'Metal',
    'Rhodium': 'Metal',  # Replaced Iron Ore with Rhodium
    
    # Non-Metals
    'Brent': 'Others',
    'Natural gas': 'Others',  # Note: lowercase 'g' in 'gas' from your CSV
    'Soybeans': 'Others',
    'Wheat': 'Others',
    'Cocoa': 'Others'
}

clean_rows = []
current_category = None
headers = None

# First pass: collect all selected commodities
for row in rows:
    # Category header row
    if row[0] in {
        "Energy", "Metals", "Agricultural",
        "Industrial", "Livestock", "Index", "Electricity"
    }:
        current_category = row[0]
        headers = row
        continue

    # Skip malformed rows
    if headers is None or len(row) != len(headers):
        continue

    name_unit = row[0]

    # Correct split
    commodity, unit = split_commodity_and_unit(name_unit)

    # Improve readability: CrudeOil -> Crude Oil
    commodity = re.sub(r'([a-z])([A-Z])', r'\1 \2', commodity).strip()
    
    # Check if commodity is in our selected list
    # Try both exact match and case-insensitive match for Natural Gas
    commodity_key = None
    for key in selected_commodities:
        if commodity.lower() == key.lower():
            commodity_key = key
            break
    
    if commodity_key in selected_commodities:
        # Create clean row with new category
        clean_row = [
            selected_commodities[commodity_key],  # Use our new category
            commodity_key,  # Use the standardized key name
            unit,
            *row[1:]
        ]
        clean_rows.append(clean_row)

# Sort rows: Metals first, then Non-Metals
clean_rows.sort(key=lambda x: (0 if x[0] == 'Metal' else 1, x[1]))

# Write clean CSV with only selected commodities
with open("commodities_clean.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "category", "commodity", "unit",
        "price", "day", "pct",
        "weekly", "monthly", "ytd", "yoy", "date"
    ])
    writer.writerows(clean_rows)

# print(f"Saved {len(clean_rows)} commodities to commodities_clean.csv")
# print("\nCommodities saved:")
# for row in clean_rows:
#     print(f"  {row[0]}: {row[1]}")