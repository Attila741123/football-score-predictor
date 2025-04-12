import requests
from datetime import datetime, timedelta

# API ключи
rapidapi_key = 'a46d78e235mshf84713c91f6721ap1e0f8fjsn0b4e2a83c8b7'

# URL для запросов
api_football_url = 'https://api-football-v1.p.rapidapi.com/v2/odds/league/865927/bookmaker/5?page=2'
pinnacle_odds_url = 'https://pinnacle-odds.p.rapidapi.com/kit/v1/markets?sport_id=3&is_have_odds=true'
sofascore_url = 'https://sofascore.p.rapidapi.com/players/get-all-statistics?playerId=155997'

# Заголовки для запросов
headers = {
    'x-rapidapi-key': rapidapi_key
}

# Функция для выполнения запросов и получения данных
def get_football_odds():
    try:
        response = requests.get(api_football_url, headers=headers)
        response.raise_for_status()  # Для отслеживания ошибок HTTP
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.RequestException as err:
        print(f"Request Error: {err}")
    return None

def get_pinnacle_odds():
    try:
        headers['x-rapidapi-host'] = 'pinnacle-odds.p.rapidapi.com'
        response = requests.get(pinnacle_odds_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as err:
        print(f"Request Error: {err}")
    return None

def get_sofascore_stats():
    try:
        headers['x-rapidapi-host'] = 'sofascore.p.rapidapi.com'
        response = requests.get(sofascore_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as err:
        print(f"Request Error: {err}")
    return None

# Фильтрация матчей, которые будут в течение следующих 24 часов
def filter_upcoming_matches(matches_data):
    now = datetime.utcnow()
    future_time = now + timedelta(hours=24)

    upcoming_matches = []
    if matches_data:
        for match in matches_data['api']['fixtures']:
            match_time = datetime.strptime(match['event_date'], '%Y-%m-%dT%H:%M:%SZ')
            if now <= match_time <= future_time:
                upcoming_matches.append(match)

    return upcoming_matches

# Функция для анализа матчей, статистики и коэффициентов
def analyze_match_data(matches_data, pinnacle_data, sofascore_data):
    print("Upcoming Matches in the Next 24 Hours:")
    for match in matches_data:
        home_team = match['homeTeam']['team_name']
        away_team = match['awayTeam']['team_name']
        match_time = match['event_date']

        # Коэффициенты Pinnacle для текущего матча
        odds = next((item for item in pinnacle_data['data'] if item['homeTeam']['team_id'] == match['homeTeam']['team_id'] and
                     item['awayTeam']['team_id'] == match['awayTeam']['team_id']), None)

        # Статистика игроков (можно расширить под каждого игрока)
        player_stats = sofascore_data.get('players', [])

        print(f"{home_team} vs {away_team}, Date: {match_time}")
        if odds:
            print(f"  Pinnacle Odds - Home: {odds['homeOdds']}, Away: {odds['awayOdds']}")
        else:
            print("  No Pinnacle odds available for this match.")

        if player_stats:
            print("  Players Stats (first player):")
            player = player_stats[0]  # Пример, можно расширить
            print(f"    {player['name']} - Goals: {player['goals']}")

        print("\n---\n")

# Главная функция
def main():
    # Получаем данные
    football_odds_data = get_football_odds()
    pinnacle_odds_data = get_pinnacle_odds()
    sofascore_stats_data = get_sofascore_stats()

    # Фильтруем только те матчи, которые проходят в ближайшие 24 часа
    if football_odds_data:
        upcoming_matches = filter_upcoming_matches(football_odds_data)

        if upcoming_matches:
            # Анализируем данные для матчей
            analyze_match_data(upcoming_matches, pinnacle_odds_data, sofascore_stats_data)
        else:
            print("No upcoming matches within the next 24 hours.")
    else:
        print("Error fetching football odds data.")

# Запуск программы
if __name__ == "__main__":
    main()
