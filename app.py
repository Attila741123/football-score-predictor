import streamlit as st
import requests
import datetime
import random

# Вставляем твой API токен
API_TOKEN = 'f2285e27e24948fca025d71981350602'  # Твой API токен
API_URL = 'https://api.b365api.com/v1/bet365/inplay'  # API endpoint для получения матчей

# Функция для получения данных о матчах через API
def get_match_data():
    headers = {
        'Authorization': f'Bearer {API_TOKEN}'
    }
    response = requests.get(API_URL, headers=headers)
    if response.status_code == 200:
        return response.json()['events']  # Получаем список событий
    else:
        st.error("Ошибка получения данных от API")
        return []

# Функция для прогноза точного счёта на основе статистики
def predict_score(team1_stats, team2_stats):
    # Прогнозируем счёт с учётом средней результативности команд
    home_score = round(team1_stats['avg_goals'] + random.uniform(-0.5, 0.5), 1)
    away_score = round(team2_stats['avg_goals'] + random.uniform(-0.5, 0.5), 1)

    return home_score, away_score

# Функция для оценки статистики команды за сезон
def calculate_team_stats(matches, team_name):
    total_goals = 0
    total_conceded = 0
    total_games = 0

    # Пробежимся по всем матчам команды
    for match in matches:
        if match['team1'] == team_name:
            total_goals += match['score1']
            total_conceded += match['score2']
            total_games += 1
        elif match['team2'] == team_name:
            total_goals += match['score2']
            total_conceded += match['score1']
            total_games += 1

    if total_games == 0:
        return {'avg_goals': 0, 'avg_conceded': 0}  # Если нет матчей, возвращаем пустую статистику

    avg_goals = total_goals / total_games
    avg_conceded = total_conceded / total_games

    return {'avg_goals': avg_goals, 'avg_conceded': avg_conceded, 'games_played': total_games}

# Основной код для Streamlit
def main():
    st.title('Прогнозы на футбольные матчи')

    # Получаем данные о матчах
    match_data = get_match_data()

    if match_data:
        st.subheader("Предстоящие футбольные события")

        # Перебираем все события и показываем их
        for event in match_data:
            match_name = f"{event['team1']} vs {event['team2']}"
            match_time = datetime.datetime.strptime(event['startTime'], '%Y.%m.%d %H:%M')
            formatted_time = match_time.strftime('%d %B %Y, %H:%M')

            st.write(f"**{match_name}**")
            st.write(f"Время: {formatted_time}")

            # Эмуляция статистики матчей команды для примера (здесь предполагается, что у нас есть все данные)
            team1_stats = calculate_team_stats(event['team1_matches'], event['team1'])
            team2_stats = calculate_team_stats(event['team2_matches'], event['team2'])

            # Прогнозируем счёт
            home_score, away_score = predict_score(team1_stats, team2_stats)

            st.write(f"Прогнозированный счёт: {home_score} - {away_score}")
            st.write(f"Ссылка на матч: [Перейти в Bet365]({event['evLink']})")
            st.write("-" * 50)

    else:
        st.error("Нет доступных данных для отображения.")

if __name__ == "__main__":
    main()
