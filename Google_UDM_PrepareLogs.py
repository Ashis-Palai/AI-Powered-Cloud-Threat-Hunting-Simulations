import os
import json
import argparse

def load_all_json_files(directory):
    events = []

    for file_name in os.listdir(directory):
        if file_name.endswith(".json"):
            full_path = os.path.join(directory, file_name)

            try:
                with open(full_path, "r") as f:
                    data = json.load(f)

                    # Each JSON file may contain a single object or a list
                    if isinstance(data, list):
                        events.extend(data)
                    else:
                        events.append(data)

                print(f"[+] Loaded: {file_name}")

            except Exception as e:
                print(f"[!] Failed to load {file_name}: {e}")

    return events


def save_merged(events, output_file):
    with open(output_file, "w") as f:
        json.dump(events, f, indent=2)
    print(f"\n[Merged JSON Saved] → {output_file}")
    print(f"[Total Events] → {len(events)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Merge all JSON files from json_data_Google folder into one JSON list."
    )

    parser.add_argument(
        "--directory",
        default="json_data_Google",
        help="Folder containing multiple JSON files."
    )

    parser.add_argument(
        "--output",
        default="merged_events.json",
        help="Name of the combined output JSON file."
    )

    args = parser.parse_args()

    all_events = load_all_json_files(args.directory)
    save_merged(all_events, args.output)
