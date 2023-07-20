import DataManager as dm
import Reccomender as rec
import pandas as pd
from tkinter import *



def Main():
    dm.UpdateAverages()
    Sports = ['Road Cycling']
    User_ID = 1
    ContentSports = []

  
    for Sport in Sports:
        SimpleContentBasedSport = rec.SimpleContentBasedSport(Sport)
        for sport2 in SimpleContentBasedSport:
            ContentSports.append(sport2)

    SimpleContentBasedUser =rec.SimpleContentBasedUser(User_ID)
    UserSports =dm.GetUserSports(User_ID ,SimpleContentBasedUser)
    ResultsDf = rec.CollaberativePartOne(User_ID)
    print('Sport Tested For', Sports)
    print('User Tested For', User_ID)
    print("Collaberative: " , (ResultsDf['Sport'][0]) , (ResultsDf['Sport'][1]) , (ResultsDf['Sport'][2]) )
    print("User Content-Based: " , UserSports , SimpleContentBasedUser)
    print("Sport Content-Based: " , ContentSports)

Main()
