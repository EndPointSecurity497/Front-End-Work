import os
class Settings:
    def __init__(self):
        self.name = ''
        self.password = ''
        self.timerun = ''
        self.manvauto = ''
        #ask for host name
        #don't ask if they have uswername or password

    def insertName(self, Thename, Thepassword):
        self.name = Thename
        self.password = Thepassword

    def inserttimeRun(self, Thetimerun):
        self.timerun = Thetimerun

    def insertmanvauto(self, choice):
        self.manvauto = choice
    def checkfile(self):
        file1 = open(r"C:\Users\zombi\Desktop\psutil\Settings.txt", "r+")  # *READ* change file path as neeeded
        print(file1.read())

    def export(self):
        file1 = open(r"C:\Users\zombi\Desktop\psutil\Settings.txt", "w+")  # *READ* change file path as neeeded
        park = self.name + "\n" + self.password + "\n" + self.timerun + "\n" + self.manvauto

        if not park.strip(): #Default Variables if no user input found if ALL inputs left blanked
            park = "Guest" + "\n" + "Password" + "\n" + "2" + "\n" + "Automatic"
            file1.write(park)
            file1.close()
            print("Default Value")
        else:
            file1.write(park)
            file1.close()




def __main__():
    path='C:\\Users\\zombi\\Desktop\\psutil\\Settings.txt'
    if os.stat(path).st_size == 0:
        print('There was no Settings file found')
        MySettings = Settings()
        print("Configure your settings")
        user_input1 = input("Do you have a user account?")
        if user_input1 == 'yes' or (user_input1 == 'y'):
            pass
        elif (user_input1 == 'no') or (user_input1 == 'n'):
            user_input2 = input("choose a username ")
            user_input3 = input("choose a password ")
            MySettings.insertName(user_input2, user_input3)

        user_input4 = input("How often would you like the program to run (seconds): ")
        MySettings.inserttimeRun(user_input4)

        user_input5 = input("Would you like to run the program manual or automatic: ")
        MySettings.insertmanvauto(user_input5)
        MySettings.export()

    else:
        print('There was a settings file found.')
        MySettings = Settings()
        print("Configure your settings")

        lines = []
        with open('C:\\Users\\zombi\\Desktop\\psutil\\Settings.txt') as f:
            lines = f.readlines()

        count = 0

        a_file = open('C:\\Users\\zombi\\Desktop\\psutil\\Settings.txt')
        lines_to_readUser = [0]
        lines_to_readPass = [1]
        lines_to_readSecs = [2]
        lines_to_readAuMa = [3]

        for position, line in enumerate(a_file):
            if position in lines_to_readUser:
                user_input2 = line
            if position in lines_to_readPass:
                user_input3 = line
            if position in lines_to_readSecs:
                user_input4 = line
            if position in lines_to_readAuMa:
                user_input5 = line


        MySettings.inserttimeRun(user_input4)
        MySettings.insertmanvauto(user_input5)
        MySettings.export()

__main__()






