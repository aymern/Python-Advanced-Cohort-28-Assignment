import os
from datetime import datetime, timedelta

# Custom Exception
class DuplicateVisitorError(Exception):
    pass

class TooSoonError(Exception):
    pass

def log_visitor():
    filename = "visitors.txt"
    visitor_name = input("Enter visitor's name: ").strip()

    try:
        # Create file if it doesn't exist
        if not os.path.exists(filename):
            with open(filename, "w", encoding="utf-8") as f:
                pass

        last_name = None
        last_time = None

        # Read the last line of the file
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
            if lines:
                last_line = lines[-1].strip()
                # The format is "Name - Timestamp"
                parts = last_line.split(" - ")
                if len(parts) == 2:
                    last_name, last_timestamp = parts
                    last_time = datetime.strptime(last_timestamp, "%Y-%m-%d %H:%M:%S")

        # Check for duplicate visitor
        if last_name and visitor_name.lower() == last_name.lower():
            raise DuplicateVisitorError(f"Duplicate visitor detected: {visitor_name}")

        # Check 5-minute rule
        if last_time:
            if datetime.now() < last_time + timedelta(minutes=5):
                remaining = (last_time + timedelta(minutes=5)) - datetime.now()
                raise TooSoonError(
                    f"New visitors are not allowed yet. Please wait {remaining.seconds // 60} min {remaining.seconds % 60} sec."
                )

        # Append visitor name with timestamp
        with open(filename, "a", encoding="utf-8") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{visitor_name} - {timestamp}\n")
        print(f"{visitor_name} logged successfully! on {timestamp}")

    except DuplicateVisitorError as e:
        print("Error:", e)
    except TooSoonError as e:
        print("Error:", e)
    except Exception as e:
        print("An unexpected error occurred:", e)

log_visitor()