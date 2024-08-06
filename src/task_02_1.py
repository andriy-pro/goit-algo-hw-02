import queue
import threading
import time
from queue import Queue

from colorama import Fore, Style, init
from faker import Faker

# Ініціалізація colorama для автоматичного скидання кольорів
init(autoreset=True)

# Створення об'єкта Faker з локалізацією 'uk_UA' для генерації імен
fake = Faker("uk_UA")


def generate_request(request_id: int) -> str:
    name = fake.first_name()
    surname = fake.last_name()
    return f"№ {request_id}: {name} {surname}"


def process_request(q: Queue) -> str:
    if not q.empty():
        processed_request = q.get()
        return Fore.YELLOW + f"Обробляється {processed_request}"
    else:
        return Fore.GREEN + Style.BRIGHT + "Вільна каса!" + Style.RESET_ALL


def print_queue(q: Queue, last_message: str) -> None:
    clear_screen()
    print(last_message)
    if not q.empty():
        for item in list(q.queue):
            print(item)
    print(
        "\nНатисніть Enter для додавання нової заявки, або введіть будь-який інший символ для завершення."
    )


def clear_screen() -> None:
    print("\033[H\033[J", end="")


def main() -> None:
    q: Queue = queue.Queue()
    request_id: int = 0  # Початковий ідентифікатор заявки
    last_message: str = (
        ""  # Останнє повідомлення для відображення після очищення екрану
    )

    interval_input: str = input(
        "Введіть швидкість обробки заявок у секундах (1-9, за замовчуванням 3): "
    )
    if interval_input == "":
        interval: int = 3
    else:
        try:
            interval = int(interval_input)
            if not (1 <= interval <= 9):
                raise ValueError
        except ValueError:
            print(
                Fore.RED
                + f"Введено: '{Fore.YELLOW}{interval_input}{Fore.RED}'\nНевірне значення. Використовується значення за умовчанням: 3 сек"
            )
            input("Натисніть Enter для продовження...")
            interval = 3

    stop_event: threading.Event = threading.Event()

    def user_input_thread() -> None:
        """
        Потік для обробки введення користувача.
        """
        nonlocal request_id, last_message  # Дозволяє змінювати ці змінні всередині функції
        while not stop_event.is_set():  # Поки сигнал зупинки не встановлено
            key: str = input()  # Очікування введення користувача
            if key == "":  # Якщо натиснуто Enter
                request_id += 1  # Збільшення лічильника заявок
                request: str = generate_request(request_id)  # Генерація нової заявки
                q.put(request)  # Додавання заявки до черги
                last_message = Fore.BLUE + f"Додана заявка {request}"
            else:
                print(Fore.MAGENTA + "Завершення роботи.")
                stop_event.set()  # Встановлення сигналу зупинки
                break
            print_queue(q, last_message)  # Вивід поточного стану черги

    def request_processing_thread() -> None:
        """
        Потік для обробки заявок з черги.
        """
        nonlocal last_message
        while not stop_event.is_set():
            last_message = process_request(q)  # Обробка заявки
            print_queue(q, last_message)
            time.sleep(interval)  # Затримка відповідно до вказаного інтервалу

    input_thread: threading.Thread = threading.Thread(
        target=user_input_thread, daemon=True
    )
    processing_thread: threading.Thread = threading.Thread(
        target=request_processing_thread, daemon=True
    )
    input_thread.start()  # Запуск потоку введення користувача
    processing_thread.start()  # Запуск потоку обробки заявок

    input_thread.join()  # Блокування потоку до завершення input_thread
    stop_event.set()  # Встановлення сигналу зупинки для інших потоків
    processing_thread.join()  # Блокування потоку до завершення processing_thread


if __name__ == "__main__":
    main()
