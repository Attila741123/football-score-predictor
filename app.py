import streamlit as st
import requests

# Функция для получения предстоящих матчей
def get_upcoming_matches():
    url = "https://sofascore.p.rapidapi.com/matches/live"
    headers = {
        "x-rapidapi-key": "a46d78e235mshf84713c91f6721ap1e0f8fjsn0b4e2a83c8b7",
        "x-rapidapi-host": "sofascore.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    return response.json()

# Функция для получения состава команды
def get_lineups(match_id):
    url = "https://sofascore.p.rapidapi.com/matches/get-lineups"
    headers = {
        "x-rapidapi-key": "a46d78e235mshf84713c91f6721ap1e0f8fjsn0b4e2a83c8b7",
        "x-rapidapi-host": "sofascore.p.rapidapi.com"
    }
    querystring = {"matchId": match_id}
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

# Функция для отображения матчей и их составов
def display_matches():
    matches = get_upcoming_matches()
    
    if "events" in matches:
        for match in matches['events']:
            home_team = match['homeTeam']['name']
            away_team = match['awayTeam']['name']
            match_id = match['id']
            start_time = match['startDate']
            
            # Получаем составы команд для каждого матча
            lineups = get_lineups(match_id)
            home_lineup = lineups.get('home', {}).get('players', [])
            away_lineup = lineups.get('away', {}).get('players', [])
            
            # Показ информации
            st.write(f"{home_team} vs {away_team} - {start_time}")
            st.write(f"Составы команд:")
            st.write(f"  {home_team} - {[player['name'] for player in home_lineup]}")
            st.write(f"  {away_team} - {[player['name'] for player in away_lineup]}")
            st.write("---")
    else:
        st.write("Нет предстоящих матчей.")

# Настройка Streamlit
st.title('Предстоящие футбольные матчи')
display_matches()
