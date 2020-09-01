import base64
import os
from time import asctime
from datetime import datetime

import tkinter as tk
from tkinter import ttk, StringVar
from tkinter import LEFT, NO, DISABLED, NORMAL
import tkinter.messagebox

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class Auslegung:

    def __init__(self):
        self.heslo = "Petr975"
        self.odemceno = False
        self.uzivatel = Auslegung.odemknout(self)
        self.zaznamy = []
        self.sifrovane_zaznamy = []
        self.nazev_soubor = "U:/AV_Beku/Projekty/AuslegungGUI/auslegung.txt"
        self.soubor_overeni = "U:/AV_Beku/Projekty/AuslegungGUI/licence.stj"
        self.pristupy = "U:/AV_Beku/Projekty/AuslegungGUI/pristupy.tjn"
        self.hledam_nuz = ""
        self.nalezeno = []
        self.kontrola = []
        self.klic = self.priprav_klic(self.heslo)
        self.odemknout()
        self.pristup()
        self.klic_licence = self.priprav_klic_pro_licenci()
        self.expirace = self.odkoduj_licenci(self.klic_licence)
        self.test_licence = self.overeni(self.expirace)

    def priprav_klic_pro_licenci(self):
        heslo = "PyladiesPlzen"
        salt = b"/*-*/"
        kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=default_backend()
        )
        klic = base64.urlsafe_b64encode(kdf.derive(heslo.encode()))
        return klic

    def odkoduj_licenci(self, klic_licence):
        try:
            with open(self.soubor_overeni, mode="r", encoding="utf-8") as expirace:
                expirace = expirace.read()
                f = Fernet(klic_licence)
                expirace = ((f.decrypt(expirace.encode()).decode("utf-8")))
                return expirace
        except:
            tk.messagebox.showwarning("Licence", "Poškozený licenční soubor")
            os._exit(0)
    


    def overeni(self, expirace):
        # self.klic_licence = self.priprav_klic_pro_licenci()
        # self.expirace = self.odkoduj_zaznamy(self.klic_licence)
        if expirace[-3:] != "Aus":  # pro Auslegung zaměnit za "Aus"
            tk.messagebox.showwarning("Licence", "Neplatná licence!!")
            os._exit(0)

        self.pocet_carek = 0
        self.rok = ""
        self.mesic = ""
        self.den = ""
        for ii in expirace:
            if ii != ",":
                if self.pocet_carek == 0:
                    self.rok = self.rok + ii
                elif self.pocet_carek == 1:
                    self.mesic = self.mesic + ii
                elif self.pocet_carek == 2:
                    self.den = self.den + ii
                else:
                    break
            else:
                self.pocet_carek = self.pocet_carek + 1


        self.systemovy_cas = asctime()
        self.systemovy_cas = self.systemovy_cas.replace("  ", " ")

        self.mezera = 0
        self.mesic_akt = ""
        self.den_akt = ""
        self.rok_akt = ""

        for qq in self.systemovy_cas:
            if qq == " ":
                self.mezera = self.mezera + 1
            elif qq != " ":
                if self.mezera == 0:
                    pass
                elif self.mezera == 1:
                    self.mesic_akt = self.mesic_akt + qq
                elif self.mezera == 2:
                    self.den_akt = self.den_akt + qq
                elif self.mezera == 3:
                    pass
                else:
                    self.rok_akt = self.rok_akt + qq

        if self.mesic_akt == "Jan":
            self.mesic_akt = "1"
        elif self.mesic_akt == "Feb":
            self.mesic_akt = "2"
        elif self.mesic_akt == "Mar":
            self.mesic_akt = "3"
        elif self.mesic_akt == "Apr":
            self.mesic_akt = "4"
        elif self.mesic_akt == "May":
            self.mesic_akt = "5"
        elif self.mesic_akt == "Jun":
            self.mesic_akt = "6"
        elif self.mesic_akt == "Jul":
            self.mesic_akt = "7"
        elif self.mesic_akt == "Aug":
            self.mesic_akt = "8"
        elif self.mesic_akt == "Sep":
            self.mesic_akt = "9"
        elif self.mesic_akt == "Oct":
            self.mesic_akt = "10"
        elif self.mesic_akt == "Nov":
            self.mesic_akt = "11"
        elif self.mesic_akt == "Dec":
            self.mesic_akt = "12"


        self.d1 = datetime(int(self.rok), int(self.mesic), int(self.den))
        self.d2 = datetime(int(self.rok_akt), int(self.mesic_akt), int(self.den_akt))
        self.rozdil = self.d1 - self.d2
        self.rozdil = str(self.rozdil)
        self.pocet_dnu = ""
        for aa in self.rozdil:
            if aa == " ":
                break
            else:
                self.pocet_dnu += aa

        if self.pocet_dnu == "0:00:00":
            tk.messagebox.showwarning("Licence", "Vaše licence dnes vyprší.")
            return
        elif int(self.pocet_dnu) > 14:
            return
        elif (int(self.pocet_dnu) <= 30) and (int(self.pocet_dnu) > 0):
            tk.messagebox.showwarning("Licence", "Vaše licence brzy vyprší.")
            return
        else:
            tk.messagebox.showwarning("Licence", "Licence vypršela.")
            os._exit(0)


    def odemknout(self):
        self.uzivatel = os.getenv('username')
        if (self.uzivatel == "fiser") or (self.uzivatel == "bekucad") or (self.uzivatel == "hana.dufkova"):
            self.odemceno = True
            return self.uzivatel
        else:
            self.odemceno = False
            return self.uzivatel


    def pridej_zaznam(self, cislo, X, Y, draha, vyseky, krizeni, poznamka):
        self.test = ""
        for ii in cislo:
            try:
                if int(ii):
                    self.test = self.test + ii
                elif ii == "0":
                    self.test = self.test + ii
            except ValueError:
                self.test = self.test + "/"

        cislo = self.test
        self.zaznamy.append((cislo, X, Y, draha, vyseky, krizeni, poznamka))
        self.uloz(self.nazev_soubor)

    def priprav_klic(self, heslo):
        salt = b"/*-*/"
        kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=default_backend()
        )
        return base64.urlsafe_b64encode(kdf.derive(heslo.encode()))

    def zakoduj_zaznamy(self):
        f = Fernet(self.klic)
        sifrovane_zaznamy = []
        for ii in self.zaznamy:
            zasifrovany_zaznam = ((f.encrypt(ii[0].encode()).decode("utf-8")),
                                    (f.encrypt(ii[1].encode()).decode("utf-8")),
                                    (f.encrypt(ii[2].encode()).decode("utf-8")),
                                    (f.encrypt(ii[3].encode()).decode("utf-8")),
                                    (f.encrypt(ii[4].encode()).decode("utf-8")),
                                    (f.encrypt(ii[5].encode()).decode("utf-8")),
                                    (f.encrypt(ii[6].encode()).decode("utf-8")))
            self.sifrovane_zaznamy.append(zasifrovany_zaznam)
        


    def odkoduj_zaznamy(self):
        f = Fernet(self.klic)
        ozaznamy = []
        # sifrovane_zaznamy = []
        for ii in self.zaznamy:
            zasifrovany_zaznam = ((f.decrypt(ii[0].encode()).decode("utf-8")),
                                    (f.decrypt(ii[1].encode()).decode("utf-8")),
                                    (f.decrypt(ii[2].encode()).decode("utf-8")),
                                    (f.decrypt(ii[3].encode()).decode("utf-8")),
                                    (f.decrypt(ii[4].encode()).decode("utf-8")),
                                    (f.decrypt(ii[5].encode()).decode("utf-8")),
                                    (f.decrypt(ii[6].encode()).decode("utf-8")))
            ozaznamy.append(zasifrovany_zaznam)
        self.zaznamy = ozaznamy
        # print(ozaznamy)


    def uloz(self, nazev_soubor):
        # print(self.zaznamy)
        self.priprav_klic(self.heslo)
        self.zakoduj_zaznamy()
        with open(self.nazev_soubor, "w", encoding="utf-8") as soubor:
            for cislo, X, Y, draha, vyseky, krizeni, poznamka in self.sifrovane_zaznamy:
                print(cislo + "◙" + X + "◙" + Y + "◙" + draha + "◙" + vyseky + "◙" + krizeni + "◙" + poznamka, file=soubor)
        self.sifrovane_zaznamy = []

    def nacti_soubor(self):
        # print(self.zaznamy)
        try:
            with open(self.nazev_soubor, "r", encoding="utf-8") as soubor:
                for radka in soubor:
                    radka = radka.splitlines()
                    self.zaznamy.append(radka[0].split("◙"))
            self.priprav_klic(self.heslo)
            self.odkoduj_zaznamy()
        except FileNotFoundError:
            return


    def pristup(self):
        try:
            self.datum_cas = asctime()   #  načtení aktuálního data a času
            self.log = self.datum_cas + " " + self.uzivatel
            with open(self.pristupy, mode="a", encoding="UTF-8") as pr:
                print(self.log, file=pr)
        except FileNotFoundError:
            return




    def smaz(self, index):
        self.zaznamy.pop(index)


    def vyhledat(self, hledam_nuz):
        self.opraveny_nuz = ""

        for ii in self.hledam_nuz:
            try:
                if int(ii):
                    self.opraveny_nuz = self.opraveny_nuz + ii
                elif ii == "0":
                    self.opraveny_nuz = self.opraveny_nuz + ii
            except ValueError:
                self.opraveny_nuz = self.opraveny_nuz + "/"

        for radek in self.zaznamy:
            for cislo in radek:
                if cislo == self.opraveny_nuz:
                    self.nalezeno.append(radek)
                    break
                else:
                    pass
                    break

class AuslegungGUI(tk.Frame):

    def __init__(self, parent, auslegung):
        super().__init__(parent)
        self.parent = parent
        self.auslegung = auslegung
        self.parent.title("Auslegung Paragon")
        self.entry_width = 30

        self.parent.protocol("WM_DELETE_WINDOW", self.on_close)
        self.create_widgets()


    def create_widgets(self):

        self.frame_nacti = tk.Frame()
        self.frame_nacti.pack()

        self.button_nacti = tk.Button(self.frame_nacti, width=100, text="Načti všechny záznamy", command=self.nacti)
        self.button_nacti.pack(side=LEFT)

        self.frame_mezera = tk.Frame()
        self.frame_mezera.pack()

        self.label_mez = tk.Label(self.frame_mezera, text="   ")
        self.label_mez.pack(side=LEFT)

        # Vyhledat
        self.frame_vyhledat = tk.Frame()
        self.frame_vyhledat.pack()

        self.cislo_noze = StringVar()
        self.entry_cislo_noze = ttk.Entry(self.frame_vyhledat, width=20, textvariable=self.cislo_noze)
        self.entry_cislo_noze.pack(side=LEFT)


        self.button_vyhledat = tk.Button(self.frame_vyhledat, width=30, text="Vyhledat záznamy", command=self.vyhledej)
        self.button_vyhledat.pack(side=LEFT)

        self.frame_mezera = tk.Frame()
        self.frame_mezera.pack()

        self.label_mez = tk.Label(self.frame_mezera, text="   ")
        self.label_mez.pack(side=LEFT)


        # Pridavani zaznamu
        self.frame_zaznam = tk.Frame()
        self.frame_zaznam.pack()

        self.cislo = StringVar()
        self.entry_cislo = ttk.Entry(self.frame_zaznam, width=28, textvariable=self.cislo)
        self.entry_cislo.pack(side=LEFT)


        self.X = StringVar()
        self.entry_X = ttk.Entry(self.frame_zaznam, width=19, textvariable=self.X)
        self.entry_X.pack(side=LEFT)


        self.Y = StringVar()
        self.entry_Y = ttk.Entry(self.frame_zaznam, width=19, textvariable=self.Y)
        self.entry_Y.pack(side=LEFT)


        self.draha = StringVar()
        self.entry_draha = ttk.Entry(self.frame_zaznam, width=19, textvariable=self.draha)
        self.entry_draha.pack(side=LEFT)


        self.vyseky = StringVar()
        self.entry_vyseky = ttk.Entry(self.frame_zaznam, width=19, textvariable=self.vyseky)
        self.entry_vyseky.pack(side=LEFT)


        self.krizeni = StringVar()
        self.entry_krizeni = ttk.Entry(self.frame_zaznam, width=32, textvariable=self.krizeni)
        self.entry_krizeni.pack(side=LEFT)


        self.poznamka = StringVar()
        self.entry_poznamka = ttk.Entry(self.frame_zaznam, width=43, textvariable=self.poznamka)
        self.entry_poznamka.pack(side=LEFT)


        # tlačítko přidat záznam
        self.pridej_button = ttk.Button(self.frame_zaznam, text="Přidat", state=NORMAL, width=30, command=self.on_pridej)
        self.pridej_button.pack(side=LEFT)

        # Seznam zaznamu
        self.frame_seznam = tk.Frame()
        self.frame_seznam.pack()
        self.tree_zaznamy = ttk.Treeview(self.frame_seznam, columns=("cislo", "X", "Y", "draha", "vyseky", "krizeni", "poznamka"), height=40)

        self.tree_zaznamy.heading("#0", text="#")
        self.tree_zaznamy.column("#0", minwidth=0, width=50, stretch=NO)

        self.tree_zaznamy.heading("cislo", text="Číslo")
        self.tree_zaznamy.column("cislo", minwidth=0, width=120, stretch=NO)

        self.tree_zaznamy.heading("X", text="X")
        self.tree_zaznamy.column("X", minwidth=0, width=120)
        self.tree_zaznamy.pack()

        self.tree_zaznamy.heading("Y", text="Y")
        self.tree_zaznamy.column("Y", minwidth=0, width=120)
        self.tree_zaznamy.pack()

        self.tree_zaznamy.heading("draha", text="Dráha")
        self.tree_zaznamy.column("draha", minwidth=0, width=120)
        self.tree_zaznamy.pack()

        self.tree_zaznamy.heading("vyseky", text="Výseky")
        self.tree_zaznamy.column("vyseky", minwidth=0, width=120)
        self.tree_zaznamy.pack()

        self.tree_zaznamy.heading("krizeni", text="Křížení")
        self.tree_zaznamy.column("vyseky", minwidth=0, width=120)
        self.tree_zaznamy.pack()

        self.tree_zaznamy.heading("poznamka", text="Poznámka")
        self.tree_zaznamy.column("poznamka", minwidth=0, width=450)
        self.tree_zaznamy.pack()

        # Tlačítka operací
        self.frame_operace = tk.Frame()
        self.frame_operace.pack()

        self.smaz_button = ttk.Button(self.frame_operace, text="Smazat záznam", state=NORMAL, command=self.on_smaz)
        self.smaz_button.pack()


    def on_smaz(self):
        if self.auslegung.odemceno == True:
            if self.tree_zaznamy.focus():
                index = int(self.tree_zaznamy.item(self.tree_zaznamy.focus())["text"])
                self.auslegung.smaz(index)
                self.auslegung.uloz(self.auslegung.nazev_soubor)
                self.zobraz()
        else:
            tk.messagebox.showwarning("Smazat", "Nemáš oprávnění.")


    def nacti(self):
        # self.auslegung.pristup() # zapíše do logu přístup uživatele
        if self.auslegung.zaznamy == []:
            self.auslegung.nacti_soubor()
            self.zobraz()


    def vyhledej(self):
        self.auslegung.zaznamy = []
        auslegung.nacti_soubor()
        self.auslegung.nalezeno = []
        self.auslegung.hledam_nuz = self.cislo_noze.get()
        self.auslegung.vyhledat(self.auslegung.hledam_nuz)
        self.zobraz_nalezene()
        self.cislo_noze.set("")


    def on_pridej(self):
        if self.auslegung.odemceno == True:
            self.auslegung.zaznamy == [] # test
            self.auslegung.sifrovane_zaznamy == []
            self.nacti()
            
            self.auslegung.pridej_zaznam(
                                self.cislo.get(),
                                self.X.get(),
                                self.Y.get(),
                                self.draha.get(),
                                self.vyseky.get(),
                                self.krizeni.get(),
                                self.poznamka.get())

            self.zobraz()
            self.cislo.set("")
            self.X.set("")
            self.Y.set("")
            self.draha.set("")
            self.vyseky.set("")
            self.krizeni.set("")
            self.poznamka.set("")
            self.auslegung.zaznamy = []
            self.auslegung.nacti_soubor()
            self.zobraz()

        else:
            tk.messagebox.showwarning("Přidej", "Nemáš oprávnění.")
            self.cislo.set("")
            self.X.set("")
            self.Y.set("")
            self.draha.set("")
            self.vyseky.set("")
            self.krizeni.set("")
            self.poznamka.set("")


    def on_close(self):
        self.parent.destroy()


    def zobraz(self):

        for ii in self.tree_zaznamy.get_children():
            self.tree_zaznamy.delete(ii)

        pozice = 0
        for zaznam in self.auslegung.zaznamy:
            self.tree_zaznamy.insert("", "end", text=pozice, values=zaznam)
            pozice += 1


    def zobraz_nalezene(self):
        # for ii in self.tree_nalezeno.get_children():
            # self.tree_nalezeno.delete(ii)
        self.auslegung.zaznamy = []
        self.zobraz()
        for zaznam in self.auslegung.nalezeno:
            self.tree_zaznamy.insert("", "end",
                                 text=f"{len(self.tree_zaznamy.get_children())}",
                                 values=zaznam)

if __name__ == '__main__':
    root = tk.Tk()
    auslegung = Auslegung()
    app = AuslegungGUI(root, auslegung)
    app.mainloop()