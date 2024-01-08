from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from mydatabase import Database

Builder.load_string("""
#: import CButton custom_widgets                    
#: import CTextInput custom_widgets                    
#: import SignupText custom_widgets                    
<Login>:
    name:"login"
    BoxLayout:
        orientation: "vertical"
        padding: dp(20)
        BoxLayout:
            size_hint:1,0.35
            Image:
                source: "LOGO1.png"
        AnchorLayout:
            size_hint:1,0.55
            anchor_y:"top"

            BoxLayout:
                orientation: "vertical"
                size_hint_y:None
                height: self.minimum_height
                spacing: dp(10)
                padding: [dp(30),0, dp(30),0]
                Label:
                    text: "Login to your Account"
                    font_size:'16sp'
                    halign:"left"
                    text_size: self.size
                    size_hint_y:None
                    size:self.texture_size
                    color:0,0,0,1
                CTextInput:
                    id: email
                    size_hint_y:None
                    height: dp(50)
                    multiline: False
                    hint_text:"Email"
                CTextInput:
                    id: password
                    size_hint_y:None
                    height: dp(50)
                    multiline: False
                    hint_text:"Password"
                CButton:
                    text:"Login"
                    size_hint_y:None
                    height:dp(50)
                    on_press: root.login()
        AnchorLayout:    
            size_hint:1,0.1
            anchor_x:"center"
            BoxLayout:
                size_hint_x:None
                width: self.minimum_width
                Label:
                    text:"Dont have an account ?"
                    color:0,0,0,1
                    size_hint_x: None
                    size: self.texture_size
                SignupText:
                    text:"Signup"
                    size_hint_x: None
                    size: self.texture_size
                    on_press: root.switchToSignup()


""")

class Login(Screen):
    def login(self):
        email=self.ids.email.text
        password=self.ids.password.text
        if(Database.isExist(email,password)):
            print("Login Succes")
            self.manager.current="Home"
        else:
            print("Login Fail")
    def switchToSignup(self):
        self.manager.current="signup"