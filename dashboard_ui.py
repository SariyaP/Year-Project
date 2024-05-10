import tkinter as tk
from tkinter import ttk, messagebox
import csv, os
import matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from nutrition import Nutrition

class DashBoardUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.window = self
        self.window.resizable(True, True)
        self.window.title("Cereal Nutritions")
        self.window.minsize(960,540)
        self.window.maxsize(960, 540)
        self.window.configure(bg='#D9D9D9')
        self.data = []
        self.load_data()
        self.selected = self.data.copy()
        self.df = pd.DataFrame(self.selected.copy())
        self.init_components()

    def init_components(self):
        self.top_label()
        self.top_cereal()
        self.bar_chart()
        self.num_cereal()
        self.scatter_chart()
        self.find_cereal()

    def top_label(self):
        tk.Canvas(self.window, width=940, height=34, bg='white').place(x=10, y=10)
        tk.Label(self.window, text='Nutritions of cereals', font="Arial 14", bg='white').place(x=15, y=15)
        tk.Label(self.window, text='Manufacture:', font="Arial 14", bg='white').place(x=685, y=15)
        self.mfr = ['All'] + self.get_value_from_attribute('mfr')
        self.choosen_mfr = ttk.Combobox(self.window,values=self.mfr, state='readonly')
        self.choosen_mfr.current(0)
        self.choosen_mfr.bind('<<ComboboxSelected>>', self.choose_mfr)
        self.choosen_mfr.place(x=805, y=19)

    def top_cereal(self):
        self.topcereal = tk.Canvas(self.window, width= 450, height= 220, bg='white').place(x=10, y= 54)
        tk.Label(self.window, text='Top 5 Cereals', font="Arial 14", bg='white').place(x=12, y=58)
        tk.Canvas(self.topcereal, width=200, height=25, bg='white', highlightcolor='black', highlightthickness=2).place(x=25, y=98)
        tk.Canvas(self.topcereal, width=200, height=25, bg='white', highlightcolor='black', highlightthickness=2).place(x=25, y=133)
        tk.Canvas(self.topcereal, width=200, height=25, bg='white', highlightcolor='black', highlightthickness=2).place(x=25, y=168)
        tk.Canvas(self.topcereal, width=200, height=25, bg='white', highlightcolor='black', highlightthickness=2).place(x=25, y=203)
        tk.Canvas(self.topcereal, width=200, height=25, bg='white', highlightcolor='black', highlightthickness=2).place(x=25, y=238)
        self.top = sorted(self.selected, key=lambda d: d['rating'], reverse=True)
        place = [100, 135, 170, 205, 240]
        for i in range(5) if len(self.top) >= 5 else len(self.top):
            tk.Canvas(self.topcereal, width=float(self.top[i].get('rating', 0))*2, height=25, bg='#41B8D5', highlightthickness=0).place(x=25, y=place[i])
            tk.Label(self.topcereal, text=f"{self.top[i].get('name', 0)[:28]}{'...' if len(self.top[i].get('name', 0)) > 28 else ''}", bg='white', font='Arial 12').place(x=245, y=place[i])


    def num_cereal(self):
        tk.Canvas(self.window, width= 300, height=220, bg='white').place(x= 470, y=54)
        self.num_all = tk.Label(self.window, text='77', font='Arial 48', bg='white')
        self.num_all.place(x=640, y=104)
        tk.Label(self.window, text='Total Cereal', font='Arial 20', bg='white').place(x=600, y=194)
        tk.Canvas(self.window, width=170, height=105, bg='white').place(x=780, y=54)
        self.num_hot = tk.Label(self.window, text='3', font='Arial 25', bg='white')
        self.num_hot.place(x=855, y=74)
        tk.Label(self.window, text='Total Hot Cereal', font='Arial 15', bg='white').place(x=793, y=119)
        tk.Canvas(self.window, width=170, height=105, bg='white').place(x=780, y=169)
        self.num_cold = tk.Label(self.window, text='74', font='Arial 25', bg='white')
        self.num_cold.place(x=855, y=184)
        tk.Label(self.window, text='Total Cold Cereal', font='Arial 15', bg='white').place(x=788, y=229)

    def bar_chart(self):
        tk.Canvas(self.window, width= 390, height= 246, bg='white').place(x=10, y= 284)
        self.bar_fig, self.bar_ax = plt.subplots(figsize=(3, 2))
        x = pd.DataFrame(self.selected)
        fat_data = x['fat'].sort_values()
        self.bar_ax.bar(fat_data, range(len(fat_data)), color='#41B8D5')
        self.bar_ax.set_title('Histogram of Fats')
        self.bar_ax.set_xlabel('Fat')
        self.bar_ax.set_xlim(-1, 5)
        if self.choosen_mfr.get() == 'All':
            self.bar_ax.set_ylim(0, 70)
        else:
            self.bar_ax.set_ylim(0, 25)
        self.bar_ax.spines[['top', 'right']].set_visible(False)
        self.bar_canvas = FigureCanvasTkAgg(self.bar_fig, master=self.window)
        self.bar_canvas.draw()
        self.bar_canvas_widget = self.bar_canvas.get_tk_widget()
        self.bar_canvas_widget.place(x=40, y=304)

    def plot_bar(self):
        self.bar_canvas_widget.destroy()
        matplotlib.pyplot.close(self.bar_fig)
        self.bar_chart()

    def scatter_chart(self):
        self.scatterchart = tk.Canvas(self.window, width= 390, height= 246, bg='white').place(x=410, y= 284)
        self.pair_fig, self.pair_ax = plt.subplots(figsize=(3, 2))
        x = pd.DataFrame(self.selected)
        sugar = pd.to_numeric(x['sugars'])
        calorie = x['calories'].sort_values(ascending= False)
        self.pair_ax.scatter(sugar, calorie, color='#41B8D5')
        self.pair_ax.set_title('Correlation of Sugars and Calories')
        self.pair_ax.set_xlim(-4, 20)
        self.pair_ax.spines[['top', 'right']].set_visible(False)
        self.pair_canvas = FigureCanvasTkAgg(self.pair_fig, master=self.scatterchart)
        self.pair_canvas.draw()
        self.pair_canvas_widget = self.pair_canvas.get_tk_widget()
        self.pair_canvas_widget.place(x=450, y=304)

    def plot_scatter(self):
        self.pair_canvas_widget.destroy()
        matplotlib.pyplot.close(self.pair_fig)
        self.scatter_chart()

    def find_cereal(self):
        tk.Canvas(self.window, width= 140, height=246, bg='white').place(x=810, y = 284)
        tk.Label(self.window, text= 'Find', bg='white', font='Arial 20').place(x=852, y=306)
        tk.Label(self.window, text='your', bg='white', font='Arial 20').place(x=852, y=346)
        tk.Label(self.window, text='cereal?', bg='white', font='Arial 20').place(x=842, y=386)
        self.button = ttk.Button(self.window, text='Go', command=self.cereal_button).place(x=842, y=446)
        ttk.Button(self.window, text='Exit', command=self.window.quit).place(x=842, y=486)

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
        self.window.destroy()
        FindCereal(self.data)

    def run(self):
        self.window.mainloop()

    def choose_mfr(self, *args):
        if self.choosen_mfr.get() == "All":
            self.selected = self.data.copy()
            self.df = pd.DataFrame(self.selected)
            self.plot_bar()
            self.plot_scatter()
            self.change_label()
            self.top_cereal()
        else:
            self.selected = self.filter('mfr', self.choosen_mfr.get())
            self.df = pd.DataFrame(self.selected)
            self.plot_bar()
            self.plot_scatter()
            self.change_label()
            self.top_cereal()

    def change_label(self):
        type = self.df['type'].value_counts()
        self.num_hot['text'] = type.get('Hot', 0)
        self.num_cold['text'] = type.get('Cold', 0)
        self.num_all['text'] = len(pd.DataFrame(self.selected))

    def filter(self, attribute, value):
        filtered = []
        for item in self.data:
            if item.get(attribute) == value:
                filtered.append(item.copy())
        return filtered


class FindCereal(tk.Tk):
    def __init__(self, data):
        super().__init__()
        self.listbox = []
        self.all_nutritions = []
        self.compare = ['More than', 'Less than', 'Equal to']
        self.data = data
        self.df = pd.DataFrame(data)
        self.selected = None
        self.init_components()

    def init_components(self):
        self.window = self
        self.window.title("Find your cereal")
        self.window.minsize(650,450)
        self.window.maxsize(650, 450)
        for name in Nutrition:
            self.all_nutritions += [name.name]
        self.nutrition = ttk.Combobox(self.window, values=self.all_nutritions, state='readonly')
        self.nutrition.current(0)
        self.nutrition.place(x=20, y=20)
        self._compare = ttk.Combobox(self.window, values=self.compare, state='readonly')
        self._compare.current(0)
        self._compare.place(x=230,  y=20)
        self.value = ttk.Entry(self.window, width=10)
        self.value.place(x=440, y=20)
        self.filtered = tk.Listbox(self.window, height=15, width=45, justify='center', font='Arial 14', selectmode=tk.SINGLE)
        self.filtered.place(x=20, y=80)
        self.filter_listbox()
        self.filter = ttk.Button(self.window, text='Filter', command=self.filter_button)
        self.filter.place(x=540, y=80)
        self.more = ttk.Button(self.window, text='More..', command=self.more_info)
        self.more.place(x=540, y=120)
        self.go_back = ttk.Button(self.window, text='Go back', command=self.back)
        self.go_back.place(x=540, y=160)
        self.exit = ttk.Button(self.window, text='Exit', command=self.window.quit)
        self.exit.place(x=540, y=200)

    def filter_listbox(self):
        self.filtered.delete(0, tk.END)
        self.listbox = []
        for index, row in self.df.iterrows():
            display = row.values[0]
            self.listbox += [display]
            self.filtered.insert(tk.END, display)

    def filter_button(self):
        self.selected = self.filter_compare()
        self.df = pd.DataFrame(self.selected)
        self.filter_listbox()

    def filter_compare(self):
        filtered = []
        attribute = self.nutrition.get()
        compare = self._compare.get()
        value = self.value.get()
        if compare == "More than":
            for item in self.data:
                if item.get(Nutrition[attribute].value) > value:
                    filtered.append(item.copy())
        elif compare == "Less than":
            for item in self.data:
                if item.get(Nutrition[attribute].value) < value:
                    filtered.append(item.copy())
        elif compare == "Equal to":
            for item in self.data:
                if item.get(Nutrition[attribute].value) == value:
                    filtered.append(item.copy())
        return filtered

    def more_info(self):
        if self.filtered.curselection() == ():
            messagebox.showerror('Error Happens', 'Error: Please choose your cereal')
        else:
            select_cereal = self.listbox[self.filtered.curselection()[0]]
            CerealInformation(select_cereal, self.data)

    def back(self):
        self.window.destroy()
        DashBoardUI()

class CerealInformation(tk.Tk):
    def __init__(self, selected_cereal, data):
        super().__init__()
        self.cereal = self
        self.data = data
        self.selected_cereal = selected_cereal
        self.cereal.title("Cereal Information")
        self.cereal.minsize(900, 420)
        self.cereal.maxsize(900, 420)
        self.init_components()

    def init_components(self):
        tk.Canvas(self.cereal, height=380, width=860, bg='white').place(x=20, y=20)
        self.name = tk.Label(self.cereal, text=self.selected_cereal, bg='white', font='Arial 30')
        self.name.place(x=40, y=30)
        self.info = [d for d in self.data if d['name'] == self.selected_cereal]
        tk.Label(self.cereal, text=f"Rating: {float(self.info[0]['rating']):.2f} out of 100", bg='white', font='Arial 15').place(x=40, y=85)
        tk.Label(self.cereal, text=f"Manufacture: {self.info[0]['mfr']}", bg='white', font='Arial 14').place(x=40, y=115)
        tk.Label(self.cereal, text=f"Calorie: {self.info[0]['calories']} per serving", bg='white', font='Arial 13').place(x=40, y=160)
        tk.Label(self.cereal, text=f"Fat: {self.info[0]['fat']} grams", bg='white', font='Arial 13').place(x=40, y=210)
        tk.Label(self.cereal, text=f"Fiber: {self.info[0]['fiber']} grams", bg='white', font='Arial 13').place(x=40, y=260)
        tk.Label(self.cereal, text=f"Carbohydrates: {self.info[0]['carbo']} grams", bg='white', font='Arial 13').place(x=40, y=310)
        tk.Label(self.cereal, text=f"Potassium: {self.info[0]['potass']} milligrams", bg='white', font='Arial 13').place(x=40, y=360)
        tk.Label(self.cereal, text=f"Type: {self.info[0]['type']} Cereal", bg='white', font='Arial 13').place(x=270, y=160)
        tk.Label(self.cereal, text=f"Protein: {self.info[0]['protein']} grams", bg='white', font='Arial 13').place(x=270, y=210)
        tk.Label(self.cereal, text=f"Sodium: {self.info[0]['sodium']} milligrams", bg='white', font='Arial 13').place(x=270, y=260)
        tk.Label(self.cereal, text=f"Sugars: {self.info[0]['sugars']} grams", bg='white', font='Arial 13').place(x=270, y=310)
        tk.Label(self.cereal, text=f"Vitamins: {self.info[0]['vitamins']}", bg='white', font='Arial 13').place(x=270, y=360)
        self.plot_pie()

    def plot_pie(self):
        self.pie_fig, self.pie_ax = plt.subplots(figsize=(4, 3))
        value_list = []
        all_att = ['protein', 'fat', 'sodium',
                   'carbo', 'sugars', 'potass']
        colors = ['r', 'g', 'b', 'pink', 'orange', 'purple']
        for item in self.info:
            for value in all_att:
                value_list.append(item.get(value, 0))
        value_list[2] = float(value_list[2])/1000
        value_list[5] = float(value_list[2]) / 1000
        self.pie_ax.pie(np.array(value_list), labels=all_att, colors=colors)
        self.pie_canvas = FigureCanvasTkAgg(self.pie_fig, master=self.cereal)
        self.pie_canvas.draw()
        self.pie_canvas_widget = self.pie_canvas.get_tk_widget()
        self.pie_canvas_widget.place(x=445, y=100)