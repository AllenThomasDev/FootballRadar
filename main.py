import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import textwrap
import pandas as pd
import seaborn as sns

from complex_radar import ComplexRadar

colors = ["#f72585ff", "#7209b7ff", "#3a0ca3ff",
          "#4361eeff", "#4cc9f0ff", "#c77dff"]


def load_data():
    data = pd.DataFrame()
    leagues = ['Bundesliga', 'LaLiga', 'Ligue1', 'PL', 'SerieA']
    for league in leagues:
        df = pd.read_csv('resources/' + league + ".csv")
        df['League'] = league
        data = pd.concat([data, df])
    data = data[data['minutes'] >= 1080]
    return data

def get_ranges(df, metrics):
    metric_ranges = []
    data = df
    for metric, column_name in metrics.items():
        # Calculate the per 90 minutes value
        data['normalized_value'] = data[column_name] * 90 / data['minutes']
        max_row = data[data['normalized_value'] == data['normalized_value'].max()]
        metric_ranges.append((0,round(max_row['normalized_value'].values[0], 2)))
    return metric_ranges

template_metrics = {
    "Midfielders": {"metrics":{
                    'Penalty area entries': 'carries_into_penalty_area',
                    'Final third entries': 'carries_into_final_third',
                    'Passes into final third': 'passes_into_final_third',
                    'Ball recoveries': 'ball_recoveries',
                    'Interceptions made': 'interceptions',
                    'Tackles made': 'tackles',
                    'Aerial duels won': 'aerials_won',
                    'Shots attempted': 'shots_on_target',
                    'Touches in opposition box': 'touches_att_pen_area',
                    'Assisted Shot': 'assisted_shots'}},
    "Forwards": {"metrics":{
                    'Goals': 'goals',
                    'Shots On Target': 'shots_on_target',
                    'Touches in the Box': 'touches_att_pen_area',
                    'Aerials Won': 'aerials_won',
                    "Interceptions" : "interceptions",
                    "Touches" : "touches",
                    "Assists" : "assists",
                    'Chances Created': 'assisted_shots'}}, 
    "Defenders": {"metrics":{
                    'Penalty area entries': 'carries_into_penalty_area',
                    'Final third entries': 'carries_into_final_third',
                    'Passes into final third': 'passes_into_final_third',
                    'Ball recoveries': 'ball_recoveries',
                    'Interceptions made': 'interceptions',
                    'Tackles made': 'tackles',
                    'Aerial duels won': 'aerials_won',
                    'Shots attempted': 'shots_on_target',
                    'Touches in opposition box': 'touches_att_pen_area',
                    'Assisted Shot': 'assisted_shots'}}}


df = load_data()
mf_df = df[df['position'].isin(['MF','DF,MF','MF,FW','FW,MF','MF,DF'])]
fw_df = df[df['position'].isin(['FW,MF','MF,FW','FW'])]
def_df = df[df['position'].isin(['DF','DF,MF','DF,FW','FW,DF','MF,DF'])]

mf_ranges=get_ranges(mf_df,template_metrics['Midfielders']['metrics'])
fw_ranges=get_ranges(fw_df,template_metrics['Forwards']['metrics'])
def_ranges=get_ranges(def_df,template_metrics['Defenders']['metrics'])

template_metrics['Midfielders']['ranges']=mf_ranges
template_metrics['Midfielders']['data']=mf_df
template_metrics['Forwards']['ranges']=fw_ranges
template_metrics['Forwards']['data']=fw_df
template_metrics['Defenders']['ranges']=def_ranges
template_metrics['Defenders']['data']=def_df
template_metrics['Midfielders']['default']=["Martin Ødegaard" , "Kai Havertz" ,"Declan Rice"]
template_metrics['Forwards']['default']=["Kylian Mbappé" , "Erling Haaland" ,"Lionel Messi"]
template_metrics['Defenders']['default']=["Virgil van Dijk","Kim Min-jae","John Stones"]

format_cfg = {
    'rad_ln_args': {'visible': True, 'color': 'grey', 'linestyle': '--', 'zorder': 1},
    'outer_ring': {'visible': False},
    'angle_ln_args': {'visible': False},
    'rgrid_tick_lbls_args': {'fontsize': 12, 'color': 'white', 'va': 'center', 'ha': 'center', 'zorder': 10},
    'theta_tick_lbls': {'fontsize': 15},
    'theta_tick_lbls_pad': 25,
    'theta_tick_color': 'grey',
    'axes_args': {'facecolor': 'black'},
    'incl_endpoint': True
}

def main():
    sns.set_style("dark")
    selected_template = st.sidebar.selectbox(
        "Select template", ['Midfielders', 'Forwards', 'Defenders'])
    all_players = sorted(list(template_metrics[selected_template]['data']['player']))
    selected_players = st.sidebar.multiselect("Select players", all_players,default=template_metrics[selected_template]['default'], max_selections=6)
    metrics = template_metrics[selected_template]['metrics']
    ranges = template_metrics[selected_template]['ranges']
    data=template_metrics[selected_template]['data']
    fig = plt.figure(figsize=(8, 8))
    fig.patch.set_facecolor('black')
    radar = ComplexRadar(fig, list(metrics.keys()), n_ring_levels=5,
                         ranges=ranges, show_scales=True, format_cfg=format_cfg)

    for idx, player in enumerate(selected_players):
        player_data = data[data['player'] == player]
        minutes_played = player_data['minutes'].values[0]
        values = [round((player_data[metrics[metric]].values[0]
                        * 90/minutes_played), 2) for metric in metrics.keys()]
        print(player)
        radar.plot(values, color=colors[idx],
                   alpha=0.3, marker='o', markersize=4)
        radar.fill(values, color=colors[idx], label=player, alpha=0.5)

    radar.use_legend(loc='upper left', bbox_to_anchor=(1.1, 1))
    st.title(selected_template + " Comparison 2022/23")
    st.pyplot(fig)


if __name__ == "__main__":
    main()
