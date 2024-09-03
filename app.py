import streamlit as st
import pandas as pd
import numpy as np
import pre_processor
import helper
import plotly.express as px    
import seaborn as sns
import matplotlib.pyplot as plt  
import plotly.figure_factory as ff



df=pd.read_csv('athlete_events.csv')
region_df=pd.read_csv('noc_regions.csv')

st.sidebar.title("Olympics Analysis")
st.sidebar.image('flag1.png')

df=pre_processor.preprocess(df,region_df)

user_menu=st.sidebar.radio('Select an Option',
    ('Medal_Tally','Overall Analysis','Country_Wise_Analysis','Athlete_Wise_Analysis'))


if user_menu=='Medal_Tally':
    st.sidebar. header("Medal_Tally")
    years,country=helper.country_year_list(df)

    selected_year=st.sidebar.selectbox("Select Year",years)
    selected_country=st.sidebar.selectbox("Select Country",country)
    if selected_country=="Overall" and selected_year=="Overall":
        st.title("Overall Tally")

    if selected_country=="Overall" and selected_year !="Overall":
        st.title("Medal Tally in " + str(selected_year))
    
    if selected_country!="Overall" and selected_year =="Overall":
        st.title(selected_country + " Medal Tally " )
    if selected_country!="Overall" and selected_year !="Overall":
        st.title(selected_country + " Medal Tally in "+str(selected_year) +"  Olympics" )
    medal_tally=helper.fetch_medal_tally(df,selected_year,selected_country)
    st.table(medal_tally)

if user_menu=='Overall Analysis':
    st.header("Top Statistics")
    Editions=df['Year'].unique().shape[0]-1
    Cities=df['City'].unique().shape[0]
    Sports=df['Sport'].unique().shape[0]
    Events=df['Event'].unique().shape[0]
    Atheltes=df['Name'].unique().shape[0]
    Nations=df['region'].unique().shape[0]

    col1,col2,col3=st.columns(3)
    with col1:
        st.header("Editions")
        st.title(Editions)
    with col2:
        st.header("Hosts")
        st.title(Cities)
    with col3:
        st.header("Sports")
        st.title(Sports)

    col1,col2,col3=st.columns(3)
    with col1:
        st.header("Events")
        st.title(Events)
        
    with col2:
        st.header("Athletes")
        st.title(Atheltes)
    with col3:
        st.header("Nations")
        st.title(Nations)
    nations_over_time=helper.data_over_time(df,'region')
    fig = px.line(nations_over_time, x='Year', y='region')
    st.title("Participating Nations Over The Years")
    st.plotly_chart(fig)

    events_over_time=helper.data_over_time(df,'Event')
    fig = px.line(events_over_time, x='Year', y='Event')
    st.title("Total Events Over The Years")
    st.plotly_chart(fig)

    athlete_over_time=helper.data_over_time(df,'Name')
    fig = px.line(athlete_over_time, x='Year', y='Name')
    st.title("Total Athletes Over The Years")
    st.plotly_chart(fig)

    st.title("Most Successfull Athletes")
    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport_list=st.selectbox('Select Sport',sport_list)
    x=helper.most_successfull(df,selected_sport_list)
    st.table(x)

if user_menu=='Country_Wise_Analysis':

    country_list=df['region'].dropna().unique().tolist()
    country_list.sort()
    st.sidebar.title("Country_Wise_Analysis")
    selected_country_list=st.sidebar.selectbox('Select Sport',country_list)
    country_df=helper.Year_wise_medal_tally(df,selected_country_list)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title(selected_country_list+" Total Medals Over The Years")
    st.plotly_chart(fig)
    
    st.title(selected_country_list+" Excels in folllowing Sports")
    pt=helper.country_event_heatmap(df,selected_country_list)

    fig,ax=plt.subplots(figsize=(20,20))
    ax=sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title("Top 20 Athletes of "+selected_country_list)
    top_df=helper.most_successfull_country_wise(df,selected_country_list)
    st.table(top_df)

if user_menu=='Athlete_Wise_Analysis':
    Athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = df['Age'].dropna()  
    x2 = Athlete_df[Athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = Athlete_df[Athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = Athlete_df[Athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    figure = ff.create_distplot(
        [x1, x2, x3, x4],  
        ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'], 
        show_hist=False,  
        show_rug=False    
    )
    figure.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution Of Age ")
    st.plotly_chart(figure)



    famous_sports=['Basketball',  'Football', 'Tug-Of-War', 'Athletics',
       'Swimming', 'Badminton', 'Sailing', 'Gymnastics', 'Handball', 'Weightlifting', 'Wrestling',
       'Water Polo', 'Hockey', 
       'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving',
       'Tennis', 'Golf', 'Archery',
       'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
       'Beach Volleyball','Polo',
        'Ice Hockey']
    x=[]
    name=[]
    for sport in famous_sports:
        temp_df=Athlete_df[Athlete_df['Sport']==sport]
        x.append(temp_df[temp_df['Medal']=='Gold']['Age'].dropna())
        name.append(sport)
    fig=ff.create_distplot(x,name,show_hist=False,show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of age wrt Sports")

    st.plotly_chart(fig)

    st.title("Men VS Women Participation")

    final=helper.men_women(df)
    fig=px.line(final,x='Year',y=["Male","Female"])
    st.plotly_chart(fig)





