import tkinter as tk
from tkinter import messagebox
import os
from GUI import mainFn

# File where users will be stored
USER_FILE = 'users.txt'

# Dark mode color variables
BG_COLOR = "#2e2e2e"  # Dark background
FG_COLOR = "#ffffff"  # Light text
BUTTON_BG_COLOR = "#3c3f41"  # Darker button background
BUTTON_FG_COLOR = "#ffffff"  # Light text on buttons
ENTRY_BG_COLOR = "#3c3f41"  # Entry box background
ENTRY_FG_COLOR = "#ffffff"  # Entry text color

# Load users from the file into a dictionary
def load_users():
    users = {}
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r') as file:
            for line in file:
                username, password, path = line.strip().split(',')
                users[username] = (password, path)
    return users

# Save a new user into the file
def save_user(username, password, path):
    with open(USER_FILE, 'a') as file:
        file.write(f'{username},{password},{path}\n')

# Remove a user from the file and the user list
def remove_user(username):
    users = load_users()
    if username in users:
        del users[username]  # Remove from dictionary
        with open(USER_FILE, 'w') as file:  # Rewrite the user file
            for user, (password, path) in users.items():
                file.write(f'{user},{password},{path}\n')
        return True
    else:
        messagebox.showwarning("Removal Failed", "User not found.")
        return False

# Function to open the Calendar App window
def open_calendar_app():
    mainFn()

# Function to handle login
def open_user_list():
    if not users:
        messagebox.showwarning("No Users", "No registered users available.")
        return

    user_list_window = tk.Toplevel(window)
    user_list_window.title("Select User")
    user_list_window.geometry("250x200")
    user_list_window.configure(bg=BG_COLOR)  # Dark mode

    label_select_user = tk.Label(user_list_window, text="Select a user to log in:", bg=BG_COLOR, fg=FG_COLOR)
    label_select_user.pack(pady=5)
    
    listbox = tk.Listbox(user_list_window, bg=ENTRY_BG_COLOR, fg=ENTRY_FG_COLOR)
    for user in users:
        listbox.insert(tk.END, user)
    listbox.pack(pady=5)

    def on_user_select(event):
        selected_user = listbox.get(listbox.curselection())
        if selected_user:
            messagebox.showinfo("Login", f"Login successful for user: {selected_user}")
            print(f"Logged into {selected_user}")
            user_list_window.destroy()  # Close user selection window
            window.destroy()  # Close the main login window
            open_calendar_app()  # Open Calendar App
        else:
            messagebox.showwarning("Login Failed", "Please select a user.")

    listbox.bind("<<ListboxSelect>>", on_user_select)

# Function to handle user registration
def register():
    username = entry_username.get()
    password = entry_password.get()
    path = entry_path.get()

    if username in users:
        messagebox.showwarning("Registration Failed", "Username already exists.")
    elif username == "" or password == "" or path == "":
        messagebox.showwarning("Registration Failed", "All fields are required.")
    else:
        users[username] = (password, path)
        save_user(username, password, path)
        messagebox.showinfo("Registration", "User Registered Successfully!")
        entry_username.delete(0, tk.END)
        entry_password.delete(0, tk.END)
        entry_path.delete(0, tk.END)

# Function to remove a user
def remove_user_dialog():
    if not users:
        messagebox.showwarning("No Users", "No registered users available.")
        return

    remove_user_window = tk.Toplevel(window)
    remove_user_window.title("Remove User")
    remove_user_window.geometry("250x200")
    remove_user_window.configure(bg=BG_COLOR)

    label_select_user = tk.Label(remove_user_window, text="Select a user to remove:", bg=BG_COLOR, fg=FG_COLOR)
    label_select_user.pack(pady=5)

    listbox = tk.Listbox(remove_user_window, bg=ENTRY_BG_COLOR, fg=ENTRY_FG_COLOR)
    for user in users:
        listbox.insert(tk.END, user)
    listbox.pack(pady=5)

    def on_user_select(event):
        selected_user = listbox.get(listbox.curselection())
        if selected_user:
            if messagebox.askyesno("Confirm", f"Are you sure you want to remove {selected_user}?"):
                if remove_user(selected_user):
                    listbox.delete(listbox.curselection())  # Remove from listbox
                    messagebox.showinfo("Success", f"User {selected_user} removed successfully.")
                else:
                    messagebox.showwarning("Failed", f"Failed to remove {selected_user}.")

    listbox.bind("<<ListboxSelect>>", on_user_select)

def refresh_user_list():
    global users
    users = load_users()

# Load existing users from the file
users = load_users()

# Creating the main window
window = tk.Tk()
window.title("Login Screen")
window.geometry("300x350")
window.configure(bg=BG_COLOR)  # Dark mode

label_username = tk.Label(window, text="Username:", bg=BG_COLOR, fg=FG_COLOR)
label_username.pack(pady=5)
entry_username = tk.Entry(window, bg=ENTRY_BG_COLOR, fg=ENTRY_FG_COLOR)
entry_username.pack(pady=5)

label_password = tk.Label(window, text="Password:", bg=BG_COLOR, fg=FG_COLOR)
label_password.pack(pady=5)
entry_password = tk.Entry(window, show='*', bg=ENTRY_BG_COLOR, fg=ENTRY_FG_COLOR)
entry_password.pack(pady=5)

label_path = tk.Label(window, text="Path:", bg=BG_COLOR, fg=FG_COLOR)
label_path.pack(pady=5)
entry_path = tk.Entry(window, bg=ENTRY_BG_COLOR, fg=ENTRY_FG_COLOR)
entry_path.pack(pady=5)

register_button = tk.Button(window, text="Register", bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR, command=register)
register_button.pack(pady=5)

login_button = tk.Button(window, text="Login", bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR, command=open_user_list)
login_button.pack(pady=5)

# Add Remove User button
remove_user_button = tk.Button(window, text="Remove User", bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR, command=remove_user_dialog)
remove_user_button.pack(pady=5)

# Run the application
window.mainloop()
