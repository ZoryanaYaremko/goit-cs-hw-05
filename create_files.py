import os
from pathlib import Path
import random

# Функція для створення файлів
def create_test_files(folder: Path, num_files: int):
    extensions = ['txt', 'jpg', 'png', 'pdf', 'docx', 'xlsx']  # Різні типи файлів
    folder.mkdir(parents=True, exist_ok=True)  # Створення папки, якщо вона не існує

    for i in range(1, num_files + 1):
        ext = random.choice(extensions)
        file_name = f'file_{i}.{ext}'  # Ім'я файлу
        file_path = folder / file_name
        with open(file_path, 'w') as f:
            f.write(f"Це файл номер {i}. Він містить розширення {ext}.")  # Текст у файлі

    print(f"Створено {num_files} файлів у папці {folder}")

if __name__ == "__main__":
    # Введення шляху до папки та кількості файлів від користувача
    output_folder = input("Введіть шлях до папки для файлів: ") or "test_folder"
    num_files = int(input("Введіть кількість файлів для створення: ") or 30)

    folder_path = Path(output_folder)

    # Виклик функції для створення файлів
    create_test_files(folder_path, num_files)
