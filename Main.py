import DataManager as dm
import Reccomender as rec
import pandas as pd
from tkinter import *

def Main():
    ValidLogin = False
    ValidEntry = False
    ExistingAccount = ''
    #Login
    while not ValidLogin:
        while ExistingAccount.lower() != 'yes' and ExistingAccount.lower() != 'no':
            ExistingAccount = input("Welcome, Do you have an exisitng account 'Yes' or 'No'")

        if ExistingAccount == 'yes':
            print('Welcome Back, Please enter your login credentials')
            Email = input("Please Enter Email")
            Password =input("please Enter Password")
            ValidLogin, User_ID = dm.UserLoginCheck(Email, Password)
        else:
            while not ValidEntry:
                print('Welcome, Please fill in the information boxes')
                Email = input("Please Enter Email")
                Password =input("please Enter Password")
                ValidEntry = dm.AddUser(Email, Password)
            ValidLogin, User_ID = dm.UserLoginCheck(Email, Password)
            Gender = input("Please enter your gender")
            Age = input("Please enter your Age")
            Postcode = input("Please enter the first half of your Postcode without numbers")  
            Sport_Type = input("Please enter 'Team Sports' or 'Individual Sports' ")            
            DataToEnter = {'USER_ID': int(User_ID) , 'Gender': str(Gender),'Age': int(Age), 'Postcode': str(Postcode), 'Sport Type': str(Sport_Type)}
            dm.AddUserInfo(DataToEnter)



    #Data Initialisation
    dm.UpdateAverages()
    Sports = ['Road Cycling']

    #Content Based reccomendation for sports
    #Loops through multiple sport inputs from the user
    ContentSports = []
    for Sport in Sports:
        SimpleContentBasedSport = rec.SimpleContentBasedSport(Sport)
        for sport2 in SimpleContentBasedSport:
            ContentSports.append(sport2)

    #Content Based reccomendation for the specif user based on similar users
    SimpleContentBasedUser =rec.SimpleContentBasedUser(int(User_ID))
    UserSports =dm.GetUserSports(int(User_ID) ,SimpleContentBasedUser)
    
    #Collaberative reccomendation based on user sport ratings
    ResultsDf = rec.CollaberativePartOne(int(User_ID))

    #Outputs
    print('Sport Tested For', Sports)
    print('User Tested For', User_ID)
    print("Collaberative: " , (ResultsDf['Sport'][0]) , (ResultsDf['Sport'][1]) , (ResultsDf['Sport'][2]) )
    print("User Content-Based: " , UserSports , SimpleContentBasedUser)
    print("Sport Content-Based: " , ContentSports)

Main()
