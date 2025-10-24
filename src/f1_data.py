import requests
import json
from datetime import datetime


class F1DataCollector:
    def __init__(self):
        self.base_url = "https://api.openf1.org/v1"

    def get_current_drivers(self):
        """Получить информацию о всех пилотах текущего сезона"""
        try:
            url = f"{self.base_url}/drivers"
            response = requests.get(url)
            response.raise_for_status()

            drivers = response.json()

            print("=== ПИЛОТЫ ФОРМУЛЫ 1 ===")
            for driver in drivers[:10]:  # Покажем первых 10
                full_name = f"{driver.get('first_name', '')} {driver.get('last_name', '')}"
                team = driver.get('team_name', 'N/A')
                country = driver.get('country', 'N/A')
                driver_number = driver.get('driver_number', 'N/A')

                print(f"{driver_number}. {full_name} - {team} ({country})")

            return drivers

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к API: {e}")
            return None

    def get_current_sessions(self):
        """Получить информацию о текущих сессиях"""
        try:
            url = f"{self.base_url}/sessions"
            params = {
                'year': 2024,  # Текущий год
                'session_key': 'latest'  # Последняя сессия
            }
            response = requests.get(url, params=params)
            response.raise_for_status()

            sessions = response.json()

            print("\n=== ТЕКУЩИЕ СЕССИИ ===")
            for session in sessions[:5]:  # Покажем 5 последних сессий
                session_name = session.get('session_name', 'N/A')
                meeting_name = session.get('meeting_name', 'N/A')
                date_start = session.get('date_start', 'N/A')

                print(f"{session_name} - {meeting_name} ({date_start[:10]})")

            return sessions

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к API: {e}")
            return None

    def get_driver_standings(self):
        """Получить позиции пилотов (имитация через данные сессий)"""
        try:
            # Получаем последнюю сессию
            sessions_url = f"{self.base_url}/sessions"
            params = {'session_key': 'latest'}
            sessions_response = requests.get(sessions_url, params=params)
            sessions_response.raise_for_status()

            sessions = sessions_response.json()
            if not sessions:
                print("Нет данных о сессиях")
                return None

            latest_session = sessions[0]
            session_key = latest_session.get('session_key')

            # Получаем позиции для этой сессии
            positions_url = f"{self.base_url}/position"
            params = {'session_key': session_key}
            positions_response = requests.get(positions_url, params=params)
            positions_response.raise_for_status()

            positions = positions_response.json()

            print("\n=== ПОЗИЦИИ В ПОСЛЕДНЕЙ СЕССИИ ===")
            # Группируем по driver_number и берем последнюю позицию
            driver_positions = {}
            for position in positions:
                driver_num = position.get('driver_number')
                if driver_num:
                    driver_positions[driver_num] = position.get('position', 'N/A')

            # Получаем информацию о пилотах
            drivers_url = f"{self.base_url}/drivers"
            drivers_response = requests.get(drivers_url)
            drivers_response.raise_for_status()
            drivers = drivers_response.json()

            # Сопоставляем позиции с именами пилотов
            for driver_num, position in list(driver_positions.items())[:10]:
                driver_info = next((d for d in drivers if d.get('driver_number') == driver_num), None)
                if driver_info:
                    full_name = f"{driver_info.get('first_name', '')} {driver_info.get('last_name', '')}"
                    print(f"P{position}. {full_name} (#{driver_num})")

            return driver_positions

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к API: {e}")
            return None

    def save_data_to_file(self, data, filename_prefix):
        """Сохранить данные в файл JSON"""
        if data:
            filename = f"{filename_prefix}_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"\nДанные сохранены в файл: {filename}")
            return filename
        return None


# Простая функция для тестирования
def test_f1_api():
    collector = F1DataCollector()

    print("🏎️ Тестируем OpenF1 API...")

    # Тестируем получение данных о пилотах
    drivers = collector.get_current_drivers()
    collector.save_data_to_file(drivers, "drivers")

    # Тестируем получение сессий
    sessions = collector.get_current_sessions()
    collector.save_data_to_file(sessions, "sessions")

    # Тестируем получение позиций
    standings = collector.get_driver_standings()


if __name__ == "__main__":
    test_f1_api()