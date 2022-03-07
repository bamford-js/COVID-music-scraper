# -*- coding: utf-8 -*-
"""
-- COVID-music YouTube Scraper --

Script for scraping COVID music videos from YouTube in order to fill
gaps in an existing database. This was built using cells in Spyder, for 
Python 3.7. It could be easily adapted into a Jypiter Notebook, if 
preferred. Make sure to set the parameters in the next cell, but otherwise
this should run without further alteration. If there is no existing database, 
you may have to remove three lines of code, and these should be clearly marked. 

Created on 16 Oct 2020

Latest update on 4 Nov 2020

@author: Joshua Bamford

"""

from googlesearch import search
import pandas as pd
import time
import random

# import existing database
video_database = pd.read_csv('video_database.csv') # remove this if not filling gaps in an existing database

#%% Set parameters

start_date = '2020-02-26'
end_date = '2020-04-28'
video_num = 25 # number of videos to take per day per country
countries = ['AU','GB','DK','US','IT'] # list of countries to search
domains = {'AU':'com.au', 'GB':'co.uk', 'DK':'dk', 'US':'com','IT':'it'} # maps country codes to TLD
filename = 'NewVideos.csv' # filename for exported file
search_terms = 'music OR musica OR musik OR musique OR muziek OR song OR tune OR lied OR liedje OR chanson OR canzone OR sang) AND (covid OR covid19 OR “covid-19” OR coronavirus OR corona OR "sars-cov-2" OR #quarantunes OR #covidance OR #coronasongs OR #coronamusic OR #TogetherAtHome OR #StayHome OR #Pandemix OR #COVered19 OR #gratitunes'
# note that this is the maximum number of search terms

#%% Find the videos!

dates = pd.date_range(start=start_date, end=end_date)
new_video_database = pd.DataFrame(data={'date': ['place'], 'URL': ['holder']})
new = True
abort = False

for i in range(len(dates)-1):
    if abort == True:
        print('Run away!')
        break        
    # select days
    sdate = str(dates[i])[0:10]
    edate = str(dates[i+1])[0:10]
        
    for n in countries:
        # generate list of videos 
        query = 'site:youtube.com before:{} after:{} ({})'.format(edate,sdate,search_terms)
        video_list = []
        dailySearch = search(query, tld=domains[n], num=video_num, stop=video_num, pause=10, country=n, extra_params={'pws':'0','gl':n}) 
        try:
            for j in dailySearch:
                j = j[0:43] # remove fluff
                if j in video_database[['URLs']].values: # remove if there is no existing database
                    print(j+' is already in database') # remove if there is no existing database
                elif j[0:29] != 'https://www.youtube.com/watch':
                    print(j+' is not a video')
                else:
                    video_list.append(j)
                    print(j)
                # random delay to keep Google off our trail
                time.sleep(random.randrange(5, 10, 1))
        except:
            print('Google is on to us! Abort mission!')
            abort = True
            break
        
        # write videos to database
        df = pd.DataFrame(data={'date': sdate, 'country': n, 'URL': video_list})
        if new == True:
            new_video_database = df
            new = False
            print('Created new database starting at {} in {}.'.format(sdate, n))
        else:    
            new_video_database = pd.concat([new_video_database, df], ignore_index=True)
            print('Added videos from {} and {} to database.'.format(sdate, n))
        
        # random delay to keep Google off our trail
        time.sleep(random.randrange(5, 20, 1))

if abort == False:
    print('Mission complete.')
else:
    print('Finished searching at {} in {}. Please try again later.'.format(sdate, n))

#%% Export CSV

new_video_database.to_csv(filename, index_label=True)
print('Exported to .csv file')


    
