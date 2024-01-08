from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from mydatabase import Database

Builder.load_string("""
#: import CTextInput custom_widgets
<Signup>:
    name:"signup"

    BoxLayout:
        orientation:"vertical"
        padding: dp(40)
        BoxLayout:
            size_hint:1,0.4
            Image:
                source:"LOGO1.png"
        
        AnchorLayout:
            size_hint: 1,0.6
            anchor_y:"top"
        
            BoxLayout:
                orientation:"vertical"
                size_hint_y:None
                spacing: dp(10)
                height: self.minimum_height
                Label:
                    text: "Create your  Account"
                    color: 0,0,0,1
                    halign: "left"
                    text_size: self.size
                    
                CTextInput:
                    id: email
                    size_hint_y:None
                    height: dp(50)
                    hint_text:"Email"
                CTextInput:
                    id: password
                    size_hint_y:None
                    height: dp(50)
                    hint_text:"Password"
                CTextInput:
                    id: cpassword
                    size_hint_y:None
                    height: dp(50)
                    hint_text:"Confirm Password"
                CButton:
                    text:"Signup"
                    on_press: root.createEntry()
                    size_hint_y:None
                    height: dp(50)
                
            

""")

class Signup(Screen):
    def createEntry(self):
        email=self.ids.email.text
        password=self.ids.password.text
        cpassword=self.ids.cpassword.text
        if(password==cpassword):
            if(Database.isValid(email)):
                Database.insertdata(email,password)
                self.manager.current="login"
                
            else:
                print("Email exists")