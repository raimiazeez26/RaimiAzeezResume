
import plotly.express as px
import pandas as pd

def covid_map():
    #covid data
    data_cov = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')

    da = data_cov.T
    da.columns = da.loc["Country/Region"].values
    da = da.drop(["Province/State", "Lat",  "Long", "Country/Region"], axis = 0)

    data = da.copy()
    data.drop(["China", "Canada", "United Kingdom", "Australia", "Denmark", "France", "Netherlands", "New Zealand"], 
              axis =1, inplace = True)


    data["China"] = da["China"].sum(axis = 1)
    data["Canada"] = da["Canada"].sum(axis = 1)
    data["United Kingdon"] = da["United Kingdom"].sum(axis = 1)
    data["Australia"] = da["Australia"].sum(axis = 1)
    data["Denmark"] = da["Denmark"].sum(axis = 1)
    data["France"] = da["France"].sum(axis = 1)
    data["Netherlands"] = da["Netherlands"].sum(axis = 1)
    data["New Zealand"] = da["New Zealand"].sum(axis = 1)


    data = data.reset_index()
    data = data.rename(columns = {"index" : "date"})

    data = data.melt(id_vars='date', var_name='country', value_name='cases')
    data

    cas = []
    for i in data["cases"]:
        i = int(i)
        cas.append(i)

    data["cases"] = cas
    data['date'] = pd.to_datetime(data['date'])
    data['Date'] = data['date'].apply(lambda x: x.strftime('%m-%Y')) 

    #plot map
    fig = px.scatter_geo(data, locationmode= 'country names', locations="country",# color="country",
                         hover_name="country", size="cases", size_max= 40, color_discrete_sequence=['red'],
                         animation_frame="Date",
                         projection='equirectangular')

    fig.update_traces(marker_color=['red'], selector=dict(type='scattergeo')),
    fig.update_layout(title_text="Time lapse of COVID-19 confirmed cases from Jan 2020 till date", title_x=0.5)

    return fig 
