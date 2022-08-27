import UserInterface
import os

def startProgram():
    choiceStart = input("Warning - shutting down all web browsers, Y/N")
    if choiceStart == 'Y':
        os.system("taskkill /im msedge.exe /f")
        UserInterface.start()

startProgram()

