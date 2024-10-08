from datetime import datetime


events_list = ['Python hackathon, November 8-10. \n', 'Futsal tournament postponed, new date TBA. \n', 'Accenture Innovation Challenge: AI for Business \n']
timestamps_list = ['2024-09-21 15:00:03.000000', '2024-09-21 10:54:47.000000', '2024-09-21 09:43:47.000000']

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
