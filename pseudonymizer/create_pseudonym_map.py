    
import tkinter as tk
from tkinter import messagebox
from utils import *
import time 

GIVEN_NAME_MALE = 0
GIVEN_NAME_FEMALE = 1
SURNAME_OTHER = 2
SURNAME_CH = 3
SURNAME_MORO = 4
NOT_NAME = 5
GIVEN_NAME_EITHER = 6

person_start = 3000
person_index = person_start
end_limit = 3500
name_cat = {}
person_names = read_file(get_path([ "data", "person_names_filtered.json"]))    

root = tk.Tk()

def mark_name(category):
    print(category)
    global person_index 
    try:

        person_name = person_names[person_index].lower()
        print(person_name)
        if person_index < end_limit and not person_name in name_cat:
            name_cat[person_name] = category
        
            person_index += 1
            
        if person_index >= end_limit:
            close_window()

        # Update the label with the next name if available
        if person_index < len(person_names):
            name_label.config(text=f"{person_index}.) {person_names[person_index]}")

    except Exception as e:
        print(e)
        close_window()

def close_window():
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    print("Closing application.")
    write_file(get_path(["pseudonymizer", f"person_cat-{person_start}-{person_index}-{timestamp}"]), name_cat)
    root.after(5000, root.destroy())


if __name__ == "__main__":
    root.geometry("800x600")  # Widened window to 800px width and 600px height
    root.title("Name Identifier")

    # # Label to display the name
    name_label = tk.Label(root, text=f"{person_index}.) {person_names[person_index]}", font=("Helvetica", 16))
    name_label.pack(pady=20, fill=tk.BOTH, expand=True)

    # Buttons for Given Name and Surname
    name_female_btn = tk.Button(root, text="(1) Female", command=lambda: mark_name(GIVEN_NAME_FEMALE))
    name_female_btn.pack(padx=10, pady=10)

    name_male_btn = tk.Button(root, text="(2) Male", command=lambda: mark_name(GIVEN_NAME_MALE))
    name_male_btn.pack(padx=10, pady=10)

    name_male_btn = tk.Button(root, text="(3) Unisex", command=lambda: mark_name(GIVEN_NAME_EITHER))
    name_male_btn.pack(padx=10, pady=10)

    surname_chinese_btn = tk.Button(root, text="(4) Chinese", command=lambda: mark_name(SURNAME_CH))
    surname_chinese_btn.pack(padx=10, pady=10)

    surname_moro_btn = tk.Button(root, text="(5) Moro", command=lambda: mark_name(SURNAME_MORO))
    surname_moro_btn.pack(padx=10, pady=10)

    surname_other_btn = tk.Button(root, text="(6) Other", command=lambda: mark_name(SURNAME_OTHER))
    surname_other_btn.pack(padx=10, pady=10)

    surname_other_btn = tk.Button(root, text="(7) Not name", command=lambda: mark_name(NOT_NAME))
    surname_other_btn.pack(padx=10, pady=10)

    close_btn = tk.Button(root, text="close", command=close_window)
    close_btn.pack(padx=10, pady=10)

    root.bind('1', lambda event: mark_name(GIVEN_NAME_FEMALE))  # "1" for Female
    root.bind('2', lambda event: mark_name(GIVEN_NAME_MALE))    # "2" for Male
    root.bind('3', lambda event: mark_name(GIVEN_NAME_EITHER))         # "3" for Unisex
    root.bind('4', lambda event: mark_name(SURNAME_CH))       # "4" for Moro
    root.bind('5', lambda event: mark_name(SURNAME_MORO))       # "5" for Moro
    root.bind('6', lambda event: mark_name(SURNAME_OTHER))       # "6" for Other surname
    root.bind('7', lambda event: mark_name(NOT_NAME))      # "7" for NOT Name
 

    root.mainloop()

