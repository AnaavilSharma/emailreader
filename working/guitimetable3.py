import tkinter as tk
from tkinter import messagebox

class TimetableApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Class Timetable")
        self.root.geometry("1200x700")
        self.root.configure(bg='black')

        # Set up the table structure
        self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        
        # Define time slots for theory and lab classes
        self.time_slots_theory = [
            '8:00-8:50', '9:00-9:50', '10:00-10:50', '11:00-11:50', '12:00-12:50',
            '2:00-2:50', '3:00-3:50', '4:00-4:50', '5:00-5:50', '6:00-6:50'
        ]
        self.time_slots_lab = [
            '8:00-9:40', '9:50-11:30', '11:40-1:20', '2:00-3:40', '3:50-5:30', '5:40-7:20'
        ]

        self.current_time_slots = self.time_slots_theory  # Default to theory time slots
        self.timetable = {day: [None] * len(self.current_time_slots) for day in self.days}

        # Dropdown for selecting class type (Theory or Lab)
        self.class_type_var = tk.StringVar(value='Theory')  # Default value is 'Theory'
        self.class_type_menu = tk.OptionMenu(self.root, self.class_type_var, 'Theory', 'Lab', command=self.switch_class_type)
        self.class_type_menu.grid(row=0, column=0, padx=10, pady=10)
        self.class_type_menu.config(bg='gray', fg='white', borderwidth=2)

        # Create labels for days and time slots
        self.create_table_structure()

        # Save and Update buttons
        self.save_button = tk.Button(root, text="Save Timetable", command=self.save_timetable, bg='gray', fg='white', borderwidth=2)
        self.save_button.grid(row=len(self.days) + 2, column=0, padx=5, pady=5)

        self.update_button = tk.Button(root, text="Update Timetable", command=self.update_timetable, bg='gray', fg='white', borderwidth=2)
        self.update_button.grid(row=len(self.days) + 2, column=1, padx=5, pady=5)

    def create_table_structure(self):
        # Clear existing grid for timetable entries
        for widget in self.root.grid_slaves():
            if widget not in [tk.OptionMenu, tk.Button]:
                widget.config(text = "")
            if int(widget.grid_info()["row"]) > 1 and widget not in (self.save_button, self.update_button):
                widget.grid_forget()

        # Create table headers for time slots
        for i, time_slot in enumerate(self.current_time_slots):
            tk.Label(self.root, text=time_slot, borderwidth=2, relief='solid', padx=5, pady=5, bg='black', fg='white').grid(row=1, column=i+1)

        # Create row headers for days
        for i, day in enumerate(self.days):
            tk.Label(self.root, text=day, borderwidth=2, relief='solid', padx=5, pady=5, bg='black', fg='white').grid(row=i+2, column=0)

        # Create Entry widgets for each cell
        for i, day in enumerate(self.days):
            for j in range(len(self.current_time_slots)):
                entry = tk.Entry(self.root, width=15, borderwidth=1, relief="solid", bg='gray', fg='white')
                entry.grid(row=i+2, column=j+1, padx=5, pady=5)
                self.timetable[day][j] = entry

    def switch_class_type(self, selected_type):
        """Switch between theory and lab class time slots."""
        if selected_type == 'Theory':
            self.current_time_slots = self.time_slots_theory
        elif selected_type == 'Lab':
            self.current_time_slots = self.time_slots_lab
        self.timetable = {day: [None] * len(self.current_time_slots) for day in self.days}
        self.create_table_structure()

    def save_timetable(self):
        timetable_data = {}
        
        # Gather data from each Entry widget
        for day in self.days:
            day_schedule = []
            for entry in self.timetable[day]:
                class_info = entry.get()
                day_schedule.append(class_info)
            timetable_data[day] = day_schedule
        
        # Print or Save timetable data
        print("Saved Timetable Data:")
        for day, schedule in timetable_data.items():
            print(f"{day}: {schedule}")
        
        messagebox.showinfo("Save", "Timetable saved successfully!")

    def update_timetable(self):
        messagebox.showinfo("Update", "Timetable updated!")

# Create the root window
root = tk.Tk()
app = TimetableApp(root)

# Run the application
root.mainloop() 