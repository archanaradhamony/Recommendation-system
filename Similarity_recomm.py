# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 00:06:12 2021

@author: archa
"""

import pandas as pd
import numpy as np
from scipy.spatial import distance

#define the super class to generate similarity matrices, that initializes the input parameters
class distance_quest:
    def __init__(df,MasterArray, LookupArray):
        df.__MasterArray = MasterArray
        df.__LookupArray = LookupArray
        
    def get_LookupArray(df):
        return df.__LookupArray 
    def get_MasterArray(df):
        return df.__MasterArray

#define sub classes for finding each similarity matrix, utilizing polimorphism
#define the sub class for eucledean distance   
class euc_distance(distance_quest):
    def __init__(df, MasterArray, LookupArray):
        distance_quest.__init__(df, MasterArray, LookupArray) 
    
    def find_distance(df, MasterArray, LookupArray):
        return(distance.cdist(MasterArray, LookupArray, 'euclidean'))
    
#define the sub class for cosine distance
class cos_distance(distance_quest):
    def __init__(df, MasterArray, LookupArray):
        distance_quest.__init__(df, MasterArray, LookupArray) 
        
    def find_distance(df, MasterArray, LookupArray):
        return(distance.cdist(MasterArray, LookupArray, 'cosine'))
    
#define the sub class for Manhattan distance
class manhattan_distance(distance_quest):
    def __init__(df, MasterArray, LookupArray):
        distance_quest.__init__(df, MasterArray, LookupArray) 
    
    def find_distance(df, MasterArray, LookupArray):
        return(distance.cdist(MasterArray, LookupArray, 'cityblock'))
    
#define the sub class for Pearson correlation
class pearson_distance(distance_quest):
    def __init__(df, MasterArray, LookupArray):
        distance_quest.__init__(df, MasterArray, LookupArray) 
        
    def find_distance(df, MasterArray, LookupArray):
        return(distance.cdist(MasterArray, LookupArray, 'correlation'))
    
        
#define the sub class for Jaccard correlation
class jaccard_distance(distance_quest):
    def __init__(df, MasterArray, LookupArray):
        distance_quest.__init__(df, MasterArray, LookupArray) 
        
    def find_distance(df, MasterArray, LookupArray):
        return(distance.cdist(MasterArray, LookupArray, 'jaccard'))
    
    
#Class to build a dataframe with the artist name(s), music name(s) and corresponding values of all the 5 similarity matrices. 
class dist_Matrix_df:
    def __init__(df, source_df, dest_df, euc_array, cos_array, manhattan_array, pearson_array, jaccard_array):
        df.__source_df = source_df
        df.__dest_df = dest_df
        df.__euc_array = euc_array
        df.__cos_array = cos_array
        df.__manhattan_array = manhattan_array
        df.__pearson_array = pearson_array
        df.__jaccard_array = jaccard_array
        
    
    def build_dist_matrix(df,source_df, dest_df, euc_array, cos_array, manhattan_array, pearson_array, jaccard_array):
        dest_df = source_df
        dest_df = dest_df.drop(columns = ['acousticness', 'danceability', 'energy', 'liveness', 'loudness', 'popularity', 'speechiness', 'tempo', 'valence'])
        dest_df['euclidean'] = euc_array
        dest_df['cosine'] = cos_array
        dest_df['manhattan'] = manhattan_array
        dest_df['pearson'] = pearson_array
        dest_df['jaccard'] = jaccard_array
        return (dest_df)
    
    def sort_df(df):
        pass
        

#sub classes, utilizing polymorphism to sort the dataframe based on each distance matrix
class euc_matrix_df(dist_Matrix_df):
    def __init__(df, source_df, dest_df, euc_array, cos_array, manhattan_array, pearson_array, jaccard_array):
        dist_Matrix_df.__init__(df, source_df, dest_df, euc_array, cos_array, manhattan_array, pearson_array, jaccard_array)

    def sort_df(df, dest_df):
        dest_df = dest_df.sort_values('euclidean')
        dest_df.reset_index(drop=True, inplace=True)
        return(dest_df)
        
class cos_matrix_df(dist_Matrix_df):
    def __init__(df, source_df, dest_df, euc_array, cos_array, manhattan_array, pearson_array, jaccard_array):
        dist_Matrix_df.__init__(df, source_df, dest_df, euc_array, cos_array, manhattan_array, pearson_array, jaccard_array)

    def sort_df(df, dest_df):
        dest_df = dest_df.sort_values('cosine')
        dest_df.reset_index(drop=True, inplace=True)
        return(dest_df)
    
class manhattan_matrix_df(dist_Matrix_df):
    def __init__(df, source_df, dest_df, euc_array, cos_array, manhattan_array, pearson_array, jaccard_array):
        dist_Matrix_df.__init__(df, source_df, dest_df, euc_array, cos_array, manhattan_array, pearson_array, jaccard_array)

    def sort_df(df, dest_df):
        dest_df = dest_df.sort_values('manhattan')
        dest_df.reset_index(drop=True, inplace=True)
        return(dest_df)
    
class pearson_matrix_df(dist_Matrix_df):
    def __init__(df, source_df, dest_df, euc_array, cos_array, manhattan_array, pearson_array, jaccard_array):
        dist_Matrix_df.__init__(df, source_df, dest_df, euc_array, cos_array, manhattan_array, pearson_array, jaccard_array)

    def sort_df(df, dest_df):
        dest_df = dest_df.sort_values('pearson')
        dest_df.reset_index(drop=True, inplace=True)
        return(dest_df)
    
class jaccard_matrix_df(dist_Matrix_df):
    def __init__(df, source_df, dest_df, euc_array, cos_array, manhattan_array, pearson_array, jaccard_array):
        dist_Matrix_df.__init__(df, source_df, dest_df, euc_array, cos_array, manhattan_array, pearson_array, jaccard_array)

    def sort_df(df, dest_df):
        dest_df = dest_df.sort_values('jaccard')
        dest_df.reset_index(drop=True, inplace=True)
        return(dest_df)
    
#class to generate top n recommended music/artists from the sorted dataframe having the song, music and all the distance matrix
class recommendations:
    def __init__(df, am_dataframe, artist, music, count, artist_list, music_list):
        df.__am_dataframe = am_dataframe
        df.__artist = artist
        df.__music = music
        df.__count = count
        df.__artist_list = artist_list
        df.__music_list = music_list

#method to return a list of n artist recommendations, corresponding to the artist entered by the user
    def get_top_n_artists(df, am_dataframe, count, artist):
        artist_list = []
        for i in range(0, int(count)+1):
            if artist in am_dataframe.loc[i,'artists']:
                continue
                #print("artist matches", am_dataframe.loc[i,'artists'], artist)
            else:
                #print("artist do not matches", am_dataframe.loc[i,'artists'], artist)
                #print(am_dataframe.loc[i,'artists'])
                artist_list.append(am_dataframe.loc[i,'artists'])
        return(artist_list)
    
#method to return a list of n music recommendations corresponding to the artist entered by the user   
    def get_top_n_music_frm_artists(df, am_dataframe, count, artist):
        count_music = 0
        music_list = []
        for j in range(1,int(count)+1):
            for temp_music in am_dataframe.loc[j,'name']:
                if (count_music > int(count)):
                    continue
                else:
                    if temp_music not in music_list:
                        music_list.append(temp_music)
                       # print(temp_music)
                        count_music = count_music+1
                    else:
                        continue
        return(music_list)
 
 #method to return a list of n music recommendations corresponding to the music entered by the user
    def get_top_n_music_frm_music(df, am_dataframe, count, music):
        music_list = []
        for i in range(0, int(count)+1):
            if music in am_dataframe.loc[i,'name']:
                continue
               # print("music matches", am_dataframe.loc[i,'name'], music)
            else:
               # print("music do not matches", am_dataframe.loc[i,'name'], music)
               # print(am_dataframe.loc[i,'name'])
                music_list.append(am_dataframe.loc[i,'name'])
        return(music_list)
        
            
                
        
        