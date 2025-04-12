import streamlit as st
import requests
from datetime import datetime, timedelta

API_TOKEN = "f2285e27e24948fca025d71981350602"
HEADERS = {'X-Auth-Token': API_TOKEN}
BASE_URL = "https://api.football-data.org/v4"

def get_todays_matches():
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    url = f"{BASE_URL}/matches?dateFrom={today}&dateTo={tomorrow}"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    return data.get('matches', [])

def predict_score(home_team, away_team):
    # Простая заглушка — можно заменить на ML модель
    return f"{home_team} 2 : 1 {away_team}"

st.title("⚽ Автоматический прогноз матчей на 24 часа")

if st.button("📅 Показать матчи и предсказать счёт"):
    matches = get_todays_matches()
    if not matches:
        st.warning("Нет матчей в течение 24 часов.")
    else:
        for match in matches:
            home = match['homeTeam']['name']
            away = match['awayTeam']['name']
            prediction = predict_score(home, away)
            st.write(f"**{home} vs {away}** — Предсказание: `{prediction}`")
