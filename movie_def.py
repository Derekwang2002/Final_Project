import pandas as pd 
import json
import plotly.express as px
from collections import Counter
import streamlit as st
import plotly.figure_factory as ff
from scipy import stats
import plotly.graph_objects as go


def movie_map(data:pd.DataFrame, color1):
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
    #轉化爲pandas
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
                            mapbox_style="carto-positron", zoom=4,color_continuous_scale=color1)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()
    st.plotly_chart(fig)
    return df #返回國家和對應的數量，可以進一步繪圖

def movie_duration(data:pd.DataFrame, color_str:str):
    movie_time_data = data[(data['duration']!= "") & (data['type']=='Movie')]
    data2 = pd.DataFrame(movie_time_data['duration'].dropna().apply(lambda x:float(x.split(' min')[0])))
    data2['zscore'] = stats.zscore(data2.duration)
    data2_drop = data2[(-3<data2['zscore']) & (data2['zscore']<4)]
    data2_out = data2[(data2['zscore']<-3)|(4<data2['zscore'])]
    x1 = data2_drop['duration']
    fig = ff.create_distplot([x1], ['times'], bin_size=0.7, curve_type='kde', colors=[color_str])#別忘了換顏色
    fig.update_layout(title_text='Movie time with KDE Distribution')
    st.plotly_chart(fig)

def show_number(data:pd.DataFrame, color_str:str):
    col = 'season_count'
    tv_data = data[(data['duration'] != "") & (data['type']=='TV Show')]
    data2 = pd.DataFrame(tv_data['duration'].fillna('0').apply(lambda x:float(x.split(' Season')[0])))
    vc1 = data2.duration.value_counts().reset_index()
    vc1 = vc1.rename(columns = {'duration':'number',"index" : col})
    trace1 = go.Bar(x=vc1[col].astype(int), y=vc1["number"], name="TV Shows", marker=dict(color=color_str))
    data = [trace1]
    layout = go.Layout(title="Seasons", legend=dict(x=0.1, y=1.1, orientation="h"))
    fig = go.Figure(data, layout=layout)
    st.plotly_chart(fig)