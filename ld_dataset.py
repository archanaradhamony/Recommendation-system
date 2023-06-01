# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 23:14:46 2021

@author: archa
"""

import pandas as pd

#define the class to read csv file and create the dataframe music_features
class csv_read:
    
#set the dataframe as read the csv file
    def __init__(df, file, music_features):
        #df.__music_features = music_features
        df.__music_features = pd.read_csv(file, usecols =['name','artists','acousticness', 'danceability', 'energy', 'liveness', 'loudness', 'popularity', 'speechiness', 'tempo', 'valence'])
        df.__music_features.fillna(0, inplace = True)
        

#return the dataframe
    def get_data_frame(df):
        return df.__music_features    
    


#define class to create artist music lookup dictionary
class create_dict(csv_read):
    
    
    def __init__(df, file, music_features, Artist_music):
        csv_read.__init__(df, file,music_features)
        df.__Artist_music = Artist_music
        
#create artist music divtionary in the format {artist1:[music1, music2], artist2:[music1, music3],...}    
    def get_artist_features(df, Artist_music, music_features):
        #Artist_music = {}
        bad_Chars = ['[', ']', ',', "'"]
        for i in range(len(music_features)):
#Code to extract each artist from the "artist" field in the input file (There are multiple artists in some of the rows) and write to a dictionary
            for x in music_features.loc[i,'artists'].split(','):
                for j in bad_Chars:
                    x=x.replace(j,'')   
                y=x.strip()
                #print(y)
                if y not in Artist_music.keys():
                    Artist_music[y] = list()
                    Artist_music[y].append(music_features.loc[i,'name'])
                else:
                    Artist_music[y].append(music_features.loc[i,'name'])
        return df.__Artist_music
    
    
#class to create the dataframe for each unique artist, with the list of music names and the average of each music feature for the list of music corresponding to each artist

class create_artist_music_feature(create_dict):
    def __init__(df, file, music_features, Artist_music, artist_music_features):
        create_dict.__init__(df, file, music_features, Artist_music)
        df.__artist_music_features = artist_music_features
        
    def build_artist_music_features(df, music_features, Artist_music, artist_music_features):
    
    #build data frame with data from the artist_music dictionary
        artist_music_features = pd.DataFrame(list(Artist_music.items()),columns = ['artists','name'])
        
    #initialize the music features columns in the data frame
        artist_music_features.insert(2,'acousticness', 0.0)
        artist_music_features.insert(3,'danceability', 0.0)
        artist_music_features.insert(4,'energy', 0.0)
        artist_music_features.insert(5,'liveness', 0.0)
        artist_music_features.insert(6,'loudness', 0.0)
        artist_music_features.insert(7,'popularity', 0.0)
        artist_music_features.insert(8,'speechiness', 0.0)
        artist_music_features.insert(9,'tempo', 0.0)
        artist_music_features.insert(9,'valence', 0.0)
        #print(artist_music_features)
        
    #from the master dataframe (data frame created in the super class csv_read), create a temporary dataframe for each artist in the new dataframe.
    #get the average of each music feature from the temporary data frame and update the value for each music feature with these values for the corresponding artist in the new dataframe
        for i in range(len(artist_music_features)):
            artist = artist_music_features.loc[i,'artists']
            temp_df = music_features.loc[music_features['artists'].str.contains(artist)]
            #print(temp_df)
            avg_feature = temp_df.mean()
            #print(avg_feature)
            #print(avg_feature['acousticness'])
            music_features_cols = ['acousticness', 'danceability', 'energy', 'liveness', 'loudness', 'popularity', 'speechiness', 'tempo', 'valence']
            for col in music_features_cols:
                artist_music_features.loc[i, col] = avg_feature[col]
        return(artist_music_features) 
    