import DataManager as dm
import Reccomender as rec
import pandas as pd
from tkinter import *

def Main():
    ValidLogin = False
    #Login
    while not ValidLogin:
        print("Please Enter Email")
        Email = input()
        print("please Enter Password")
        Password = input()
        ValidLogin, User_ID = dm.UserLoginCheck(Email, Password)

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
    SimpleContentBasedUser =rec.SimpleContentBasedUser(User_ID)
    UserSports =dm.GetUserSports(User_ID ,SimpleContentBasedUser)
    
    #Collaberative reccomendation based on user sport ratings
    ResultsDf = rec.CollaberativePartOne(User_ID)

    #Outputs
    print('Sport Tested For', Sports)
    print('User Tested For', User_ID)
    print("Collaberative: " , (ResultsDf['Sport'][0]) , (ResultsDf['Sport'][1]) , (ResultsDf['Sport'][2]) )
    print("User Content-Based: " , UserSports , SimpleContentBasedUser)
    print("Sport Content-Based: " , ContentSports)

Main()
