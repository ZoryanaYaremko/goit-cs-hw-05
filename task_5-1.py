import asyncio
import aiofiles
import shutil
import os
from pathlib import Path
import argparse
import logging

# Налаштування логування
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', handlers=[logging.FileHandler('file_sort.log', 'w'), logging.StreamHandler()])

# Асинхронна функція для копіювання файлів
async def copy_file(file: Path, target_folder: Path):
    try:
        ext = file.suffix[1:]  # Отримуємо розширення без крапки
        if not ext:
            ext = "no_extension"  # Якщо немає розширення, кладемо в окрему папку
        target_dir = target_folder / ext
        target_dir.mkdir(parents=True, exist_ok=True)
        target_file = target_dir / file.name

        # Копіювання файлу
        async with aiofiles.open(file, 'rb') as fsrc:
            async with aiofiles.open(target_file, 'wb') as fdst:
                while chunk := await fsrc.read(1024):
                    await fdst.write(chunk)
        logging.info(f"Файл {file.name} скопійовано у {target_dir}")

    except Exception as e:
        logging.error(f"Помилка копіювання файлу {file}: {e}")

# Асинхронна функція для читання файлів з вихідної папки
async def read_folder(source_folder: Path, target_folder: Path):
    tasks = []
    try:
        for item in source_folder.rglob('*'):  # Рекурсивний обхід папок
            if item.is_file():
                tasks.append(copy_file(item, target_folder))
        await asyncio.gather(*tasks)  # Виконання всіх задач
    except Exception as e:
        logging.error(f"Помилка читання папки {source_folder}: {e}")

# Головна функція для запуску
async def main(source: str, target: str):
    source_folder = Path(source)
    target_folder = Path(target)
    if not source_folder.is_dir():
        logging.error(f"Вихідна папка {source_folder} не існує!")
        return

    target_folder.mkdir(parents=True, exist_ok=True)
    await read_folder(source_folder, target_folder)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Сортування файлів за розширенням")
    parser.add_argument("source", type=str, help="Шлях до вихідної папки")
    parser.add_argument("target", type=str, help="Шлях до папки призначення")
    args = parser.parse_args()

    # Запуск асинхронної функції
    asyncio.run(main(args.source, args.target))
