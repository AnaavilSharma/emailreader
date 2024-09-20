import os
import
import tkinter as tk
from tkinter import messagebox
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from datetime import datetime, timedelta

# ai ki api 

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/calendar']

def authenticate_google():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def read_emails():
    creds = authenticate_google()
    service = build('gmail', 'v1', credentials=creds)
    result = service.users().messages().list(userId='me', q="subject:event OR subject:meeting").execute()
    messages = result.get('messages', [])
    
    events = []
    for message in messages[:100]:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        snippet = msg.get('snippet')
        event_summary = summarize_event(snippet)
        events.append(event_summary)
    return events

def summarize_event(snippet):
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=f"Summarize the following event email snippet: {snippet}",
        max_tokens=50
    )
    return response.choices[0].text.strip()

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


class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")

        self.create_widgets()

    def create_widgets(self):
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
            self.root.destroy()
            run_event_app()
        else:
            messagebox.showerror("Error", "Please enter both email and password.")


entApp:
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


def run_event_app():
    events = read_emails()
    if not events:
        print("No events found.")
        return
    
    root = tk.Tk()
    app = EventApp(root, events)
    root.mainloop()

def main():
    root = tk.Tk()
    login_app = LoginApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()


