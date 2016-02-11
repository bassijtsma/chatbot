'''
In order to start the run.py, you must:
1. Rename this file to credentials.py
2. Define your login and password on line 10 and 11.

To get your login and password, please read the yowsup instructions at:
https://github.com/tgalal/yowsup/wiki/yowsup-cli-2.0
'''
class Credentials:
    login = "" # Add your cell number with country code here
    password = "" # Add your password here


    def __init__(self):
        if self.login == "" or self.password = "":
            print """\nYou have probably forgotten to set your username and
            password. Define these in the credentials.py file and restart the
            script \n\n"""
        return

    def getpassword(self):
        return Credentials.password

    def getlogin(self):
        return Credentials.login
