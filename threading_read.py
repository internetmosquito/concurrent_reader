import concurrent.futures
import csv
import threading
import time
from pathlib import Path

c_lock = threading.Lock()
counter = 0


def read_data_file(files):
    # Get the info from second item from tuple
    info = files[1].stat()
    global c_lock
    global counter
    c_lock.acquire()
    print(f'File name is {files[1].name} with size {round(info.st_size / float(1 << 10), 2)} KB')
    with open(files[0]) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            # Just assume we do something very interesting with these values...
            values = ''
            for item in row:
                values = values + item + ' '
            #print(values)
            line_count += 1
        print(f'Processed {line_count} lines in file {files[1].name}.')
    counter += 1
    c_lock.release()


def read_data_files(path):
    # List all files in data folder
    data_dir = Path(path)
    files_in_basepath = (entry for entry in data_dir.iterdir() if entry.is_file())
    list_of_files = [(path + '/' + file.name, file) for file in files_in_basepath]
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
        executor.map(read_data_file, list_of_files)


def main():
    data_files = 'test_data'
    start_time = time.time()
    read_data_files(data_files)
    duration = time.time() - start_time
    print(f"Processed {counter} data files in {duration} seconds")
    return duration
