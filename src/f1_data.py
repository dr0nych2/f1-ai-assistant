import requests
import pandas as pd


class F1DataCollector:
    def __init__(self):
        self.base_url = "http://ergast.com/api/f1"

    def get_current_standings(self):
        """Получить текущую таблицу чемпионата пилотов"""
        try:
            url = f"{self.base_url}/current/driverStandings.json"
            response = requests.get(url)
            response.raise_for_status()  # Проверка на ошибки

            data = response.json()
            standings = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']

            print("=== ТЕКУЩИЙ ЧЕМПИОНАТ ПИЛОТОВ ===")
            for driver in standings:
                position = driver['position']
                driver_name = f"{driver['Driver']['givenName']} {driver['Driver']['familyName']}"
                points = driver['points']
                team = driver['Constructors'][0]['name']

                print(f"{position}. {driver_name} ({team}) - {points} очков")

            return standings

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к API: {e}")
            return None

    def get_last_race_result(self):
        """Получить результаты последней гонки"""
        try:
            url = f"{self.base_url}/current/last/results.json"
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()
            race = data['MRData']['RaceTable']['Races'][0]

            print(f"\n=== ПОСЛЕДНЯЯ ГОНКА: {race['raceName']} ===")
            print(f"Трасса: {race['Circuit']['circuitName']}")
            print(f"Дата: {race['date']}")

            print("\nТоп-5 гонщиков:")
            for result in race['Results'][:5]:
                pos = result['position']
                driver = f"{result['Driver']['givenName']} {result['Driver']['familyName']}"
                team = result['Constructor']['name']
                print(f"{pos}. {driver} ({team})")

            return race

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к API: {e}")
            return None


# Простая функция для тестирования
def test_f1_api():
    collector = F1DataCollector()
    collector.get_current_standings()
    collector.get_last_race_result()


if __name__ == "__main__":
    test_f1_api()
