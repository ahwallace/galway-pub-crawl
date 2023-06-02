import osmnx as ox
import gradio as gr
import pandas as pd
import plotly.express as px
from pub_crawl_script import pub_crawl

df = pd.read_csv('galway_pubs.csv')
G =  ox.io.load_graphml('galway.graphml')

def galway_map():
    fig = px.scatter_mapbox(df, lat='latitude', lon='longitude', hover_name='name', 
                                  # hover_data=f"Address: {str(df['address'])}", 
                                  color_discrete_sequence=["fuchsia"], 
                                  zoom=14, height=300, opacity=0.8, size=[1]*len(df), size_max=12)
    fig.update_layout(mapbox_style='open-street-map',
                      margin={"r": 0, "t": 0, "l": 0, "b": 0},
                      mapbox_bounds={"west": -9.0644, "east": -9.0456, "south": 53.2691, "north": 53.2763})
    return fig

def execute_crawl_optimiser(start_pub, pubs_considered):
    crawler = pub_crawl(df, G)
    crawler.optimise(start_pub, pubs_considered)
    route_str = ''
    for i in range(len(crawler.optimal_route)-1):
        route_str += f'{crawler.optimal_route[i]} --> '
    route_str += crawler.optimal_route[-1]
    return crawler.optimal_distance, route_str, crawler.plot_route(crawler.optimal_route)

with gr.Blocks() as pub_crawl_ui:
    with gr.Row():
        with gr.Column():
            map = gr.Plot(galway_map, label='Galway Map')
        with gr.Column():
            start_pub = gr.Dropdown(df['name'].to_list(), value='Caribou', label="Start Pub")
            pubs_considered = gr.CheckboxGroup(df['name'].to_list(), label='Pubs to Visit', 
            info='Please make sure "Start Pub" is selected')
    with gr.Row():
        run_btn = gr.Button("Run")
    with gr.Row():
        with gr.Column(scale=1):
            distance = gr.Number(value=None, label="Route Distance (meters)")
        with gr.Column(scale=3):
            route = gr.Textbox(label="Route")
    with gr.Row():
        route_plot = gr.Plot(label="Route Map", height=1200)
    
    run_btn.click(fn=execute_crawl_optimiser, inputs=[start_pub, pubs_considered], outputs=[distance, route, route_plot], api_name="pub_crawl")

pub_crawl_ui.launch()