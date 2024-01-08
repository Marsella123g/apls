from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from styles import Styles

Builder.load_string("""
#: import CTextInput custom_widgets                    
<menu0>:
    name:"menu0"
    MDTopAppBar:
        title: "INFORMASI"
        elevation: 4
        pos_hint: {"top": 1}
        md_bg_color: "#9BCDD2"
        specific_text_color: "#4a4939"
        font_name: "Comic"
        right_action_items: [["alpha-x-box", lambda x: setattr(root.manager, 'current', 'login')]]
        
    BoxLayout:
        orientation: "vertical"
        padding: dp(20)
        Image:
            source: "LOGO1.png"
        Label:
            text: "Dibuat Oleh:"
            font_size:'26sp'
            halign:"center"
            text_size: self.size
            size_hint_y:None
            size:self.texture_size
            color:0,0,0,1
        Label:
            text: "MARSELLA ANGELINA"
            font_size:'30sp'
            halign:"center"
            text_size: self.size
            font_name:"04B_19__.ttf"
            size_hint_y:None
            size:self.texture_size
            color:0,0,0,1
        
    
    


""")
class Menu0(Screen):
    bg_color=Styles.primary_color 