#!/usr/bin/env python3
"""
Demo script for VisiData MCP Server

This script demonstrates how to use the VisiData MCP server tools
to analyze and manipulate data.
"""

import json
import os
from pathlib import Path

# Import the VisiData MCP server functions directly for demo purposes
import sys
sys.path.append(str(Path(__file__).parent.parent / "src"))

from visidata_mcp.server import (
    load_data,
    get_data_sample,
    analyze_data,
    convert_data,
    filter_data,
    get_column_stats,
    sort_data,
    get_supported_formats
)


def create_sample_data(file_path):
    """Create sample CSV data for demo purposes."""
    sample_data = """name,age,city,salary,department,hire_date
Alice Johnson,28,New York,75000,Engineering,2022-03-15
Bob Smith,35,San Francisco,85000,Marketing,2021-07-20
Carol Davis,42,Chicago,95000,Sales,2020-11-08
David Wilson,31,Austin,72000,Engineering,2023-01-12
Eve Brown,29,Seattle,78000,Design,2022-09-03
Frank Miller,38,Boston,88000,Marketing,2021-04-25
Grace Lee,26,Portland,68000,Engineering,2023-06-18
Henry Taylor,45,Denver,92000,Sales,2019-12-05
Iris Chen,33,Los Angeles,80000,Design,2022-11-30
Jack Anderson,27,Miami,70000,Marketing,2023-02-14
Kate Thompson,39,Philadelphia,89000,Engineering,2020-08-17
Liam Garcia,32,San Diego,76000,Sales,2022-05-22
Maya Patel,30,Atlanta,77000,Design,2021-10-09
Noah Rodriguez,41,Phoenix,91000,Marketing,2020-03-28
Olivia Martinez,34,Dallas,83000,Engineering,2021-12-11"""
    
    with open(file_path, 'w') as f:
        f.write(sample_data)


def demo_basic_operations():
    """Demonstrate basic VisiData operations."""
    print("=== VisiData MCP Server Demo ===\n")
    
    print("ℹ️  Note: You may see VisiData warnings like 'setting unknown option confirm_overwrite'")
    print("   These warnings are harmless and don't affect functionality.\n")
    
    # Get the sample data file path
    sample_file = Path(__file__).parent / "sample_data.csv"
    
    if not sample_file.exists():
        print(f"❌ Sample data file not found: {sample_file}")
        print("Creating sample data file...")
        create_sample_data(sample_file)
        print(f"✅ Created sample data file: {sample_file}\n")
    
    print("1. Loading data...")
    result = load_data(str(sample_file))
    print(json.dumps(json.loads(result), indent=2))
    print()
    
    print("2. Getting data sample (first 5 rows)...")
    result = get_data_sample(str(sample_file), 5)
    data = json.loads(result)
    print(f"Dataset: {data['filename']}")
    print(f"Total rows: {data['total_rows']}, Columns: {data['total_columns']}")
    print("Sample data:")
    for i, row in enumerate(data['data'][:3]):  # Show first 3 rows
        print(f"  Row {i+1}: {row}")
    print("...")
    print()
    
    print("3. Analyzing data structure...")
    result = analyze_data(str(sample_file))
    analysis = json.loads(result)
    print(f"Analysis for {analysis['filename']}:")
    print(f"- Total rows: {analysis['total_rows']}")
    print(f"- Total columns: {analysis['total_columns']}")
    print("- Column details:")
    for col in analysis['columns'][:5]:  # Show first 5 columns
        print(f"  • {col['name']} ({col['type']}): {col['sample_values'][:2]}...")
    print()
    
    print("4. Getting column statistics...")
    result = get_column_stats(str(sample_file), "salary")
    stats = json.loads(result)
    print(f"Statistics for '{stats['column']}' column:")
    print(f"- Type: {stats['type']}")
    print(f"- Values: {stats['total_values']}")
    print(f"- Null count: {stats['null_count']}")
    if 'min' in stats:
        print(f"- Range: ${stats['min']:,} - ${stats['max']:,}")
        print(f"- Average: ${stats['mean']:,.2f}")
    print()
    
    print("5. Filtering data (salary > 70000)...")
    output_file = Path(__file__).parent / "high_salary.csv"
    result = filter_data(str(sample_file), "salary", "greater_than", "70000", str(output_file))
    filter_result = json.loads(result)
    print(f"Filter results:")
    print(f"- Original rows: {filter_result['original_rows']}")
    print(f"- Filtered rows: {filter_result['filtered_rows']}")
    print(f"- Filter: {filter_result['filter_applied']}")
    if 'saved_to' in filter_result:
        print(f"- Saved to: {filter_result['saved_to']}")
    print()
    
    print("6. Converting to JSON...")
    json_output = Path(__file__).parent / "sample_data.json"
    result = convert_data(str(sample_file), str(json_output))
    print(f"Conversion result: {result}")
    print()
    
    print("7. Sorting data by age (descending)...")
    sorted_output = Path(__file__).parent / "sorted_by_age.csv"
    result = sort_data(str(sample_file), "age", True, str(sorted_output))
    sort_result = json.loads(result)
    print(f"Sort results:")
    print(f"- Sorted by: {sort_result['sorted_by']}")
    print(f"- Descending: {sort_result['descending']}")
    print(f"- Total rows: {sort_result['total_rows']}")
    if 'saved_to' in sort_result:
        print(f"- Saved to: {sort_result['saved_to']}")
    print()
    
    print("8. Getting supported formats...")
    result = get_supported_formats()
    formats = json.loads(result)
    print(f"VisiData supports {formats['total_formats']} formats:")
    for fmt, desc in list(formats['supported_formats'].items())[:10]:
        print(f"- {fmt}: {desc}")
    print("...")
    print()
    
    print("Demo completed! Check the output files:")
    print(f"- High salary employees: {output_file}")
    print(f"- JSON format: {json_output}")
    print(f"- Sorted by age: {sorted_output}")


def cleanup_demo_files():
    """Clean up demo output files."""
    demo_files = [
        "high_salary.csv",
        "sample_data.json",
        "sorted_by_age.csv"
    ]
    
    for filename in demo_files:
        filepath = Path(__file__).parent / filename
        if filepath.exists():
            filepath.unlink()
            print(f"Removed: {filepath}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="VisiData MCP Server Demo")
    parser.add_argument("--cleanup", action="store_true", help="Clean up demo output files")
    args = parser.parse_args()
    
    if args.cleanup:
        cleanup_demo_files()
    else:
        demo_basic_operations() 