from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

from login import Login
from signup import Signup
from home import Home
from menu1 import Menu1
from menu2 import Menu2
from menu3 import Menu3
from menu0 import Menu0
from kivy.lang import Builder

from mydatabase import Database

Window.size=(480,600)
# Window.softinput_mode ="below_target"

KV="""
Interface:
    canvas.before:
        Color:
            rgba:1,1,1,1
        Rectangle:
            pos: self.pos
            size: self.size"""

class Interface(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            Database.connectDatabase()
        except Exception as e:
            print(e)
        login=Login()
        signup=Signup()
        home=Home()
        menu1=Menu1()
        menu2=Menu2()
        menu3=Menu3()
        menu0=Menu0()
        self.add_widget(login)
        self.add_widget(signup)
        self.add_widget(home)
        self.add_widget(menu1)
        self.add_widget(menu2)
        self.add_widget(menu3)
        self.add_widget(menu0)
class KalibrasiApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

KalibrasiApp().run()