from datetime import datetime, timezone, timedelta
#file with all the fn related to the fetching of mails and summarizing of the mails

import calendar
from tkinter import ttk
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

SCOPES = ['https://www.googleapis.com/auth/calendar']


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


def read_emails(User_Creds):
    
  
    events = []
    time_responses = []
    discriptions = []
    disc_dict = {}
    start_time_dict = {}
    end_time_dict = {}
    canCalendar = {}

    # Access Gmail messages via POP3
    with MailBox("pop.gmail.com").login(User_Creds[0],User_Creds[1], "Inbox") as mb:
        for message in mb.fetch(limit=3, reverse=True, mark_seen=False):
            # Extract the unique message ID (assuming Gmail messages sync via POP3)
            message_id = message.uid  # For POP3, this is typically a unique message identifier

            # Get the email snippet or part of the body (using the POP3 object)
            snippet = message.text or 'No snippet available'

            # Summarize the event details from the snippet
            small_response = model.generate_content(f"You are an assistant that summarizes event details from emails. Summarise the following in 3 to 5 words :{snippet}")
            discription_response = model.generate_content(f"You are an assistant that summarizes event details from emails. Summarise the following in 200 words and write all the links in the text at the bottom with labels and also write event start and end time{snippet}")
            time_response_start_res = model.generate_content(f'Find the start date and time of this event and give it back to me in YYYY-MM-DDTHH:MM:SS format dont put any text in it and respond with only the dates and time, in case that there is no start date or time respond with the word empty: {snippet} ')
            time_response_end_res = model.generate_content(f'Find the end date and time of this event and give it back to me in YYYY-MM-DDTHH:MM:SS format dont put any text in it and respond with only the dates and time, in case that there is no end date or time respond with the word empty: {snippet} ')
            timeResST = time_response_start_res.text
            timeResEN = time_response_end_res.text
            time_response_start = (timeResST).replace(' \n','')
            time_response_end = (timeResEN).replace(' \n','')
            index_ = small_response.text
    



            if time_response_end == time_response_start:
                time_response_end = 'empty'

            if time_response_end != 'empty' and time_response_start != 'empty':
                canCalendar[index_] = True

            elif time_response_start == 'empty' and time_response_end == 'empty':
                canCalendar[index_] = False

            elif time_response_end == 'empty' and time_response_start != 'empty':
                tempVar = datetime.fromisoformat(time_response_end)
                tempVar2 = tempVar + timedelta(days=1)
                time_response_end = tempVar2.isoformat
                canCalendar[index_] = True
            else:
                canCalendar = False
            
            # Get the received date of the email

            print(f'start :{time_response_start} and end :{time_response_end}')

            if time_response_start != 'empty':
                # Convert to timestamp in milliseconds
                oneLineResponse = small_response.text
                print(oneLineResponse)
                events.append((oneLineResponse))

                # Example datetime object with timezone info
                dt = datetime.strptime(time_response_start,"%Y-%m-%dT%H:%M:%S")
                # Convert to the desired format: YYYY-MM-DD HH:MM:SS.ffffff
                formatted_dt = dt.strftime("%Y-%m-%d %H:%M:%S.%f")
                print(formatted_dt)

                time_responses.append(formatted_dt)

                start_time_dict[oneLineResponse] = time_response_start
                end_time_dict[oneLineResponse] = time_response_end
                disc_dict[oneLineResponse] = discription_response.text
            else:
                # Log if no date is found for debugging purposes
                print(f"No date found for message ID {message_id}")

        
        # Sort the events by internalDate in descending order (most recent first)
        events.sort(key=lambda event: event[1], reverse=True)
        print(events)
        print('this is time responcse',time_responses)

    # Initialize empty dictionary
    # Loop through both lists together
    events_dict = {}

    
        



    for (event, timestamp) in (zip(events, time_responses)):
        date = datetime.fromisoformat(timestamp).date()
        date_tuple = (date.year, date.month, date.day)
        if date_tuple not in events_dict:
            events_dict[date_tuple] = [event]
        elif date_tuple in events_dict:
            events_dict[date_tuple] = ((events_dict[date_tuple]) + [event])

    print(events_dict)
    print(disc_dict)
    print(start_time_dict)
    print(end_time_dict)
    print(canCalendar)
    return events_dict , disc_dict  ,start_time_dict ,end_time_dict , canCalendar


def mainFn(events_dict,disc_dict,timeDict_start,timeDict_end,canCalendar):
    root = tk.Tk()
    root.title("Event Calendar")
    root.state('zoomed')  # Set window to maximized (instead of fullscreen)
    root.configure(bg="#1f1f1f")  # Dark background

    # Dark theme colors
    bg_color = "#1f1f1f"  # Dark background
    fg_color = "#ffffff"  # White text
    button_bg = "#333333"  # Dark button background
    event_button_bg = "#003366"  # Dark blue for event days

    # Dictionary to store event information for each day

    # Variable to keep track of the currently selected date
    selected_day = None

    # Get current month and year
    current_year = datetime.now().year
    current_month = datetime.now().month
    current_day = datetime.now().day

    # Function to update the preview section
    def update_preview(day):
        global selected_day, current_month, current_year
        selected_day = day  # Keep track of the selected day
        date_key = (current_year, current_month, day)
        events = events_dict.get(date_key, [])

        # Clear the existing preview frame
        for widget in preview_frame.winfo_children():
            widget.destroy()

        # Display the selected date
        tk.Label(preview_frame, text=f"Selected Date: {day} {calendar.month_name[current_month]}, {current_year}",
                 bg=bg_color, fg=fg_color, font=("Arial", 14)).grid(row=0, column=0, columnspan=3, pady=10)

        if events:
            for idx, event in enumerate(events):
                event_frame = tk.Frame(preview_frame, bg=bg_color)
                event_frame.grid(row=idx + 1, column=0, sticky="w", padx=5, pady=5)

                # Display the event as a label
                event_label = tk.Label(event_frame, text=event, bg=bg_color, fg=fg_color, font=("Arial", 12))
                event_label.grid(row=idx, column=5, sticky="w", padx=10)

                # Create a tick button for confirming the event
                tick_button = tk.Button(event_frame, text="✔", width=2, bg="green", fg=fg_color,
                                        command=lambda ev=event: confirm_event(date_key, ev))
                tick_button.grid(row=idx, column=1, sticky="w", padx=5)

                # Create a cross button for deleting the event
                cross_button = tk.Button(event_frame, text="✘", width=2, bg="red", fg=fg_color,
                                         command=lambda ev=event: cancel_event(date_key, ev))
                cross_button.grid(row=idx, column=4, sticky="w", padx=5)

        else:
            # Display "No events" if no events are present for the selected day
            tk.Label(preview_frame, text="No events", bg=bg_color, fg=fg_color, font=("Arial", 12)).grid(row=1, column=4)

    # Function to confirm event selection
    def confirm_selection(day_btn, day):
        global current_month, current_year
        day_btn.config(bg="blue")  # Change button color to blue
        event = f"Event on {day} {calendar.month_name[current_month]}"
        date_key = (current_year, current_month, day)

        if date_key not in events_dict:
            events_dict[date_key] = []  # Initialize a list for multiple events
        events_dict[date_key].append(event)  # Append the event to the list

        update_preview(day)

##################################################################################################################

    # Function to confirm an event
    def confirm_event(date_key, event):
        print(f"Confirmed: {event} on {date_key}")
        index = event
        if canCalendar[index] == True:
            add_event_to_calendar(disc_dict[index],timeDict_start[index],timeDict_end[index])
        else:
            print('Cannot add event with no set duration')


##################################################################################################################

    # Function to cancel an individual event
    def cancel_event(date_key, event):
        if date_key in events_dict and event in events_dict[date_key]:
            events_dict[date_key].remove(event)
            print(f"Cancelled: {event} on {date_key}")
            if not events_dict[date_key]:  # If no more events, remove the key from the dict
                del events_dict[date_key]
            update_preview(selected_day)

    # Create a frame for the calendar grid
    grid_frame = tk.Frame(root, bg=bg_color)
    grid_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    # Create labels for days of the week
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i, day in enumerate(days):
        tk.Label(grid_frame, text=day, bg=bg_color, fg=fg_color, font=("Arial", 16)).grid(row=0, column=i, padx=5, pady=5)

    # Display the current date in the top right corner
    current_date_label = tk.Label(grid_frame, text=f"{datetime.now().strftime('%Y-%m-%d')}", bg=bg_color, fg=fg_color, font=("Arial", 16))
    current_date_label.grid(row=0, column=6, padx=5, pady=5, sticky='ne')

    # Function to create the day buttons
    def create_day_buttons(month, year):
        global current_month, current_year
        # Clear the previous buttons
        for widget in grid_frame.winfo_children()[7:]:
            widget.destroy()

        # Get the first weekday and number of days
        first_weekday, num_days = calendar.monthrange(year, month)

        day = 1
        row = 1
        col = first_weekday

        while day <= num_days:
            date_key = (year, month, day)
            event_summary = "\n".join(events_dict.get(date_key, []))  # Get event summary

            # Determine button background color
            btn_bg = event_button_bg if date_key in events_dict else button_bg

            day_btn = tk.Button(grid_frame, text=f"{day}\n{event_summary}", width=8, height=3,  # Button size
                                bg=btn_bg, fg=fg_color, highlightbackground="white",
                                bd=1, relief="solid", command=lambda day=day: update_preview(day))
            day_btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")  # Make buttons stretchable

            # Bind right-click and middle-click events
            day_btn.bind("<Button-3>", lambda e, day_btn=day_btn, day=day: confirm_selection(day_btn, day))
            day_btn.bind("<Button-2>", lambda e, day_btn=day_btn, day=day: cancel_selection(day_btn, day))

            day += 1
            col += 1
            if col > 6:
                col = 0
                row += 1

    # Initial call to create buttons for the current month and year
    create_day_buttons(current_month, current_year)

    # Create a dropdown to filter events
    filter_label = tk.Label(root, text="Filter:", bg=bg_color, fg=fg_color, font=("Arial", 14))
    filter_label.pack(side=tk.LEFT, padx=20)

    filter_var = tk.StringVar()
    filter_options = ["Events", "Sports", "Internship Opportunity", "Competitions", "Gravitas", "Rivera", "CAT", "Other"]
    filter_dropdown = ttk.Combobox(root, textvariable=filter_var, values=filter_options)
    filter_dropdown.pack(side=tk.LEFT, padx=10)
    filter_dropdown.configure(background="#333333", foreground="white", state='readonly')

    # Dropdowns for month and year selection
    def update_calendar(event):
        global current_month, current_year
        current_month = list(calendar.month_name).index(month_var.get())
        current_year = year_var.get()
        create_day_buttons(current_month, current_year)

    # Initialize month and year dropdowns with current values
    month_var = tk.StringVar(value=calendar.month_name[current_month])
    month_dropdown = ttk.Combobox(root, textvariable=month_var, values=list(calendar.month_name)[1:])
    month_dropdown.pack(side=tk.LEFT, padx=10)
    month_dropdown.bind("<<ComboboxSelected>>", update_calendar)
    month_dropdown.configure(background="#333333", foreground="white", state='readonly')

    year_var = tk.IntVar(value=current_year)
    year_dropdown = ttk.Combobox(root, textvariable=year_var, values=list(range(current_year - 10, current_year + 10)))
    year_dropdown.pack(side=tk.LEFT, padx=10)
    year_dropdown.bind("<<ComboboxSelected>>", update_calendar)
    year_dropdown.configure(background="#333333", foreground="white", state='readonly')

    # Create a preview section
    preview_frame = tk.Frame(root, bg=bg_color)
    preview_frame.pack(pady=20, fill=tk.X)

    # Configure grid frame to expand
    grid_frame.columnconfigure(tuple(range(7)), weight=1)  # Make columns stretchable
    grid_frame.rowconfigure(tuple(range(1, 7)), weight=1)  # Make rows stretchable

    # Run the application
    root.mainloop()

def authenticate_google(path):
    creds = None
    # Check if token.json exists (used to store credentials between sessions)
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Run OAuth2 flow for first-time authentication
            flow = InstalledAppFlow.from_client_secrets_file(
                path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds


def add_event_to_calendar(event_summary,start_time,end_time):
    creds = authenticate_google(r'C:\Users\krish\Desktop\hack\emailreader\working\credentials.json')
    service = build('calendar', 'v3', credentials=creds)
    
    event = {
        'summary': event_summary,
        'start': {
            'dateTime': start_time,
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'UTC',
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f"Event created: {event.get('htmlLink')}")
# Call the function to run the calendar application



# print(authenticate_google(r'C:\Users\krish\Desktop\hack\emailreader\working\credentials.json'))
# add_event_to_calendar('event try')