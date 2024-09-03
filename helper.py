import numpy as np
def fetch_medal_tally(df,year,country):
    #Removing Duplicate Rows
    medal_df=df.drop_duplicates(subset=['Team','NOC','Year','Games','City','Sport','Event','Medal'])
    flag=0
    if year == 'Overall' and country =='Overall':
        temp_df=medal_df
    if year == 'Overall' and country !='Overall':
        flag=1
        temp_df=medal_df[medal_df['region'] == country]
    
    if year != 'Overall' and country =='Overall':
        temp_df=medal_df[medal_df['Year']==int(year)]
    
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

        
    if flag==1:
        x=temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    else:
        x=temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()


    
    x['total']=x['Gold']+x['Silver']+x['Bronze']
    return x
    



def Medal_tally(df):
    #Removing Duplicate Rows
    medal_tally=df.drop_duplicates(subset=['Team','NOC','Year','Games','City','Sport','Event','Medal'])
    medal_tally=medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    medal_tally['total']=medal_tally['Gold']+medal_tally['Silver']+medal_tally['Bronze']
    return medal_tally


def country_year_list(df):
    years=df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')

    country=np.unique(df['region'].dropna().values).tolist()
    country.insert(0,'Overall')
    country.sort()
    return years,country

def data_over_time(df,col):
    nations_over_time=df.drop_duplicates(['Year',col])['Year'].value_counts().reset_index().sort_values('Year')
    nations_over_time.rename(columns={'count':col},inplace=True)

    

    return nations_over_time

def most_successfull(df, sport):
    # Drop rows where 'Medal' is NaN
    temp_df = df.dropna(subset=['Medal'])
    
    # Filter by sport if it's not 'Overall'
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
    
    # Get the top 20 most successful athletes
    top_athletes = temp_df['Name'].value_counts().reset_index()
    top_athletes.columns = ['Name', 'count']  # Rename columns for clarity
    
    # Merge with the original DataFrame to get other details
    x = top_athletes.merge(df, left_on='Name', right_on='Name', how='left')[['Name', 'Sport', 'region', 'count']]
    
    # Drop duplicates based on the 'Name' column to avoid repeating the same athlete
    x = x.drop_duplicates(subset=['Name'])
    x=x.head(20)
    x.rename(columns={'count':'Medals'},inplace=True)
    
    return x

def Year_wise_medal_tally(df,country):
    temp_df=df.dropna(subset='Medal')
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
    new_df=temp_df[temp_df['region']==country]
    final_df=new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_event_heatmap(df,country):
    temp_df=df.dropna(subset='Medal')
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
    new_df=temp_df[temp_df['region']==country]
    pt=new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)
    return pt

def most_successfull_country_wise(df, country):
    # Drop rows where 'Medal' is NaN
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    top_athletes = temp_df['Name'].value_counts().reset_index()
    top_athletes.columns = ['Name', 'count']  # Rename columns for clarity
    x = top_athletes.merge(df, left_on='Name', right_on='Name', how='left')[['Name', 'Sport', 'count']]
    x = x.drop_duplicates(subset=['Name'])
    x=x.head(20)
    x.rename(columns={'count':'Medals'},inplace=True)
    
    return x

def men_women(df):
    Athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men=Athlete_df[Athlete_df['Sex']=='M'].groupby('Year').count()['Name'].reset_index()
    women=Athlete_df[Athlete_df['Sex']=='F'].groupby('Year').count()['Name'].reset_index()
    final=men.merge(women,on='Year')
    final.fillna(0,inplace=True)
    final.rename(columns={'Name_x':'Male','Name_y':'Female'},inplace=True)
    return final



   
     