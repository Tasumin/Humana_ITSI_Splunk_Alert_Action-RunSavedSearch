import sys
import time
import json

def process_events(events):
    """
    Process all events after sleeping for the specified duration.
    """
    for event in events:
        event["status"] = f"Processed after sleeping for {sleep_time} seconds"
        yield event

if __name__ == "__main__":
    try:
        # Parse arguments
        sleep_time = 0  # Default sleep time
        for arg in sys.argv[1:]:
            if "=" in arg:
                key, value = arg.split("=", 1)
                if key == "sleep_time":
                    sleep_time = int(value)  # Convert sleep time to an integer

        # Sleep once for the specified duration
        time.sleep(sleep_time)

        # Read all events from stdin
        events = []
        for line in sys.stdin:
            try:
                event = json.loads(line.strip())  # Read and parse event as JSON
                events.append(event)
            except json.JSONDecodeError:
                print(json.dumps({"error": "Invalid JSON event"}), file=sys.stderr)

        # Process and output all events
        for processed_event in process_events(events):
            print(json.dumps(processed_event))  # Output processed event to stdout

    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)
