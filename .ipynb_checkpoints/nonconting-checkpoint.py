import numpy as np
import pandas as pd
import pandas as pd
import geopandas as gpd
import geoplot as gplt
import geoplot.crs as gcrs
import matplotlib.pyplot as plt
import mapclassify as mc
import datetime

data_population = pd.read_csv('data/us-population.csv', index_col=['state'])
data_population.head()
print(data_population.loc['Puerto Rico'])

data_cases = pd.read_csv('data/us-states.csv', index_col=['date', 'state'])
data_cases['state'] = data_cases.index.get_level_values('state')
print(data_cases.head())

def get_cases_per_million(row):
    cases, state = row['cases'], row['state']
    #print(cases, state)
    return (cases/data_population.loc[state].population) * 1000000 if state in data_population.index else cases

def get_deaths_per_million(row):
    deaths, state = row['deaths'], row['state']
    #print(deaths, state)
    return (deaths/data_population.loc[state].population) * 1000000 if state in data_population.index else deaths

data_cases['cases_per_million'] = data_cases.apply(lambda row: get_cases_per_million(row), axis=1)
data_cases['deaths_per_million'] = data_cases.apply(lambda row: get_deaths_per_million(row), axis=1)

lo, hi = data_cases['deaths_per_million'].min(), data_cases['deaths_per_million'].max()
print(data_cases.head(), lo, hi)


data_population = pd.read_csv('data/us-population.csv', index_col=['state'])
data_population.head()

data_maps = pd.read_csv('data/us-contiguous-states.csv', index_col=['state'])
data_maps.head()

states = data_maps.index.to_list()
print(states)

data_color = pd.read_csv('data/us-states-color.csv', index_col=['state'])
data_color.head()

data_maps_albers = pd.read_csv('data/albers_composite_us_states_data.csv', index_col=['state'])
data_maps_albers.head()
data_color = pd.read_csv('data/us-states-color.csv', index_col=['state'])
data_color.head()
states = data_maps_albers.index.to_list()
print(states)

data_maps_albers = pd.read_csv('data/albers_composite_us_states_data.csv', index_col=['state'])
data_maps_albers.head()
data_color = pd.read_csv('data/us-states-color.csv', index_col=['state'])
data_color.head()
states = data_maps_albers.index.to_list()
print(states)

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

us_abbrev_state = {v: k for k, v in us_state_abbrev.items()}


data_cases = pd.read_csv('data/us_states_covid19_daily.csv', index_col=['date', 'state'])
#print(data_cases.head(10))
print(data_cases.columns)
data_cases['state2'] = data_cases.index.get_level_values('state')
#print(data_cases.head())

def get_cases_per_million(row):
    cases, state = row['positive'], row['state2']
    state = us_abbrev_state[state]
    #print(cases, state)
    return (cases/data_population.loc[state].population) * 1000000 if state in data_population.index else cases

def get_current_cases_per_million(row):
    cases, state = row['positive'], row['state2']
    state = us_abbrev_state[state]
    cases -= row['recovered']
    #print(cases, state)
    return (cases/data_population.loc[state].population) * 1000000 if state in data_population.index else cases


def get_deaths_per_million(row):
    deaths, state = row['death'], row['state2']
    state = us_abbrev_state[state]
    #print(death, state)
    return (deaths/data_population.loc[state].population) * 1000000 if state in data_population.index else deaths

def get_population(row):
    state = row['state2']
    state = us_abbrev_state[state]
    if state not in data_population.index: return 1
    return data_population.loc[state].population

data_cases['cases_per_million'] = data_cases.apply(lambda row: get_cases_per_million(row), axis=1)
data_cases['deaths_per_million'] = data_cases.apply(lambda row: get_deaths_per_million(row), axis=1)
data_cases['population'] = data_cases.apply(lambda row: get_population(row), axis=1)
data_cases['recovered'] = data_cases['recovered'].fillna(0)
data_cases['current_cases_per_million'] = data_cases.apply(lambda row: get_current_cases_per_million(row), axis=1)

data_cases_cleaned = data_cases[['positive','recovered','death','state2','population','cases_per_million','current_cases_per_million','deaths_per_million']]

lo, hi = data_cases_cleaned['deaths_per_million'].min(), data_cases_cleaned['deaths_per_million'].max()
print(data_cases_cleaned.head(10), lo, hi)

import warnings;

warnings.simplefilter('ignore')
from datetime import date, timedelta
import geopandas as gpd
import geoplot as gplt


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


days = []
start_date = date(2020, 1, 22)
end_date = date(2020, 7, 21)
for date in daterange(start_date, end_date):
    date = int(date.strftime("%Y%m%d"))
    days.append(date)


def get_cases(state):
    state = us_state_abbrev[state]
    return data_cases_cleaned_day.query("state == @state").iloc[0]['cases_per_million']


def get_deaths(state):
    state = us_state_abbrev[state]
    return data_cases_cleaned_day.query("state == @state").iloc[0]['deaths_per_million']


#days = [20200201, 20200301, 20200401, 20200501, 20200601, 20200701]
'''f, axes = plt.subplots(figsize=(20, 10), ncols=3, nrows=2)
world.plot(ax=axes[0][0], column='pop_est', cmap='Blues')
world.plot(ax=axes[0][1], column='gdp_md_est', cmap='Reds')
world.plot(ax=axes[1][0], column='continent')
world.plot(ax=axes[1][1])
scheme = mc.Quantiles(contiguous_usa['population'], k=5)'''

# f, axes = plt.subplots(figsize=(20, 10), ncols=2, nrows=1)
# plt.figure()

########
day = 20200720
contiguous_usa = gpd.read_file(gplt.datasets.get_path('contiguous_usa'))
data_cases_cleaned_day = data_cases_cleaned.loc[(day)].copy()
# print(data_cases_cleaned_day.head(3))
for state in states:
    if (us_state_abbrev[state]) not in data_cases_cleaned_day.index:
        data_cases_cleaned_day.loc[us_state_abbrev[state]] = [0, 0, 0, us_state_abbrev[state], 0, 0, 0, 0]
data_cases_cleaned_day = data_cases_cleaned_day.fillna(0)
# print(data_cases_cleaned_day)
contiguous_usa['cases'] = contiguous_usa['state'].map(get_cases)

contiguous_usa['deaths'] = contiguous_usa['state'].map(get_deaths)

scheme = mc.Quantiles(contiguous_usa['deaths'], k=5)
########
for i, day in enumerate(days):
    contiguous_usa = gpd.read_file(gplt.datasets.get_path('contiguous_usa'))
    data_cases_cleaned_day = data_cases_cleaned.loc[(day)].copy()
    # print(data_cases_cleaned_day.head(3))
    for state in states:
        if (us_state_abbrev[state]) not in data_cases_cleaned_day.index:
            data_cases_cleaned_day.loc[us_state_abbrev[state]] = [0, 0, 0, us_state_abbrev[state], 0, 0, 0, 0]
    data_cases_cleaned_day = data_cases_cleaned_day.fillna(0)
    # print(data_cases_cleaned_day)
    contiguous_usa['cases'] = contiguous_usa['state'].map(get_cases)

    contiguous_usa['deaths'] = contiguous_usa['state'].map(get_deaths)

    #scheme = mc.Quantiles(contiguous_usa['deaths'], k=5)

    m, n = i % 2, i // 2
    try:
        ax = gplt.cartogram(
            contiguous_usa,
            scale='cases',
            projection=gcrs.AlbersEqualArea(central_longitude=-98, central_latitude=39.5),
            hue='deaths', cmap='YlOrRd',
            #norm=colors.Normalize(vmin=0, vmax=18000),
            scheme=scheme,
            linewidth=0.5,
            legend=True, legend_kwargs={'loc': 'lower right'}, legend_var='hue',
            figsize=(16, 20),
            # ax = axes[m][n]
        );
        gplt.polyplot(contiguous_usa, facecolor='lightgray', edgecolor='None', ax=ax);
    except:
        pass

    plt.title("Covid 19 confirmed cases and deaths - " + datetime.datetime.strptime(str(day), '%Y%m%d').strftime('%Y-%m-%d'));
    plt.savefig('data/noncontiguous/' + str(day) + '.png', bbox_inches='tight', pad_inches=0.1);