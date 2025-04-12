import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import poisson

@st.cache_data
def load_data():
    return pd.read_csv("teams_stats.csv")

def predict_score_prob(home_team, away_team, stats, max_goals=5, home_bonus=0.3):
    home_avg_score = stats[home_team]['avg_scored']
    home_avg_concede = stats[home_team]['avg_conceded']
    away_avg_score = stats[away_team]['avg_scored']
    away_avg_concede = stats[away_team]['avg_conceded']

    home_expected = (home_avg_score + away_avg_concede) / 2 + home_bonus
    away_expected = (away_avg_score + home_avg_concede) / 2

    matrix = np.zeros((max_goals + 1, max_goals + 1))
    for i in range(max_goals + 1):
        for j in range(max_goals + 1):
            matrix[i][j] = poisson.pmf(i, home_expected) * poisson.pmf(j, away_expected)
    return matrix, home_expected, away_expected

def main():
    st.title("⚽ Прогноз точного счёта матча")

    df = load_data()
    teams = df['team'].tolist()

    home_team = st.selectbox("Команда-хозяин", teams, index=0)
    away_team = st.selectbox("Команда-гость", teams, index=1)

    stats = {
        row['team']: {
            'avg_scored': row['avg_scored'],
            'avg_conceded': row['avg_conceded']
        }
        for _, row in df.iterrows()
    }

    if st.button("Спрогнозировать"):
        matrix, home_xg, away_xg = predict_score_prob(home_team, away_team, stats)
        score = np.unravel_index(np.argmax(matrix), matrix.shape)
        prob = matrix[score]

        st.markdown(f"### 🔮 Прогноз: **{home_team} {score[0]} : {score[1]} {away_team}**")
        st.markdown(f"📊 Ожидаемые голы: {home_team} — {home_xg:.2f}, {away_team} — {away_xg:.2f}")
        st.markdown(f"📈 Вероятность этого счёта: **{prob:.2%}**")

        st.subheader("🧮 Матрица вероятностей (0–5 голов)")
        df_matrix = pd.DataFrame(
            matrix,
            columns=[f'{away_team} {i}' for i in range(matrix.shape[1])],
            index=[f'{home_team} {i}' for i in range(matrix.shape[0])]
        )
        st.dataframe(df_matrix.style.background_gradient(cmap='Blues').format("{:.2%}"))

if __name__ == "__main__":
    main()
