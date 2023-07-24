import DataManager as dm
import Reccomender as rec
import pandas as pd
from tkinter import *

def Main():
    ValidLogin = False
    ValidEntry = False
    ExistingAccount = ''
    Running = True
    while Running:
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

        print("What would you like to do today")
        MenuChoice = input("Please Choose one, 1.Get Reccomendations 2.Enter Sports you have Tried 3.Exit")
        if MenuChoice == '1':
            #Content Based reccomendation for the specif user based on similar users
            SimpleContentBasedUser =rec.SimpleContentBasedUser(int(User_ID))
            UserSports =dm.GetUserSports(int(User_ID) ,SimpleContentBasedUser)

  
            Sports = dm.GetUserSports(0 , User_ID)

            #Content Based reccomendation for sports
            #Loops through muliple sport inputs from the user
            ContentSports = []
            for Sport in Sports:
                SimpleContentBasedSport = rec.SimpleContentBasedSport(Sport)
                for sport2 in SimpleContentBasedSport:
                    ContentSports.append(sport2)
    
            #Collaberative reccomendation based on user sport ratings
            CollResults = rec.CollaberativePartOne(int(User_ID))
            CollSports = dm.GetSportFromID(CollResults)

            #Outputs
            print('Sport Tested For', Sports)
            print('User Tested For', User_ID)
            print("Collaberative: " , CollSports)
            print("User Content-Based: " , UserSports)
            print("Sport Content-Based: " , ContentSports)
        elif MenuChoice == '2':
            print("Please choose sports from the list below")
            df = dm.RetriveSportData()
            for ind in df.index:
                print((df['Sport_ID'][ind]),". " , (df['Sport'][ind]))
            UserSportsEntry = []
            SportEntry = -1
            while SportEntry != 0:
                try:
                    SportEntry = int(input('Please enter a number each time, when you have entered all sports please enter 0'))
                    if int(SportEntry) > 0 and int(SportEntry) < 39 and SportEntry not in UserSportsEntry:
                        UserSportsEntry.append(SportEntry)
                    elif int(SportEntry) != 0:
                        print("Please enter a valid or non repeated value")
                except:
                    print("Please enter a valid value")
            if UserSportsEntry is not None:
                dm.AddSports(UserSportsEntry , User_ID)
        

        elif MenuChoice == '3':
            print('Goodbye, have a good day')
            User_ID = 0
            Running =  False
        else:
            print("Please enter a valid choice")

Main()
