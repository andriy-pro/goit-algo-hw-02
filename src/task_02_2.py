from collections import deque


def is_palindrome(input_string: str) -> bool:
    # Виділення із заданого рядка цифро-буквених символів та приведення їх до нижнього регістру
    cleaned_string = "".join(char.lower() for char in input_string if char.isalnum())

    # Створення двосторонньої черги
    dq = deque(cleaned_string)

    while len(dq) > 1:
        if dq.popleft() != dq.pop():
            return False
    return True


# Тестування функції
test_strings = [
    "Hello",
    "A man a plan a canal Panama",
    "racecar",
    "Was it a car or a cat I saw",
    "No lemon no melon",
    "Паліндром — і ні морд, ні лап",
    "Три психи пили Пилипихи спирт",
    "Уму – мінімуму!",
    "А результатів? Вітать лузера!",
    "Аргентина манить негра",
    "А баба на волі — цілована баба",
    "І розморозь зором зорі",
    "Кит на морі романтик",
    "Літо, домашки, дедлайни... Здуріти! Иті рудзи нйал, де дик шамо - до тіл!",
]

for test in test_strings:
    print(f"'{test}' is a palindrome: {is_palindrome(test)}")
