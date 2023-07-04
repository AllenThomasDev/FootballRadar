import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import textwrap
import pandas as pd
import seaborn as sns

from complex_radar import ComplexRadar


def load_data():
    data = pd.DataFrame()
    leagues = ['Bundesliga', 'LaLiga', 'Ligue1', 'PL', 'SerieA']
    for league in leagues:
        df = pd.read_csv('resources/' + league + ".csv")
        df['League'] = league
        data = pd.concat([data, df])
    data = data[data['minutes'] >= 1080]
    data = data[data['position'].isin(['MF', 'MF,FW', 'MF,DF', 'DF,MF', 'FW,MF'])]
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
format_cfg = {
    'rad_ln_args': {'visible':True, 'color': 'grey', 'linestyle':'--'},
    'outer_ring': {'visible':True},
    'angle_ln_args' : {'visible':False},
    'rgrid_tick_lbls_args': {'fontsize':12, 'color': 'white', 'va':'bottom', 'ha':'left'},
    'theta_tick_lbls': {'fontsize':15},
    'theta_tick_lbls_pad':25,
    'theta_tick_color' : 'grey',
    'axes_args' : {'facecolor':'black'},
    'incl_endpoint' : True
}

ranges = [(0, 3.28), (0, 4.88), (0, 15.54), (0, 9.69), (0, 2.22), (0, 4.26), (0, 4.04), (0, 1.3), (0, 6.78), (0, 3.57)]

def main():
    sns.set_style("dark")
    st.title("Midfielders Comparison 2022/23")
    data = load_data()
    all_players = sorted(list(data['player']))
    
    selected_players = st.sidebar.multiselect("Select players", all_players, default = ["Martin Ødegaard","Casemiro","Declan Rice"],max_selections=5)
    
    fig = plt.figure(figsize=(8, 8))
    fig.patch.set_facecolor('black')
    radar = ComplexRadar(fig, list(metrics.keys()), n_ring_levels=5 ,ranges=ranges, show_scales=True, format_cfg=format_cfg)
    
    for player in selected_players:
        player_data = data[data['player'] == player]
        minutes_played = player_data['minutes'].values[0]
        values = [round((player_data[metrics[metric]].values[0]*90/minutes_played),2) for metric in metrics.keys()]
        print(player)
        radar.plot(values, label=player, marker='o')
        radar.fill(values, alpha=0.5)
    
    radar.use_legend(loc='upper left', bbox_to_anchor=(1.1, 1))    
    st.pyplot(fig)

if __name__ == "__main__":
    main()
