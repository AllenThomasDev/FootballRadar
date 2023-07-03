import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def load_data():
    data = pd.DataFrame()
    leagues = ['Bundesliga', 'LaLiga', 'Ligue1', 'PL', 'SerieA']
    for league in leagues:
        df = pd.read_csv('resources/' + league + ".csv")
        df['League'] = league
        data = pd.concat([data, df])
    data = data[data['minutes'] >= 1080]
    return data

metrics = {
    'Penalty area entries': 'carries_into_penalty_area',
    'Final third entries': 'carries_into_final_third',
    'Passes into final third': 'passes_into_final_third',
    'Ball recoveries': 'ball_recoveries',
    'Interceptions made': 'interceptions',
    'Tackles made': 'tackles',
    'Aerial duels won': 'aerials_won',
    'Shots attempted': 'shots_on_target',
    'Touches in opposition box': 'touches_att_pen_area',
    'Assisted Shot': 'assisted_shots'
}

df = load_data()
hav_df = df[df['player'] == 'Kai Havertz']
print(hav_df['minutes'].values[0], type(hav_df['minutes'].values[0]))

def main():
    st.title("Soccer Player Comparison")
    data = load_data()
    all_players = sorted(list(data['player']))
    
    selected_players = st.sidebar.multiselect("Select players", all_players, max_selections=3)
    
    fig = go.Figure()
    
    for player in selected_players:
        player_data = data[data['player'] == player]
        minutes_played = player_data['minutes'].values[0]
        values = [(player_data[metrics[metric]].values[0]*90/minutes_played) for metric in metrics]
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=list(metrics.keys()),
            fill='toself',
            name=player
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True)
        ),
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
