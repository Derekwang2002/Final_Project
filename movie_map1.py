import pandas as pd 
import json
import plotly.express as px
from collections import Counter
import streamlit as st

# input dataframe, return dataframe, show map on st.
def movie_map(data:pd.DataFrame,color_st:str):
    country_codes_file = open('country_code.json')
    country_codes = json.load(country_codes_file)
    country_codes_file.close()
    shows_countries = ", ".join(data['country'].dropna()).split(", ")
    country_number = {}
    
    for c,v in dict(Counter(shows_countries)).items():
        code = ""
        if c.lower() in country_codes:
            code = country_codes[c.lower()]
            if code not in country_number.keys():
                country_number[code] = v
            else:country_number[code] = country_number[code]+v
    #turn to pandas
    dic_pandas = {}
    dic_pandas['ISO3'] = []
    dic_pandas['number'] = []
    for key,value in country_number.items():
        dic_pandas['ISO3'].append(key)
        dic_pandas['number'].append(value)
    df = pd.DataFrame.from_dict(dic_pandas)
    df['ISO3'] = df['ISO3'].astype('str')
    dic_pandas['number'] = df['number'].astype('float')
    world_json_file = open('geo.geojson')
    world_geojson_data = json.load(world_json_file)
    world_json_file.close()
  
    fig = px.choropleth_mapbox(df, geojson=world_geojson_data, color="number",
                            locations="ISO3", featureidkey="properties.ISO_A3",
                            center={"lat": 45.5517, "lon": -73.7073},
                            mapbox_style="carto-positron", zoom=4,color_continuous_scale=color_st)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)

    return df # return df - (index: code of country; variable: counts)