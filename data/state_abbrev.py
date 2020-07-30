state_abbrev = us_state_abbrev[state]
import os

from datetime import timedelta, date
from PIL import ImageColor
from PIL import Image

import math
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm
#from colorspacious import cspace_converter
from collections import OrderedDict

cmaps = OrderedDict()
cmaps['Sequential'] = [
            'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
            'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
            'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


lo, hi = data_cases_cleaned['deaths_per_million'].min(), data_cases['deaths_per_million'].max()
print(lo, hi)

def getColor(x, lo=lo, hi=hi):
    x = (x - lo) / (hi - lo)
    rgb = cm.get_cmap(cmaps['Sequential'][2])([x])[np.newaxis, :, :3]
    return rgb[0][0]

start_date = date(2020, 3, 1)
end_date = date(2020, 3, 11)
for date in daterange(start_date, end_date):
    date = int(date.strftime("%Y%m%d"))
    #if date not in [20200401, 20200501, 20200601, 20200701]: continue
    print(date)
    #print(data_cases_cleaned.loc[date])
    fname = 'data/csvs_albers/' + str(date) + '.csv'
    cases, base_cases = 0, 0.009
    for state in states:
        state_abbrev = us_state_abbrev[state]
        if (date, state_abbrev) in data_cases_cleaned.index:
            base_cases = min(base_cases, data_cases_cleaned.loc[(date, state_abbrev)].current_cases_per_million)
    base_cases /= 100.0
    print(base_cases)
    fd = open(fname, 'w')
    for state in states:
        state_abbrev = us_state_abbrev[state]
        line = []
        line.append(int(data_maps_albers.loc[state].id))
        #cases = 1
        cases = base_cases
        deaths = 0
        #print(state, state_abbrev)
        if (date, state_abbrev) in data_cases_cleaned.index:
            #print(data_cases_cleaned.loc[(date, state_abbrev)])
            cases += data_cases_cleaned.loc[(date, state_abbrev)].current_cases_per_million
            deaths += data_cases_cleaned.loc[(date, state_abbrev)].deaths_per_million
            #print(data_cases_cleaned.loc[(date, state_abbrev)].current_cases_per_million, data_cases_cleaned.loc[(date, state_abbrev)].recovered, data_cases_cleaned.loc[(date, state_abbrev)].deaths_per_million)
        else:
            pass
            #print("Not there, ", date, state_abbrev)
        #print(cases)
        line.append(cases)
        line.append(state)
        
        if cases == base_cases:
            line.extend([0.5, 0.5, 0.5])
        else:
            line.extend(getColor(deaths))
        #print(line)
        fd.write(','.join(map(str, line))+'\n')
    fd.close()
    os.system('cartogram -eg data/albers_composite_us_states_processedmap.json -a ' + fname)
    

    bounds = (1024, 1024)

    # Needs ghostscript installed for this to run
    pic = Image.open('cartogram.eps')
    pic.load(scale=10)

    if pic.mode in ('P', '1'):
        pic = pic.convert("RGB")

    ratio = min(bounds[0] / pic.size[0],
                bounds[1] / pic.size[1])
    new_size = (int(pic.size[0] * ratio), int(pic.size[1] * ratio))
    pic = pic.resize(new_size, Image.ANTIALIAS)

    # Save to PNG
    pic.save(fname.split('.')[0] + '.png')
    #https://stackoverflow.com/questions/45828514/how-to-convert-an-eps-file-into-a-png-in-python-3-6
            