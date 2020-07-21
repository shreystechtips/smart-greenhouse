import plotly.graph_objects as go
from plotly.subplots import make_subplots
# import numpy as np
import json 
from datetime import datetime
from datetime import timedelta
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import const
cred = credentials.Certificate('greenhouse.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://greenhouse-85aa5.firebaseio.com'
})

fig = make_subplots(specs=[[{"secondary_y": True}]])

def plot(input,outfile):
    total = [[],{'co2':[],'humid':[],'tvoc':[],'temp':[]}]
    archive = extract_archive(input)
    archive.update(input["sensordata"])
    # input["sensordata"].update(
    for k,v in archive.items():
        if isinstance(v,dict) :   
            # and v["temp"] >= 33.7
            total[0].append(datetime.strptime(k,const.TIME_FMT)-timedelta(hours=7))
            total[1]["co2"].append(v["co2"])
            total[1]["temp"].append(v["temp"])
            total[1]["humid"].append(v["humid"])
            total[1]["tvoc"].append(v["tvoc"])
    for k,v in total[1].items():
        fig.add_trace((go.Scatter(x=total[0], y=v, name=k)), secondary_y = (k=='co2' or k == 'tvoc'))
    # fig.write_html(outfile)
    fig.show()
def extract_archive(data):
    data = data['archive']
    out = {}
    for date in data:
        out[date] = {}
        for t in data[date]:
            out[date][t] = data[date][t]['value']
        for t in const.FALLBACK_VALUES:
            if not t in out[date]:
                out[date][t] = const.FALLBACK_VALUES[t]
    return out

def get_data(main_last=None,outfile=datetime.now()):
    data= {}
    if main_last != None:
        data = {'sensordata':db.reference('sensordata').order_by_key().limit_to_last(main_last).get(),'archive':db.reference('archive').get()} 
    else:
        data = db.reference('/').get()
    open(f'{outfile.strftime(const.TIME_FMT)}.json','w').write(json.dumps(data))
    return data

# plot(get_data(main_last=5000),'plot.html')
plot(json.loads(open('last.json','r').read()),'plot.html')