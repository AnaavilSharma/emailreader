import tkinter as tk
from tkinter import messagebox
import os

# File where the user will be stored
USER_FILE = 'users.txt'

# Dark mode color variables
BG_COLOR = "#2e2e2e"  # Dark background
FG_COLOR = "#ffffff"  # Light text
BUTTON_BG_COLOR = "#6A5ACD"  # Button background
BUTTON_FG_COLOR = "#ffffff"  # Button text
ENTRY_BG_COLOR = "#5A4B8A"  # Entry background
ENTRY_FG_COLOR = "#ffffff"  # Entry text color
WELCOME_TEXT_COLOR = "#f5f5f5"  # Matt white for welcome text

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Page")
        self.root.geometry("800x400")
        self.root.configure(bg=BG_COLOR)

        # Create title bar
        self.create_title_bar()

        # Fullscreen mode (optional)
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", self.exit_fullscreen)

        # Frame for login inputs
        self.input_frame = tk.Frame(root, bg=BG_COLOR)
        self.input_frame.pack(side='left', expand=True, fill='both', padx=20, pady=20)

        # Align Login ID, Password, and Path with grid layout
        self.label_login_id = tk.Label(self.input_frame, text="Login ID", bg=BG_COLOR, fg=FG_COLOR)
        self.label_login_id.grid(row=0, column=0, padx=10, pady=(20, 5), sticky="e")
        self.entry_login_id = tk.Entry(self.input_frame, width=30, bg=ENTRY_BG_COLOR, fg=ENTRY_FG_COLOR, bd=0, highlightthickness=0)
        self.entry_login_id.grid(row=0, column=1, padx=10, pady=(20, 5), sticky="w")

        self.label_password = tk.Label(self.input_frame, text="Password", bg=BG_COLOR, fg=FG_COLOR)
        self.label_password.grid(row=1, column=0, padx=10, pady=(10, 5), sticky="e")
        self.entry_password = tk.Entry(self.input_frame, show='*', width=30, bg=ENTRY_BG_COLOR, fg=ENTRY_FG_COLOR, bd=0, highlightthickness=0)
        self.entry_password.grid(row=1, column=1, padx=10, pady=(10, 5), sticky="w")

        self.label_path = tk.Label(self.input_frame, text="Path", bg=BG_COLOR, fg=FG_COLOR)
        self.label_path.grid(row=2, column=0, padx=10, pady=(10, 5), sticky="e")
        self.entry_path = tk.Entry(self.input_frame, width=30, bg=ENTRY_BG_COLOR, fg=ENTRY_FG_COLOR, bd=0, highlightthickness=0)
        self.entry_path.grid(row=2, column=1, padx=10, pady=(10, 5), sticky="w")

        # Welcome message placed below login credentials
        self.welcome_text = tk.Label(self.input_frame, bg=BG_COLOR, fg=WELCOME_TEXT_COLOR, font=("Helvetica Neue", 18, "bold"))
        self.welcome_text.grid(row=3, column=0, columnspan=2, pady=(40, 10))

        # Frame for buttons
        self.button_frame = tk.Frame(root, bg=BG_COLOR)
        self.button_frame.pack(side='left', fill='y', padx=(30, 0))

        # Buttons
        self.btn_existing_user = tk.Button(self.button_frame, text="Existing User", command=self.open_user_list,
                                            bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR, borderwidth=0, relief="flat", padx=20, pady=10, width=20)
        self.btn_existing_user.pack(pady=(40, 10), anchor='w')

        self.btn_new_user = tk.Button(self.button_frame, text="New User", command=self.register,
                                       bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR, borderwidth=0, relief="flat", padx=20, pady=10, width=20)
        self.btn_new_user.pack(pady=10, anchor='w')

        # Text area on the right side (optional)
        self.text_frame = tk.Frame(root, bg=BG_COLOR)
        self.text_frame.pack(side='right', fill='y', padx=20, pady=20)

        self.additional_text = tk.Label(self.text_frame, bg=BG_COLOR, fg=FG_COLOR)
        self.additional_text.pack(pady=10)

        self.load_user()  # Load a single user

    def create_title_bar(self):
        title_bar = tk.Frame(self.root, bg="#5A4B8A", relief='raised', bd=0)
        title_bar.pack(fill='x')

        minimize_btn = tk.Button(title_bar, text='_', command=self.minimize, bg="#5A4B8A", fg="white", borderwidth=0, relief='flat')
        minimize_btn.pack(side='right')

        maximize_btn = tk.Button(title_bar, text='[]', command=self.toggle_fullscreen, bg="#5A4B8A", fg="white", borderwidth=0, relief='flat')
        maximize_btn.pack(side='right')

        close_btn = tk.Button(title_bar, text='X', command=self.root.quit, bg="#C0392B", fg="white", borderwidth=0, relief='flat')
        close_btn.pack(side='right')

    def exit_fullscreen(self, event):
        self.root.attributes('-fullscreen', False)

    def toggle_fullscreen(self):
        self.root.attributes('-fullscreen', not self.root.attributes('-fullscreen'))

    def minimize(self):
        self.root.iconify()

    def load_user(self):
        self.user = None
        if os.path.exists(USER_FILE):
            with open(USER_FILE, 'r') as file:
                line = file.readline().strip()
                if line:  # Check if there's a line to read
                    parts = line.split(',')
                    if len(parts) == 3:  # Ensure there are exactly 3 parts
                        username, password, path = parts
                        self.user = (username, password, path)

    def save_user(self, username, password, path):
        with open(USER_FILE, 'w') as file:  # Overwrite user file
            file.write(f'{username},{password},{path}\n')

    def remove_user(self):
        if self.user:
            self.user = None
            os.remove(USER_FILE)  # Remove the user file
            return True
        else:
            messagebox.showwarning("Removal Failed", "No user found.")
            return False

    def open_calendar_app(self):
        calendar_app_window = tk.Tk()
        calendar_app_window.title("Calendar App")
        calendar_app_window.geometry("300x350")
        calendar_app_window.configure(bg=BG_COLOR)

        tk.Label(calendar_app_window, text="Welcome to the Calendar App!", bg=BG_COLOR, fg=FG_COLOR).pack(pady=20)

        calendar_app_window.mainloop()

    def open_user_list(self):
        if not self.user:
            messagebox.showwarning("No Users", "No registered user available.")
            return

        user_list_window = tk.Toplevel(self.root)
        user_list_window.title("Select User")
        user_list_window.geometry("250x200")
        user_list_window.configure(bg=BG_COLOR)

        label_select_user = tk.Label(user_list_window, text="Select a user to log in:", bg=BG_COLOR, fg=FG_COLOR)
        label_select_user.pack(pady=5)

        listbox = tk.Listbox(user_list_window, bg=ENTRY_BG_COLOR, fg=ENTRY_FG_COLOR)
        listbox.insert(tk.END, self.user[0])  # Insert only the single user
        listbox.pack(pady=5)

        def on_user_select(event):
            selected_user = listbox.get(listbox.curselection())
            if selected_user:
                messagebox.showinfo("Login", f"Login successful for user: {selected_user}")
                user_list_window.destroy()
                self.root.destroy()
                self.open_calendar_app()

        listbox.bind("<<ListboxSelect>>", on_user_select)

    def register(self):
        username = self.entry_login_id.get()
        password = self.entry_password.get()
        path = self.entry_path.get()

        if self.user:  # Check if a user already exists
            self.remove_user()  # Remove existing user credentials
        elif username == "" or password == "" or path == "":
            messagebox.showwarning("Registration Failed", "All fields are required.")
            return

        # Save the new user
        self.save_user(username, password, path)
        self.user = (username, password, path)  # Store the new user in memory
        messagebox.showinfo("Registration", "User registered successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
