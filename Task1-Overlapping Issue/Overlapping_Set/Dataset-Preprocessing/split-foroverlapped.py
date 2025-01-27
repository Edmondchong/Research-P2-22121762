# -*- coding: utf-8 -*-
"""Split.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1fvFhhggZRJUqSUxlxFknRA4GO9CumEOv
"""

from google.colab import drive
drive.mount('/content/drive')

"""# Visualize dataset"""

import pandas as pd
import matplotlib.pyplot as plt

# Load the expanded dataset
expanded_df = pd.read_csv("/content/drive/MyDrive/P2/T1/Dataset/overlapped/overlapped.csv")

# Print the total number of rows in the CSV file
total_rows = len(expanded_df)
print(f"Total number of rows in the dataset: {total_rows}")

# Group the expanded dataset by disease to count rows per disease
disease_distribution = expanded_df["disease_label"].value_counts()

# Create a bar graph
plt.figure(figsize=(18, 12))
bars = plt.bar(disease_distribution.index, disease_distribution.values, alpha=0.7)

# Add row counts on top of each bar
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height + 1, f'{int(height)}', ha='center', va='bottom', fontsize=9)

# Customize the plot
plt.title("Number of Rows Per Disease in overlapped Dataset", fontsize=14)
plt.xlabel("Disease Label", fontsize=12)
plt.ylabel("Number of Rows", fontsize=12)
plt.xticks(rotation=90, fontsize=8)
plt.tight_layout()

# Show the plot
plt.show()

"""# Split training,validation and testing set based on symptom combinations"""

import pandas as pd
from sklearn.model_selection import train_test_split

# Load the dataset
data = pd.read_csv("/content/drive/MyDrive/P2/T1/Dataset/overlapped/overlapped.csv")

# Set percentages for test and validation
test_ratio = 0.10  # 10% for testing
val_ratio = 0.10   # 10% for validation

# Group by unique symptom_combination
data["combination_id"] = data["symptom_combination"]  # Unique identifier for combinations

# Map each combination_id to the dominant disease_label for stratification
combination_label_mapping = data.groupby("combination_id")["disease_label"].agg(lambda x: x.mode()[0])

# Exclude rare disease labels (classes with fewer than 2 samples)
valid_labels = combination_label_mapping.value_counts()[combination_label_mapping.value_counts() > 1].index
valid_combinations = combination_label_mapping[combination_label_mapping.isin(valid_labels)].index
filtered_data = data[data["combination_id"].isin(valid_combinations)]

# Get unique symptom combinations and their labels for stratified splitting
filtered_combinations = filtered_data["combination_id"].unique()
filtered_labels = combination_label_mapping.loc[filtered_combinations].values

# Split symptom combinations into train and test
train_combinations, test_combinations = train_test_split(
    filtered_combinations,
    test_size=test_ratio,
    random_state=42,
    stratify=filtered_labels
)

# Further split training combinations into train and validation
train_combinations, val_combinations = train_test_split(
    train_combinations,
    test_size=val_ratio / (1 - test_ratio),
    random_state=42,
    stratify=combination_label_mapping.loc[train_combinations].values
)

# Filter data to create training, validation, and testing sets
training_data = filtered_data[filtered_data["combination_id"].isin(train_combinations)].drop(columns=["combination_id"])
validation_data = filtered_data[filtered_data["combination_id"].isin(val_combinations)].drop(columns=["combination_id"])
testing_data = filtered_data[filtered_data["combination_id"].isin(test_combinations)].drop(columns=["combination_id"])

# Save the datasets
training_data.to_csv("/content/drive/MyDrive/P2/T1/Dataset/overlapped/ML_o_train.csv", index=False)
validation_data.to_csv("/content/drive/MyDrive/P2/T1/Dataset/overlapped/ML_o_val.csv", index=False)
testing_data.to_csv("/content/drive/MyDrive/P2/T1/Dataset/overlapped/ML_o_test.csv", index=False)

# Print confirmation and class distributions
print(f"Training dataset saved with {training_data.shape[0]} samples.")
print(f"Validation dataset saved with {validation_data.shape[0]} samples.")
print(f"Testing dataset saved with {testing_data.shape[0]} samples.")

print("\nTraining Data Distribution:")
print(training_data['disease_label'].value_counts())

print("\nValidation Data Distribution:")
print(validation_data['disease_label'].value_counts())

print("\nTesting Data Distribution:")
print(testing_data['disease_label'].value_counts())

# Validate the number of unique disease labels
training_labels = set(training_data["disease_label"].unique())
testing_labels = set(testing_data["disease_label"].unique())
validation_labels = set(validation_data["disease_label"].unique())

if training_labels == testing_labels == validation_labels :
    print("All training, validation and testing datasets have all same disease labels.")
else:
    missing_in_training = testing_labels - training_labels
    missing_in_testing = training_labels - testing_labels
    missing_in_validation = training_labels - validation_labels
    print(f"Labels missing in training dataset: {missing_in_training}")
    print(f"Labels missing in testing dataset: {missing_in_testing}")
    print(f"Labels missing in validation dataset: {missing_in_validation}")

"""# Balance the disease label across all 3 train,validate,test sets"""

# Identify the common disease labels across all splits
common_labels = training_labels.intersection(testing_labels).intersection(validation_labels)

# Filter datasets to include only the common disease labels
training_data = training_data[training_data["disease_label"].isin(common_labels)]
validation_data = validation_data[validation_data["disease_label"].isin(common_labels)]
testing_data = testing_data[testing_data["disease_label"].isin(common_labels)]

# Save the updated datasets
training_data.to_csv("/content/drive/MyDrive/P2/T1/Dataset/overlapped/ML_o_train_filtered.csv", index=False)
validation_data.to_csv("/content/drive/MyDrive/P2/T1/Dataset/overlapped/ML_o_val_filtered.csv", index=False)
testing_data.to_csv("/content/drive/MyDrive/P2/T1/Dataset/overlapped/ML_o_test_filtered.csv", index=False)

# Validate the consistency of disease labels across splits
training_labels = set(training_data["disease_label"].unique())
testing_labels = set(testing_data["disease_label"].unique())
validation_labels = set(validation_data["disease_label"].unique())

if training_labels == testing_labels == validation_labels:
    print("All training, validation, and testing datasets now have the same disease labels.")
else:
    print("Mismatch still exists in disease labels.")

# Print the final count of disease labels
print(f"Final number of unique disease labels: {len(training_labels)}")

# Validate the number of unique disease labels
training_labels = set(training_data["disease_label"].unique())
testing_labels = set(testing_data["disease_label"].unique())
validation_labels = set(validation_data["disease_label"].unique())

if training_labels == testing_labels == validation_labels :
    print("All training, validation and testing datasets have all same disease labels.")
else:
    missing_in_training = testing_labels - training_labels
    missing_in_testing = training_labels - testing_labels
    missing_in_validation = training_labels - validation_labels
    print(f"Labels missing in training dataset: {missing_in_training}")
    print(f"Labels missing in testing dataset: {missing_in_testing}")
    print(f"Labels missing in validation dataset: {missing_in_validation}")

import pandas as pd
import matplotlib.pyplot as plt

# Load the training dataset
training_dataset = pd.read_csv("/content/drive/MyDrive/P2/T1/Dataset/overlapped/ML_o_train_filtered.csv")

# Plot the distribution of diseases in the training dataset
def plot_training_distribution(data, title):
    disease_counts = data['disease_label'].value_counts().sort_values()
    plt.figure(figsize=(18, 8))
    bars = disease_counts.plot(kind='bar', color='blue', alpha=0.7)

    # Add the number of rows on top of each bar
    for index, value in enumerate(disease_counts):
        plt.text(index, value + 10, str(value), ha='center', va='bottom', fontsize=9)

    # Customize the plot
    plt.title(title, fontsize=16)
    plt.xlabel("Disease Label", fontsize=12)
    plt.ylabel("Number of Samples", fontsize=12)
    plt.xticks(rotation=90, fontsize=8)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# Call the plotting function for training dataset
plot_training_distribution(training_dataset, "Training Dataset Distribution")

"""# Check any duplicate rows in train,valid, and test sets"""

# Check for duplicate rows within each dataset
import pandas as pd

train_data = pd.read_csv("/content/drive/MyDrive/P2/T1/Dataset/overlapped/ML_o_train_filtered.csv")
val_data =  pd.read_csv("/content/drive/MyDrive/P2/T1/Dataset/overlapped/ML_o_val_filtered.csv")
test_data =  pd.read_csv("/content/drive/MyDrive/P2/T1/Dataset/overlapped/ML_o_test_filtered.csv")

train_duplicates = train_data.duplicated().sum()
val_duplicates = val_data.duplicated().sum()
test_duplicates = test_data.duplicated().sum()

# Output the results
{
    "Train Duplicates": train_duplicates,
    "Validation Duplicates": val_duplicates,
    "Test Duplicates": test_duplicates
}