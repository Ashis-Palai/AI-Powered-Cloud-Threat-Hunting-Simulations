import json
import argparse
import re


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
# Mandatory AND conditions
# ------------------------------------------------------------

def satisfies_mandatory(event, mandatory_dict):
    for field, expected in mandatory_dict.items():
        value = deep_get(event, field)
        if value != expected:
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

def hunt(events, mandatory_conditions, optional_contains, output_fields):
    results = []

    for event in events:

        # Mandatory AND logic
        if not satisfies_mandatory(event, mandatory_conditions):
            continue

        # Optional OR logic
        if not satisfies_optional_contains(event, optional_contains):
            continue

        # Build output dictionary
        output_entry = {
            field: deep_get(event, field)
            for field in output_fields
        }

        results.append(output_entry)

    return results


# ------------------------------------------------------------
# CLI parsing logic
# ------------------------------------------------------------

def parse_cli():
    parser = argparse.ArgumentParser(
        description="Unified UDM Hunting Engine (CLI-enabled)"
    )

    parser.add_argument(
        "--events",
        required=True,
        help="Path to JSON file containing the list of UDM events"
    )

    parser.add_argument(
        "--mandatory",
        action="append",
        default=[],
        help="Mandatory AND conditions: field=value"
    )

    parser.add_argument(
        "--contains",
        action="append",
        default=[],
        help="Optional OR substring match: field=subvalue"
    )

    parser.add_argument(
        "--output",
        action="append",
        default=[],
        help="Fields to return from matching events"
    )

    return parser.parse_args()


# ------------------------------------------------------------
# Convert CLI flags into dicts/lists
# ------------------------------------------------------------

def parse_conditions(mandatory_list, contains_list):
    mandatory_dict = {}
    contains_pairs = []

    # Parse mandatory AND conditions
    for item in mandatory_list:
        if "=" not in item:
            raise ValueError(f"Invalid mandatory condition format: {item}")
        field, value = item.split("=", 1)
        mandatory_dict[field] = value

    # Parse optional OR contains conditions
    for item in contains_list:
        if "=" not in item:
            raise ValueError(f"Invalid contains condition format: {item}")
        field, value = item.split("=", 1)
        contains_pairs.append((field, value))

    return mandatory_dict, contains_pairs


# ------------------------------------------------------------
# Main entry point
# ------------------------------------------------------------

if __name__ == "__main__":

    args = parse_cli()

    # Load event JSON file
    with open(args.events, "r") as f:
        events = json.load(f)

    # Parse conditions from CLI flags
    mandatory_conditions, optional_contains = parse_conditions(
        args.mandatory, args.contains
    )

    # Run hunt
    results = hunt(
        events=events,
        mandatory_conditions=mandatory_conditions,
        optional_contains=optional_contains,
        output_fields=args.output
    )

    # Display results
    print("\n=== HUNT RESULTS ===")
    for entry in results:
        print(json.dumps(entry, indent=2))
