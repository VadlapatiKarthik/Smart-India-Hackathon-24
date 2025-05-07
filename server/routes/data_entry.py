import pandas as pd
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# File path to the centralized Excel sheet
file_path = r"C:\Users\nischay\Documents\10000patients.xlsx"

# Function to append data to Excel
def submit_data():
    try:
        # Convert necessary fields to integers after retrieving and stripping whitespace
        age = int(entries[0].get().strip())
        height = int(entries[1].get().strip())
        weight = int(entries[2].get().strip())
        income = int(entries[3].get().strip())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values for Age, Height, Weight, and Income.")
        return

    # Retrieve other form data
    gender = gender_var.get()
    district = district_var.get()
    prescribed_medicines = medicine_entry.get("1.0", tk.END).strip()  # Get the prescribed medicines from the text box

    # Prepare the data dictionary
    patient_data = {
        'Age': age,
        'Height': height,
        'Weight': weight,
        'Gender': gender,
        'District': district,
        'Income': income,
        'Prescribed Medicines': prescribed_medicines
    }

    # Add disease data
    for disease, var in disease_vars.items():
        patient_data[disease] = var.get()

    # Add new diseases entered in the "Other" text box
    new_diseases = other_diseases_entry.get("1.0", tk.END).strip().split('\n')
    for new_disease in new_diseases:
        new_disease = new_disease.strip()
        if new_disease:
            patient_data[new_disease] = 'Y'

    # Load existing Excel file and append new data
    try:
        df = pd.read_excel(file_path)
    except FileNotFoundError:
        df = pd.DataFrame(columns=patient_data.keys())  # If file doesn't exist, create a new DataFrame

    # Update the DataFrame with any new disease columns
    for new_disease in new_diseases:
        new_disease = new_disease.strip()
        if new_disease and new_disease not in df.columns:
            df[new_disease] = 'N'

    # Convert the new data to a DataFrame
    new_data = pd.DataFrame([patient_data])

    # Concatenate the new data with the existing data
    df = pd.concat([df, new_data], ignore_index=True)

    # Save the updated DataFrame to the Excel file
    df.to_excel(file_path, index=False)

    # Clear form fields after submission
    for entry in entries:
        entry.delete(0, tk.END)

    # Clear disease checkboxes
    for var in disease_vars.values():
        var.set('N')

    # Clear the prescribed medicines text box
    medicine_entry.delete("1.0", tk.END)

    # Clear the "Other" diseases text box
    other_diseases_entry.delete("1.0", tk.END)

    messagebox.showinfo("Success", "Data and prescription submitted successfully!")

# Create the form using tkinter
root = tk.Tk()
root.title("Doctor - Patient Entry and Prescription Form")

# Create a canvas and a scrollbar to make the form scrollable
canvas = tk.Canvas(root, borderwidth=0)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

# Configure the scrollable frame
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

# Set up the canvas
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Place the canvas and scrollbar on the main window
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Set a consistent padding and font
pad_x = 15
pad_y = 10
font = ('Arial', 12)

# Labels and Entry fields
labels = ['Age', 'Height', 'Weight', 'Gender', 'Income']  # 'District' moved to dropdown

# Create input fields in the scrollable frame
entries = []
for idx, label in enumerate(labels):
    tk.Label(scrollable_frame, text=label, font=font).grid(row=idx, column=0, padx=pad_x, pady=pad_y, sticky='e')

    if label == 'Gender':  # Dropdown for Gender
        gender_var = tk.StringVar(value='Male')
        gender_dropdown = tk.OptionMenu(scrollable_frame, gender_var, 'Male', 'Female', 'Other')
        gender_dropdown.config(font=font)
        gender_dropdown.grid(row=idx, column=1, padx=pad_x, pady=pad_y, sticky='w')
    else:
        entry = tk.Entry(scrollable_frame, font=font, width=25)  # Increase width for better appearance
        entry.grid(row=idx, column=1, padx=pad_x, pady=pad_y, sticky='w')
        entries.append(entry)

# District dropdown
tk.Label(scrollable_frame, text="District", font=font).grid(row=len(labels), column=0, padx=pad_x, pady=pad_y, sticky='e')
district_var = tk.StringVar(value='Central')
district_dropdown = tk.OptionMenu(scrollable_frame, district_var, 'Central', 'East', 'West', 'South', 'North')
district_dropdown.config(font=font)
district_dropdown.grid(row=len(labels), column=1, padx=pad_x, pady=pad_y, sticky='w')

# Store variables for diseases (Y/N)
disease_labels = ['Diabetes', 'Hypertension', 'Asthma', 'COPD', 'CAD', 'Stroke', 'Alzheimer', 'Parkinson', 'CKD',
                  'Hepatitis B', 'TB', 'Malaria', 'HIV/AIDS', 'Influenza', 'Pneumonia', 'Rheumatoid Arthritis', 
                  'Osteoporosis', 'Cancer', 'Anemia', 'Migraine']

disease_vars = {}
for idx, disease in enumerate(disease_labels):
    var = tk.StringVar(value='N')
    tk.Checkbutton(scrollable_frame, text=disease, variable=var, onvalue='Y', offvalue='N', font=font).grid(row=(idx//2)+len(labels)+1, column=idx % 2, padx=pad_x, pady=pad_y, sticky='w')
    disease_vars[disease] = var

# "Other" diseases option
other_var = tk.StringVar(value='N')
tk.Checkbutton(scrollable_frame, text="Other", variable=other_var, onvalue='Y', offvalue='N', font=font, command=lambda: other_diseases_entry.grid(row=len(labels) + (len(disease_labels) // 2) + 2, column=0, columnspan=2, padx=pad_x, pady=pad_y)).grid(row=len(labels) + (len(disease_labels) // 2) + 1, column=0, padx=pad_x, pady=pad_y, sticky='w')

# Entry for "Other" diseases
other_diseases_entry = tk.Text(scrollable_frame, height=4, width=50, font=font)
other_diseases_entry.grid_remove()  # Hide until "Other" is checked

# Label and large text box for prescribing medicines
tk.Label(scrollable_frame, text="Prescribed Medicines", font=font).grid(row=len(labels) + (len(disease_labels) // 2) + 3, column=0, padx=pad_x, pady=pad_y, sticky='n')
medicine_entry = tk.Text(scrollable_frame, height=8, width=50, font=font)  # Increased height and width for better usability
medicine_entry.grid(row=len(labels) + (len(disease_labels) // 2) + 4, column=0, columnspan=2, padx=pad_x, pady=pad_y)

# Submit Button
submit_button = tk.Button(scrollable_frame, text="Submit", command=submit_data, font=font, width=15)
submit_button.grid(row=len(labels) + (len(disease_labels) // 2) + 5, column=0, columnspan=2, padx=pad_x, pady=pad_y)

root.mainloop()
