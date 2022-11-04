import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import pandas as pd
from PIL import Image
from wordcloud import WordCloud

import json
import plotly.express as px
from collections import Counter
import plotly.figure_factory as ff
from scipy import stats
import plotly.graph_objects as go

class color_set:

    def __init__(
        self, 
        color_basic:str, color_dount:str, color_cloud:list, 
        color_heatmap:str, color_map:str, color_duration:str, img_path:str
    ):
        self.color_basic = color_basic
        self.color_dount = color_dount
        self.color_cloud = color_cloud
        self.color_heatmap = color_heatmap
        self.color_map = color_map
        self.color_duration = color_duration
        self.img_path = img_path


def draw_dount(data:pd.DataFrame, color:str):
    colors = plt.get_cmap(color)(np.linspace(0.7, 0.3, len(data.type.value_counts())))
    fig, ax = plt.subplots(figsize=(9,4), subplot_kw=dict(aspect="equal"), facecolor='none', edgecolor='none')
    ax.set_facecolor = 'none'

    recipe = data.type.value_counts().index
    data = data.type.value_counts(normalize=True)
    wedges, texts = ax.pie(data, wedgeprops=dict(width=0.5), startangle=90, colors=colors)

    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(arrowprops=dict(arrowstyle="-"),
            bbox=bbox_props, zorder=0, va="center")

    for i, p in enumerate(wedges): # format followed as matplotlib docs, where the angle changed
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        annotation = ax.annotate(f'{recipe[i]}: {data[i]:.2%} ', xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                    horizontalalignment=horizontalalignment, fontfamily='serif', **kw)
                    # may set facecolor as none here

    st.pyplot(fig)
    

def draw_wordcloud(data:pd.DataFrame, img_path:str, color_range:str):
    try:
        fig, ax = plt.subplots(facecolor='none', edgecolor='none', figsize=(12,6))

        # custom colour map ('#221f1f', '#b20710' are the range of colors)
        col_map = matplotlib.colors.LinearSegmentedColormap.from_list("", color_range) 
        # text: convert title in df to str then format it. 
        text = ' '.join(data['title'].tolist())
        # str(list(data['title'])).replace(',', '').replace('[', '').replace("'", '').replace(']', '').replace('.', '')
        
        # shape of the wordcloud
        mask = np.array(Image.open(img_path))
        wordcloud = WordCloud(background_color = 'white', colormap=col_map, max_words = 150, mask = mask).generate(text)

        plt.imshow(wordcloud, interpolation = 'bilinear')
        plt.axis('off') # turn off the axis
        plt.tight_layout(pad=0)
        st.pyplot(fig) # show on app
    except:
        st.write('Oops, wordcloud is not available, at least 1 word!')


def draw_date_line(data:pd.DataFrame, color:list):
    # running_copy = data.dropna(subset=['date_added'])

    month_order = [
        'January', 
        'February', 
        'March', 
        'April', 
        'May', 
        'June', 
        'July', 
        'August', 
        'September', 
        'October', 
        'November', 
        'December'
    ]

    
    data['month'] = pd.Categorical(data['date_added'].apply(lambda x: str(x).split()[0]), categories=month_order, ordered=True)
    sort_type = data.type.unique().tolist()
    sort_type.sort(reverse=True)
    month_count = data.groupby('type')['month'].value_counts().unstack().fillna(0).loc[sort_type].cumsum(axis=0).T # error in .loc at first

    fig, ax = plt.subplots(figsize=(12, 6), facecolor='none', edgecolor='none') # draw chart

    for i, type in enumerate(data['type'].value_counts()[sort_type[::-1]].index):
        input_type = month_count[type]
        ax.fill_between(input_type.index, 0, input_type, color=color[i], label=type, alpha=0.9)

    for s in ['top', 'right','bottom','left']:
        ax.spines[s].set_visible(False)

    ax.axhline(y = 0, color = 'black', linewidth = 1.3, alpha = .4)
    ax.tick_params(axis=u'both', which=u'both',length=0)
    ax.grid(False)
    ax.margins(x=0)
    ax.set_facecolor('none')
    ax.set_xticks(np.arange(0,12), month_order, fontfamily='serif', rotation=30, fontsize=12)

    # type = data.type.value_counts(dropna=True)[data.type.unique().tolist()]
    # data_type1 = data[data.type == type.index[0]]
    # data_type2 = data[data.type == type.index[1]]
    # filtered_month1 = data_type1.date_added.apply(lambda x: str(x).split()[0]).value_counts(dropna=True)[month_order]
    # filtered_month2 = data_type2.date_added.apply(lambda x: str(x).split()[0]).value_counts(dropna=True)[month_order]
    # stack = np.vstack([filtered_month1, filtered_month2])
    # ax.stackplot(month_order, stack, label=data.type.unique())

    x = 0.06
    y = 0.9
    fig.text(x, y, "Movie", fontweight="bold", fontfamily='serif', fontsize=15, color=color[0])
    fig.text(x+0.06, y, "|", fontweight="bold", fontfamily='serif', fontsize=15, color='#221f1f')
    fig.text(x+0.07, y, "TV Show", fontweight="bold", fontfamily='serif', fontsize=15, color=color[1])
    st.pyplot(fig)


def draw_heatmap(data:pd.DataFrame, color:str):
    try:
        df_date = data[['date_added']].dropna()
        df_date['year'] = df_date['date_added'].apply(lambda x : x.split(', ')[-1])
        df_date['month'] = df_date['date_added'].apply(lambda x : x.lstrip().split(' ')[0])

        month_order = [
            'January', 
            'February', 
            'March', 
            'April', 
            'May', 
            'June', 
            'July', 
            'August', 
            'September', 
            'October', 
            'November', 
            'December'
        ][::-1]

        ### month of year
        df_moy = df_date.groupby('year')['month'].value_counts().unstack().fillna(0)[month_order].T

        fig_hmp, ax = plt.subplots(figsize=(15, 10), dpi=300)

        hmp = ax.pcolormesh(df_moy, cmap=color, edgecolors='white', linewidths=2) # heatmap
        ax.set_xticks(np.arange(0.5, len(df_moy.columns), 1), df_moy.columns, fontsize=14)
        ax.set_yticks(np.arange(0.5, len(df_moy.index), 1), df_moy.index, fontsize=15)

        fig_hmp.colorbar(hmp, ax=ax)
        st.pyplot(fig_hmp)
    except:
        st.write('Oops, heatmap is not available due to lacking of enough month info!')
    
# get single entity series
def single_serires(series):
    stringed = ','.join(series.dropna())
    mid_list = list(map(lambda x: x.strip(), stringed.split(',')))
    final_list = list(filter(lambda x: x!='1', mid_list))
    final_series = pd.Series(final_list)
    return final_series

# bar plot for ferq count
def draw_freq_bar(data:pd.DataFrame, color:str, type:str):
    if type == 'director':
        single_variable = single_serires(data.director)
    elif type == 'cast':
        single_variable = single_serires(data.cast)
    elif type == 'country':
        single_variable = single_serires(data.country)

    fig, ax = plt.subplots(figsize=(12, 6), facecolor='none', edgecolor='none')
    # bar = single_variable.value_counts()[:10].plot.bar(color=color)
    bar = single_variable.value_counts()[:10]
    ax.bar(bar.index, bar, color=color)
    # ax.set_xticks(np.arange(0,10), bar.index, fontfamily='serif', rotation=60, fontsize=12)
    for label in ax.get_xticklabels():
        label.set(fontsize=12)
        label.set_fontfamily('serif')
        label.set_rotation(40)
        label.set_horizontalalignment('right')
    ax.margins(x=0)
    ax.set_facecolor('none')
    st.pyplot(fig)

# input dataframe, return dataframe, show map on st.
def movie_map(data:pd.DataFrame, color_st:str):
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
    
    for key,value in country_codes.items(): # added
        if value not in country_number.keys():
            country_number[value] = 0
    
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
                            mapbox_style="carto-positron", zoom=4, color_continuous_scale=color_st)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)

    return df # return df - (index: code of country; variable: counts)


def movie_duration(data:pd.DataFrame, color_str:str):
    movie_time_data = data[(data['duration']!= "") & (data['type']=='Movie')]
    data2 = pd.DataFrame(movie_time_data['duration'].dropna().apply(lambda x:float(x.split(' min')[0])))
    data2['zscore'] = stats.zscore(data2.duration)
    data2_drop = data2[(-3<data2['zscore']) & (data2['zscore']<4)]
    data2_out = data2[(data2['zscore']<-3)|(4<data2['zscore'])]
    x1 = data2_drop['duration']
    fig = ff.create_distplot([x1], ['times'], bin_size=0.7, curve_type='kde', colors=[color_str])#別忘了換顏色
    fig.update_layout(title_text='Movie time duration with KDE curve')
    st.plotly_chart(fig)


def show_number(data:pd.DataFrame, color_str:str):
    col = 'season_count'
    tv_data = data[(data['duration'] != "") & (data['type']=='TV Show')]
    data2 = pd.DataFrame(tv_data['duration'].fillna('0').apply(lambda x:float(x.split(' Season')[0])))
    vc1 = data2.duration.value_counts().reset_index()
    vc1 = vc1.rename(columns = {'duration':'number',"index" : col})
    trace1 = go.Bar(x=vc1[col].astype(int), y=vc1["number"], name="TV Shows", marker=dict(color=color_str))
    data = [trace1]
    layout = go.Layout(title="Tv show seasons duration bar plot", legend=dict(x=0.1, y=1.1, orientation="h"))
    fig = go.Figure(data, layout=layout)
    st.plotly_chart(fig)

# this may not be used, however, you can have a try.
import base64
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpeg"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
    


