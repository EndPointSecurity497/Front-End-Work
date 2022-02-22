#import psutil


class Settings:
    def __init__(self):
        self.name = []
        self.password = []
        self.timerun = []
        self.manvauto = []

    def insertName(self, Thename, Thepassword):
        self.name = Thename
        self.password = Thepassword

    def inserttimeRun(self, Thetimerun):
        self.timerun = Thetimerun

    def inserttimeRun(self, choice):
        self.manvauto = choice

    def export(self):
        file1 = open(r"C:\Users\zombi\Desktop\psutil\Settings.txt", "w+")  # change path as neeeded
        # park = str(self.name+self.password+self.timerun+self.manvauto)
        park = self.name + "\n" + self.password + "\n" + str(self.timerun) + "\n" + self.manvauto
        file1.write(park)

'''
Code being worked on for creating default variables (not working yet)
        if (len(park)):
            print(self.manvauto)
            file1.write(park)
        else:
            #park = "Guest" + "\n" + "Password" + "\n" + "2" + "\n" + "Automatic"
            file1.write(park)
            print("The string is empty")

'''

def __main__():
    MySettings = Settings()
    print("Configure your settings")
    user_input1 = input("Do you have a user account?")
    if user_input1 == 'yes':
        pass
    elif user_input1=='no':
        user_input2 = input("choose a username ")
        user_input3 = input("choose a password ")
        MySettings.insertName(user_input2, user_input3)

    user_input4 = input("How often would you like the program to run (seconds): ")
    MySettings.inserttimeRun(user_input4)
    auto = 0
    while (auto == 0):
        user_input5 = input("Would you like to run the program manual or automatic: ")
        if user_input5 == "manual" or user_input5 == "automatic":
            MySettings.inserttimeRun(user_input5)
            auto = 1
        else:
            print("Invalid input, Try again")


    MySettings.export()
__main__()







