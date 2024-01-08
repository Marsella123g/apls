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
import matplotlib.pyplot as plt
import datetime
from datetime import datetime




Builder.load_string("""
<menu1>:
    name:"menu1"
    BoxLayout:
        orientation:"vertical"
        MDTopAppBar:
            title: "KALIBRASI DAYA REAKTOR"
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
                        root.kalibrasi_daya(selected_path.text)
                    
                
                TextInput:
                    id:file_path_output
                    text: ""
                    font_size:15
                    text_size: self.width, None
                    halign:'left'
                    bold:True
                
                MDRaisedButton:
                    text: "Grafik"
                    md_bg_color:"#1D2B53"
                    pos_hint: {"center_y":.5, "center_x":.6}
                    on_release:
                        root.display_plot()
                    
""")


class Menu1(Screen):
    bg_color=Styles.primary_color 
    
    def file_chooser(self):
        # filechooser.open_file(on_selection=self.selected)
        file_path = filechooser.open_file(title="Select a CSV file", filters=[("CSV Files", "*.csv")])
        if file_path:
            self.ids.selected_path.text=file_path[0]
        
    
    def kalibrasi_daya(self,file_path):
        
        data = []
        data2 = []
        res = []
        with open(file_path, 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                data.append(row)
        res = data.pop(0)
        banyak_data = len(data)
        print("banyak data : ",banyak_data)


        for i in range (0,banyak_data):
            data2.append(data[i])
            

        # data_awalan=data[0]
        # print("data awal: ",data_awalan)
        #KOLOM DIJADIKAN LIST    
        A  = []
        B  = []
        C  = []
        D  = []
        E  = []
        A2 = []
        for i in data2:
            A.append(i[0])
            B.append(i[1])
            C.append(i[2])
            D.append(i[3])
            E.append(i[4])


        B2 = [float(i) for i in B]
        C2 = [float(i) for i in C]
        D2 = [float(i) for i in D]
        E2 = [float(i) for i in E]

        '''ini untuk data awal'''
        # print(A[0])

        '''ini untuk data akhir'''
        # print([i])

        for i in A:
            dt_object = datetime.strptime(i, "%H:%M:%S")
            
            Hour=dt_object.hour
            Menit=dt_object.minute
            Detiks=dt_object.second
            jumlahdetiknya=(Hour*3600)+(Menit*60)+Detiks
            A2.append(jumlahdetiknya)
        
        # print(type([i]))  
        # print(A2)
        # print(type(A2))

        Waktu_awal = datetime.strptime(A[0],"%H:%M:%S")
        waktu1_jam=Waktu_awal.hour
        waktu1_menit=Waktu_awal.minute
        waktu1_detiks=Waktu_awal.second
        jumlah1_detiknya=(waktu1_jam*3600)+(waktu1_menit*60)+waktu1_detiks
        print("Jumlah detik awal : ",jumlah1_detiknya)


        Waktu_akhir=datetime.strptime(i,"%H:%M:%S")
        waktu2_jam=Waktu_akhir.hour
        waktu2_menit=Waktu_akhir.minute
        waktu2_detiks=Waktu_akhir.second
        jumlah2_detiknya=(waktu2_jam*3600)+(waktu2_menit*60)+waktu2_detiks
        print("Jumlah detik akhir : ",jumlah2_detiknya)

        Banyak_detik_keseluruhan=jumlah2_detiknya-jumlah1_detiknya
        print("Jumlah detik keseluruhan : ",Banyak_detik_keseluruhan)
        W2= len(A2)

        rata_rata=Banyak_detik_keseluruhan/W2
        print("Rata-rata : ",rata_rata)

        F2 = list(np.arange(0,Banyak_detik_keseluruhan,rata_rata))

        col2=[]
        for i in range(1,len(A2)):
            hit = A2[i] - A2[i-1]
            col2.append(hit)

        # print(col2)
        # col2 = kolom untuk perbedaan waktu kedua dan pertama

        col3=[0]
        for i in range(len(col2)):
            coba = col2[i] - rata_rata
            col3.append(coba)
        # print(col3)
        # col3 = kolom untuk selisih perbedaan dengan rata-rata waktu
        indeks = []
        for i in range(len(col3)):
            if col3[i] >= 0:
                indeks.append(i)
                
        col4=[]

        B3 = []
        C3 = []
        D3 = []
        E3 = []
        F3 = []

        for i in indeks:
            col4.append(A2[i])
            B3.append(B2[i])
            C3.append(C2[i])
            D3.append(D2[i])
            E3.append(E2[i])
            F3.append(F2[i])
            
        columns = ['atrtemp', 'atr1temp', 'atr2temp', 'atr3temp']
        H = 19.0476
        results = ""

        for col in range(len(columns)):
            T = [B3, C3, D3, E3][col]
            t = F3
            y = np.array(T)
            x = np.array([[1, val] for val in t])

            xt = np.transpose(x)
            yt = np.transpose(y)
            m = np.dot(xt, x)
            m1 = np.linalg.inv(m)
            b = np.dot(np.dot(m1, xt), yt)

            RE = b[-1]
            P = H * RE * 3600

            print("Nilai Regresi", columns[col], "=", RE)
            print("Daya Pada", columns[col], "=", P)
            print("==========================================")
            results += f"Nilai Regresi {columns[col]} = {RE}\n"
            results += f"Daya Pada {columns[col]} = {P}\n"
            results += "==========================================\n"
        self.create_plot(columns, [B3, C3, D3, E3], t)
        self.hasil_csv(results)
        return results
    
    def create_plot(self, columns, data, t):
        self.fig, self.ax = plt.subplots()
        for col, d in enumerate(data):
            label = columns[col]
            self.ax.plot(t, d, label=label)
            self.ax.scatter(t, d, label=label)

        self.ax.set_xlabel('Waktu')
        self.ax.set_ylabel('Temperatur')
        self.ax.set_title('Waktu Terhadap Temperatur')
        self.ax.legend()
        
    def display_plot(self):
        
        plot_container = BoxLayout(orientation='vertical', padding=5)
        close_button = Button(text='Close', size_hint=(1, 0.1))
        save_button = Button(text='Save', size_hint=(1, 0.1))
        
        self.graph = FigureCanvasKivyAgg(figure=self.fig)
        
        plot_container.add_widget(self.graph)
        plot_container.add_widget(close_button)
        plot_container.add_widget(save_button)

        def save_plot(instance):
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"plot_{timestamp}.png"  
            self.fig.savefig(filename)

            popup.dismiss()
        
        popup = Popup(title='Plot', content=plot_container, size_hint=(0.9, 0.9))
        close_button.bind(on_release=popup.dismiss)
        save_button.bind(on_release=save_plot)
        popup.open()
    
    
    def hasil_csv(self,results):
        self.ids.file_path_output.text = results
        
    
        