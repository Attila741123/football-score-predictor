import streamlit as st
import requests
import pandas as pd
import random  # Модуль для имитации предсказания счета

# Функция для получения данных о предстоящих матчах
def get_upcoming_matches():
    url = "https://api.bet365.com/v1/football/matches"  # Пример API (необходимо использовать правильный API endpoint)
    headers = {
        "Authorization": "Bearer YOUR_API_TOKEN"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()  # Возвращаем список матчей
    else:
        return []

# Прогнозирование точного счёта (используем случайный результат для примера)
def predict_score():
    return f"{random.randint(0, 4)}:{random.randint(0, 4)}"  # Имитация прогнозируемого счёта

# Функция для отображения матчей в Streamlit
def display_matches():
    matches = get_upcoming_matches()
    
    if matches:
        match_data = []
        for match in matches:
            event_name = match['eventName']
            team1 = match['team1']
            team2 = match['team2']
            start_time = match['startTime']
            score_prediction = predict_score()  # Генерация прогноза
            match_data.append([event_name, team1, team2, start_time, score_prediction])
        
        # Создаём таблицу
        df = pd.DataFrame(match_data, columns=["Match", "Home Team", "Away Team", "Start Time", "Predicted Score"])
        
        # Отображаем таблицу в Streamlit
        st.write("### Upcoming Football Matches with Predictions")
        st.dataframe(df)
    else:
        st.write("No upcoming matches found.")

# Основная часть приложения Streamlit
if __name__ == "__main__":
    st.title("Football Score Prediction System")
    display_matches()
