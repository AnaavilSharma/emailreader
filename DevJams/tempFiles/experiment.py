import datetime

def create_event_dict(event_list, timestamp_list):
  """Creates a dictionary of events keyed by date tuples.

  Args:
    event_list: A list of event descriptions.
    timestamp_list: A list of timestamps in ISO 8601 format.

  Returns:
    A dictionary where keys are date tuples (year, month, day) and values
    are event descriptions.
  """

  events_dict = {}
  for event, timestamp in zip(event_list, timestamp_list):
    date = datetime.datetime.fromisoformat(timestamp).date()
    date_tuple = (date.year, date.month, date.day)
    events_dict[date_tuple] = event.strip()
  return events_dict

# Example usage
list1 = ['Python hackathon for engineering students. \n', 'Futsal tournament postponed, new date TBA. \n', "Art competition registration for graVITas '24. \n", 'Welcome to Google AI Studio. \n', 'Accenture Innovation Challenge: AI for Business \n', 'VIT sports events today. \n', "PCB Design Workshop at graVITas'24 \n"]
list2 = ['2024-09-21 15:00:03.000000', '2024-09-21 10:54:47.000000', '2024-09-21 09:43:47.000000', '2024-08-21 08:15:07.000000', '2024-06-20 23:55:49.000000', '2024-07-20 20:34:43.000000', '2024-09-20 07:14:55.000000']

events_dict = create_event_dict(list1, list2)
print(events_dict)