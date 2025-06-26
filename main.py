from tkinter import *
import tkintermapview
import requests
from bs4 import BeautifulSoup


class ObiektMapy:
    def __init__(self, nazwa, miejscowosc):
        self.nazwa = nazwa
        self.miejscowosc = miejscowosc
        self.coordinates = self.get_coordinates()
        self.marker = None

    def get_coordinates(self):
        try:
            url = f"https://pl.wikipedia.org/wiki/{self.miejscowosc}"
            response = requests.get(url, timeout=5).text
            soup = BeautifulSoup(response, "html.parser")
            latitudes = soup.select(".latitude")
            longitudes = soup.select(".longitude")
            if latitudes and longitudes:
                latitude = float(latitudes[0].text.replace(",", "."))
                longitude = float(longitudes[0].text.replace(",", "."))
                return [latitude, longitude]
            else:
                raise ValueError("Brak współrzędnych na stronie")
        except Exception as e:
            print(f"Błąd pobierania współrzędnych dla {self.miejscowosc}: {e}")
            return [52.23, 21.0]  # Warszawa jako domyślna

class DomDziecka(ObiektMapy):
    pass

class Pracownik(ObiektMapy):
    def __init__(self, nazwa, miejscowosc, dom):
        self.dom = dom
        super().__init__(nazwa, miejscowosc)

class Dziecko(ObiektMapy):
    def __init__(self, nazwa, miejscowosc, dom):
        self.dom = dom
        super().__init__(nazwa, miejscowosc)

domy = []
pracownicy = []
dzieci = []
wszystkie_markery = []

def dodaj_dom():
    nazwa = entry_name.get()
    miejscowosc = entry_location.get()
    if nazwa and miejscowosc:
        dom = DomDziecka(nazwa, miejscowosc)
        domy.append(dom)
        listbox_domy.insert(END, dom.nazwa)
    clear_entries()

def dodaj_pracownika():
    nazwa = entry_name.get()
    miejscowosc = entry_location.get()
    dom = entry_extra.get()
    if nazwa and miejscowosc and dom:
        pracownik = Pracownik(nazwa, miejscowosc, dom)
        pracownicy.append(pracownik)
        listbox_pracownicy.insert(END, pracownik.nazwa)
    clear_entries()

def dodaj_dziecko():
    nazwa = entry_name.get()
    miejscowosc = entry_location.get()
    dom = entry_extra.get()
    if nazwa and miejscowosc and dom:
        dziecko = Dziecko(nazwa, miejscowosc, dom)
        dzieci.append(dziecko)
        listbox_dzieci.insert(END, dziecko.nazwa)
    clear_entries()

def edytuj_dom():
    index = listbox_domy.curselection()
    if index:
        dom = domy[index[0]]
        dom.nazwa = entry_name.get()
        dom.miejscowosc = entry_location.get()
        dom.coordinates = dom.get_coordinates()
        listbox_domy.delete(index)
        listbox_domy.insert(index, dom.nazwa)
        clear_entries()

def edytuj_pracownika():
    index = listbox_pracownicy.curselection()
    if index:
        pracownik = pracownicy[index[0]]
        pracownik.nazwa = entry_name.get()
        pracownik.miejscowosc = entry_location.get()
        pracownik.dom = entry_extra.get()
        pracownik.coordinates = pracownik.get_coordinates()
        listbox_pracownicy.delete(index)
        listbox_pracownicy.insert(index, pracownik.nazwa)
        clear_entries()

def edytuj_dziecko():
    index = listbox_dzieci.curselection()
    if index:
        dziecko = dzieci[index[0]]
        dziecko.nazwa = entry_name.get()
        dziecko.miejscowosc = entry_location.get()
        dziecko.dom = entry_extra.get()
        dziecko.coordinates = dziecko.get_coordinates()
        listbox_dzieci.delete(index)
        listbox_dzieci.insert(index, dziecko.nazwa)
        clear_entries()

def usun_dom():
    index = listbox_domy.curselection()
    if index:
        del domy[index[0]]
        listbox_domy.delete(index)

def usun_pracownika():
    index = listbox_pracownicy.curselection()
    if index:
        del pracownicy[index[0]]
        listbox_pracownicy.delete(index)

def usun_dziecko():
    index = listbox_dzieci.curselection()
    if index:
        del dzieci[index[0]]
        listbox_dzieci.delete(index)

def clear_entries():
    entry_name.delete(0, END)
    entry_location.delete(0, END)
    if entry_extra:
        entry_extra.delete(0, END)
    entry_name.focus_set()

def usun_wszystkie_markery():
    global wszystkie_markery
    for marker in wszystkie_markery:
        marker.delete()
    wszystkie_markery = []

def pokaz_wszystkie_domy():
    usun_wszystkie_markery()
    map_widget.set_zoom(6)
    for d in domy:
        d.marker = map_widget.set_marker(d.coordinates[0], d.coordinates[1], text=d.nazwa)
        wszystkie_markery.append(d.marker)

def pokaz_wszystkich_pracownikow():
    usun_wszystkie_markery()
    map_widget.set_zoom(6)
    lokalizacje = {}
    for p in pracownicy:
        key = tuple(p.coordinates)
        lokalizacje.setdefault(key, []).append(p.nazwa)
    for coords, imiona in lokalizacje.items():
        text = "\n".join(imiona)
        marker = map_widget.set_marker(coords[0], coords[1], text=text)
        wszystkie_markery.append(marker)

def pokaz_dzieci_domu():
    usun_wszystkie_markery()
    nazwa_domu = entry_domu_dziecko.get()
    if nazwa_domu:
        lokalizacje = {}
        for d in dzieci:
            if d.dom == nazwa_domu:
                key = tuple(d.coordinates)
                lokalizacje.setdefault(key, []).append(d.nazwa)
        for coords, imiona in lokalizacje.items():
            text = "\n".join(imiona)
            marker = map_widget.set_marker(coords[0], coords[1], text=text)
            wszystkie_markery.append(marker)

def pokaz_pracownikow_domu():
    usun_wszystkie_markery()
    nazwa_domu = entry_domu_pracownik.get()
    if nazwa_domu:
        lokalizacje = {}
        for p in pracownicy:
            if p.dom == nazwa_domu:
                key = tuple(p.coordinates)
                lokalizacje.setdefault(key, []).append(p.nazwa)
        for coords, imiona in lokalizacje.items():
            text = "\n".join(imiona)
            marker = map_widget.set_marker(coords[0], coords[1], text=text)
            wszystkie_markery.append(marker)

def pokaz_formularz(typ):
    for widget in frame_formularz.winfo_children():
        widget.destroy()

    Label(frame_formularz, text="Nazwa").grid(row=0, column=0)
    global entry_name
    entry_name = Entry(frame_formularz)
    entry_name.grid(row=0, column=1)

    Label(frame_formularz, text="Miejscowość").grid(row=1, column=0)
    global entry_location
    entry_location = Entry(frame_formularz)
    entry_location.grid(row=1, column=1)

    global entry_extra
    entry_extra = None

    if typ != "dom":
        Label(frame_formularz, text="Dom dziecka").grid(row=2, column=0)
        entry_extra = Entry(frame_formularz)
        entry_extra.grid(row=2, column=1)

    if typ == "dom":
        Button(frame_formularz, text="Dodaj dom", command=dodaj_dom).grid(row=3, column=0)
        Button(frame_formularz, text="Edytuj dom", command=edytuj_dom).grid(row=3, column=1)
    elif typ == "pracownik":
        Button(frame_formularz, text="Dodaj pracownika", command=dodaj_pracownika).grid(row=3, column=0)
        Button(frame_formularz, text="Edytuj pracownika", command=edytuj_pracownika).grid(row=3, column=1)
    elif typ == "dziecko":
        Button(frame_formularz, text="Dodaj dziecko", command=dodaj_dziecko).grid(row=3, column=0)
        Button(frame_formularz, text="Edytuj dziecko", command=edytuj_dziecko).grid(row=3, column=1)

def wczytaj_dane_formularz(typ, index):
    if typ == "dom":
        obiekt = domy[index]
        pokaz_formularz("dom")
        entry_name.insert(0, obiekt.nazwa)
        entry_location.insert(0, obiekt.miejscowosc)
    elif typ == "pracownik":
        obiekt = pracownicy[index]
        pokaz_formularz("pracownik")
        entry_name.insert(0, obiekt.nazwa)
        entry_location.insert(0, obiekt.miejscowosc)
        entry_extra.insert(0, obiekt.dom)
    elif typ == "dziecko":
        obiekt = dzieci[index]
        pokaz_formularz("dziecko")
        entry_name.insert(0, obiekt.nazwa)
        entry_location.insert(0, obiekt.miejscowosc)
        entry_extra.insert(0, obiekt.dom)

def on_select_listbox(typ):
    try:
        if typ == "dom":
            index = listbox_domy.curselection()[0]
        elif typ == "pracownik":
            index = listbox_pracownicy.curselection()[0]
        elif typ == "dziecko":
            index = listbox_dzieci.curselection()[0]
        else:
            return
        wczytaj_dane_formularz(typ, index)
    except IndexError:
        pass


# ------------------ GUI ------------------

root = Tk()
root.geometry("1200x800")
root.title("Mapa Domów Dziecka")

frame_left = Frame(root)
frame_left.grid(row=0, column=0, sticky=N)

Button(frame_left, text="Formularz: Dom", command=lambda: pokaz_formularz("dom")).grid(row=0, column=0, columnspan=2)
Button(frame_left, text="Formularz: Pracownik", command=lambda: pokaz_formularz("pracownik")).grid(row=1, column=0, columnspan=2)
Button(frame_left, text="Formularz: Dziecko", command=lambda: pokaz_formularz("dziecko")).grid(row=2, column=0, columnspan=2)

frame_formularz = Frame(frame_left)
frame_formularz.grid(row=3, column=0, columnspan=2, pady=10)

Button(frame_left, text="Pokaż wszystkie domy", command=pokaz_wszystkie_domy).grid(row=4, column=0, columnspan=2)
Button(frame_left, text="Pokaż wszystkich pracowników", command=pokaz_wszystkich_pracownikow).grid(row=5, column=0, columnspan=2)

Label(frame_left, text="Dom dla dzieci:").grid(row=6, column=0, columnspan=2)
entry_domu_dziecko = Entry(frame_left)
entry_domu_dziecko.grid(row=7, column=0, columnspan=2)
Button(frame_left, text="Pokaż dzieci domu", command=pokaz_dzieci_domu).grid(row=8, column=0, columnspan=2)

Label(frame_left, text="Dom dla pracowników:").grid(row=9, column=0, columnspan=2)
entry_domu_pracownik = Entry(frame_left)
entry_domu_pracownik.grid(row=10, column=0, columnspan=2)
Button(frame_left, text="Pokaż pracowników domu", command=pokaz_pracownikow_domu).grid(row=11, column=0, columnspan=2)

Label(frame_left, text="Domy dziecka").grid(row=12, column=0)
listbox_domy = Listbox(frame_left, height=5)
listbox_domy.grid(row=13, column=0, columnspan=2)
Button(frame_left, text="Usuń dom", command=usun_dom).grid(row=14, column=0, columnspan=2)
listbox_domy.bind("<<ListboxSelect>>", lambda e: on_select_listbox("dom"))

Label(frame_left, text="Pracownicy").grid(row=15, column=0)
listbox_pracownicy = Listbox(frame_left, height=5)
listbox_pracownicy.grid(row=16, column=0, columnspan=2)
Button(frame_left, text="Usuń pracownika", command=usun_pracownika).grid(row=17, column=0, columnspan=2)
listbox_pracownicy.bind("<<ListboxSelect>>", lambda e: on_select_listbox("pracownik"))

Label(frame_left, text="Dzieci").grid(row=18, column=0)
listbox_dzieci = Listbox(frame_left, height=5)
listbox_dzieci.grid(row=19, column=0, columnspan=2)
Button(frame_left, text="Usuń dziecko", command=usun_dziecko).grid(row=20, column=0, columnspan=2)
listbox_dzieci.bind("<<ListboxSelect>>", lambda e: on_select_listbox("dziecko"))

map_widget = tkintermapview.TkinterMapView(root, width=800, height=800, corner_radius=0)
map_widget.grid(row=0, column=1)
map_widget.set_position(52.23, 21.0)
map_widget.set_zoom(6)


root.mainloop()
