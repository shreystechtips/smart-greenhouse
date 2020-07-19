import plotly.graph_objects as go
from plotly.subplots import make_subplots
# import numpy as np
import json 
from datetime import datetime


fig = make_subplots(specs=[[{"secondary_y": True}]])

def plot(input,outfile):
    total = [[],{'co2':[],'humid':[],'tvoc':[],'temp':[]}]
    for k,v in input["sensordata"].items():
        if isinstance(v,dict) :   
            # and v["temp"] >= 33.7
            total[0].append(datetime.strptime(k,"%Y-%m-%dT%H:%M:%S"))
            total[1]["co2"].append(v["co2"])
            total[1]["temp"].append(v["temp"])
            total[1]["humid"].append(v["humid"])
            total[1]["tvoc"].append(v["tvoc"])
    for k,v in total[1].items():
        fig.add_trace((go.Scatter(x=total[0], y=v, name=k)), secondary_y = (k=='co2' or k == 'tvoc'))
    fig.write_html(outfile)
    # fig.show()
plot(json.loads(open("greenhouse-85aa5-export.json","r").read()),'plot.html')