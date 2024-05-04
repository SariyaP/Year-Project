import tkinter as tk
from tkinter import ttk
import csv, os
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DashBoardUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.resizable(True, True)
        self.window.title("Cereal Nutritions")
        self.window.maxsize(960, 540)
        self.window.configure(bg='#D9D9D9')
        self.data = []
        self.load_data()
        self.selected = self.data.copy()
        self.init_components()

    def init_components(self):
        self.top_label()
        self.top_cereal()
        self.bar_chart()
        self.num_cereal()
        self.scatter_chart()
        self.find_cereal()

    def top_label(self):
        self.maintitle = tk.Canvas(self.window, width=940, height=34, bg='white').place(x=10, y=10)
        tk.Label(self.maintitle, text='Nutritions of cereals', font="Arial 14", bg='white').place(x=15, y=15)
        tk.Label(self.maintitle, text='Manufacture:', font="Arial 14", bg='white').place(x=685, y=15)
        self.mfr = ['All'] + self.get_value_from_attribute('mfr')
        self.choosen_mfr = ttk.Combobox(self.maintitle, values=self.mfr)
        self.choosen_mfr.bind('<<ComboboxSelected>>', self.choose_mfr)
        self.choosen_mfr.place(x=805, y=19)

    def top_cereal(self):
        self.topcereal = tk.Canvas(self.window, width= 450, height= 220, bg='white').place(x=10, y= 54)
        tk.Label(self.maintitle, text='Top 5 Cereals', font="Arial 14", bg='white').place(x=12, y=58)
        tk.Canvas(self.topcereal, width=200, height=25, bg='#41B8D5', highlightthickness=0).place(x=25, y=98)
        tk.Canvas(self.topcereal, width=200, height=25, bg='#41B8D5', highlightthickness=0).place(x=25, y=133)
        tk.Canvas(self.topcereal, width=200, height=25, bg='#41B8D5', highlightthickness=0).place(x=25, y=168)
        tk.Canvas(self.topcereal, width=200, height=25, bg='#41B8D5', highlightthickness=0).place(x=25, y=203)
        tk.Canvas(self.topcereal, width=200, height=25, bg='#41B8D5', highlightthickness=0).place(x=25, y=238)


    def num_cereal(self):
        self.n_all = tk.Canvas(self.window, width= 300, height=220, bg='white').place(x= 470, y=54)
        self.num_all = tk.Label(self.maintitle, text='0', font='Arial 48', bg='white')
        self.num_all.place(x=640, y=104)
        tk.Label(self.maintitle, text='Total Cereal', font='Arial 20', bg='white').place(x=600, y= 194)
        self.n_hot = tk.Canvas(self.window, width=170, height=105, bg='white')
        self.n_hot.place(x=780, y=54)
        self.num_hot = tk.Label(self.maintitle, text='0', font='Arial 25', bg='white').place(x=855, y=74)
        tk.Label(self.maintitle, text='Total Hot Cereal', font='Arial 15', bg='white').place(x=793, y=119)
        self.n_cold = tk.Canvas(self.window, width=170, height=105, bg='white')
        self.n_cold.place(x=780, y=169)
        self.num_cold = tk.Label(self.maintitle, text='0', font='Arial 25', bg='white').place(x=855, y=184)
        tk.Label(self.maintitle, text='Total Cold Cereal', font='Arial 15', bg='white').place(x=788, y=229)

    def bar_chart(self):
        self.barchart = tk.Canvas(self.window, width= 390, height= 246, bg='white').place(x=10, y= 284)
        self.bar_fig, self.bar_ax = plt.subplots(figsize=(3.5, 2))
        x = pd.DataFrame(self.selected)
        fat_data = x['fat'].sort_values()
        self.bar_ax.bar(fat_data, range(len(fat_data)))
        self.bar_ax.set_title('Histogram of Fats')
        self.bar_ax.set_xlabel('Fat')
        self.bar_ax.set_ylabel('Frequency')
        self.bar_ax.spines[['top', 'right']].set_visible(False)
        self.bar_canvas = FigureCanvasTkAgg(self.bar_fig, master=self.barchart)
        self.bar_canvas.draw()
        self.bar_canvas_widget = self.bar_canvas.get_tk_widget()
        self.bar_canvas_widget.place(x=40, y=304)

    def plot_bar(self):
        pass

    def scatter_chart(self):
        self.scatterchart = tk.Canvas(self.window, width= 390, height= 246, bg='white').place(x=410, y= 284)
        fig = plt.Figure(figsize=(3, 2))
        ax = fig.add_subplot(111)
        self.bar_canvas = FigureCanvasTkAgg(fig, master=self.window)
        self.bar_canvas_widget = self.bar_canvas.get_tk_widget()
        self.bar_canvas_widget.configure(background='white')
        self.bar_canvas_widget.place(x=450, y=304)

    def find_cereal(self):
        self.find = tk.Canvas(self.window, width= 140, height=246, bg='white').place(x=810, y = 284)
        tk.Label(self.maintitle, text= 'Find', bg='white', font='Arial 20').place(x=852, y=306)
        tk.Label(self.maintitle, text='your', bg='white', font='Arial 20').place(x=852, y=346)
        tk.Label(self.maintitle, text='cereal?', bg='white', font='Arial 20').place(x=842, y=386)
        self.button = ttk.Button(self.window, text='Go', command=self.cereal_button).place(x=842, y=446)

    def load_data(self):
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(__location__, 'cereal.csv')) as f:
            rows = csv.DictReader(f)
            for value in rows:
                self.data.append(dict(value))

        self.dataframe = pd.read_csv('cereal.csv')

    def get_value_from_attribute(self, attribute):
        values = set()
        for item in self.data:
            values.add(item[attribute])
        return list(values)

    def cereal_button(self):
        fc = FindCereal(self.data)

    def run(self):
        self.window.mainloop()

    def choose_mfr(self, *args):
        if self.choosen_mfr.get() == "All":
            self.selected = self.data.copy()
            self.plot_bar()
            self.change_label()
        else:
            self.selected = self.filter('mfr', self.choosen_mfr.get())
            self.plot_bar()
            self.change_label()

    def change_label(self):
        # self.num_hot['text'] = len(pd.DataFrame(self.selected)
        self.num_all['text'] = len(pd.DataFrame(self.selected))

    def filter(self, attribute, value):
        filtered = []
        for item in self.data:
            if item.get(attribute) == value:
                filtered.append(item.copy())
        return filtered

class FindCereal:
    def __init__(self, data):
        self.data = data
        self.init_components()

    def init_components(self):
        self.window = tk.Tk()
        self.window.title("Still Editing")