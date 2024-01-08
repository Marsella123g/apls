from kivy.lang import Builder
from kivy.uix.screenmanager import Screen


Builder.load_string("""
<home>:
    name:"Home"
    MDTopAppBar:
        title: "FISIKA NUKLIR IRL BATAN YOGYAKARTA"
        elevation: 4
        pos_hint: {"top": 1}
        md_bg_color: "#9BCDD2"
        specific_text_color: "#4a4939"
        font_name: "Comic"
        right_action_items: [["alpha-x-box", lambda x: setattr(root.manager, 'current', 'login')]]
    MDGridLayout:
        size_hint_y:.75
        cols:2
        padding:[dp(15),dp(15),dp(15),dp(35)]
        spacing:dp(15)
        ElementCard:
            on_press: root.switchToMenu1()
            Image:
                source:"radioactive.png"
                pos_hint:{"center_x":.5,"center_y":.5}
            MDLabel:
                text: "KALIBRASI DAYA REAKTOR"
                font_size:20
                halign:'center'
                bold:True
            
                
        ElementCard:
            on_press: root.switchToMenu2()
            Image:
                source:"radioactive-circle.png"
                pos_hint:{"center_x":.5,"center_y":.5}
            MDLabel:
                text: "REAKTIVITAS BATANG KENDALI"
                font_size:20
                halign:'center'
                bold:True
        
        ElementCard:
            on_press: root.switchToMenu3()
            Image:
                source:"radioactive-circle-outline.png"
                pos_hint:{"center_x":.5,"center_y":.5}
            MDLabel:
                text: "KOEFISIEN SUHU BAHAN BAKAR"
                font_size:20
                halign:'center'
                bold:True
        
        ElementCard:
            on_press: root.switchToMenu0()
            Image:
                source:"home-account.png"
                pos_hint:{"center_x":.5,"center_y":.5}
            MDLabel:
                text: "INFORMASI APLIKASI ANALISIS"
                font_size:20
                halign:'center'
                bold:True
            
        
<ElementCard@MDCard>:
    md_bg_color:25/255,108/255,241/255,.65
    padding:dp(15)
    spacing:dp(15)
    radius:dp(25)
    ripple_behavior: True
    orientation:'vertical'


""")
class Home(Screen):
    def switchToMenu1(self):
        self.manager.current="menu1"
    def switchToMenu2(self):
        self.manager.current="menu2"
    def switchToMenu3(self):
        self.manager.current="menu3" 
    def switchToMenu0(self):
        self.manager.current="menu0"