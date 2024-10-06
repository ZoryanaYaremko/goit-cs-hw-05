import requests
import re
import matplotlib.pyplot as plt
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

# Функція для завантаження тексту з URL
def load_text_from_url(url):
    response = requests.get(url)
    return response.text

# Функція для очищення та розбиття тексту на слова
def clean_and_split_text(text):
    text = re.sub(r'[^\w\s]', '', text)  # Видалити всі символи, окрім слів та пробілів
    words = text.lower().split()  # Перетворити текст на нижній регістр та розбити на слова
    return words

# Map-функція для підрахунку слів у частині тексту
def map_word_count(text_chunk):
    return Counter(text_chunk)

# Reduce-функція для об'єднання результатів підрахунку слів
def reduce_word_counts(results):
    total_count = Counter()
    for result in results:
        total_count.update(result)
    return total_count

# Візуалізація топ N слів
def visualize_top_words(word_counts, top_n=10):
    common_words = word_counts.most_common(top_n)
    words, counts = zip(*common_words)
    
    plt.barh(words, counts, color='skyblue')
    plt.xlabel('Frequency')
    plt.ylabel('Words')
    plt.title(f'Top {top_n} Most Frequent Words')
    plt.gca().invert_yaxis()  # Інвертувати вісь Y для більш зручного вигляду
    plt.show()

# Головна функція, яка завантажує текст, обробляє та візуалізує результат
def main(url, top_n=10, num_threads=4):
    # Завантажити текст
    text = load_text_from_url(url)
    
    # Очищення тексту
    words = clean_and_split_text(text)
    
    # Розбити текст на частини для багатопотоковості
    chunk_size = len(words) // num_threads
    text_chunks = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]
    
    # Виконання Map-фази в потоках
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        results = list(executor.map(map_word_count, text_chunks))
    
    # Reduce-фаза для об'єднання результатів
    total_word_count = reduce_word_counts(results)
    
    # Візуалізація результату
    visualize_top_words(total_word_count, top_n)

if __name__ == "__main__":
    # URL для тестування (замість цього використовуйте власну URL)
    url = "https://www.gutenberg.org/files/84/84-0.txt"  # Текст книги "Frankenstein"
    
    # Виклик головної функції
    main(url, top_n=10)
