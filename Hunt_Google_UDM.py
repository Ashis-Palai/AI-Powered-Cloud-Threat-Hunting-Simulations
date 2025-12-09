import json
import argparse
import re
from datetime import datetime

# ------------------------------------------------------------
# Deep extractor for ANY nested JSON structure
# ------------------------------------------------------------
def deep_get(data, field_path):
    """Extract a nested field using dot notation (works with lists & dicts)."""
    keys = field_path.split(".")
    current = [data]

    for key in keys:
        next_level = []
        for item in current:
            if isinstance(item, dict) and key in item:
                next_level.append(item[key])
            elif isinstance(item, list):
                for sub in item:
                    if isinstance(sub, dict) and key in sub:
                        next_level.append(sub[key])
        current = next_level
        if not current:
            return None

    return current[0] if len(current) == 1 else current

# ------------------------------------------------------------
# Timestamp parsing & comparison
# ------------------------------------------------------------
def parse_timestamp(ts):
    """Convert timestamp string to datetime object."""
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except Exception:
        return None

def compare_values(event_value, operator, expected_value):
    """Compare two timestamp strings with operator."""
    ev = parse_timestamp(event_value)
    ex = parse_timestamp(expected_value)

    if ev is None or ex is None:
        return False

    if operator == ">":
        return ev > ex
    elif operator == "<":
        return ev < ex
    elif operator == ">=":
        return ev >= ex
    elif operator == "<=":
        return ev <= ex
    else:
        return ev == ex  # fallback equality

# ------------------------------------------------------------
# Mandatory AND conditions
# ------------------------------------------------------------
def satisfies_mandatory(event, mandatory_dict, mandatory_ops):
    # Standard equality checks
    for field, expected in mandatory_dict.items():
        value = deep_get(event, field)
        if value != expected:
            return False

    # Operator-based checks (timestamps)
    for field, (operator, expected_value) in mandatory_ops.items():
        value = deep_get(event, field)
        if value is None or not compare_values(value, operator, expected_value):
            return False

    return True

# ------------------------------------------------------------
# Optional OR conditions
# ------------------------------------------------------------
def satisfies_optional_contains(event, contains_list):
    if not contains_list:
        return True  # If none provided, treat as pass

    for field, keyword in contains_list:
        value = deep_get(event, field)
        if value and keyword.lower() in str(value).lower():
            return True
    return False

# ------------------------------------------------------------
# Main hunting function
# ------------------------------------------------------------
def hunt(events, mandatory_conditions, optional_contains, mandatory_ops, output_fields):
    results = []

    for event in events:

        # Mandatory AND logic
        if not satisfies_mandatory(event, mandatory_conditions, mandatory_ops):
            continue

        # Optional OR logic
        if not satisfies_optional_contains(event, optional_contains):
            continue

        # Build output dictionary
        output_entry = {field: deep_get(event, field) for field in output_fields}
        results.append(output_entry)

    return results

# ------------------------------------------------------------
# CLI parsing logic
# ------------------------------------------------------------
def parse_cli():
    parser = argparse.ArgumentParser(description="Unified UDM Hunting Engine (CLI-enabled)")

    parser.add_argument("--events", required=True,
                        help="Path to JSON file containing the list of UDM events")
    parser.add_argument("--mandatory", action="append", default=[],
                        help="Mandatory AND conditions: field=value")
    parser.add_argument("--mandatory-op", action="append", default=[],
                        help="Mandatory operator conditions (timestamps): field>=value, field<=value, field>value, field<value")
    parser.add_argument("--contains", action="append", default=[],
                        help="Optional OR substring match: field=subvalue")
    parser.add_argument("--output", action="append", default=[],
                        help="Fields to return from matching events")

    return parser.parse_args()

# ------------------------------------------------------------
# Convert CLI flags into dicts/lists
# ------------------------------------------------------------
def parse_conditions(mandatory_list, contains_list, mandatory_ops_list):
    mandatory_dict = {}
    contains_pairs = []
    mandatory_ops = {}

    # Parse mandatory equality conditions
    for item in mandatory_list:
        if "=" not in item:
            raise ValueError(f"Invalid mandatory condition format: {item}")
        field, value = item.split("=", 1)
        mandatory_dict[field] = value

    # Parse operator-based conditions
    for item in mandatory_ops_list:
        operator = None
        for op in [">=", "<=", ">", "<"]:
            if op in item:
                operator = op
                break
        if not operator:
            raise ValueError(f"Invalid operator mandatory condition: {item}")
        field, value = item.split(operator, 1)
        mandatory_ops[field] = (operator, value)

    # Parse optional contains conditions
    for item in contains_list:
        if "=" not in item:
            raise ValueError(f"Invalid contains condition format: {item}")
        field, value = item.split("=", 1)
        contains_pairs.append((field, value))

    return mandatory_dict, contains_pairs, mandatory_ops

# ------------------------------------------------------------
# Main entry point
# ------------------------------------------------------------
if __name__ == "__main__":

    args = parse_cli()

    # Load event JSON file
    with open(args.events, "r") as f:
        events = json.load(f)

    # Parse CLI conditions
    mandatory_conditions, optional_contains, mandatory_ops = parse_conditions(
        args.mandatory, args.contains, args.mandatory_op
    )

    # Run hunt
    results = hunt(
        events=events,
        mandatory_conditions=mandatory_conditions,
        optional_contains=optional_contains,
        mandatory_ops=mandatory_ops,
        output_fields=args.output
    )

    # Display results
    print("\n=== HUNT RESULTS ===")
    for entry in results:
        print(json.dumps(entry, indent=2))
