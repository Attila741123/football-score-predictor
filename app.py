import streamlit as st
import requests
from datetime import datetime, timedelta

# Ваш API токен
API_TOKEN = "f2285e27e24948fca025d71981350602"
HEADERS = {"X-Auth-Token": API_TOKEN}

# Доступные турниры
COMPETITIONS = ["PL", "CL", "BL1", "FL1", "SA", "PD", "DED", "BSA", "EL1"]

# Получение матчей в течение 24 часов по всем турнирам
def get_upcoming_matches():
    date_from = datetime.utcnow().date().isoformat()
    date_to = (datetime.utcnow() + timedelta(days=1)).date().isoformat()
    matches = []

    for comp in COMPETITIONS:
        url = f"https://api.football-data.org/v4/competitions/{comp}/matches?dateFrom={date_from}&dateTo={date_to}"
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            matches.extend(data.get("matches", []))
        else:
            st.warning(f"Ошибка получения данных по {comp}: {response.status_code}")

    return matches

# Простая заглушка для модели прогноза
def predict_score(home_team, away_team):
    import random
    return f"{random.randint(0, 3)} : {random.randint(0, 3)}"

# Интерфейс
st.title("⚽ Прогнозы на точный счёт")

if st.button("🔄 Получить матчи на 24 часа"):
    upcoming_matches = get_upcoming_matches()

    if upcoming_matches:
        for match in upcoming_matches:
            utc_date = datetime.fromisoformat(match["utcDate"].replace("Z", "+00:00"))
            home = match["homeTeam"]["name"]
            away = match["awayTeam"]["name"]
            match_time = utc_date.strftime("%d.%m %H:%M")
            with st.expander(f"{home} vs {away} ({match_time})"):
                if st.button(f"Показать прогноз: {home} vs {away}", key=match["id"]):
                    score = predict_score(home, away)
                    st.success(f"Прогноз: {home} {score} {away}")
    else:
        st.info("Нет матчей в ближайшие 24 часа.")
