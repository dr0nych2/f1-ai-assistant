from src.f1_data import test_f1_api
from src.simple_ai import test_simple_assistant


def main():
    print("🏎️ F1 AI Assistant - Запуск!")

    # Сначала собираем данные
    print("=== СБОР ДАННЫХ F1 ===")
    test_f1_api()

    # Затем тестируем упрощенного AI ассистента
    print("\n=== ЗАПУСК ПРОСТОГО AI АССИСТЕНТА ===")
    test_simple_assistant()


if __name__ == "__main__":
    main()