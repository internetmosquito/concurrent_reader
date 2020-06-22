import asyncio
import time
import csv
from pathlib import Path

counter = 0


async def read_data_file(files):
    # Get the info from second item from tuple
    info = files[1].stat()
    global counter
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


async def read_data_files(path):
    # List all files in data folder
    data_dir = Path(path)
    files_in_basepath = (entry for entry in data_dir.iterdir() if entry.is_file())
    list_of_files = [(path + '/' + file.name, file) for file in files_in_basepath]
    tasks = []
    for file in list_of_files:
        task = asyncio.ensure_future(read_data_file(file))
        tasks.append(task)
    await asyncio.gather(*tasks, return_exceptions=True)


def main():
    data_files = 'test_data'
    start_time = time.time()
    asyncio.get_event_loop().run_until_complete(read_data_files(data_files))
    duration = time.time() - start_time
    print(f"Processed {counter} data files in {duration} seconds")
    return duration
