import pandas as pd

# Use raw string to prevent issues with backslashes in file paths
file_path = r"C:\Users\Nischay\Documents\Schemes.xlsx"  # Ensure the path is correct

# Load the Excel file
df = pd.read_excel(file_path, sheet_name='Sheet1')

# Convert all text columns to lowercase for case-insensitive matching
df['Disease'] = df['Disease'].str.lower()
df['Gender'] = df['Gender'].str.lower()
df['Income Level (INR)'] = df['Income Level (INR)'].str.lower()
df['Age Group'] = df['Age Group'].str.lower()

# Get disease input from the user
user_disease = input("Disease: ").strip().lower()

# Get age input from the user
user_age = int(input("Age: ").strip())

# Provide income range options to the user
income_ranges = ["0-20000", "20000-40000", "40000-60000", "60000-100000"]
print("Select an income range from the options below:")
for i, range_ in enumerate(income_ranges, 1):
    print(f"{i}. {range_}")

# Get income range input from the user
income_choice = int(input("Enter the number corresponding to your income range: ").strip())
user_income_range = income_ranges[income_choice - 1]

# Get gender input from the user
user_gender = input("Gender (female/male/other): ").strip().lower()

# Function to check if age falls within the age group range
def is_age_in_group(age, group):
    if group == 'all':
        return True
    age_range = group.split('-')
    if len(age_range) == 2:
        return int(age_range[0]) <= age <= int(age_range[1])
    return False

# Function to check if income falls within the income range
def is_income_in_group(income_range, group):
    income_range_cleaned = group.replace(',', '').split('-')
    if len(income_range_cleaned) == 2:
        return income_range_cleaned[0] == income_range.split('-')[0] and income_range_cleaned[1] == income_range.split('-')[1]
    return False

# Filter the dataframe based on the user's input
eligible_schemes = df[df['Disease'] == user_disease]

# Further filter schemes based on the user's age
eligible_schemes = eligible_schemes[eligible_schemes['Age Group'].apply(lambda x: is_age_in_group(user_age, x))]

# Further filter schemes based on the user's income range
eligible_schemes = eligible_schemes[eligible_schemes['Income Level (INR)'].apply(lambda x: is_income_in_group(user_income_range, x))]

# Further filter schemes based on the user's gender, including "All"
if user_gender in ["F", "M", "other"]:
    eligible_schemes = eligible_schemes[(eligible_schemes['Gender'] == user_gender) | (eligible_schemes['Gender'] == "all")]
else:
    eligible_schemes = eligible_schemes[eligible_schemes['Gender'] == "all"]

# Check if there are any schemes for the selected disease, age, income, and gender
if eligible_schemes.empty:
    print(f"No schemes found for disease: {user_disease}, age: {user_age}, income: {user_income_range}, and gender: {user_gender}")
else:
    # Iterate through the filtered dataframe and display the eligible schemes
    for index, row in eligible_schemes.iterrows():
        print(f"Scheme Name: {row['Scheme Name']}")
        print(f"Age Group: {row['Age Group']}")
        print(f"Gender: {row['Gender']}")
        print(f"Income Level: {row['Income Level (INR)']}")
        print(f"Disease: {row['Disease']}")
        print(f"Description: {row['Description of the Scheme']}")
        print("-" * 50)