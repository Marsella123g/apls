from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from styles import Styles
from plyer import filechooser

import matplotlib.pyplot as plt
import pandas as pd
import datetime
from datetime import datetime




Builder.load_string("""
<menu2>:
    name:"menu2"
    BoxLayout:
        orientation:"vertical"
        MDTopAppBar:
            title: "REAKTIVITAS BATANG KENDALI"
            elevation: 4
            pos_hint: {"top": 1}
            md_bg_color: "#9BCDD2"
            specific_text_color: "#4a4939"
            font_name: "Comic"
            right_action_items: [["alpha-x-box", lambda x: setattr(root.manager, 'current', 'Home')]]

        # ScrollView:
        #     do_scroll_y: True
        MDGridLayout:
            size_hint_y:.95
            cols:1
            padding:[dp(15),dp(15),dp(15),dp(35)]
            spacing:dp(15)
            height:self.minimum_height
            width:self.minimum_width
            
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
                height:"210dp"
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
                    root.kalibrasi_batangkendali(selected_path.text)
            
            TextInput:
                id:file_path_output
                text: ""
                font_size:15
                width: 5
                halign:'left'
                bold:True
            
            MDRaisedButton:
                text: "Grafik"
                md_bg_color:"#1D2B53"
                pos_hint: {"center_y":.5, "center_x":.6}
                on_release:
                    root.display_plot2()
                    root.display_plot3()
                    root.display_plot4()
            
            
                    
""")


class Menu2(Screen):
    
    def file_chooser(self):
        # filechooser.open_file(on_selection=self.selected)
        file_path = filechooser.open_file(title="Select a CSV file", filters=[("CSV Files", "*.csv")])
        if file_path:
            self.ids.selected_path.text=file_path[0]
        
    
    def kalibrasi_batangkendali (self, file_path):
        df= pd.read_csv(file_path)
        # df= pd.read_csv('CR Calibration 14 april231.csv')

        # setelah diurutkan
        ac=df.loc[::-1].reset_index(drop=True)
        # pemilihan kolom
        bc=ac.loc[:,['htime','safe','shim','reg','reactivity']]
        df = pd.DataFrame(bc)

        # Inisialisasi list untuk menyimpan baris yang memenuhi kriteria
        stabil_pengatur = []
        stabil_kompensasi = []
        stabil_pengaman = []
        parts = []
        current_part = []

        # =============BATANG KENDALI PENGATUR===================

        # ========KONDISI 1 (KRITIS)==============
        for index, row in df.iterrows():
            if row['safe'] == 100:
                if row['shim'] == 100:
                    if -0.3 < row['reactivity'] < 0:
                        if 10 < row['reg'] <16:
                            stabil_pengatur.append(row)
                            
        selected1_df = pd.DataFrame(stabil_pengatur)
        hasil1 = selected1_df['reg'].mode().iloc[0]


        # ========KONDISI 2 (REAKTIVITAS)==============
        filtered_data = df[df['reactivity'] > 15]
        threshold = 16
        continue_adding = True

        for index, row in df.iterrows():
            if continue_adding and row['safe'] == 100 and row['reactivity'] > threshold and row['reg'] <= 100:
                current_part.append(row)
            elif current_part:
                if row['reg'] == 100:
                    current_part.append(row)
                    parts.append(pd.DataFrame(current_part))
                    current_part = []
                    continue_adding = False
                else:
                    parts.append(pd.DataFrame(current_part))
                    current_part = []

        for i, part in enumerate(parts):
            max_rec = part['reactivity'].max()

        result_df = pd.DataFrame(columns=['reg', 'reactivity'])
        result_df = pd.concat([part.loc[part['reactivity'].idxmax(), ['reg', 'reactivity']].to_frame().T for part in parts], ignore_index=True)

        # ========KONDISI 3 (CORE EXCESS)==============
        for index, row in df.iterrows():
            if row['safe'] == 100:
                if row['shim'] == 100:
                    if -30< row['reactivity'] < -12:
                        if 0<= row['reg'] <=hasil1:
                            stabil_pengatur.append(row)
                            
        selectedd1_df = pd.DataFrame(stabil_pengatur)
        hasill1 = selectedd1_df['reactivity']*(-1)
        rect=hasill1.max()

        # ======== TABEL DATA==============
        baris_baru = pd.DataFrame({'reg': [0,hasil1], 'reactivity': [0,rect]})
        result_df = pd.concat([baris_baru, result_df], ignore_index=True)
        result_df = result_df.rename(columns={'reg': 'posisi', 'reactivity':'reaktivitas'})

        c1=result_df['reaktivitas']
        c_list1 = result_df['reaktivitas'].tolist()

        # ========PERHITUNGAN INTEGRAL==============
        d_values = [0]

        for i in range(1, len(c_list1)):
            d_values.append(d_values[i-1] + c_list1[i])

        for i, d in enumerate(d_values):
            as1=d
            # print(d)

        result_df['Integral'] =d_values
        result_df = result_df.reset_index(drop=True)
        result2= str(result_df)
        # self.show_results2_popup(result2)
        self.create_and_save_plot2(result_df, d_values)
        # print(result_df)

        # ========PENGOLAHAN DATA==============
        total_pengatur=result_df['reaktivitas'].sum()
        core_pengatur=total_pengatur-rect

        # =========BATANG KENDALI KOMPENSASI===========

        # ========KONDISI 1==============
        for index, row in df.iterrows():
            if row['safe'] == 100:
                if row['reg'] == 100:
                    if 0< row['reactivity'] < 0.5:
                        stabil_kompensasi.append(row)

        selected2_df = pd.DataFrame(stabil_kompensasi)
        hasil2 = selected2_df['shim'].mode().iloc[0]

        # ========KONDISI 2==============
        filtered_data = df[df['reactivity'] >= 3]
        # Create an empty list to store the parts
        parts = []
        # Set a threshold for the 'rec' values to split the data into parts
        threshold = 3
        # Initialize variables for the loop
        current_part = []
        result_data = []
        # Iterate through the data
        continue_adding = True 
        # Iterate through the data
        for index, row in df.loc[selected2_df.index[0]:].iterrows():
            if continue_adding and row['safe'] == 100 and row['reactivity'] >= threshold and row['shim'] <= 100:
                current_part.append(row)
            elif current_part:
                # Stop adding rows once 'reg' reaches 100
                if row['shim'] == 100:
                    current_part.append(row)
                    parts.append(pd.DataFrame(current_part))
                    current_part = []
                    continue_adding = False
                else:
                    parts.append(pd.DataFrame(current_part))
                    current_part = []

        for part in parts:
            if not part.empty :
                # Exclude the rows where 'shim' is 100 for Bagian 10 and Bagian 11
                if part['shim'].iloc[0] < 100 and part['reg'].iloc[-1] < 100:
                    max_row = part.loc[part['reactivity'].idxmax(), ['shim', 'reactivity']]
                    result_data.append(max_row.to_dict())

        # Create the resulting DataFrame
        result_df = pd.DataFrame(result_data)

        # Print the resulting DataFrame
        # print(result_df)

        # ========KONDISI 3==============
        for index, row in df.iterrows():
            # Check apakah Nilai1 sama dengan 100
            if 95<= row['safe'] <= 100:
                # Jika ya, check kriteria Nilai4
                if row['reg'] == 100:
                    if -3< row['reactivity'] < -0.05:
                        if 0<= row['shim'] <=hasil2:
                            # Jika memenuhi kriteria, tambahkan baris ke list selected_rows
                            stabil_kompensasi.append(row)
                            

        # Buat DataFrame baru dari baris yang memenuhi kriteria
        selectedd2_df = pd.DataFrame(stabil_kompensasi)
        hasill2 = selectedd2_df['reactivity']*(-100)
        rect2=hasill2.max()


        # ======== TABEL DATA==============
        baris_baru = pd.DataFrame({'shim': [0,hasil2], 'reactivity': [0,rect2]})
        result_df = pd.concat([baris_baru, result_df], ignore_index=True)
        result_df = result_df.rename(columns={'shim': 'posisi', 'reactivity':'reaktivitas'})
        # print(result_df)

        c2=result_df['reaktivitas']
        # print(c1)
        c_list2 = result_df['reaktivitas'].tolist()
        # print(c_list1)

        # ========PERHITUNGAN INTEGRAL==============
        d_values2 = [0]

        # Calculate d values using a loop
        for i in range(1, len(c_list2)):
            d_values2.append(d_values2[i-1] + c_list2[i])

        # Print the results
        for i, d in enumerate(d_values2):
            as1=d
            # print(d)

        result_df['Integral'] =d_values2
        result_df = result_df.reset_index(drop=True)
        # print(result_df)
        result3= str(result_df)
        # self.show_results3_popup(result3)
        self.create_and_save_plot3(result_df, d_values2)
        

        # ========PENGOLAHAN DATA==============
        total_kompensasi=result_df['reaktivitas'].sum()
        core_kompensasi=total_kompensasi-rect2
        
        # # =========BATANG KENDALI PENGAMAN===========

        # ========KONDISI 1==============
        for index, row in df.iterrows():
            # Check apakah Nilai1 sama dengan 100
            if row['shim'] == 100:
                # Jika ya, check kriteria Nilai4
                if row['reg'] == 100:
                    if 0< row['reactivity'] < 0.5:
                        # Jika memenuhi kriteria, tambahkan baris ke list selected_rows
                        stabil_pengaman.append(row)

        # Buat DataFrame baru dari baris yang memenuhi kriteria
        selected3_df = pd.DataFrame(stabil_pengaman)
        hasil3 = selected3_df['safe'].mode().iloc[0]

        # ========KONDISI 2==============
        filtered_data = df[df['reactivity'] >= 3]
        # Create an empty list to store the parts
        parts = []
        # Set a threshold for the 'rec' values to split the data into parts
        threshold = 3
        # Initialize variables for the loop
        current_part = []
        result_data = []
        # Iterate through the data
        continue_adding = True 
        # Iterate through the data
        for index, row in df.loc[selected3_df.index[0]:].iterrows():
            if continue_adding:
                if (row['reg'] == 100 and row['reactivity'] >= threshold and row['safe'] <= 100) or \
                (row['shim'] == 100 and row['reactivity'] >= threshold and row['safe'] <= 100):
                    current_part.append(row)
                elif current_part:
                    # Stop adding rows once 'reg' or 'shim' reaches 100
                    if row['safe'] == 100:
                        current_part.append(row)
                        parts.append(pd.DataFrame(current_part))
                        current_part = []
                        continue_adding = False
                    else:
                        parts.append(pd.DataFrame(current_part))
                        current_part = []

        for part in parts:
            if not part.empty and part['safe'].iloc[0] < 100:
                if (part['shim'].iloc[-1] < 100) or (part['reg'].iloc[-1] < 100):
                    max_row = part.loc[part['reactivity'].idxmax(), ['safe', 'reactivity']]
                    result_data.append(max_row.to_dict())

        # Create the resulting DataFrame
        result_df = pd.DataFrame(result_data)

        # ========KONDISI 3==============
        for index, row in df.iterrows():
            # Check apakah Nilai1 sama dengan 100
            if 95<= row['reg'] <= 100:
            # if 95<= row['shim'] <= 100:
                # Jika ya, check kriteria Nilai4
                if row['shim'] == 100:
                # if row['reg'] == 100:
                    if -2< row['reactivity'] < -0.02:
                        if 0<= row['safe'] <=hasil3 :
                            # Jika memenuhi kriteria, tambahkan baris ke list selected_rows
                            stabil_pengaman.append(row)
                            

        # Buat DataFrame baru dari baris yang memenuhi kriteria
        selectedd3_df = pd.DataFrame(stabil_pengaman)
        hasill3 = selectedd3_df['reactivity']*(-100)
        rect3=hasill3.max()
        
        # ======== TABEL DATA==============
        baris_baru = pd.DataFrame({'safe': [0,hasil3], 'reactivity': [0,rect3]})
        result_df = pd.concat([baris_baru, result_df], ignore_index=True)
        result_df = result_df.rename(columns={'safe': 'posisi', 'reactivity':'reaktivitas'})
        # print(result_df)

        c3=result_df['reaktivitas']
        # print(c1)
        c_list3 = result_df['reaktivitas'].tolist()
        # print(c_list1)

        # ========PERHITUNGAN INTEGRAL==============
        d_values3 = [0]

        # Calculate d values using a loop
        for i in range(1, len(c_list3)):
            d_values3.append(d_values3[i-1] + c_list3[i])

        # Print the results
        for i, d in enumerate(d_values3):
            as1=d
            # print(d)

        result_df['Integral'] =d_values3
        result_df = result_df.reset_index(drop=True)
        # print(result_df)
        result4= str(result_df)
        # self.show_results4_popup(result4)
        self.create_and_save_plot4(result_df, d_values3)
        
        gb4=result_df['posisi']

        # ========PENGOLAHAN DATA==============
        total_pengaman=result_df['reaktivitas'].sum()
        core_pengaman=total_pengaman-rect3

        # =========PENGOLAHAN REAKTIVITAS BATANG KENDALI=========
        total_reaktivitas=(total_pengatur+total_kompensasi+total_pengaman)
        persen_total=total_reaktivitas/100
        core_excess=((core_pengatur+core_kompensasi+core_pengaman)/3)
        persen_core = core_excess/100
        shutdown_margin=(total_reaktivitas-core_excess-total_kompensasi)
        persen_shutdown = shutdown_margin/100
        results =f"Reaktivitas Batang pengatur={total_pengatur} cent \nCore Excess pengatur={core_pengatur} cent\nReaktivitas Batang kompensasi={total_kompensasi} cent \nCore Excess kompensasi={core_kompensasi}\nReaktivitas Batang Pengaman={total_pengaman} cent\nCore Excess Pengaman={core_pengaman}\n\ntotal_reaktivitas = {total_reaktivitas} atau {persen_total}\ncore_excess= {core_excess} atau {persen_total}%\nshutdown_margin={shutdown_margin}cent atau {persen_shutdown}%"
        
    
        self.hasil_csv(results)
        return results
    
    def create_and_save_plot4(self,result_df, d_values3):
        self.fig, self.ax = plt.subplots()

        self.ax.plot(result_df['posisi'], d_values3, label='Some Label')  # Replace 'Some Label' with an appropriate label for your data
        self.ax.scatter(result_df['posisi'], d_values3)
        
        self.ax.set_xlabel('Posisi')
        self.ax.set_ylabel('Reaktivitas')
        self.ax.set_title('Grafik Integral Batang Kendali Pengaman')
        self.ax.legend()

        
    def display_plot4(self):
        
        plot_container = BoxLayout(orientation='vertical', padding=5)
        close_button = Button(text='Close', size_hint=(1, 0.1))
        save_button = Button(text='Save', size_hint=(1, 0.1))
        self.graph = FigureCanvasKivyAgg(figure=self.fig)
        self.fig.savefig('plot')
        plot_container.add_widget(self.graph)
        plot_container.add_widget(close_button)
        plot_container.add_widget(save_button)
        
        def save_plot(instance):
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"plot_{timestamp}.png"  # You can use a different file format if needed
            self.fig.savefig(filename)
            print(f"Plot saved as {filename}")
            popup.dismiss()

        popup = Popup(title='Plot', content=plot_container, size_hint=(1, 1))
        close_button.bind(on_release=popup.dismiss)
        save_button.bind(on_release=save_plot)
        popup.open()
    
    def create_and_save_plot3(self,result_df, d_values2):
        self.fig1, self.ax = plt.subplots()

        self.ax.plot(result_df['posisi'], d_values2)  # Replace 'Some Label' with an appropriate label for your data
        self.ax.scatter(result_df['posisi'], d_values2)
        
        self.ax.set_xlabel('Posisi')
        self.ax.set_ylabel('Reaktivitas')
        self.ax.set_title('Grafik Integral Batang Kendali Kompensasi')
        self.ax.legend()
        
    def display_plot3(self):
        
        plot_container = BoxLayout(orientation='vertical', padding=5)
        close_button = Button(text='Close', size_hint=(1, 0.1))
        save_button = Button(text='Save', size_hint=(1, 0.1))
        self.graph = FigureCanvasKivyAgg(figure=self.fig1)
        self.fig.savefig('gambar')
        plot_container.add_widget(self.graph)
        plot_container.add_widget(close_button)
        plot_container.add_widget(save_button)
        
        def save_plot(instance):
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"plot_{timestamp}.png"  # You can use a different file format if needed
            self.fig.savefig(filename)
            print(f"Plot saved as {filename}")
            popup.dismiss()

        popup = Popup(title='Plot', content=plot_container, size_hint=(1, 1))
        close_button.bind(on_release=popup.dismiss)
        save_button.bind(on_release=save_plot)
        popup.open()
        
    def create_and_save_plot2(self,result_df, d_values):
        self.fig2, self.ax = plt.subplots()

        self.ax.plot(result_df['posisi'], d_values)  # Replace 'Some Label' with an appropriate label for your data
        self.ax.scatter(result_df['posisi'], d_values)
        
        self.ax.set_xlabel('Posisi')
        self.ax.set_ylabel('Reaktivitas')
        self.ax.set_title('Grafik Integral Batang Kendali Pengatur')
        self.ax.legend()
        
    def display_plot2(self):
        
        plot_container = BoxLayout(orientation='vertical', padding=5)
        close_button = Button(text='Close', size_hint=(1, 0.1))
        save_button = Button(text='Save', size_hint=(1, 0.1))
        self.graph = FigureCanvasKivyAgg(figure=self.fig2)
        self.fig.savefig('gambar')
        plot_container.add_widget(self.graph)
        plot_container.add_widget(close_button)
        plot_container.add_widget(save_button)
        
        def save_plot(instance):
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"plot_{timestamp}.png"  # You can use a different file format if needed
            self.fig.savefig(filename)
            print(f"Plot saved as {filename}")
            popup.dismiss()

        popup = Popup(title='Plot', content=plot_container, size_hint=(1, 1))
        close_button.bind(on_release=popup.dismiss)
        save_button.bind(on_release=save_plot)
        popup.open()
    
    
    def hasil_csv(self,results):
        self.ids.file_path_output.text = results
        
    
        