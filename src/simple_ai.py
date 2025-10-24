import json
import os
import re
from sentence_transformers import SentenceTransformer
import numpy as np


class SimpleF1Assistant:
    def __init__(self):
        # Используем легкую модель для эмбеддингов
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.knowledge_base = []
        self.drivers_data = []

    def load_f1_data(self, data_files):
        """Загружаем данные F1"""
        for file_path in data_files:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.drivers_data.extend(data)
                    self._build_knowledge_base(data)

        print(f"Загружено {len(self.drivers_data)} пилотов")
        print(f"Создано {len(self.knowledge_base)} фактов")

    def _build_knowledge_base(self, data):
        """Строим базу знаний из данных"""
        for driver in data:
            facts = [
                f"Пилот {driver.get('first_name', '')} {driver.get('last_name', '')}",
                f"Номер машины: {driver.get('driver_number', 'N/A')}",
                f"Команда: {driver.get('team_name', 'N/A')}",
                f"Страна: {driver.get('country', 'N/A')}"
            ]
            self.knowledge_base.extend([f for f in facts if 'N/A' not in f])

    def find_best_match(self, question):
        """Находим наиболее подходящий ответ простым поиском"""
        question_lower = question.lower()

        # Простой поиск по ключевым словам
        if any(word in question_lower for word in ['команда', 'team', 'за кого']):
            return self._answer_team_question(question)
        elif any(word in question_lower for word in ['номер', 'number', 'driver number']):
            return self._answer_number_question(question)
        elif any(word in question_lower for word in ['пилот', 'driver', 'водитель']):
            return self._answer_driver_question(question)
        else:
            return self._semantic_search(question)

    def _answer_team_question(self, question):
        """Отвечаем на вопросы о командах"""
        for driver in self.drivers_data:
            full_name = f"{driver.get('first_name', '')} {driver.get('last_name', '')}"
            if full_name.lower() in question.lower():
                return f"{full_name} выступает за команду {driver.get('team_name', 'N/A')}"

        return "Не могу найти информацию об этом пилоте. Попробуйте спросить по-другому."

    def _answer_number_question(self, question):
        """Отвечаем на вопросы о номерах"""
        for driver in self.drivers_data:
            full_name = f"{driver.get('first_name', '')} {driver.get('last_name', '')}"
            if full_name.lower() in question.lower():
                return f"{full_name} использует номер {driver.get('driver_number', 'N/A')}"

        return "Не могу найти информацию об этом пилоте."

    def _answer_driver_question(self, question):
        """Отвечаем на вопросы о пилотах в командах"""
        for driver in self.drivers_data:
            team = driver.get('team_name', '').lower()
            if team and team in question.lower():
                drivers_in_team = [
                    f"{d.get('first_name', '')} {d.get('last_name', '')}"
                    for d in self.drivers_data
                    if d.get('team_name', '').lower() == team
                ]
                if drivers_in_team:
                    return f"В команде {driver.get('team_name')} выступают: {', '.join(drivers_in_team)}"

        return "Не могу найти информацию об этой команде."

    def _semantic_search(self, question):
        """Семантический поиск с использованием эмбеддингов"""
        if not self.knowledge_base:
            return "База знаний пуста. Сначала загрузите данные F1."

        try:
            # Создаем эмбеддинги
            question_embedding = self.model.encode([question])
            knowledge_embeddings = self.model.encode(self.knowledge_base)

            # Вычисляем схожесть
            similarities = np.dot(knowledge_embeddings, question_embedding.T).flatten()
            best_match_idx = np.argmax(similarities)

            best_fact = self.knowledge_base[best_match_idx]
            return f"Нашел информацию: {best_fact}"

        except Exception as e:
            return f"Произошла ошибка при поиске: {e}"

    def chat(self):
        """Простой чат-интерфейс"""
        print("\n🤖 Простой F1 Assistant готов к работе!")
        print("Задавайте вопросы о пилотах и командах (напишите 'стоп' для выхода)")
        print("Примеры вопросов:")
        print("- За какую команду выступает Макс Ферстаппен?")
        print("- Какой номер у Льюиса Хэмилтона?")
        print("- Кто выступает за Ferrari?")

        while True:
            question = input("\n🧐 Ваш вопрос: ").strip()

            if question.lower() in ['стоп', 'stop', 'exit', 'quit']:
                print("🏁 До свидания! Возвращайтесь за новой информацией о F1!")
                break

            if question:
                answer = self.find_best_match(question)
                print(f"🤖 {answer}")
            else:
                print("Пожалуйста, введите вопрос")


def test_simple_assistant():
    """Тестируем упрощенного ассистента"""
    assistant = SimpleF1Assistant()

    # Загружаем сохраненные данные
    data_files = [f for f in os.listdir() if f.startswith('drivers_')]
    if data_files:
        print("Загружаем данные F1...")
        assistant.load_f1_data(data_files[:1])  # Берем первый файл

        # Тестовые вопросы
        test_questions = [
            "За какую команду выступает Макс Ферстаппен?",
            "Какой номер у Ландо Норриса?",
            "Кто выступает за Red Bull?",
            "Расскажи о Фернандо Алонсо"
        ]

        print("\n🧪 Тестовые вопросы:")
        for question in test_questions:
            answer = assistant.find_best_match(question)
            print(f"Q: {question}")
            print(f"A: {answer}\n")

        # Запускаем интерактивный чат
        assistant.chat()
    else:
        print("❌ Сначала запустите сбор данных F1! Запустите: python main.py")


if __name__ == "__main__":
    test_simple_assistant()