import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkcalendar import Calendar
import datetime

class CalendarApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calendar App")
        self.geometry("1000x600")  # Increased width to 1000

        # Create main frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill="both", expand=True)

        # Create left frame for calendar
        self.left_frame = ttk.Frame(self.main_frame)
        self.left_frame.pack(side="left", fill="both", expand=True)

        # Create calendar
        self.calendar = Calendar(self.left_frame, selectmode="day",
                                 daybackground='darkblue', weekendbackground='lightcoral',
                                 headersbackground='black', font=('Helvetica', 12),
                                 borderwidth=5)  # Increased border width for thicker squares
        self.calendar.pack(fill="both", expand=True)

        # Create right frame for preview and remainder tab
        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.pack(side="right", fill="y", padx=10)

        # Create preview label
        self.preview_label = ttk.Label(self.right_frame, text="Preview", style="Rounded.TLabel")
        self.preview_label.pack(pady=50)

        # Create preview text widget
        self.preview_text = scrolledtext.ScrolledText(self.right_frame, width=50, height=10, wrap=tk.WORD)
        self.preview_text.pack(pady=30)

        # Create frame for buttons
        self.button_frame = ttk.Frame(self.right_frame)
        self.button_frame.pack(pady=30)

        # Create yes button
        self.yes_button = ttk.Button(self.button_frame, text="Yes", style="Rounded.TButton", command=self.add_to_remainder)
        self.yes_button.pack(side="left", padx=5)

        # Create no button
        self.no_button = ttk.Button(self.button_frame, text="No", style="Rounded.TButton", command=self.clear_preview)
        self.no_button.pack(side="left", padx=5)

        # Set default preview text
        self.preview_text.insert(tk.END, "Are you sure you want to add this day to the reminder tab?")

        # Bind calendar selection event
        self.calendar.bind("<<CalendarSelected>>", self.show_preview)

        # Apply styles
        self.apply_styles()

    def apply_styles(self):
        # Define styles
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Choose a theme with rounded corners (e.g., clam, alt)

        # Configure styles for rounded edges and colors
        self.style.configure("Rounded.TLabel", padding=10, relief="flat", borderwidth=1,
                             background="#8732a8", foreground="#FF474C", font=("Helvetica Neue", 15, "bold"))
        self.style.configure("Rounded.TButton", padding=10, relief="flat", borderwidth=1,
                             background="#4caf50", foreground="#ffffff", font=("Helvetica Neue", 15, "bold"))

    def show_preview(self, event):
        selected_date = self.calendar.selection_get()
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(tk.END, f"Do you want to add {selected_date} to the reminder tab?")

    def add_to_remainder(self):
        selected_date = self.calendar.selection_get()
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(tk.END, "Day added to reminder tab.")

    def clear_preview(self):
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(tk.END, "Action cancelled.")

if __name__ == "__main__":
    app = CalendarApp()
    app.mainloop()
