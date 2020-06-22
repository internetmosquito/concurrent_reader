import time
import csv
from pathlib import Path


def read_data_file(file, path):
    # This will only work on Linux or Mac though...need to get separator by OS platform instead
    with open(path + '/' + file.name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            # Just assume we do something very interesting with these values...
            values = ''
            for item in row:
                values = values + item + ' '
            #print(values)
            line_count += 1
        print(f'Processed {line_count} lines in file {file.name}.')


def read_data_files(path):
    # List all files in data folder
    num_files = 0
    data_dir = Path(path)
    files_in_basepath = (entry for entry in data_dir.iterdir() if entry.is_file())
    for item in files_in_basepath:
        info = item.stat()
        print(f'File name is {item.name} with size {round(info.st_size / float(1<<10), 2)} KB')
        read_data_file(item, data_dir.name)
        num_files += 1
    return num_files


def main():
    data_files = 'test_data'
    start_time = time.time()
    num_files = read_data_files(data_files)
    duration = time.time() - start_time
    print(f"Processed {num_files} data files in {duration} seconds")
    return duration
