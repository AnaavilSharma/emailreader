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
model = palm.GenerativeModel('gemini-1.5-flash-latest')
# If modifying these SCOPES, delete the token.json file.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/calendar']

CREDENTIALS_FILE = 'credentials.txt'


# fast api local db sqllite
# Function to store email credentials
def store_email_credentials(email, password):
    with open(CREDENTIALS_FILE, 'w') as f:
        f.write(f"{email}\n{password}")


# Function to retrieve stored email credentials
def retrieve_email_credentials():
    if os.path.exists(CREDENTIALS_FILE):
        try:
            with open(CREDENTIALS_FILE, 'r') as f:
                lines = f.readlines()
                if len(lines) >= 2:
                    email = lines[0].strip()
                    password = lines[1].strip()
                    return email, password
                else:
                    print("Error: Invalid credentials format in the file.")
        except IOError as e:
            print(f"Error reading credentials file: {e}")
    else:
        print("Credentials file not found.")
    return None, None


# Google Authentication for Gmail and Calendar
def authenticate_google():
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
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds


def read_emails():
    creds = retrieve_email_credentials()

    # Get messages via Gmail API based on the query

    events = []

    # Access Gmail messages via POP3
    with MailBox("pop.gmail.com").login(creds[0], 'camx nufx yryj nvac', "Inbox") as mb:
        for message in mb.fetch(reverse=True, mark_seen=False):
            # Extract the unique message ID (assuming Gmail messages sync via POP3)
            message_id = message.uid  # For POP3, this is typically a unique message identifier

            # Get the email snippet or part of the body (using the POP3 object)
            snippet = message.text or 'No snippet available'
            print(snippet)
            try:
                with open("Email.txt", "a", encoding="utf-8") as f:
                    f.write(str(snippet) + "#\#")
            except Exception as e:
                print(f"Error writing to file: {e}")
            # Summarize the event details from the snippet
            #event_summary = summarize_event(snippet)

            # Get the received date of the email
            internal_date = message.date

    #         if internal_date:
    #             # Convert to timestamp in milliseconds
    #             internal_date = int(internal_date.timestamp() * 1000)
    #             events.append((event_summary, internal_date))
    #         else:
    #             # Log if no date is found for debugging purposes
    #             print(f"No date found for message ID {message_id}")
    #
    #     # Sort the events by internalDate in descending order (most recent first)
    #     events.sort(key=lambda event: event[1], reverse=True)
    #
    # # Return only the event summaries (sorted)
    # return [event[0] for event in events]


# Use Gemini (PaLM API) to summarize event details
def summarize_event(snippet):
    try:
        response = model.generate_content(
            f"You are an assistant that summarizes event details from emails. Summarise the following:{snippet}", )
        ##print(response.text)
        return response.text
    except:
        print("Gemini API error trying again")
        summarize_event(snippet)


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


# GUI for user login
class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")

        # Hide the main login window initially
        self.root.withdraw()

        # Ask if user wants to retrieve or input new credentials
        self.ask_credentials_window()

    def ask_credentials_window(self):
        # Create a window to ask whether to use stored or new credentials
        self.ask_window = tk.Toplevel(self.root)
        self.ask_window.title("Credentials")
        tk.Label(self.ask_window, text="Do you want to use stored credentials or enter new ones?").pack(pady=10)

        tk.Button(self.ask_window, text="Use Stored Credentials", command=self.use_stored_credentials).pack(pady=5)
        tk.Button(self.ask_window, text="Enter New Credentials", command=self.new_credentials_form).pack(pady=5)

    def use_stored_credentials(self):
        email, password = retrieve_email_credentials()
        if email and password:
            self.ask_window.destroy()
            messagebox.showinfo("Success", f"Using stored credentials for {email}.")
            run_event_app()  # Proceed with the app after using stored credentials
        else:
            messagebox.showerror("Error", "No stored credentials found. Please enter new credentials.")
            self.ask_window.destroy()
            self.new_credentials_form()

    def new_credentials_form(self):
        # Close the credentials window
        self.ask_window.destroy()

        # Show the main window for entering new credentials
        self.root.deiconify()

        tk.Label(self.root, text="Enter your Gmail credentials").pack(pady=10)

        tk.Label(self.root, text="Email:").pack()
        self.email_entry = tk.Entry(self.root, width=30)
        self.email_entry.pack()

        tk.Label(self.root, text="Password:").pack()
        self.password_entry = tk.Entry(self.root, show="*", width=30)
        self.password_entry.pack()

        tk.Button(self.root, text="Submit", command=self.submit_credentials).pack(pady=20)

    def submit_credentials(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if email and password:
            save_credentials = messagebox.askyesno("Save Credentials",
                                                   "Do you want to save these credentials for future use?")
            if save_credentials:
                store_email_credentials(email, password)
                messagebox.showinfo("Saved", "Credentials have been saved.")
            self.root.destroy()
            run_event_app()
        else:
            messagebox.showerror("Error", "Please enter both email and password.")
# Event App to display and add events to the calendar
class EventApp:
    def __init__(self, root, events):
        self.root = root
        self.root.title("Event Manager")
        self.events = events

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Here are your upcoming events:").pack()

        self.event_var = tk.StringVar(value="")

        for event in self.events:
            frame = tk.Frame(self.root)
            frame.pack(pady=5)

            label = tk.Label(frame, text=event, wraplength=400, justify="left")
            label.pack(side="left", padx=10)

            yes_button = tk.Button(frame, text="Yes", command=lambda ev=event: self.add_event(ev))
            yes_button.pack(side="right", padx=5)

            no_button = tk.Button(frame, text="No", command=frame.destroy)
            no_button.pack(side="right")

    def add_event(self, event_summary):
        add_event_to_calendar(event_summary)
        messagebox.showinfo("Event Added", f"Event '{event_summary}' has been added to your calendar!")
        self.root.quit()


# Function to run the Event Manager after login
def run_event_app():
    events = read_emails()
    if not events:
        print("No events found.")
        return

    root = tk.Tk()
    app = EventApp(root, events)
    root.mainloop()


# Main function for starting the application
def main():
    root = tk.Tk()
    login_app = LoginApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
