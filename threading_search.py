import os
import threading
import time
from collections import defaultdict

# Функція для пошуку ключових слів у файлах
def search_keywords_in_files(file_list, keywords, result):
    for file_path in file_list:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                for keyword in keywords:
                    if keyword in content:
                        result[keyword].append(file_path)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

# Функція для багатопотокового пошуку
def threaded_search(files, keywords):
    threads = []
    num_threads = 4
    result = defaultdict(list)
    chunk_size = len(files) // num_threads

    for i in range(num_threads):
        start_index = i * chunk_size
        end_index = (i + 1) * chunk_size if i != num_threads - 1 else len(files)
        thread = threading.Thread(target=search_keywords_in_files, args=(files[start_index:end_index], keywords, result))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return result

# Основна функція для багатопотокового пошуку
def main_threaded_search(directory, keywords):
    files = [os.path.join(directory, file) for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]
    start_time = time.time()
    result = threaded_search(files, keywords)
    end_time = time.time()
    print(f"Threaded search took {end_time - start_time} seconds")
    return result

# Виклик функції
directory = '/Users/asd/Documents/University_Code/Algorithms'
keywords = ['Цільовий елемент порівнюється із середнім.', 'Правильно підібраний алгоритм пошуку']
result_threaded = main_threaded_search(directory, keywords)
print(result_threaded)
