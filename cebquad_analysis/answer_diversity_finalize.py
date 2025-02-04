import tkinter as tk
from tkinter import messagebox
from utils import *
import time

DATE_TIME = "DATE_TIME"
NUMERIC = "NUMERIC"
PERSON = "PERSON"
LOCATION = "LOCATION"
OTHER_ENTITY = "OTHER_ENTITY"
NOUN = "NOUN"
ADJ = "ADJ"
VERB = "VERB"
OTHERS = "OTHERS"

initial = "answer_diversity-20250204-233450-f.json"
data = read_file(get_path([ "cebquad_analysis", initial]))

current_index = 0  # Track which item is being edited

def update_display():
    """Update the UI with current data."""
    entry_id.config(text=f"ID: {data[current_index]['id']}")
    entry_answer.config(text=f"Answer: {data[current_index]['answer']}")
    entry_type.config(text=f"Current Type: {data[current_index]['type']}")

def change_type(new_type):
    """Change the type of the current item."""
    data[current_index]["type"] = new_type
    update_display()
    next_item()

def next_item(event=None):
    """Move to the next item in the list."""
    global current_index
    if current_index < len(data) - 1:
        current_index += 1
        update_display()
    else:
        messagebox.showinfo("End", "You have reached the last item.")

def prev_item(event=None):
    """Move to the previous item in the list."""
    global current_index
    if current_index > 0:
        current_index -= 1
        update_display()
    else:
        messagebox.showinfo("Start", "You are at the first item.")

def save_to_json():
    """Save the modified list to a JSON file."""
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    write_file(get_path(["cebquad_analysis", initial]), data)
    messagebox.showinfo("Saved", "Data saved successfully!")

# Tkinter UI
root = tk.Tk()
root.title("Edit Answer Types")
root.geometry("1600x1000")

# Labels
entry_id = tk.Label(root, text="", font=("Arial", 12))
entry_id.pack(pady=5)

entry_answer = tk.Label(root, text="", font=("Arial", 12), wraplength=450, justify="left")
entry_answer.pack(pady=5)

entry_type = tk.Label(root, text="", font=("Arial", 12, "bold"), fg="grey")
entry_type.pack(pady=5)

# Buttons for type selection
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

type_buttons = [DATE_TIME, NUMERIC, PERSON, LOCATION, OTHER_ENTITY, NOUN, ADJ, VERB, OTHERS]
for idx in range(len(type_buttons)):
    t = type_buttons[idx]
    tk.Button(frame_buttons, text=f"{idx+1}.) {t}", width=10, command=lambda t=t: change_type(t)).pack(side=tk.LEFT, padx=5)

# Navigation buttons
frame_nav = tk.Frame(root)
frame_nav.pack(pady=10)

tk.Button(frame_nav, text="<< Previous", command=prev_item).pack(side=tk.LEFT, padx=5)
tk.Button(frame_nav, text="Next >>", command=next_item).pack(side=tk.LEFT, padx=5)

# Save button
tk.Button(root, text="Save to JSON", command=save_to_json).pack(pady=10)

root.focus_set()

root.bind("<Return>", next_item)  # Enter (Mac & Windows)
root.bind("<KP_Enter>", next_item)  # Keypad Enter (Mac)
root.bind("<BackSpace>", prev_item)  # Works on Windows/Linux
root.bind("<Delete>", prev_item)  # Works on Mac

for index in range(len(type_buttons)):
    root.bind(index+1, lambda event, t=type_buttons[index]: change_type(t))  # Lowercase key

# Initialize UI with first item
update_display()

root.mainloop()
