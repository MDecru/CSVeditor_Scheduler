
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import pandas as pd


root = tk.Tk()
frame = ttk.Frame(root)


#######################
## General lists 
#######################

command_combo_list = ['testpattern', 'power', 'shutter', 'mode']
shutter_combo_list = ['open', 'close']
mode_combo_list = ['standby', 'ready', 'on']
testpattern_combo_list = ['black', 'native-white', 'native-red', 'native-green', 'native-blue', 'red', 'green', 'blue', 'white']

#######################
## Dataframe creation
#######################
cols = ("interval", "command", "value")
global df
df = pd.DataFrame(columns=cols)


#######################
## Functions
#######################

def selected_command(event):

    selected = command_combobox.get()

    match(selected):
        case "testpattern":
            power_spinbox.config(state="disabled")
            value_combobox.config(state="normal")
            value_combobox.config(values=testpattern_combo_list)
            value_combobox.current(0)
        case "shutter":
            power_spinbox.config(state="disabled")
            value_combobox.config(state="normal")
            value_combobox.config(values=shutter_combo_list)
            value_combobox.current(0)
        case "mode":
            power_spinbox.config(state="disabled")
            value_combobox.config(state="normal")
            value_combobox.config(values=mode_combo_list)
            value_combobox.current(0)
        case "power":
            power_spinbox.config(state="normal")
            value_combobox.config(state="disabled")

def load_data(testing = False):
    global df
    treeview = data_treeview
    
    if testing == True:
        csv_file_path = "data.csv"
        df = pd.read_csv(csv_file_path)

    # Function to load DataFrame into Treeview 
    treeview.delete(*treeview.get_children())
    treeview["column"] = cols
    treeview["show"] = "headings" 
    
    for column in treeview["columns"]:
        treeview.heading(column, text=column, anchor=tk.CENTER) 
        treeview.column(column, minwidth=50, width=75, anchor=tk.CENTER) 

    for index, row in df.iterrows():
        treeview.insert("", "end", values=[row[col] for col in cols if col in row.index])


    update_interval_total()

def update_interval_total(): 
    global df # Ensure all values in the 'interval' column are numeric 
    df['interval'] = pd.to_numeric(df['interval'], errors='coerce') 
    # Calculate the sum of all interval values, ignoring NaNs 
    total_seconds = df['interval'].sum() 
    # Convert total seconds to hours, minutes, and seconds 
    hours = total_seconds // 3600 
    minutes = (total_seconds % 3600) // 60 
    seconds = total_seconds % 60

    # Update the label with the formatted time
    total_cyclet_result_label.config(text=f"{int(hours)} hrs    {int(minutes)} min   {int(seconds)} s")


def append_row():
    global df
    command = command_combobox.get()
    if(command == "power"):
        value = power_spinbox.get()
    else:
        value = value_combobox.get()
    interval = interval_spinbox.get()

    # Insert the strings as a new row 
    new_row = pd.DataFrame([[interval, command, value]], columns=cols) 
    df = pd.concat([df, new_row], ignore_index=True) 
    load_data()


def delete_selected_row(): 
    global df 
    data_treeview

    selected_item = data_treeview.selection()
    if not selected_item:
        show_warning("No item selected") 
        return

    selected_item = (data_treeview.selection()[0])
    selected_index = data_treeview.index(selected_item)
    data_treeview.delete(selected_item)
    df = df.drop(selected_index).reset_index(drop=True)
    load_data()


def check_input():
    warning_count = 0
    command = command_combobox.get()
    if(command == "power"):
        value = power_spinbox.get()
    else:
        value = value_combobox.get()
    interval = interval_spinbox.get()

    try:
        interval = int(interval)
    except:
        warning_count += 1
        show_warning("Interval not a number")
        return

    try:
        if(command == "power"):
            value = int(value)
    except:
        warning_count += 1
        show_warning("Power percentage incorrect")
        return

    try:
        if(command not in command_combo_list):
            raise ValueError("Wrong testpattern was given")
        if(command == "testpattern"):
            if value not in testpattern_combo_list:
                raise ValueError("Wrong testpattern was given")
        if(command == "shutter"):
            if value not in shutter_combo_list:
                raise ValueError("Wrong shutter was given")
        if(command == "mode"):
            if value not in mode_combo_list:
                raise ValueError("Wrong mode type was given")
        if int(interval) < 0: 
            interval = 0
            raise ValueError("Interval can not be less than 0 seconds")
    except ValueError as e:
        warning_count += 1
        show_warning(f"Error: {e}")
        return




    if warning_count == 0:
        if(command == "power"):
            if value < 0: value = 0
            if value > 100: value = 100
            value_combobox.delete(0, "end")
            value_combobox.insert(0, value)



        append_row()
    
def load_file(): 
    global df 
    file_path = filedialog.askopenfilename(
        initialdir=".", 
        title="Load file", 
        filetypes=(("CSV files", "*.csv"), ("all files", "*.*"))
        ) 
    if file_path: 
        df = pd.read_csv(file_path)
        load_data()
                                    

def save_to_csv():
    try:
        df.to_csv("export.csv", index=False)
        show_info("Saved to export.csv")
    except:
        show_warning("Failed to save to file")

def show_warning(message): 
    messagebox.showwarning("Warning", message)

def show_info(message): 
    messagebox.showinfo("Info", message)


#######################
## UI ELEMENTS
#######################

widgets_frame = ttk.LabelFrame(frame, text="Create a Test Plan")
widgets_frame.grid(row=0, column=0, padx=20, pady=10)


#######################
## INPUT
#######################

# Button to load file 
load_button = ttk.Button(widgets_frame, text="Load File", command=load_file)
load_button.grid(row=0, column=0, sticky="ew", pady=(10,10))

value_label = ttk.Label(widgets_frame, text="Command")
value_label.grid(row=1, column=0, sticky="ew")

command_combobox = ttk.Combobox(widgets_frame, values=command_combo_list)
command_combobox.current(0)
command_combobox.grid(row=2, column=0, sticky="ew", pady=(0,10))
command_combobox.bind("<<ComboboxSelected>>", selected_command)

value_label = ttk.Label(widgets_frame, text="Value")
value_label.grid(row=3, column=0, sticky="ew")

value_combobox = ttk.Combobox(widgets_frame, values=testpattern_combo_list)
value_combobox.current(0)
value_combobox.grid(row=4, column=0, sticky="ew", pady=(0,10))

power_label = ttk.Label(widgets_frame, text="Power (0 - 100%)")
power_label.grid(row=5, column=0, sticky="ew")

power_spinbox = ttk.Spinbox(widgets_frame, from_=0, to=100)
power_spinbox.insert(0, "15")
power_spinbox.grid(row=6, column=0, sticky="ew", pady=(0,10))

interval_label = ttk.Label(widgets_frame, text="Interval (seconds)")
interval_label.grid(row=7, column=0, sticky="ew")

interval_spinbox = ttk.Spinbox(widgets_frame, from_=0, to=10000)
interval_spinbox.insert(0, "30")
interval_spinbox.grid(row=8, column=0, sticky="ew", pady=(0,10))

append_button = ttk.Button(widgets_frame, text="Append", command=check_input)
append_button.grid(row=9, column=0, sticky="ew", pady=(0,10))

delete_button = ttk.Button(widgets_frame, text="Delete Selected Row", command=delete_selected_row)
delete_button.grid(row=10, column=0, sticky="ew", pady=(0,10))

save_button = ttk.Button(widgets_frame, text="Save to export.csv", command=save_to_csv)
save_button.grid(row=11, column=0, sticky="ew", pady=(0,10))


total_cycle_label = ttk.Label(widgets_frame, text="Total cycle time:")
total_cycle_label.grid(row=12, column=0, sticky="ew")

total_cyclet_result_label = ttk.Label(widgets_frame, text="0 seconds")
total_cyclet_result_label.grid(row=13, column=0, sticky="ew")

#######################
## TREEVIEW
#######################


treeview_frame = ttk.LabelFrame(frame, text="Make this list as a cycle which will be repeated:")
treeview_frame.grid(row=0, column=1, padx=20, pady=10)

tree_frame = ttk.Frame(treeview_frame)
tree_frame.grid(row=1, column=1, pady=10, padx=10)
tree_scroll = ttk.Scrollbar(tree_frame)
tree_scroll.pack(side="right", fill="y")
data_treeview = ttk.Treeview(tree_frame, show='headings', columns=cols, height=13)
data_treeview.pack()


#######################
## Default setting
## and final pack
#######################

power_spinbox.config(state='disabled')
frame.pack()
load_data()
root.mainloop()