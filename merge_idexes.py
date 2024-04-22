import os
import csv


def merge_csv_files(folder_path, output_file):
    # Check if the folder path exists
    if not os.path.isdir(folder_path):
        print("Folder path does not exist.")
        return

    # Get a list of CSV files in the folder
    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

    if not csv_files:
        print("No CSV files found in the folder.")
        return

    # Open the output CSV file in write mode
    with open(output_file, 'w', newline='') as output_csv_file:
        # Create a CSV writer object
        writer = csv.writer(output_csv_file)

        # Iterate over each CSV file and write its data to the output file
        for file in csv_files:
            file_path = os.path.join(folder_path, file)
            with open(file_path, 'r', newline='') as input_csv_file:
                # Create a CSV reader object
                reader = csv.reader(input_csv_file)

                # Write the header row only if it's the first file
                if file == csv_files[0]:
                    writer.writerow(next(reader))  # Write the header row

                # Write the data rows
                for row in reader:
                    writer.writerow(row)

    print(f"Merged data saved to '{output_file}'.")


# Example usage
folder_path = "indices"
output_file = "merged_output.csv"

merge_csv_files(folder_path, output_file)
