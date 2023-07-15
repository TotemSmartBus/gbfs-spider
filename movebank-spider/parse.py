import os
import csv


def parse_csv_file(input_file):
    print(f"File: {input_file}")
    output_data = []
    required_columns = ['location-long', 'location-lat']
    try:
        with open(input_file, 'r') as file:
            reader = csv.DictReader(file)
            headers = reader.fieldnames
            if not all(col in headers for col in required_columns):
                print('Error: File does not contain all required columns!')
                output_data.clear()
            else:
                for row in reader:
                    if row.get('location-long') and row.get('location-lat'):
                        lat = row['location-lat']
                        lng = row['location-long']
                        output_data.append({'lng': lng, 'lat': lat})
    except UnicodeDecodeError as e:
        print('Error: Failed to decode file!')
        output_data.clear()
    return output_data


def write_csv_file(output_file, data):
    fieldnames = ['lng', 'lat']
    with open(output_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def is_file_parsed(file_path):
    output_file = f"{os.path.splitext(file_path)[0]}-data.csv"
    return os.path.exists(output_file)


def process_files(input_dir, output_dir):
    for root, _, files in os.walk(input_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            test_path = os.path.join(output_dir, file_name)
            if os.path.isfile(file_path) and file_name.lower().endswith('.csv'):
                if is_file_parsed(test_path):
                    print("Skip: File already existed!")
                    continue
                output_data = parse_csv_file(file_path)
                if output_data:
                    # output_subdir = os.path.relpath(root, input_dir)
                    output_file_name = f"{os.path.splitext(file_name)[0]}-data.csv"
                    output_file_path = os.path.join(output_dir, output_file_name)
                    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
                    write_csv_file(output_file_path, output_data)
                    print("Done")
            print()


input_directory = r'/home/lyy/movebank-all'
output_directory = r'/home/lyy/movebank-clean'

process_files(input_directory, output_directory)
