from datetime import datetime, timezone, timedelta
#file with all the fn related to the fetching of mails and summarizing of the mails


import os
import tkinter as tk
import google.generativeai as palm
from tkinter import messagebox
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from datetime import datetime, timedelta
from imap_tools import MailBox

palm.configure(api_key="AIzaSyDnAEmnXo1nfb4dQY-IQZg6L8kpfEUiDDg")
model=palm.GenerativeModel('gemini-1.5-flash-latest')
# If modifying these SCOPES, delete the token.json file.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/calendar']



# Function to retrieve stored email credentials
def retrieve_email_credentials(user_file):
    users_file = 'users.txt'  # The file containing user credentials
    email = None
    password = None

    if os.path.exists(users_file):
        try:
            with open(users_file, 'r') as f:
                # Iterate through each line and split by comma to get username, password, and path
                for line in f:
                    line = line.strip()
                    if line:
                        username, pwd, pat = line.split(',')
                        email = username
                        password = pwd
                        path = pat
                        # You can break if you want to stop after the first user
                        break  # Remove this if you want to process all users
        except IOError as e:
            print(f"Error reading {users_file}: {e}")
    else:
        print(f"{users_file} file not found.")
    
    # Return the email and password values
    return email, password ,path


#to trobleshoot when switching btw accounts

# def temp():
#     flow = InstalledAppFlow.from_client_secrets_file(
#     r'C:\Krishna\Application\Vs Code ka Code\Hackathon\credentials.json', SCOPES)
#     creds = flow.run_local_server(port=0)
#         # Save the credentials for the next run
#     with open('token.json', 'w') as token:
#         token.write(creds.to_json())
# temp()
# Google Authentication for Gmail and Calendar










def read_emails(user_info):
    
  
    events = []
    time_responses = []
    discriptions = []


    # Access Gmail messages via POP3
    with MailBox("pop.gmail.com").login(user_info[0], user_info[1], "Inbox") as mb:
        for message in mb.fetch(limit=3, reverse=True, mark_seen=False):
            # Extract the unique message ID (assuming Gmail messages sync via POP3)
            message_id = message.uid  # For POP3, this is typically a unique message identifier

            # Get the email snippet or part of the body (using the POP3 object)
            snippet = message.text or 'No snippet available'

            # Summarize the event details from the snippet
            small_response = model.generate_content(f"You are an assistant that summarizes event details from emails. Summarise the following in 3 to 5 words :{snippet}")
            discription_response = model.generate_content(f"You are an assistant that summarizes event details from emails. Summarise the following in 200 words :{snippet}")
            time_response = message.date
            # Get the received date of the email
            internal_date = message.date

            if internal_date:
                # Convert to timestamp in milliseconds
                events.append((small_response.text))

                # Example datetime object with timezone info
                dt = (time_response)

                # Convert to the desired format: YYYY-MM-DD HH:MM:SS.ffffff
                formatted_dt = dt.strftime("%Y-%m-%d %H:%M:%S.%f")

                time_responses.append(formatted_dt)

                discriptions.append(discription_response.text)
            else:
                # Log if no date is found for debugging purposes
                print(f"No date found for message ID {message_id}")

        # Sort the events by internalDate in descending order (most recent first)
        events.sort(key=lambda event: event[1], reverse=True)

    # Return only the event summaries (sorted)
    print(events)
    print(time_responses)
    print(discriptions)


    # Initialize empty dictionary
    events_dict = {}

    # Loop through both lists together
    for event, timestamp in zip(events, time_responses):
        # Parse the timestamp string into a datetime object
        dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
        
        # Extract year, month, and day as a tuple
        date_key = (dt.year, dt.month, dt.day)
        
        # Add the event to the dictionary under the appropriate date
        if date_key not in events_dict:
            events_dict[date_key] = []  # Initialize a list for the date if not already present
        
        events_dict[date_key].append(event.strip())  # Strip trailing newline characters and add the event




def authenticate_google(path):
    creds = None
    # Check if token.json exists (used to store credentials between sessions)
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Run OAuth2 flow for first-time authentication
            flow = InstalledAppFlow.from_client_secrets_file(
                f'r({path})', SCOPES)                                                          # path dalna hai
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds


# Function to add event to Google Calendar
def add_event_to_calendar(event_summary):
    creds = authenticate_google()
    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': event_summary,
        'start': {
            'dateTime': (datetime.now() + timedelta(days=1)).isoformat(),
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': (datetime.now() + timedelta(days=1, hours=1)).isoformat(),
            'timeZone': 'UTC',
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f"Event created: {event.get('htmlLink')}")


read_emails(retrieve_email_credentials(user_file='user.txt'))