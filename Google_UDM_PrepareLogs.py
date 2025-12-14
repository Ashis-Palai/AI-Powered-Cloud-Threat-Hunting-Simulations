import os
import json
import argparse

def load_all_json_files(directory):
    events = []

    for file_name in os.listdir(directory):
        if file_name.endswith(".json") and "inline" not in file_name.lower():
            full_path = os.path.join(directory, file_name)
            
            try:
                with open(full_path, "r") as f:
                    content = f.read().strip()
                    
                    # Handle multiple objects not in a list (split by newlines)
                    if content.startswith("{") and not content.startswith("["):
                        # Try splitting by lines
                        try:
                            objects = [json.loads(line) for line in content.splitlines() if line.strip()]
                            events.extend(objects)
                        except json.JSONDecodeError:
                            # Fallback: single object
                            events.append(json.loads(content))
                    else:
                        # Standard JSON (list or single object)
                        data = json.loads(content)
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
        description="Merge all JSON files from a folder into one JSON list, excluding files with 'inline'."
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
