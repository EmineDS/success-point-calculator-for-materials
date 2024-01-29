from tkinter import Tk, Frame, Label, Entry, Button, StringVar, DoubleVar, ttk, Menu, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class ScoringApp:
    def __init__(self):
        self.window = Tk()
        self.window.title("Puanlama Programı")
        self.window.configure(bg="white")

        self.a = 0
        self.b = 0
        self.parametreler = []
        self.malzemeler = []
        self.onemkatsayi = []
        self.degerler = [[]]  # Başlangıçta bir boş alt liste
        self.soz = {}
        self.entry_dict = {}
        self.sonuc = []
        self.selected_values = []

        self.create_widgets()

    def birlestir(self, liste):
        yeni_listeler = [[] for _ in range(len(liste[0]))]
        for alt_kume in liste:
            for i, eleman in enumerate(alt_kume):
                yeni_listeler[i].append(eleman)
        return yeni_listeler

    def islem(self):
        self.sonuc = []  # sonuc listesini temizle
        self.deger2 = [[] for _ in range(len(self.parametreler))]

        try:
            for x in range(len(self.parametreler)):
                for y in range(len(self.malzemeler)):
                    multiplied_value = self.degerler[x + 1][y] / sum(self.degerler[x + 1])
                    self.deger2[x].append(multiplied_value)
        except ZeroDivisionError:
            messagebox.showerror("Hata", "0'a bölme hatası!")
            return

        sonlist = []
        o = 0
        for val1, b in zip(self.onemkatsayi, self.deger2):
            sublist = []
            for i, x in enumerate(b):
                if self.selected_values[o] == "max":
                    multiplied_value = val1 * x
                elif self.selected_values[o] == "min":
                    multiplied_value = val1 * (1 - x)
                sublist.append(multiplied_value)
            sonlist.append(sublist)
            o += 1

        yeni_listeler = self.birlestir(sonlist)
        print("yenilist:",yeni_listeler)
        for h in range(len(yeni_listeler)):
            self.sonuc.append(sum(yeni_listeler[h]))
        print(self.sonuc)
        self.plot_results()

    def hesapla(self):
        self.parametreler.clear()
        self.malzemeler.clear()
        self.onemkatsayi.clear()
        self.degerler.clear()

        for i in range(4 + self.b):
            for j in range(4 + self.a):
                if i == 2 and j > 0:
                    self.soz[(i, j)] = self.entry_dict[(i, j)].get()
                    self.selected_values.append(self.soz[(i, j)])
                elif i > 2 and j == 0:
                    self.soz[(i, j)] = self.entry_dict[(i, j)].get()
                    self.malzemeler.append(self.entry_dict[(i, j)].get())
                elif i == 0 and not j == 0:
                    self.soz[(i, j)] = self.entry_dict[(i, j)].get()
                    self.parametreler.append(self.entry_dict[(i, j)].get())
                elif i == 1 and not j == 0:
                    value = self.entry_dict[(i, j)].get()
                    self.soz[(i, j)] = float(value) if value != "" else None
                    self.onemkatsayi.append(self.soz[(i, j)])
                elif i > 0 and j > 0 and i != 2:
                    value = self.entry_dict[(i, j)].get()
                    self.soz[(i, j)] = float(value) if value != "" else None
                    while len(self.degerler) <= j:
                        self.degerler.append([])

                    self.degerler[j].append(self.soz[(i, j)])

        if len(self.degerler) < len(self.malzemeler):
            self.degerler.append([])

        print("Parametreler:", self.parametreler)
        print("Malzemeler:", self.malzemeler)
        print("Önem Katsayıları:", self.onemkatsayi)
        print("Değerler:", self.degerler)

    def yazdir(self):
        self.hesapla()
        self.islem()

    def create_widgets(self):
        yazi = Frame(self.window)
        yaziic = Label(yazi, text="Bu bir paşarı kıyas tablosudur")
        yaziic.grid(row=0, column=0, pady=40, padx=40)

        Tablo = Frame(self.window, bg="white", width=200, height=100)
        Tablo.grid(row=1, column=0, pady=40, padx=40)

        for i in range(4 + self.b):
            for j in range(4 + self.a):
                if i == 0 and j == 0:
                    t2 = Label(Tablo, text="parametreler", fg="black", background="white")
                    t2.grid(row=0, column=0)
                if i == 1 and j == 0:
                    t3 = Label(Tablo, text="önem katsayısı", fg="black", background="white")
                    t3.grid(row=1, column=0)
                elif i == 2 and j > 0:
                    combo = ttk.Combobox(Tablo, values=["max", "min"], height=50, justify="center", state="readonly")
                    combo.grid(row=i, column=j)
                    self.entry_dict[(i, j)] = combo
                elif i > 2 and j == 0:
                    STR3 = StringVar()
                    e = Entry(Tablo, width=20, borderwidth=5, textvariable=STR3, insertbackground="black", fg="black")
                    e.grid(row=i, column=j)
                    self.entry_dict[(i, j)] = STR3
                elif i == 0 and not j == 0:
                    STR4 = StringVar()
                    e = Entry(Tablo, width=20, borderwidth=5, textvariable=STR4, fg="black", background="white")
                    e.grid(row=i, column=j)
                    self.entry_dict[(i, j)] = STR4
                elif i == 1 and not j == 0:
                    STR5 = DoubleVar()
                    e = Entry(Tablo, width=20, borderwidth=5, textvariable=STR5, fg="black", background="white")
                    e.grid(row=i, column=j)
                    self.entry_dict[(i, j)] = STR5
                elif i == 2 and j == 0:
                    t = Label(Tablo, text="malzemeler|artış yönü", fg="black", background="white")
                    t.grid(row=2, column=0, padx=2, pady=2)
                elif i > 0 and j > 0 and i != 2:
                    STR6 = DoubleVar()
                    e = Entry(Tablo, width=20, borderwidth=5, textvariable=STR6, fg="black", background="white")
                    e.grid(row=i, column=j)
                    self.entry_dict[(i, j)] = STR6

        plus = Button(Tablo, text="+", command=self.inccolumn, borderwidth=2, background="white", fg="black")
        plus.grid(row=0, column=j + 1)

        plus2 = Button(Tablo, text="+", command=self.incrow, borderwidth=2, background="white", fg="black")
        plus2.grid(row=i + 1, column=0)

        submit = Button(Tablo, text="hesapla", command=self.yazdir, background="yellow", activebackground="#987654")
        submit.grid(row=i + 1, column=j + 1)

        submit2 = Button(Tablo, text="temizle", command=self.new, background="yellow", activebackground="#987654")
        submit2.grid(row=i + 1, column=j + 2)

    def inccolumn(self):
        self.malzemeler.clear()
        self.parametreler.clear()
        self.onemkatsayi.clear()
        self.degerler.clear()
        self.a += 1
        self.create_widgets()

    def incrow(self):
        self.malzemeler.clear()
        self.parametreler.clear()
        self.onemkatsayi.clear()
        self.degerler.clear()
        self.b += 1
        self.create_widgets()

    def new(self):
        self.create_widgets()

    def plot_results(self):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        ax1.pie(self.onemkatsayi, labels=self.parametreler, autopct='%1.1f%%', startangle=90)
        ax1.set_title("önem oranı")

         #Ensure self.malzemeler and self.sonuc have the same length
        if len(self.malzemeler) < len(self.sonuc):
            self.malzemeler.extend(["" for _ in range(len(self.sonuc) - len(self.malzemeler))])

        ax2.bar(self.malzemeler, self.sonuc, color='red')
        ax2.set_title("başarı puanı")
        ax2.set_ylim(min(self.sonuc) - 5, max(self.sonuc) + 5)
        plt.show()

    def run_app(self):
        menu = Menu(self.window, activebackground="blue", activeforeground="white", activeborderwidth=5, bg="darkgray", fg="green")
        menu.config(bd=3, font="helvetica 12")

        def run_new():
            self.window.quit()
            ScoringApp().run_app()

        self.window.config(menu=menu)
        dosyamenu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Dosya", menu=dosyamenu)
        dosyamenu.add_command(label="Kapat", command=self.window.quit, activeforeground="red")
        dosyamenu.add_command(label="Yeni", command=run_new, activeforeground="red")

        self.window.mainloop()

if __name__ == "__main__":
    app = ScoringApp()
    app.run_app()