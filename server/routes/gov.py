import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Load the dataset
file_path = r"C:\Users\nischay\Documents\50_patients_new.xlsx"
data = pd.read_excel(file_path, sheet_name='Sheet1')

# Step 1: Automatically extract disease-related columns
# Define the columns that are not diseases
non_disease_columns = ['Age', 'Height (cm)', 'Weight (kg)', 'Gender', 'District', 'Income (₹)']

# Extract all columns except for the non-disease columns
disease_columns = [col for col in data.columns if col not in non_disease_columns]

# Step 2: Data Cleaning - Handle Missing Values and Ensure Data Consistency
# Fill missing values for numeric columns (Age, Height, Weight, Income) with median
numeric_columns = ['Age', 'Height (cm)', 'Weight (kg)', 'Income (₹)']
data[numeric_columns] = data[numeric_columns].fillna(data[numeric_columns].median())

# Categorical columns like Gender and District cannot have median; handle missing by filling with a mode or placeholder
data['Gender'] = data['Gender'].fillna(data['Gender'].mode()[0])
data['District'] = data['District'].fillna(data['District'].mode()[0])

# Fill missing values for disease columns with 'N' (assuming 'N' means no case)
data[disease_columns] = data[disease_columns].fillna('N')

# Step 3: Data Analytics - Visualizing Trends for Each Disease by District
for disease in disease_columns:
    plt.figure(figsize=(12, 6))
    sns.countplot(data=data, x='District', hue=disease, order=data['District'].value_counts().index)
    plt.title(f'{disease} Cases by District')
    plt.xlabel('District')
    plt.ylabel('Number of Cases')
    plt.legend(title=disease)
    plt.show()

# Step 4: Machine Learning - Clustering Analysis
# Data preprocessing for clustering (Only numeric columns should be used for clustering)
features = data[numeric_columns].copy()

# Standardizing features for clustering
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# Applying KMeans clustering
kmeans = KMeans(n_clusters=3, random_state=42)
data['Cluster'] = kmeans.fit_predict(scaled_features)

# Visualizing clusters
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Age', y='Income (₹)', data=data, hue='Cluster', palette='viridis')
plt.title('Clustering of Patients by Age and Income')
plt.xlabel('Age')
plt.ylabel('Income (₹)')
plt.legend(title='Cluster')
plt.show()
