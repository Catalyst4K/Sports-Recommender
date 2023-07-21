import DataManager as dm
from curses.ascii import SP, US
from stringprep import in_table_d2
import pandas as pd
from sqlalchemy import true
from sklearn.preprocessing import LabelEncoder
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from surprise import Dataset
from surprise import Reader
from surprise import SVD
from surprise import KNNWithMeans
from surprise.model_selection import GridSearchCV
le = LabelEncoder()

#Convert non numeric values to numeric and drop empty cells
def PrepareDataSport(df):
    df['Category'] = le.fit_transform(df['Category'])
    df['Type'] = le.fit_transform(df['Type'])
    df = df.dropna(how= 'any')
    df = df.reset_index(drop = True)
    return df

#Convert non numeric values to numeric and drop empty cells
def PrepareDataUser(df):
    df['Sport Type'] = le.fit_transform(df['Sport Type'])
    df['Gender'] = le.fit_transform(df['Gender'])
    df['Postcode'] = le.fit_transform(df['Postcode'])
    df = df.dropna(how= 'any')
    df = df.reset_index(drop = True)
    return df

#Convert non numeric values to numeric and drop empty cells
def PrepareDataRating(df):
    df['Sport'] = le.fit_transform(df['Sport'])
    df = df.dropna(how= 'any')
    df = df.reset_index(drop = True)
    return df

#Content Based for Sport
#Using cosine similarity comparing sport table attiributes
def SimpleContentBasedSport(Sport):
    SimpleReccomend = []
    df = dm.RetriveSportData()
    df = PrepareDataSport(df)
    indexList = df.index[df['Sport'] == Sport].tolist()
    SportNum = indexList[0]
    cos_sim = cosine_similarity(df.iloc[:,2:])
    recomends = np.argsort(cos_sim[SportNum])[-4:][::-1]
    for i in recomends:
        if i != SportNum:
            SimpleReccomend.append(df['Sport'][i])
    return SimpleReccomend

#Content Based for user
#Using cosine similarity comparing user table attiributes
def SimpleContentBasedUser(User):
    SimpleReccomend = []
    df = dm.RetriveUserData()
    #df.drop(df.loc[df['USER_ID']==User].index, inplace=True)
    df = PrepareDataUser(df)
    indexList = df.index[df['USER_ID'] == User].tolist()
    UserNum = indexList[0]
    cos_sim = cosine_similarity(df.iloc[:,1:])
    recomends = np.argsort(cos_sim[UserNum])[-4:][::-1]
    for i in recomends:
        if i != UserNum:
            SimpleReccomend.append(df['USER_ID'][i])
    return SimpleReccomend

#Collabertive reccomender using KNN 
#Multiple Debugging and optimisation checks commented out
def CollaberativePartOne(User_ID):
    rdf = dm.RetriveRatingData()
    sdf = dm.RetriveSportData()
    usdf = dm.RetriveUserSportData()
    reader = Reader(rating_scale=(0 , 1))
    data = Dataset.load_from_df(rdf[["USER_ID", "Sport", "Rating"]], reader)

    sim_options = {
    "name": "msd",
    "min_support": 3,
    "user_based": True,
}

    algo = KNNWithMeans(sim_options=sim_options)
    trainingSet = data.build_full_trainset()
    algo.fit(trainingSet)
    ResultsDF = pd.DataFrame(columns = ['Sport_ID' , 'Rating'])
    UserSports = usdf.loc[usdf['USER_ID'] == User_ID]
    SportIDList = UserSports.Sport_ID.values.tolist()
    for ind in sdf.index:
        SportID = (sdf['Sport_ID'][ind])
        prediction = algo.predict( User_ID , SportID )
        if SportID not in SportIDList:
            DataToEnter =  {'Sport_ID': int(SportID) , 'Rating':prediction.est }                        
            ResultsDF = ResultsDF.append(DataToEnter, ignore_index=True)


    #Exploring options

    #sim_options = {
    #"name": ["msd", "cosine"],
    #"min_support": [ 1, 2, 3, 4, 5],
    #"user_based": [False, True],
    #}

    #param_grid = {"sim_options": sim_options}

    #gs = GridSearchCV(KNNWithMeans, param_grid, measures=["rmse", "mae"], cv=3)
    #gs.fit(data)

    #print(gs.best_score["rmse"])
    #print(gs.best_params["rmse"])

    #param_grid = {
    #"n_epochs": [5, 10],
    #"lr_all": [0.002, 0.005],
    #"reg_all": [0.4, 0.6]
    #}    

    #gs = GridSearchCV(SVD, param_grid, measures=["rmse", "mae"], cv=3)

    #gs.fit(data)

    #print(gs.best_score["rmse"])
    #print(gs.best_params["rmse"])
   
    SortedDf = ResultsDF.sort_values(by=['Rating'], ascending=False, ignore_index=True )
    SportResults =[]
    for i in range(0 , 3):
        SportResults.append((SortedDf['Sport_ID'][i]))

    return SportResults
    

    

  
    

