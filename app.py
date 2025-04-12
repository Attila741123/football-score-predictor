import streamlit as st
import http.client
import json

# Настройка соединения с API
def get_upcoming_matches():
    conn = http.client.HTTPSConnection("sofascore.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': "a46d78e235mshf84713c91f6721ap1e0f8fjsn0b4e2a83c8b7",
        'x-rapidapi-host': "sofascore.p.rapidapi.com"
    }

    conn.request("GET", "/events/live?category=football", headers=headers)
    res = conn.getresponse()
    data = res.read()

    # Преобразуем данные в формат JSON
    return json.loads(data.decode("utf-8"))

# Функция отображения матчей
def display_matches():
    matches = get_upcoming_matches()
    
    if matches:
        for match in matches['events']:
            home_team = match.get('homeTeam', {}).get('name', 'Unknown')
            away_team = match.get('awayTeam', {}).get('name', 'Unknown')
            start_time = match.get('startTime', 'Unknown')
            match_name = f"{home_team} vs {away_team}"
            st.write(f"Матч: {match_name} | Начало: {start_time}")
            st.write(f"Ссылка: [Перейти на SofaScore](https://www.sofascore.com/)")  # Динамическая ссылка на матч
            st.write("------")
    else:
        st.write("Нет предстоящих матчей")

# Настройка Streamlit
st.title('Предстоящие футбольные события')
display_matches()
