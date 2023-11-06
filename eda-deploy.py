import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import copy
import re

from drawing_chart import color_set
import drawing_chart as dct

# If intend to use following line, please unavailable line15 first.
dct.add_bg_from_local('bgd.jpeg')

# plt.style.use('seaborn')
# st.set_page_config(page_title='Group 27 Data App', page_icon='🌞')

# read files
netflix_df = pd.read_csv('netflix_titles.csv')
hulu_df = pd.read_csv('hulu_titles.csv')
disney_plus_df = pd.read_csv('disney_plus_titles.csv')
amazon_prime_df = pd.read_csv('amazon_prime_titles.csv')


# data cleaning 
# (I believe this is just for sfaty but not necessary, cauz you may lose usful info)
netflix_df.dropna(subset=['duration', 'date_added'], inplace=True)

disney_plus_df.dropna(subset=['date_added'], inplace=True)

hulu_df.dropna(subset=['date_added'], inplace=True)

amazon_prime_df.drop(['date_added', 'country'], axis=1, inplace=True) # almost all is NaN


# ====================================== App content ====================================== #
st.title('Streaming media platform data app')
st.markdown('>***Exploratory Data Analysis** by **Wang Xing\'en** & **Zhang Aizhong***')

col1, col2, col3, col4 = st.columns(4)

col1.image('netflix_icon.jpeg')
col2.image('disney_icon.jpeg')  
col3.image('amazon_icon.png')
col4.image('hulu_icon.jpg')

head_container = st.container()

#set sidebar
container = st.sidebar.container()
# st.sidebar.title('Filters')

# set filter2 - choose platform 
platform_filter = st.sidebar.radio(
    'Choose a streaming platform', 
    ['Netflix', 'Disney Plus', 'Amazon Prime', 'Hulu', 'All in one'],
)

if platform_filter == 'Netflix':
    running_df = netflix_df
    df_color = color_set(
        'xkcd:wine red', 'Reds', ['#221f1f', '#b20710'], 
        'afmhot_r', 'amp', '#cc0000', 'netflix_Symbol_logo.png'
    )
elif platform_filter == 'Disney Plus':
    running_df = disney_plus_df
    df_color = color_set(
        'xkcd:royal purple', 'Purples', ['#1e001e', '#bb00bb'], 
        'RdPu', 'RdPu', '#8a2be2', 'large_thumbnail.jpg'
    )
elif platform_filter == 'Amazon Prime':
    running_df = amazon_prime_df
    df_color = color_set(
        'xkcd:dark sky blue', 'Blues', ['#005dcb', '#00152e'], 
        'PuBu', 'Blues', '#0047ab', 'amazon-logo-new.jpg'
    )
elif platform_filter == 'Hulu':
    running_df = hulu_df
    df_color = color_set(
        'xkcd:teal green', 'Greens', ['#001e00', '#00bb00'], 
        'YlGn', 'Greens', '#177245', 'hulu-Logo.jpg'
    )
elif platform_filter == 'All in one':
    running_df = pd.concat([netflix_df, disney_plus_df, amazon_prime_df, hulu_df]) # merge all ataframe
    df_color = color_set(
        'xkcd:slate grey', 'Greys', ['#161616', '#828282'], 
        'Greys', 'Greys', '#555555', 'all-shape.png'
    )

# when platform is chose: (a little mass but it's just too costly to regulate the color variable's name) 
#   running_df - dataframe 
#   uni_col - color of dount chart
#   col - color of bar chart
#   img_path - mask of wordcloud
#   cmap - color map of heatmap
#   col_range - color of wordcloud
#   col_scale - color of map
#   col_duration - color of hist & distribution
col = df_color.color_basic
uni_col = df_color.color_dount
col_range = df_color.color_cloud
cmap = df_color.color_heatmap
col_scale = df_color.color_map
col_duration = df_color.color_duration
img_path = df_color.img_path

running_df.reset_index(inplace=True)
static_df = copy.deepcopy(running_df) # unfilted data
static_all_df = pd.concat([netflix_df, disney_plus_df, amazon_prime_df, hulu_df]) # used later

# set filter3 -year
st.sidebar.markdown('---')

rel_year_df = running_df.release_year
rel_year = st.sidebar.select_slider(
    'Starting released year', 
    np.arange(min(rel_year_df), max(rel_year_df)+1),
    help='Click "Turn over" button to set the selected number as the stopping released year',
)
# set filter3 checkbox
if_turn = st.sidebar.checkbox('Turn over')

if if_turn:
    running_df = running_df[running_df['release_year'] <= rel_year]
else:
    running_df = running_df[running_df['release_year'] >= rel_year]

# set filter4 
st.sidebar.markdown('---')
list_in = dct.single_serires(running_df.listed_in.apply(lambda x: str(x))).unique()
list_options = st.sidebar.multiselect(
    'Genres you interested: ', list_in, 
    help='Default choice is empty, which means all is selected.',
)

for i in list_options:
    running_df = running_df[running_df.listed_in.str.contains(i)]

# set filter5
col_rating_1, col_rating_2 = st.sidebar.columns([1,3])

with col_rating_1:
    st.write('\n')
    st.write('\n')
    rating_check = st.checkbox('Wake', key='mute')

with col_rating_2: 
    rating = running_df.rating.dropna().apply(lambda x: str(x))
    rating_filted = rating[rating.apply(lambda x: re.search(r'\d\s\w', x) is None) & rating.apply(lambda x: re.search(r'^\d*\d$', x) is None)]
    rating_in = dct.single_serires(rating_filted).unique()

    rating_options = st.selectbox(
        'rating you interested: ', rating_in, 
        help='Click button left to wake up the selector',
        disabled= not st.session_state.mute,
    )

if rating_check:
    running_df.dropna(subset=['rating'], inplace=True)
    running_df = running_df[running_df.rating.str.contains(rating_options)]

for i in range(10): # to set some space at the ene of the sidebar
    st.sidebar.write('\n')

# go back to sidebar container
container.title('Meta Info')
if_static  = container.checkbox('Static mode')
# if below code is added, then user must be login and may cause cofused in mobile devices.
# container.write('LOGIN: ' + st.experimental_user["email"])
if if_static:
    running_df = static_df

container.markdown(f'#entities of current dataset: ***{len(running_df.index)}***')
container.markdown('**To keep things looks better, you\'d better keep the light mode on. And pictures may be extremly huge on phones.**')
container.markdown('---')

with st.expander('See title worldcloud'):
    dct.draw_wordcloud(running_df, img_path, col_range)

# ================================================= Total tab ================================================= #
tab1, tab2, tab3, tab4 = st.tabs(['OVERVIEW', 'DATE ADDED', 'FREQ COUNT', 'DURATION'])

with tab1:
    st.header('1 Overview')
    st.write('A quick overall look. Try to compare the dount with different released year!')
    st.caption('TBN: "Dataframe" didn\'t includes derciption of content, since it\'s too long to show.')
    tab01, tab02, tab03 = st.tabs(['Type', 'Backgrounds', 'Dataframe'])

    with tab01: 
        st.subheader(f'Types of {platform_filter}')
        col01, col02 = st.columns(2)

        with col01:
            ave_movie_perc = static_all_df.type.value_counts(normalize=True)['Movie']

            if str(running_df['type']).__contains__('Movie'):
                movie_perc = running_df.type.value_counts(normalize=True)['Movie']
                st.metric(f'% of Movies', f'{movie_perc:.2%}', f'{(movie_perc-ave_movie_perc):.2%}')
            else:
                st.metric(f'% of Movies', f'{0:.2%}', f'{0-ave_movie_perc:.2%}')

        with col02:
            ave_tv_perc = static_all_df.type.value_counts(normalize=True)['TV Show']
            if str(running_df['type']).__contains__('TV Show'):
                tv_perc = running_df.type.value_counts(normalize=True)['TV Show']
                st.metric(f'% of TV Shows', f'{tv_perc:.2%}', f'{(tv_perc-ave_tv_perc):.2%}')
            else:
                st.metric(f'% of TV Shows', f'{0:.2%}', f'{(0-ave_tv_perc):.2%}')

        try:
            dct.draw_dount(running_df, uni_col) # type dount chart
        except:
            st.write('Oops, not available, something goes wrong')

    with tab02:
        st.subheader(f'{platform_filter}\'s background information')
        dct.draw_info(platform_filter)   

    with tab03:
        st.write(running_df.drop(['description'], axis=1))

with tab2:
    # second part
    st.header('2 Add date chart')
    st.write('Best time for producers to release contnets')
    st.caption('TBN: Add date part is not available for amazon dataset')

    # content added month
    tab11, tab12 = st.tabs(['Line plot', 'Heatmap'])
    ## line plot
    with tab11:
        if platform_filter != 'Amazon Prime':
            st.subheader(f'{platform_filter} contents added date - Line plot')
            dct.draw_date_line(running_df, col_range[::-1])
        else:
            st.markdown('***Oops, the add-date info is not available for amazon dataset***, please try another platform!')
    ## heatmap of (year and month)
    with tab12:
        if platform_filter != 'Amazon Prime':
            st.subheader(f'{platform_filter} contents added date - Heatmap')
            dct.draw_heatmap(running_df, cmap)
        else:
            st.markdown('***Oops, the add-date info is not available for amazon dataset***, please try another platform!')

with tab3:
# directors, casts, country count
    st.header('3 Most frequent ...')
    st.write('Find most valuable person, or coountry with most potential.')
    st.caption('TBN: Country info is not available for amazon dataset')
    tab21, tab22, tab23, tab24= st.tabs(['Director', 'Cast', 'Country', 'Map'])

    with tab21:
        if platform_filter != 'Hulu':
            st.subheader(f'{platform_filter}\'s Top 10(if have) Directors')
            dct.draw_freq_bar(running_df, col, type='director')
        else:
            st.write('Oops, not available due to missing info of director info in current dataset.')

    with tab22:
        if platform_filter != 'Hulu':
            st.subheader(f'{platform_filter}\'s Top 10(if have) Casts')
            dct.draw_freq_bar(running_df, col, type='cast')
        else:
            st.write('Oops, not available due to missing of cast info in current dataset.')

    with tab23:
        if platform_filter != 'Amazon Prime':
            st.subheader(f'{platform_filter}\'s Top 10(if have) Countries')
            dct.draw_freq_bar(running_df, col, type='country')
        else:
            st.write('Oops, not availeble due to missing of countries info in current dataset.')

    with tab24:
        if platform_filter != 'Amazon Prime':
            st.subheader(f'{platform_filter}\'s Countries map')
            dct.movie_map(running_df, col_scale)
        else:
            st.write('Oops, map is not availeble due to missing of location info in current dataset.')    

with tab4:
    # Duration
    st.header('4 Duration distribution')
    st.write('How does duration of content distribute? ')
    st.write('Does more concentrated means more audience or just a regular?')
    st.caption('TBN: Some of the chosen dataset do not have \'Movie\' or \'TV Show\' info.')
    tab31, tab32 = st.tabs(['Movie Duration', 'TV Seansons'])

    with tab31:
        if str(running_df['type']).__contains__('Movie'):
            dct.movie_duration(running_df, col_duration)
        else:
            st.markdown('**Movies info not available in the dataset you chosed**')

    with tab32:
        if str(running_df['type']).__contains__('TV Show'):
            dct.show_number(running_df, col_duration)
        else:
            st.markdown('**TV Shows info not available in the dataset you chosed**')


# End of the page
with st.container():
    st.write('')
    st.write('')
    st.write('')
# captions
with st.container():
    st.markdown('---')
    st.caption(
        'More information on Kaggle: [Netflix](https://www.kaggle.com/datasets/shivamb/netflix-shows), '
        + '[Disney+](https://www.kaggle.com/datasets/shivamb/disney-movies-and-tv-shows), '
        + '[Amazon Prime](https://www.kaggle.com/datasets/shivamb/amazon-prime-movies-and-tv-shows), '
        + '[Hulu](https://www.kaggle.com/datasets/shivamb/hulu-movies-and-tv-shows). '
        + '*(all usability is 10.0)*'
    )
    st.caption('E-mail of author: derekwang0282@gmail.com, zhangaizhong20@163.com')
    st.caption(
        'Background Image: Photo by '
        + '<a href="https://unsplash.com/@evieshaffer?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Evie S.</a> on Unsplash'
        , unsafe_allow_html=True
    )
    st.caption('Github page: [Derek Wang](https://github.com/Derekwang2002/Final_Project#streaming-platform-data-app-eda)')
    st.caption('Copyright © 2022')
