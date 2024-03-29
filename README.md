# Streaming Media Platform Data App (EDA)
***MISY225 Final Project***

>By: Wang Xing'en & Zhang Aizhong  
>Create date: 2022-11-03  

Deployed python file is [`eda-deploy.py`](https://github.com/Derekwang2002/Final_Project/blob/master/eda-deploy.py)  

Custom define functions are in [`drawing_cahrt.py`](https://github.com/Derekwang2002/Final_Project/blob/master/drawing_chart.py)  

Slides is [`team27.pdf`](https://github.com/Derekwang2002/Final_Project/blob/master/team27.pdf)  


## Project Introduction
Streaming platforms is playing an more important part of people's daily entretains. It encouraged content producer to perform more high quality contents, e.g., Gmae of Thrones, The card house, or Love, Death, Robot...

Though they are not available currently in CN, we still could see what are those platforms 'looks' like.

Through this project, we'll focus on the information of content on the platform based on interactive streamlit data app. At last, hopfully, we'll get a deeper understanding of how contents on each platforms are like.

Next, let's start the journey!

## Dataset Description
- About contents inforamtion on certain streaming platform.
- Variables(columns):
  - `show_id`: Unique ID for every Movie / TV Show.
  - `type`: Identifier - A Movie or TV Show.
  - `title`: Title of the Movie / TV Show.
  - `director`: Director of the Movie / TV Show.
  - `cast`: Actors involved in the Movie / TV Show.
  - `country`: Country where the Movie / TV Show was produced.
  - `date_added`: Date it was added on the certain platform.
  - `release_year`: Actual Release year of the Movie / TV Show.
  - `rating`: TV Rating of the Movie / TV Show.
  - `duration`: Total Duration - in minutes for movies or number of seasons for TV Shows.
  - `listed_in`: Generes of contnts.
  - `description`: The summary description
- Source of data set: *Kaggle.com*, Includes:
  - [Netflix](https://www.kaggle.com/datasets/shivamb/netflix-shows)
  - [Disney+](https://www.kaggle.com/datasets/shivamb/disney-movies-and-tv-shows)
  - [Amazon Prime](https://www.kaggle.com/datasets/shivamb/amazon-prime-movies-and-tv-shows)
  - [Hulu](https://www.kaggle.com/datasets/shivamb/hulu-movies-and-tv-shows)


## Guidence of Data App
### Structure:
- Sidebar: includes meta information of dataset and the filters.
- Main body: Charts that shows different info of dataset, categoried in four types:
  1. Overview
  2. Add date chart
  3. Frequency count
  4. Duration distribution

### Sidebar
- Meta info:
  - numbers of entities.
  - 'static' mode choice(which could ignore all filters below).
- Filters:
  - radio: choose certain streaming platforms.
  (***TBN: With each choice of radio, the theme color for charts is unique!***)
  - selet_slider: choose the starting released date of contents.
  - muliselect: choose the genres of contents(default none, select all genres).

### Main Body  
From the top of the page, there are: *title, author, a picture, a title wordcloud in the expander*.  
And next is our EDA ouput:  
1. **Overview**:
    - A dount pie chart of percentage of type info.
    - Raw dataframe.  

2. **Add date chart**
    - A stacked line chart(categoried in type) of number of added contents by months.
    - A heatmap of number of added contents by months in each year.  

3. **Freuency counts**
    - Top 10 frequent directors.
    - Top 10 frequent cats.
    - Top 10 frequent countries.
    - Frequency of country counts on map.  

4. **Duration distribution**
    - Distribution of movie duration in minutes.
    - Bar chart of most freunt duration seasons of tv shows.  


At the end of the page is captions of related information.  

### Somethings to notice befor starting app...

- Map need a longer to show out, please wait for a second.
- Hulu dataset is the slowest due to its wordcloud processing.
- Picture on top of main body would be super big on mobile phones.
- Please don't turn on dark mode if you want a better look.
- There are some missing data in some dataset, be careful.
- There is a mistake in hulu's raw dataset, which put some of duration info into rating info. And I didn't process it. So, there may exist bias in EDA.


*Now, enjoy app! ->* [*Streamlit App Entrance*](https://derekwang2002-final-project-eda-deploy-sqq3hk.streamlit.app/)

## Findings of EDA
- Questions:
  - **Strategies** of certain platform?
  - Best **timing** for content producer to publish thier products?
  - Which director/cast tend to have more **business value**?
  - What are the **major market countries** for the platform or where are the **potential market countries**?
  - How **duartion distributed**, and why? Could that distribution provide any useful informations?
- Interest conclusions:
  - In general, **movies** takes a larger percentage of all platforms. However, the **tv show** is taking a larger percentage recently, it might be the current strategy for streaming platforms.
  - Overall, the **contents published more on last half year**. But it is quit different for different dataset you chose. For Disney, the peak appeared in november is caused by its **first-establish add**.
  - In 2020, there is a **drop** in added content, that may caused by the COVID-19.
  - The **United States has always been the most important market of the platform**, followed by Britain and India. Since the **beginning of the 21st century**, the color of **China, Japan and Egypt** has been deepening, indicating that the film industry of these countries has developed rapidly and quickly stepped onto the international stage. In the future, the film industry of these countries may be more valuable for investment.
  - **Most of the movie duration are between 90 to 110min**, thus such a length may be more popular with audiences. Most of the TV show only have one season. So the director and investor really need to consider whether to make another season for their TV shows


<table><tr>
<td><img src="netflix_icon.jpeg" width="150"/></td>
<td><img src="disney_icon.jpeg" width="150"/></td>
<td><img src="amazon_icon.png" width="150"/></td>
<td><img src="hulu_icon.jpg" width="150"/></td>
</tr><table>
