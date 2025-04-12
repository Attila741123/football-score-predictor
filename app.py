import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

# Твой API ключ
API_TOKEN = "f2285e27e24948fca025d71981350602"

# Функция для получения матчей, которые пройдут в течение 24 часов
def get_upcoming_matches():
    url = "https://api.football-data.org/v4/matches"
    headers = {
        'X-Auth-Token': API_TOKEN,
    }
    
    # Получаем текущую дату и дату через 24 часа
    now = datetime.utcnow()
    end_time = now + timedelta(hours=24)
    
    # Переводим в формат ISO 8601 (например: '2025-04-13T00:00:00Z')
    now_str = now.isoformat() + "Z"
    end_time_str = end_time.isoformat() + "Z"
    
    params = {
        'dateFrom': now_str,
        'dateTo': end_time_str,
    }
    
    # Отправляем запрос
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    return data.get('matches', [])

# Функция для прогноза точного счёта
def predict_score(match):
    # Простейший прогноз (можно заменить на более сложную модель)
    return f"Прогноз для матча {match['homeTeam']['name']} - {match['awayTeam']['name']}: 2-1"

# Отображение матчей и прогнозов
def display_predictions(matches):
    for match in matches:
        home_team = match['homeTeam']['name']
        away_team = match['awayTeam']['name']
        date = match['utcDate']
        
        # Создаём кнопку для каждого матча
        if st.button(f"Прогноз для {home_team} против {away_team}"):
            prediction = predict_score(match)
            st.write(f"Матч: {home_team} против {away_team}")
            st.write(f"Дата: {date}")
            st.write(f"Прогноз: {prediction}")
        
# Основная функция
def main():
    st.title("Прогнозы на футбольные матчи")

    # Кнопка для получения матчей
    if st.button("Получить прогнозы на ближайшие 24 часа"):
        st.write("Загружаю прогнозы...")
        
        # Получаем матчи
        matches = get_upcoming_matches()
        
        if not matches:
            st.write("Нет матчей, которые бы проходили в течение 24 часов.")
        else:
            # Отображаем прогнозы
            display_predictions(matches)

if __name__ == "__main__":
    main()
