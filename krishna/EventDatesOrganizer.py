from datetime import datetime


# Initialize empty dictionary
events_dict = {}

# Loop through both lists together
for event, timestamp in zip(events_list, timestamps_list):
    # Parse the timestamp string into a datetime object
    dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
    
    # Extract year, month, and day as a tuple
    date_key = (dt.year, dt.month, dt.day)
    
    # Add the event to the dictionary under the appropriate date
    if date_key not in events_dict:
        events_dict[date_key] = []  # Initialize a list for the date if not already present
    
    events_dict[date_key].append(event.strip())  # Strip trailing newline characters and add the event

# Output the resulting dictionary
print(events_dict)
