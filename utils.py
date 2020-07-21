# %%
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime
from datetime import timedelta
import random
import const
import numpy as np
cred = credentials.Certificate('greenhouse.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://greenhouse-85aa5.firebaseio.com'
})

# %%
def migrate_data_date(date):
    adjusted_date = date  + timedelta(hours =0)
    start_date = adjusted_date.strftime("%Y-%m-%d")
    end_date = (adjusted_date + timedelta(hours = 0)).strftime("%Y-%m-%d")
    # datetime.strptime(k,"%Y-%m-%dT%H:%M:%S")
    val = db.reference('sensordata').order_by_key().start_at(start_date).end_at(end_date+"\uf8ff")
    val = val.get()
    #%%
    bins = {}
    for i in range(24):
        bins[i] = {}
    for t in val:
        orig = t
        t = datetime.strptime(t,const.TIME_FMT)
        ix = (t.hour)%24     # "normalize" the hour
        bins[ix][t] = val[orig]
    avged = {}
    for b in bins:
        binval = bins[b].values()
        base = const.DT_TYPE
        total = [[] for i in base]
        for value in binval:
            for i,dtype in enumerate(base):
                total[i].append(value[dtype])
        for i,dtype in enumerate(total):
            if any(dtype):
                d = random.choice(list(bins[b].keys())).replace(minute = 30,second=0).strftime(const.TIME_FMT)
                if not d in avged:
                    avged[d] = {}
                avged[d][base[i]] = {'value':float(np.average(dtype)),'stdev':float(np.std(dtype)),'min':float(np.min(dtype)),'max':float(np.max(dtype))}
    db.reference('archive').update(avged)
    for key in val.keys():
        db.reference(f'sensordata/{key}').delete()

# %%
# migrate_data_date(datetime(2020,7,19))
