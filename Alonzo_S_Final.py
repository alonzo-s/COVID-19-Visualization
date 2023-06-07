import pandas as pd
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, NumeralTickFormatter
from bokeh.models import DatetimeTickFormatter, CDSView, GroupFilter
from bokeh.layouts import column
from bokeh.models import HoverTool


#read CSV file
dataPoints = pd.read_csv('dataset.csv', parse_dates = ['date'])
dataPoints['date'] = pd.to_datetime(dataPoints['date'])

#add tools 
TOOLS = "box_select,hover,reset,help"


#retrieve data from CSV file
dataPts = (dataPoints[(dataPoints['location'] == 'Texas') |
                    (dataPoints['location'] == 'New York')]
           .loc[:, ['date', 'location', 'death_per_10Kpeople',
                    'people_fully_vaccinated_per_hundred']]
           .sort_values(['location','date']))

#create column data source
stateComparison = ColumnDataSource(dataPts)

#create figure
fullyVacc = figure(title = 'Fully Vaccinated per 100 People', plot_width = 1000, plot_height = 500, tools=TOOLS)
deathToll = figure(title = 'Death Toll per 10,000 People', plot_width = 1000, plot_height = 500, tools=TOOLS)

#create views
texas_view = CDSView(source = stateComparison,
                     filters = [GroupFilter(column_name = 'location', group = 'Texas')])
newyork_view = CDSView(source = stateComparison,
                     filters = [GroupFilter(column_name = 'location', group = 'New York')])

#comparison between people_fully_vaccinated_per_hundred
fullyVacc.circle('date', 'people_fully_vaccinated_per_hundred', source=stateComparison, view = texas_view,
                 color = 'red', legend_label = 'Texas')
fullyVacc.circle('date', 'people_fully_vaccinated_per_hundred', source=stateComparison, view = newyork_view,
                color = 'blue', legend_label = 'New York')


#comparison between death toll per 10k ppl
deathToll.circle('date', 'death_per_10Kpeople', source=stateComparison, view = texas_view,
                 color = 'red', legend_label = 'Texas')
deathToll.circle('date', 'death_per_10Kpeople', source=stateComparison, view = newyork_view,
                color = 'blue', legend_label = 'New York')


#format x-axis and y-axis
fullyVacc.xaxis.formatter = DatetimeTickFormatter(months=["%m / %Y"])
fullyVacc.yaxis.formatter = NumeralTickFormatter(format="0,0")
fullyVacc.xaxis.axis_label = 'Time'
fullyVacc.yaxis.axis_label = 'Fully Vaccinated per 100 People'
fullyVacc.legend.location = 'top_left'
fullyVacc.legend.title = 'Legend'
deathToll.xaxis.formatter = DatetimeTickFormatter(months=["%m / %Y"])
deathToll.yaxis.formatter = NumeralTickFormatter(format="0,0")
deathToll.xaxis.axis_label = 'Time'
deathToll.yaxis.axis_label = 'Death Toll per 10,000 People'
deathToll.legend.location = 'top_left'
deathToll.legend.title = 'Legend'

#Hover tool display values and date at desired point
hover = fullyVacc.select(dict(type=HoverTool))
hover.tooltips = [
        ("Date", '@date{%F}'),
        ("Value", '@people_fully_vaccinated_per_hundred'),
        ]
hover.mode = 'mouse'
hover.formatters = ({'@date': 'datetime'})


hover = deathToll.select(dict(type=HoverTool))
hover.tooltips = [
        ("Date", '@date{%F}'),
        ("Value", '@death_per_10Kpeople'),
        ]
hover.mode = 'mouse'
hover.formatters = ({'@date': 'datetime'})


#display charts
show(column(fullyVacc,deathToll))                       
                    