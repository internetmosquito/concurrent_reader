import multiprocessing
from multiprocessing import Value
import time
import csv
from pathlib import Path

counter = 0


def init(args):
    global counter
    counter = args


def read_data_file(files):
    global counter
    name = multiprocessing.current_process().name
    # Get the info from second item from tuple
    info = files[1].stat()
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
        print(f'Processed {line_count} lines in file {files[1].name} in process {name}.')
    with counter.get_lock():
        counter.value += 1


def read_data_files(path):
    # Initialize Counter to be used among processes
    counter = Value('i', 0)
    proccesed = 0
    # List all files in data folder
    data_dir = Path(path)
    files_in_basepath = (entry for entry in data_dir.iterdir() if entry.is_file())
    list_of_files = [(path + '/' + file.name, file)for file in files_in_basepath]
    with multiprocessing.Pool(initializer=init, initargs=(counter, )) as pool:
        pool.map(read_data_file, list_of_files, chunksize=1)
        proccesed = counter.value
    return proccesed

def main():
    data_files = 'test_data'
    start_time = time.time()
    processed = read_data_files(data_files)
    duration = time.time() - start_time
    print(f"Processed {processed} data files in {duration} seconds")
    return duration

