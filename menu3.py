from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from styles import Styles
from plyer import filechooser


import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from datetime import datetime




Builder.load_string("""
<menu3>:
    name:"menu3"
    BoxLayout:
        orientation:"vertical"
        MDTopAppBar:
            title: "KOEFISIEN SUHU BAHAN BAKAR"
            elevation: 4
            pos_hint: {"top": 1}
            md_bg_color: "#9BCDD2"
            specific_text_color: "#4a4939"
            font_name: "Comic"
            right_action_items: [["alpha-x-box", lambda x: setattr(root.manager, 'current', 'Home')]]

        ScrollView:
            do_scroll_y: True
        
            
            MDGridLayout:
                size_hint_y:.85
                cols:1
                padding:[dp(15),dp(15),dp(15),dp(35)]
                spacing:dp(15)
                
                MDRaisedButton:
                    text: "Upload"
                    pos_hint: {"center_y":.6, "center_x":.4}
                    md_bg_color:"#1D2B53"
                    on_release:
                        root.file_chooser()
                MDCard:
                    md_bg_color:"#7071E8"
                    padding:dp(15)
                    spacing:dp(15)
                    radius:dp(15)
                    ripple_behavior: True
                    orientation:'horizontal'
                    size_hint_y:.3
                    
                    MDLabel:
                        id:selected_path
                        text: ""
                        halign:'center'
                        bold:True
                        
                        
                MDRaisedButton:
                    text: "Hasil"
                    pos_hint: {"center_y":.6, "center_x":.6}
                    md_bg_color:"#1D2B53"
                    on_press:
                        root.nilaikoefisiensuhu(selected_path.text)
                    
                
                TextInput:
                    id:file_path_output
                    text: ""
                    font_size:15
                    text_size: self.width, None
                    halign:'left'
                    bold:True
                    
""")


class Menu3(Screen):
    bg_color=Styles.primary_color 
    
    def file_chooser(self):
        # filechooser.open_file(on_selection=self.selected)
        file_path = filechooser.open_file(title="Select a CSV file", filters=[("CSV Files", "*.csv")])
        if file_path:
            self.ids.selected_path.text=file_path[0]
        
    
    def nilaikoefisiensuhu (self, file_path):
        
        df= pd.read_csv(file_path)
        # df= pd.read_csv('practice1_10_11_2023.csv')
        bc=df.loc[:,['Time','Power NP1000','Safety rod','Compensation rod','Regulator rod','primary flow','IFE temp']]
        df = pd.DataFrame(bc)

        # ======KONDISI1======
        index_prim_zero = df[df['primary flow'] == 0].index[0]

        # Extract the 5 rows before primary flow = 0
        hasil_df = df.iloc[max(0, index_prim_zero - 15):index_prim_zero]
        data_reg = hasil_df['Regulator rod']
        hasil_reg = hasil_df['Regulator rod'].mean()
        data_prim = hasil_df['IFE temp']
        hasil_prim = hasil_df['IFE temp'].mean()

        # print(hasil_df)
        # # print(data_reg)
        # print('Rata-Rata Posisi Batang Kendali Kondisi 1:',hasil_reg) #Nilai rata-rata batang kendali pengatur KONDISI1
        # # print(data_prim)
        # print('Rata-Rata IFE temp Kondisi 1: ',hasil_prim) #Nilai rata-rata IFE temp KONDISI1

        # ======PERHITUNGAN======
        x1=hasil_reg
        y1 = -0.0002 * x1**3 + 0.0181 * x1**2 + 1.8314 * x1 - 2.4464

        # print('Reaktivitas Batang Kendali Pengatur Kondisi 1: ',y1)

        # ======KONDISI2======
        setelah_daya= df[(df['primary flow'] == 0) & (df['Safety rod'] == 100) & (df['Power NP1000'] >= 100)]

        # Find the index of the first matching row
        if not setelah_daya.empty:
            start_index = setelah_daya.index[0]

            # Retrieve the next 10 rows after the matching row
            hasil_2 = df.iloc[start_index + 51: start_index + 61]
            # print(hasil_2)
            data_reg2 = hasil_2['Regulator rod']
            hasil_reg2 = hasil_2['Regulator rod'].mean() 
            data_prim2 = hasil_2['IFE temp']
            hasil_prim2 = hasil_2['IFE temp'].mean()
            # Display the result
            # print(data_reg2)
            # print('Rata-Rata Posisi Batang Kendali Kondisi 2:',hasil_reg2) #Nilai rata-rata batang kendali pengatur KONDISI2
            # print(data_prim2)
            # print('Rata-Rata IFE temp Kondisi 2: ',hasil_prim2) #Nilai rata-rata IFE temp KONDISI2

            # ======PERHITUNGAN======
            x=hasil_reg2
            Y = -0.0002 * x**3 + 0.0181 * x**2 + 1.8314 * x - 2.4464

            # print('Reaktivitas Batang Kendali Pengatur Kondisi 2: ',Y)
            
        else:
            print("No matching rows.")
            
        # ======PERHITUNGAN KOEFISIEN REAKTIVITAS SUHU BAHAN BAKAR======
        R=abs(Y-y1)
        R1 = str(R)
        T=(hasil_prim2-hasil_prim)
        T1=str(T)
        K=R/T
        
        print("Nilai Koefisien Negatif Temperatur: ",K)
        
        results =f"Reaktivitas Kondisi 1={y1}\nReaktivitas Kondisi 2={Y}\nRata-Rata IFE temp Kondisi 1={hasil_prim}\nRata-Rata IFE temp Kondisi 2={hasil_prim2}\nSelisih Reaktivitas= {R1}\nSelisih Temperatur= {T1}\nNilai Koefisien Negatif Temperatur= {K}"

        self.hasil_csv(results)
        return results
            
    def hasil_csv(self,results):
        self.ids.file_path_output.text = results
        
    
        