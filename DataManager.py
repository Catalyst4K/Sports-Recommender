import sqlite3
import pandas as pd
from sqlalchemy import true
from sklearn.preprocessing import LabelEncoder
import bcrypt

DB_Name = 'Data/SportReccomend_Database'

Active = sqlite3.connect(DB_Name)
c = Active.cursor()
Active.commit()

def UserLoginInitial():
    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS UserLogin (
                                    USER_ID integer PRIMARY KEY AUTOINCREMENT,
                                    Email text NOT NULL,
                                    Password text NOT NULL
                                    ); """
    c.execute(sql_create_projects_table)
    Active.commit()

def EncryptPword(Password):
    Salt = bcrypt.gensalt()
    bytePwd = Password.encode('utf-8')
    EncryptedPword = (bcrypt.hashpw(bytePwd , Salt)).decode('utf-8')
    return EncryptedPword

def UserLoginCheck(Email, Password):
    Is_Valid = False
    sql_query = "SELECT Password from UserLogin WHERE Email='"+Email+"'"
    c.execute(sql_query)
    StoredPassword = c.fetchone()
    StoredPassword=str(StoredPassword).strip("('',)'")
    StoredPassword = StoredPassword.encode('utf-8')
    Password = Password.encode('utf-8')
    if StoredPassword is not None:
        ValidPass = bcrypt.checkpw(Password , StoredPassword)
        if ValidPass:
            Is_Valid = True
            sql_query = "SELECT USER_ID from UserLogin WHERE Email='"+Email+"'"
            c.execute(sql_query)
            user = c.fetchone()
            user=str(user).strip("('',)'")
            print('Welcome User' , user)
        else:
            print('Invalid Credentials Please Try Again')
            user = 0
    else:
        print('Invalid Credentials Please Try Again')
        user = 0
    return Is_Valid, user

def AddUser(Email , Password):
    Is_Valid = False
    Password = EncryptPword(Password)
    sql_query = "SELECT * from UserLogin WHERE Email='"+Email+"'"
    c.execute(sql_query)
    if not c.fetchone():
        sql_query = "INSERT into UserLogin (Email , Password) VAlUES ('"+Email+"' , '"+Password+"' )"
        try:
            c.execute(sql_query)
            Active.commit()
            Is_Valid = True
        except sqlite3.Error as error:
            print(error)
            print("Invalid Credentials Try Again")
    else:
        print("User Allready Exists")
    return Is_Valid

#Importing initial Data
def SportsTableInitial():
    df = pd.read_csv('Data/Sports.csv')
    UpdateSportsData(df)

#Function to add user to the data
def AddUserInfo(UserData):
    df = RetriveUserData()
    df. append(UserData, ignore_index=True)
    UpdateUserTable(df)

#Initial Table Ceation from data gathering
def CreateUserSportTable(mdf, sdf):
    usdf = pd.DataFrame(columns= ['USER_ID' , 'Sport_ID'])
    for ind in mdf.index:
        User = (mdf['USER_ID'][ind])
        Sport = (mdf['Sport'][ind])
        SportID = sdf.loc[sdf['Sport'] == Sport , 'Sport_ID'].iloc[0]
        DataToEnter = {'USER_ID': int(User) , 'Sport_ID': int(SportID)}
        usdf = usdf.append(DataToEnter, ignore_index=True)
    UpdateUserSport(usdf)

#Initial Table Ceation from data gathering
def CreateUserTable(df):
    udf = pd.DataFrame(columns = ['USER_ID' , 'Gender' , 'Age' , 'Postcode', 'Sport Type'])
    CurrentUserID = 0
    for ind in df.index:
        User_ID = (df['USER_ID'][ind])
        Gender = (df['Gender'][ind])
        Age = (df['Age'][ind])
        Postcode = (df['Postcode'][ind]).upper()
        SportType = (df['Sport Type'][ind])
        if User_ID != CurrentUserID:
            DataToEnter  = {'USER_ID': User_ID, 'Gender': Gender, 'Age': Age, 'Postcode': Postcode ,'Sport Type': SportType}
            CurrentUserID = User_ID
            udf = udf.append(DataToEnter, ignore_index=True)
    UpdateUserTable(udf)


#Ratings table Matrix Style not used by KNN
def createRatingsTable(df):
    CurrentUser = 0
    rdf = pd.DataFrame(columns = ['USER_ID', 'Football' , 'Field Hockey' , 'Netball' , 'Volleyball' , 'Tennis' , 'Distance Running', 'Track and Field Athletics', 'Big Wall Climbing', 'Bouldering', 'Lacrosse' , 'Swimming', 'Golf','Rugby','Ice Hockey', 'Table Tennis', 'Badminton','Cricket','Paddle Tennis','Skiing','Snowboarding','Pool','Snooker','Karate','Jiu Jitsu','Basketball','Gymnastics','Squash','Mountain Biking','BMX','Road Cycling','Equestrian','Rowing','Taekwondo','Triathlon','Motorssport','American Football','Baseball/Softball','Weightlifting' ])
    for ind in df.index:
        User_ID = (df['USER_ID'][ind])
        Sport = (df['Sport'][ind])
        if User_ID != CurrentUser:
            DataToEnter = {'USER_ID': int(User_ID)}
            CurrentUser = User_ID
            rdf = rdf.append(DataToEnter, ignore_index=True)
        rdf.loc[rdf.USER_ID == User_ID, Sport] = 1
    rdf = rdf.fillna(0)
    UpdateRatingsTable(rdf)

#Ratings table in  a list format used by KNN
def createRatingsTableAlt():
    CurrentUser = 1
    usdf = RetriveUserSportData()
    sdf = RetriveSportData()
    rdf = pd.DataFrame(columns = ['USER_ID', 'Sport', 'Rating' ])
    included = []
    for ind in usdf.index:
        User_ID = (usdf['USER_ID'][ind])
        SportID = (usdf['Sport_ID'][ind])
        Sport = sdf.loc[sdf['Sport_ID'] == SportID , 'Sport'].iloc[0]
        if CurrentUser == User_ID:
            included.append(Sport)
        else:
            for ind2 in sdf.index:
                Sport2 = (sdf['Sport'][ind2])
                if Sport2 in included:
                    DataToEnter =  {'USER_ID':CurrentUser , 'Sport':Sport2, 'Rating':1}                        
                    rdf = rdf.append(DataToEnter, ignore_index=True)
                else:
                    DataToEnter =  {'USER_ID':CurrentUser , 'Sport':Sport2, 'Rating':0} 
                    rdf = rdf.append(DataToEnter, ignore_index=True)
            included.clear()
            included.append(Sport)
            CurrentUser = int(User_ID)

    UpdateRatingsTable(rdf)

#Function to update the average age and average gender for each sport
def UpdateAverages():

    udf = RetriveUserData()

    usdf = RetriveUserSportData()
   
    sdf = RetriveSportData()
    
    le = LabelEncoder()

    udf['Gender'] = le.fit_transform(udf['Gender'])
    for ind in sdf.index:
        DivCounter = 0
        Age = 0
        Gender = 0
        AvAge = 0
        sportID = ((sdf['Sport_ID'][ind]))
        CurrentSportDF = usdf.loc[usdf['Sport_ID'] == sportID]
        for ind2 in CurrentSportDF.index:
            CurrentUser = ((CurrentSportDF['USER_ID'][ind2]))
            Age += udf.loc[udf['USER_ID'] == CurrentUser , 'Age'].iloc[0]
            Gender += udf.loc[udf['USER_ID'] == CurrentUser , 'Gender'].iloc[0]
            DivCounter +=1
        if DivCounter > 0:    
            AvAge = Age/DivCounter
            AvGender = Gender/DivCounter
        sdf.at[ind, 'Av_Age'] = AvAge
        sdf.at[ind, 'Av_Gender'] = AvGender
    UpdateSportsData(sdf)

#Retrive the sports of specific users
def GetUserSports(UserToTest, Users):
    df = RetriveUserSportData()
    SportIDs = []
    ExcludeSports = []
    for ind in df.index:
        User_ID2 = (df['USER_ID'][ind])
        SportID = (df['Sport_ID'][ind])
        if UserToTest == User_ID2:
            ExcludeSports.append(SportID)
    for user in Users:
        for ind in df.index:
            User_ID = (df['USER_ID'][ind])
            SportID = (df['Sport_ID'][ind])
            if int(User_ID) == int(user) and SportID not in ExcludeSports and SportID not in SportIDs:
                SportIDs.append(SportID)
    SportsList = GetSportFromID(SportIDs)
    return SportsList

#Get the sport name from the sport ID
def GetSportFromID(SportIdList):
    sdf = RetriveSportData()
    SportList = []
    for ID in SportIdList:
        SportList.append(sdf.loc[sdf['Sport_ID'] == ID , 'Sport'].iloc[0])
    return SportList

#Functions to extract tables from SQL Database
def RetriveSportData():
    sql_query = pd.read_sql_query ('''
                               SELECT * 
                               FROM Sports
                               ''', Active)
    df = pd.DataFrame(sql_query, columns = ['Sport_ID', 'Sport', 'Category', 'Type', 'Av_Age', 'Av_Gender'])
    return(df)

def RetriveUserData():
    sql_query = pd.read_sql_query ('''
                               SELECT * 
                               FROM Users
                               ''', Active)
    df = pd.DataFrame(sql_query, columns = ['USER_ID', 'Gender', 'Age' ,'Postcode', 'Sport Type'])
    return(df)

def RetriveUserSportData():
    sql_query = pd.read_sql_query ('''
                               SELECT * 
                               FROM UserSport
                               ''', Active)
    df = pd.DataFrame(sql_query, columns = ['USER_ID', 'Sport_ID'])
    return(df)

def RetriveRatingData():
    sql_query = pd.read_sql_query ('''
                               SELECT * 
                               FROM Ratings
                               ''', Active)
    df = pd.DataFrame(sql_query, columns = ['USER_ID', 'Sport', 'Rating'])
    return(df)

#Functions to return table to SQL Database
def UpdateUserSport(df):
    df.to_sql('UserSport', Active, if_exists='replace', index = True)
    Active.commit()

def UpdateSportsData(df):
    df.to_sql('Sports', Active, if_exists='replace', index = False)
    Active.commit()

def UpdateUserTable(df):
    df.to_sql('Users', Active, if_exists='replace', index = False)
    Active.commit()

def UpdateRatingsTable(df):
    df.to_sql('Ratings', Active, if_exists='replace', index = False)
    Active.commit()


        