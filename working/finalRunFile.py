import tkinter as tk
from tkinter import messagebox
import os
from cryptography.fernet import Fernet
from PIL import Image, ImageTk  # Import Pillow for image handling
from finalResourceFile import *

# File where users will be stored
USER_FILE = 'users.txt'
KEY_FILE = 'key.key'

# Dark mode color variables
BG_COLOR = "#2e2e2e"
FG_COLOR = "#ffffff"
BUTTON_BG_COLOR = "#6A5ACD"
BUTTON_FG_COLOR = "#ffffff"
ENTRY_BG_COLOR = "#5A4B8A"
ENTRY_FG_COLOR = "#ffffff"
WELCOME_TEXT_COLOR = "#f5f5f5"

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
        self.input_frame.pack(side='top', fill='both', padx=20, pady=20)

        # Login ID
        self.label_login_id = tk.Label(self.input_frame, text="Login ID", bg=BG_COLOR, fg=FG_COLOR, font=("Helvetica Neue", 14))
        self.label_login_id.grid(row=0, column=0, padx=10, pady=(20, 5), sticky="e")
        self.entry_login_id = tk.Entry(self.input_frame, width=30, bg=ENTRY_BG_COLOR, fg=ENTRY_FG_COLOR, bd=0, highlightthickness=0, font=("Helvetica Neue", 12))
        self.entry_login_id.grid(row=0, column=1, padx=10, pady=(20, 5), sticky="w")

        # Password
        self.label_password = tk.Label(self.input_frame, text="Password", bg=BG_COLOR, fg=FG_COLOR, font=("Helvetica Neue", 14))
        self.label_password.grid(row=1, column=0, padx=10, pady=(10, 5), sticky="e")
        self.entry_password = tk.Entry(self.input_frame, show='*', width=30, bg=ENTRY_BG_COLOR, fg=ENTRY_FG_COLOR, bd=0, highlightthickness=0, font=("Helvetica Neue", 12))
        self.entry_password.grid(row=1, column=1, padx=10, pady=(10, 5), sticky="w")

        # Path
        self.label_path = tk.Label(self.input_frame, text="Path", bg=BG_COLOR, fg=FG_COLOR, font=("Helvetica Neue", 14))
        self.label_path.grid(row=2, column=0, padx=10, pady=(10, 5), sticky="e")
        self.entry_path = tk.Entry(self.input_frame, width=30, bg=ENTRY_BG_COLOR, fg=ENTRY_FG_COLOR, bd=0, highlightthickness=0, font=("Helvetica Neue", 12))
        self.entry_path.grid(row=2, column=1, padx=10, pady=(10, 5), sticky="w")

        # Remember credentials
        self.save_credentials_var = tk.IntVar()
        self.save_credentials_check = tk.Checkbutton(self.input_frame, text="Save Credentials", variable=self.save_credentials_var, bg=BG_COLOR, fg=FG_COLOR, selectcolor=BG_COLOR, font=("Helvetica Neue", 12))
        self.save_credentials_check.grid(row=3, columnspan=2, pady=(5, 10))

        # Welcome message
        self.welcome_text = tk.Label(self.input_frame, text="Welcome! Please log in.", bg=BG_COLOR, fg=WELCOME_TEXT_COLOR, font=("Helvetica Neue", 20, "bold"))
        self.welcome_text.grid(row=4, column=0, columnspan=2, pady=(30, 10))

        # Frame for buttons
        self.button_frame = tk.Frame(root, bg=BG_COLOR)
        self.button_frame.pack(side='top', fill='y', padx=(10, 0))

        # Buttons with styling
        self.btn_existing_user = tk.Button(self.button_frame, text="Existing User", command=self.open_user_list,
                                            bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR, borderwidth=0, relief="flat", padx=20, pady=15, width=25, font=("Helvetica Neue", 14))
        self.btn_existing_user.pack(pady=(20, 10), anchor='w')

        self.btn_new_user = tk.Button(self.button_frame, text="New User", command=self.register,
                                       bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR, borderwidth=0, relief="flat", padx=20, pady=15, width=25, font=("Helvetica Neue", 14))
        self.btn_new_user.pack(pady=10, anchor='w')

        # Frame for calendar image
        self.image_frame = tk.Frame(root, bg=BG_COLOR)
        self.image_frame.pack(side='bottom', fill='both', padx=100, pady=20)

        

        # Load users from file if it exists
        self.load_users()

        # Load saved credentials if available
        self.autofill_saved_credentials()

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

    def load_users(self):
        self.users = {}
        if os.path.exists(USER_FILE):
            with open(USER_FILE, 'r') as file:
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) == 3:  # Ensure there are exactly 3 parts
                        username, password, path = parts
                        self.users[username] = (password, path)
                    else:
                        print(f"Skipping invalid line: {line.strip()}")

    def save_user(self, username, password, path):
        with open(USER_FILE, 'a') as file:
            encrypted_password = self.encrypt_data(password)
            file.write(f'{username},{encrypted_password},{path}\n')

    def remove_user(self, username):
        if username in self.users:
            del self.users[username]
            with open(USER_FILE, 'w') as file:
                for user, (password, path) in self.users.items():
                    file.write(f'{user},{password},{path}\n')
            return True
        else:
            messagebox.showwarning("Removal Failed", "User not found.")
            return False

    def encrypt_data(self, data):
        key = self.load_key()
        f = Fernet(key)
        return f.encrypt(data.encode()).decode()

    def decrypt_data(self, encrypted_data):
        key = self.load_key()
        f = Fernet(key)
        return f.decrypt(encrypted_data.encode()).decode()

    def load_key(self):
        if not os.path.exists(KEY_FILE):
            key = Fernet.generate_key()
            with open(KEY_FILE, 'wb') as key_file:
                key_file.write(key)
        else:
            with open(KEY_FILE, 'rb') as key_file:
                key = key_file.read()
        return key

    def autofill_saved_credentials(self):
        if os.path.exists("saved_credentials.txt"):
            with open("saved_credentials.txt", 'r') as file:
                saved_username, saved_password, saved_path = file.read().split(',')
                self.entry_login_id.insert(0, saved_username)
                self.entry_password.insert(0, saved_password)
                self.entry_path.insert(0, saved_path)

    def save_credentials(self, username, password, path):
        if self.save_credentials_var.get() == 1:
            with open("saved_credentials.txt", 'w') as file:
                file.write(f"{username},{password},{path}")

    def open_user_list(self):
        """Displays the list of registered users for login."""
        if not self.users:
            messagebox.showwarning("No Users", "No registered users available.")
            return

        user_list_window = tk.Toplevel(self.root)
        user_list_window.title("Select User")
        user_list_window.geometry("250x200")
        user_list_window.configure(bg=BG_COLOR)

        label_select_user = tk.Label(user_list_window, text="Select a user to log in:", bg=BG_COLOR, fg=FG_COLOR, font=("Helvetica Neue", 12))
        label_select_user.pack(pady=5)

        listbox = tk.Listbox(user_list_window, bg=ENTRY_BG_COLOR, fg=ENTRY_FG_COLOR, font=("Helvetica Neue", 12))
        for user in self.users:
            listbox.insert(tk.END, user)
        listbox.pack(pady=5, padx=10)

        def on_user_select(event):
            selected_user = listbox.get(listbox.curselection())
            if selected_user:
                messagebox.showinfo("Login", f"Login successful for user: {selected_user}")
                user_list_window.destroy()
                self.root.destroy()
                print(selected_user)

        listbox.bind("<<ListboxSelect>>", on_user_select)

    def register(self):
        username = self.entry_login_id.get()
        password = self.entry_password.get()
        path = self.entry_path.get()

        if username in self.users:
            messagebox.showwarning("Registration Failed", "Username already exists.")
        elif username == "" or password == "" or path == "":
            messagebox.showwarning("Registration Failed", "All fields are required.")
        else:
            self.users[username] = (password, path)
            self.save_user(username, password, path)
            self.save_credentials(username, password, path)  # Save credentials if checked
            messagebox.showinfo("Registration", "User registered successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()