import requests
import time

API_TOKEN = "f2285e27e24948fca025d71981350602"
BASE_URL = "https://api.football-data.org/v4/matches"

headers = {
    "X-Auth-Token": API_TOKEN
}

def fetch_matches():
    url = BASE_URL
    matches = []

    while True:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            matches.extend(data['matches'])
            
            # Проверка на количество оставшихся запросов в минуту
            remaining_requests = int(response.headers['X-Requests-Available-Minute'])
            if remaining_requests <= 0:
                reset_time = int(response.headers['X-RequestCounter-Reset'])
                print(f"Лимит запросов достигнут, ожидаем {reset_time} секунд...")
                time.sleep(reset_time)  # Ждем, пока сбросится счетчик запросов
            else:
                break
        else:
            print(f"Ошибка при получении данных: {response.status_code}")
            break
    
    return matches

def predict_score(matches):
    # Логика прогнозирования для каждого матча
    for match in matches:
        home_team = match['homeTeam']['name']
        away_team = match['awayTeam']['name']
        print(f"Прогноз для матча {home_team} vs {away_team}")
        # Прогнозирование результатов и вывод
        # Здесь ваша логика прогнозирования

matches = fetch_matches()

# Далее, здесь вы вызываете функцию для прогнозов на матчи:
predict_score(matches)
