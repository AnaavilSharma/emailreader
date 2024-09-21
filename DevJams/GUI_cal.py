import tkinter as tk
from tkinter import ttk
import calendar
from datetime import datetime


def mainFn():
    # Create the main application window with increased resolution
    root = tk.Tk()
    root.title("Event Calendar")
    root.geometry("1000x700")  # Increased resolution for more space

    # Dark theme colors
    bg_color = "#1f1f1f"      # Dark background (matte)
    fg_color = "#ffffff"      # White text
    button_bg = "#333333"     # Dark button background (matte)
    highlight_color = "#666666"  # Lighter matte color for highlights

    # Apply the dark theme to the root window
    root.configure(bg=bg_color)

    # Create a custom style for the comboboxes (dropdowns) to set text color to black
    style = ttk.Style()
    style.theme_use("default")
    style.configure("TCombobox", fieldbackground=button_bg, background=button_bg, foreground="black", selectforeground="black")

    # Function to update the preview section
    def update_preview(day):
        event = events_dict.get(day, "")
        preview_var.set(f"Selected Date: {day} {calendar.month_name[current_month]}, {current_year}\nEvent: {event}")

    # Function to handle tick and cross button actions
    def confirm_selection(day_btn, day):
        day_btn.config(bg="blue")  # Turn the button blue
        events_dict[day] = f"Event on {day} {calendar.month_name[current_month]}"
        update_preview(day)

    def cancel_selection(day_btn, day):
        day_btn.config(bg="red")  # Turn the button red
        events_dict[day] = f"No event for {day} {calendar.month_name[current_month]}"
        update_preview(day)

    # Create a frame for the calendar grid
    grid_frame = tk.Frame(root, bg=bg_color, padx=10, pady=10)
    grid_frame.grid(row=1, column=0, padx=20, pady=10)

    # Create labels for days of the week
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i, day in enumerate(days):
        tk.Label(grid_frame, text=day, bg=bg_color, fg=fg_color).grid(row=0, column=i, padx=10, pady=5)

    # Get current month and year
    current_year = datetime.now().year
    current_month = datetime.now().month

    # Get the first weekday of the current month and the number of days
    first_weekday, num_days = calendar.monthrange(current_year, current_month)

    # Dictionary to store event information for each day
    events_dict = {}

    # Function to create the day buttons
    def create_day_buttons(month, year):
        # Clear the previous buttons
        for widget in grid_frame.winfo_children()[7:]:
            widget.destroy()

        day = 1
        row = 1
        col = first_weekday

        while day <= num_days:
            day_btn = tk.Button(grid_frame, text=day, width=10, height=5,
                                bg=button_bg, fg=fg_color, highlightbackground="white",
                                bd=2, relief="solid", command=lambda day=day: update_preview(day))
            day_btn.grid(row=row, column=col, padx=10, pady=10)
        
            # Add right-click context menu to tick or cross
            day_btn.bind("<Button-3>", lambda e, day_btn=day_btn, day=day: confirm_selection(day_btn, day))
            day_btn.bind("<Button-2>", lambda e, day_btn=day_btn, day=day: cancel_selection(day_btn, day))

            day += 1
            col += 1
            if col > 6:
                col = 0
                row += 1

    create_day_buttons(current_month, current_year)

    # Create a dropdown to filter
    filter_label = tk.Label(root, text="Filter:", bg=bg_color, fg=fg_color)
    filter_label.grid(row=0, column=0, sticky="w", padx=20)
    filter_var = tk.StringVar()
    filter_options = ["Fitness", "Meeting", "Work", "Study", "Travel", "Shopping", "Health", "Other"]
    filter_dropdown = ttk.Combobox(root, textvariable=filter_var, values=filter_options, style="TCombobox")
    filter_dropdown.grid(row=0, column=0, sticky="e", padx=80)

    # Create dropdowns for month and year
    def update_calendar(event):
        global current_month, current_year
        current_month = list(calendar.month_name).index(month_var.get())
        current_year = year_var.get()
        create_day_buttons(current_month, current_year)

    month_var = tk.StringVar(value=calendar.month_name[current_month])
    month_dropdown = ttk.Combobox(root, textvariable=month_var, values=list(calendar.month_name)[1:], style="TCombobox")
    month_dropdown.grid(row=0, column=1, padx=10)
    month_dropdown.bind("<<ComboboxSelected>>", update_calendar)

    year_var = tk.IntVar(value=current_year)
    year_dropdown = ttk.Combobox(root, textvariable=year_var, values=list(range(current_year - 10, current_year + 10)), style="TCombobox")
    year_dropdown.grid(row=0, column=2, padx=10)
    year_dropdown.bind("<<ComboboxSelected>>", update_calendar)

    # Create a preview section with a text box and dark theme
    preview_var = tk.StringVar(value="Selected Date:")
    preview_label = tk.Label(root, textvariable=preview_var, font=("Arial", 14), bg=bg_color, fg=fg_color)
    preview_label.grid(row=2, column=0, pady=20)

    # Create Tick and Cross buttons with colored buttons and white outline
    def confirm_action():
        print(f"Confirmed: {preview_var.get()}")

    def cancel_action():
        preview_var.set("Selection Cancelled")

    tick_button = tk.Button(root, text="✔", command=confirm_action, width=10, bg="green", fg=fg_color,
                            highlightbackground="white", bd=2, relief="solid")
    tick_button.grid(row=3, column=0, pady=10, sticky="w", padx=20)

    cross_button = tk.Button(root, text="✘", command=cancel_action, width=10, bg="red", fg=fg_color,
                            highlightbackground="white", bd=2, relief="solid")
    cross_button.grid(row=3, column=0, pady=10, sticky="e", padx=80)

    # Run the application
    root.mainloop()

