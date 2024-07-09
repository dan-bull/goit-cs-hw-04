import os
import multiprocessing
import time
from collections import defaultdict

# Функція для пошуку ключових слів у файлах
def search_keywords_in_files(file_list, keywords, queue):
    local_result = defaultdict(list)
    for file_path in file_list:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                for keyword in keywords:
                    if keyword in content:
                        local_result[keyword].append(file_path)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    queue.put(local_result)

# Функція для багатопроцесорного пошуку
def multiprocess_search(files, keywords):
    processes = []
    num_processes = 4
    queue = multiprocessing.Queue()
    chunk_size = len(files) // num_processes

    for i in range(num_processes):
        start_index = i * chunk_size
        end_index = (i + 1) * chunk_size if i != num_processes - 1 else len(files)
        process = multiprocessing.Process(target=search_keywords_in_files, args=(files[start_index:end_index], keywords, queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    result = defaultdict(list)
    while not queue.empty():
        local_result = queue.get()
        for keyword, paths in local_result.items():
            result[keyword].extend(paths)

    return result

# Основна функція для багатопроцесорного пошуку
def main_multiprocess_search(directory, keywords):
    files = [os.path.join(directory, file) for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]
    start_time = time.time()
    result = multiprocess_search(files, keywords)
    end_time = time.time()
    print(f"Multiprocess search took {end_time - start_time} seconds")
    return result

if __name__ == '__main__':
    directory = '/Users/asd/Documents/University_Code/Algorithms'
    keywords = ['Цільовий елемент порівнюється із середнім.', 'Правильно підібраний алгоритм пошуку']
    result_multiprocess = main_multiprocess_search(directory, keywords)
    print(result_multiprocess)
