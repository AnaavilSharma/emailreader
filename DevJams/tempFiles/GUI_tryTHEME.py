import tkinter as tk
from tkinter import messagebox
import os
import ttkbootstrap as ttk  # Use ttkbootstrap for theme support
from ttkbootstrap.constants import *

# File where users will be stored
USER_FILE = 'users.txt'

# Create LoginApp class with ttkbootstrap theme
class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Page")
        self.root.geometry("800x400")

        # Set Equilux theme from ttkbootstrap
        style = ttk.Style(theme='darkly')  # You can use 'darkly' for Equilux-like dark theme

        # Fullscreen mode (optional)
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", self.exit_fullscreen)

        # Frame for login inputs
        self.input_frame = ttk.Frame(root)
        self.input_frame.pack(side='left', expand=True, fill='both', padx=20, pady=20)

        # Align Login ID, Password, and Path with grid layout using ttk Labels and Entries
        self.label_login_id = ttk.Label(self.input_frame, text="Login ID", bootstyle=LIGHT)
        self.label_login_id.grid(row=0, column=0, padx=10, pady=(20, 5), sticky="e")
        self.entry_login_id = ttk.Entry(self.input_frame, width=30, bootstyle=DARK)
        self.entry_login_id.grid(row=0, column=1, padx=10, pady=(20, 5), sticky="w")

        self.label_password = ttk.Label(self.input_frame, text="Password", bootstyle=LIGHT)
        self.label_password.grid(row=1, column=0, padx=10, pady=(10, 5), sticky="e")
        self.entry_password = ttk.Entry(self.input_frame, show='*', width=30, bootstyle=DARK)
        self.entry_password.grid(row=1, column=1, padx=10, pady=(10, 5), sticky="w")

        self.label_path = ttk.Label(self.input_frame, text="Path", bootstyle=LIGHT)
        self.label_path.grid(row=2, column=0, padx=10, pady=(10, 5), sticky="e")
        self.entry_path = ttk.Entry(self.input_frame, width=30, bootstyle=DARK)
        self.entry_path.grid(row=2, column=1, padx=10, pady=(10, 5), sticky="w")

        # Welcome message placed below login credentials
        self.welcome_text = ttk.Label(self.input_frame, text="Hey Welcome to your own personalized Event Calendar",
                                      bootstyle=LIGHT, font=("Helvetica", 16, "bold"))
        self.welcome_text.grid(row=3, column=0, columnspan=2, pady=(40, 10))  # Added ample space

        # Frame for buttons, placed next to the input frame
        self.button_frame = ttk.Frame(root)
        self.button_frame.pack(side='left', fill='y', padx=(30, 0))  # Add space between input and button frames

        # Buttons with separation between them and padding, using ttkbootstrap buttons
        self.btn_existing_user = ttk.Button(self.button_frame, text="Existing User", command=self.open_user_list,
                                            bootstyle=SUCCESS, width=20)
        self.btn_existing_user.pack(pady=(40, 10), anchor='w')  # Space above for separation

        self.btn_new_user = ttk.Button(self.button_frame, text="New User", command=self.register,
                                       bootstyle=PRIMARY, width=20)
        self.btn_new_user.pack(pady=10, anchor='w')

        self.btn_remove_user = ttk.Button(self.button_frame, text="Remove User", command=self.remove_user_dialog,
                                          bootstyle=DANGER, width=20)
        self.btn_remove_user.pack(pady=10, anchor='w')

        # Text area on the right side (optional)
        self.text_frame = ttk.Frame(root)
        self.text_frame.pack(side='right', fill='y', padx=20, pady=20)

        self.additional_text = ttk.Label(self.text_frame, text="Additional Information Here", bootstyle=LIGHT)
        self.additional_text.pack(pady=10)

        self.load_users()

    def exit_fullscreen(self, event):
        self.root.attributes('-fullscreen', False)

    def toggle_fullscreen(self):
        self.root.attributes('-fullscreen', not self.root.attributes('-fullscreen'))

    def load_users(self):
        self.users = {}
        if os.path.exists(USER_FILE):
            with open(USER_FILE, 'r') as file:
                for line in file:
                    username, password, path = line.strip().split(',')
                    self.users[username] = (password, path)

    def save_user(self, username, password, path):
        with open(USER_FILE, 'a') as file:
            file.write(f'{username},{password},{path}\n')

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

    def open_calendar_app(self):
        calendar_app_window = tk.Tk()
        calendar_app_window.title("Calendar App")
        calendar_app_window.geometry("300x350")

        ttk.Label(calendar_app_window, text="Welcome to the Calendar App!").pack(pady=20)

        calendar_app_window.mainloop()

    def open_user_list(self):
        if not self.users:
            messagebox.showwarning("No Users", "No registered users available.")
            return

            user_list_window = tk.Toplevel(self.root)
            user_list_window.title("Select User")
            user_list_window.geometry("250x200")
            user_list_window.configure(bg=BG_COLOR)

            label_select_user = tk.Label(user_list_window, text="Select a user to log in:", bg=BG_COLOR, fg=FG_COLOR)
            label_select_user.pack(pady=5)

            listbox = tk.Listbox(user_list_window, bg=ENTRY_BG_COLOR, fg=ENTRY_FG_COLOR)
            for user in self.users:
                listbox.insert(tk.END, user)
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

            if username in self.users:
                messagebox.showwarning("Registration Failed", "Username already exists.")
            elif username == "" or password == "" or path == "":
                messagebox.showwarning("Registration Failed", "All fields are required.")
            else:
                self.users[username] = (password, path)
                self.save_user(username, password, path)
                messagebox.showinfo("Registration", "User registered successfully.")

        def remove_user_dialog(self):
            if not self.users:
                messagebox.showwarning("No Users", "No registered users available.")
                return

            remove_user_window = tk.Toplevel(self.root)
            remove_user_window.title("Remove User")
            remove_user_window.geometry("250x200")
            remove_user_window.configure(bg=BG_COLOR)

            label_select_user = tk.Label(remove_user_window, text="Select a user to remove:", bg=BG_COLOR, fg=FG_COLOR)
            label_select_user.pack(pady=5)

            listbox = tk.Listbox(remove_user_window, bg=ENTRY_BG_COLOR, fg=ENTRY_FG_COLOR)
            for user in self.users:
                listbox.insert(tk.END, user)
            listbox.pack(pady=5)

            def on_user_select(event):
                selected_user = listbox.get(listbox.curselection())
                confirm = messagebox.askyesno("Confirm", f"Are you sure you want to remove user: {selected_user}?")
                if confirm:
                    if self.remove_user(selected_user):
                        messagebox.showinfo("Success", f"User {selected_user} has been removed.")
                        listbox.delete(listbox.curselection())
                    else:
                        messagebox.showwarning("Error", "Failed to remove user.")
                remove_user_window.destroy()

            listbox.bind("<<ListboxSelect>>", on_user_select)

        if __name__ == "__main__":
            root = tk.Tk()
            app = LoginApp(root)
            root.mainloop()