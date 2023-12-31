import kivy
from kivymd.app import MDApp

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivymd.uix.pickers import MDDatePicker

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.uix.popup import Popup

import sqlite3
from datetime import datetime, timedelta
import ast

lijst_dagen = []
dagen_popup = []
TotCF = ""


class Navbar(Screen):
    pass

class BootScreen(Screen):
    pass


class Dashboard(Screen):
    def change(self):
        app = MDApp.get_running_app()
        app.call_cf()

    def on_enter(self):
        cijferlijst = Scorro.show_cijfers(self)
        cijferlijst.sort(key=lambda x: x[4])

        lay = self.ids.LayCf
        lay.clear_widgets()
        cf_size = int(int(Window.size[1]) / 20)
        vak_size = int(int(Window.size[1]) / 50)
        w = int(int(Window.size[0]) / 3)

        if cijferlijst != []:
            if len(cijferlijst) >= 3:
                l1 = Button(markup=True, text="[size={}]{}[/size]\n[size={}]{}[/size]".format(cf_size, cijferlijst[0][0], vak_size, cijferlijst[0][3]),
                    halign="center", size_hint_x=None, width=w, valign="center")
                l1.bind(size=l1.setter('text_size'))
                l1.bind(on_release=lambda x: self.change())
                lay.add_widget(l1)

                l2 = Button(markup=True, text="[size={}]{}[/size]\n[size={}]{}[/size]".format(cf_size, cijferlijst[1][0], vak_size, cijferlijst[1][3]),
                halign="center", size_hint_x=None, width=w, valign="center")
                l2.bind(size=l2.setter('text_size'))
                l2.bind(on_release=lambda x: self.change())
                lay.add_widget(l2)

                l3 = Button(markup=True, text="[size={}]{}[/size]\n[size={}]{}[/size]".format(cf_size, cijferlijst[2][0], vak_size, cijferlijst[2][3]),
                halign="center", size_hint_x=None, width=w, valign="center")
                l3.bind(size=l3.setter('text_size'))
                l3.bind(on_release=lambda x: self.change())
                lay.add_widget(l3)
            elif len(cijferlijst) == 2:
                l1 = Button(markup=True, text="[size={}]{}[/size]\n[size={}]{}[/size]".format(cf_size, cijferlijst[0][0], vak_size, cijferlijst[0][3]),
                halign="center", size_hint_x=None, width=w, valign="center")
                l1.bind(size=l1.setter('text_size'))
                l1.bind(on_release=lambda x: self.change())
                lay.add_widget(l1)

                l2 = Button(markup=True, text="[size={}]{}[/size]\n[size={}]{}[/size]".format(cf_size, cijferlijst[1][0], vak_size, cijferlijst[1][3]),
                halign="center", size_hint_x=None, width=w, valign="center")
                l2.bind(size=l2.setter('text_size'))
                l2.bind(on_release=lambda x: self.change())
                lay.add_widget(l2)

                l3 = Button()
                lay.add_widget(l3)
            elif len(cijferlijst) == 1:
                l1 = Button(markup=True, text="{}\n[size={}]{}[/size]".format(cijferlijst[0][0], vak_size, cijferlijst[0][3]),
                halign="center", size_hint_x=None, width=w, valign="center")
                l1.bind(size=l1.setter('text_size'))
                l1.bind(on_release=lambda x: self.change())
                lay.add_widget(l1)

                l2 = Button()
                lay.add_widget(l2)
                
                l3 = Button()
                lay.add_widget(l3)


class Planning(Screen):
    pass

class PopupSW(Popup):
    def on_open(self):
        naam = self.title.split(" - ")[0]

        conn = sqlite3.connect('ScorroDB.db')
        c = conn.cursor()

        c.execute(f"SELECT * FROM huiswerk WHERE naam = '{naam}'")
        records = c.fetchall()

        conn.commit()
        conn.close()
        if str(records) != "[]":
            records = ast.literal_eval(str(records).replace("(","").replace(")",""))
            self.ids.naam_hwP.text = records[0]
            self.ids.datum_hwP.text = records[1]
            self.ids.kiesvakHwP.text = records[3]
            self.ids.info_hwP.text = records[2]
        else:
            conn = sqlite3.connect('ScorroDB.db')
            c = conn.cursor()

            c.execute(f"SELECT * FROM proefwerken WHERE naam = '{naam}'")
            records = c.fetchall()

            conn.commit()
            conn.close()
            
            records = ast.literal_eval(str(records).replace("(","").replace(")",""))
            self.ids.naam_hwP.text = records[0]
            self.ids.datum_hwP.text = records[1]
            self.ids.kiesvakHwP.text = records[3]
            self.ids.info_hwP.text = records[2]

    #functies datepicker
    def get_date(self, instance, value, date_range):
        d = str(value).split("-")
        d1 = d[2]
        d2 = d[1]
        d3 = d[0]
        date = str(d1 + "-" + d2 + "-" + d3)
        self.ids.datum_hwP.text = date

    def kies_datum_HwP(self):
        date = self.ids.datum_hwP.text.split("-")
        day = int(date[0])
        month = int(date[1])
        year = int(date[2])
        date_dialog = MDDatePicker(year=year, month=month, day=day)
        date_dialog.bind(on_save=self.get_date)
        date_dialog.open()
        Window.size = (1, 1)
        Window.size = (350, 600)
    
    #functies bewerken
    def verwijderHw(self):
        naam = self.title.split(" - ")[0]

        conn = sqlite3.connect('ScorroDB.db')
        c = conn.cursor()

        c.execute(f"SELECT * FROM huiswerk WHERE naam = '{naam}'")
        records = c.fetchall()
        if str(records) != "[]":
            c.execute(f"DELETE FROM huiswerk WHERE naam = '{naam}'")
        else:
            c.execute(f"DELETE FROM proefwerken WHERE naam = '{naam}'")

        conn.commit()
        conn.close()

        schoolwerk_screen = MDApp.get_running_app().root.get_screen("schoolwerk").ids.BoxHwPw
        
        for hw in schoolwerk_screen.children:
            if hw.text.split("\n")[0] == naam:
                schoolwerk_screen.remove_widget(hw)
        
        self.dismiss()
    
    def OW_hw(self):
        old_name = self.title.split(" - ")[0]
        new_name = self.ids.naam_hwP.text
        new_date = self.ids.datum_hwP.text
        new_vak = self.ids.kiesvakHwP.text
        new_info = self.ids.info_hwP.text

        if new_name != "" and new_date != "" and new_vak != "":
            conn = sqlite3.connect('ScorroDB.db')
            c = conn.cursor()

            c.execute(f"SELECT * FROM huiswerk WHERE naam = '{old_name}'")
            r = c.fetchall()
            if str(r) != "[]":
        
                c.execute("""UPDATE huiswerk SET
                    naam = :naam,
                    datum = :datum,
                    beschrijving = :info,
                    vak = :vak
                    WHERE naam = :old_name""",
                    {
                    'naam': new_name,
                    'datum': new_date,
                    'info': new_info,
                    'vak': new_vak,
                    'old_name': old_name,
                })
            else:
                c.execute("""UPDATE proefwerken SET
                    naam = :naam,
                    datum = :datum,
                    beschrijving = :info,
                    vak = :vak
                    WHERE naam = :old_name""",
                    {
                    'naam': new_name,
                    'datum': new_date,
                    'info': new_info,
                    'vak': new_vak,
                    'old_name': old_name,
                })

            conn.commit()
            conn.close()
            print("Opgeslagen")
            
            schoolwerk_screen = MDApp.get_running_app().root.get_screen("schoolwerk").ids.BoxHwPw
            t = new_name + "\n" + new_vak + " - " + new_date
            for hw in schoolwerk_screen.children:
                if hw.text.split("\n")[0] == old_name:
                    hw.text = t
            
            schoolwerk_screen.children.sort(reverse=True, key=lambda date: datetime.strptime(date.text.split("\n")[1].split(" - ")[1], "%d-%m-%Y"))
            self.dismiss()
        else:
            print("Je vergeet iets!")
    
    #functie spinner
    def spinnerHwP_clicked(self):
        data = Scorro.show_klassen(self)
        spinner = self.ids.kiesvakHwP
        spinner.values = [str(item[0]) for item in data]

class Schoolwerk(Screen):
    def popupSW(self, text):
        naam = text.split("\n")[0]
        popup = PopupSW(title=f"{naam} - aanpassen")
        popup.open()

    def on_enter(self):
        window_size = int(Window.size[1]) / 10
        self.ids.BoxHwPw.clear_widgets()

        pw_lijst = Scorro.show_proefwerken(self)
        for item in pw_lijst:
            replace = str(item).replace("(", "").replace(")", "").replace("'", "").split(", ")
            button = Button(text=str(replace[0] + "\n" + replace[3] + " - " + replace[1]), size_hint=(None, None), height=window_size, width=Window.size[0], on_press=lambda button: self.popupSW(button.text), background_color=(1,0,0,1))
            button.text_size = (button.width-(Window.size[0]/10), None)
            button.bind(size=button.setter('text_size'))
            self.ids.BoxHwPw.add_widget(button)
            
        hw_lijst = Scorro.show_huiswerk(self)
        for item in hw_lijst:
            replace = str(item).replace("(", "").replace(")", "").replace("'", "").split(", ")
            button = Button(text=str(replace[0] + "\n" + replace[3] + " - " + replace[1]), size_hint=(None, None), height=window_size, width=Window.size[0], on_press=lambda button: self.popupSW(button.text))
            button.text_size = (button.width-(Window.size[0]/10), None)
            button.bind(size=button.setter('text_size'))
            self.ids.BoxHwPw.add_widget(button)
        
        self.ids.BoxHwPw.children.sort(reverse=True, key=lambda date: datetime.strptime(date.text.split("\n")[1].split(" - ")[1], "%d-%m-%Y"))


class PopupVak(Popup):
    def on_open(self):
        dagen_popup.clear()
        naam = self.title.split(" - ")[0]

        conn = sqlite3.connect('ScorroDB.db')
        c = conn.cursor()

        c.execute(f"SELECT * FROM vakken WHERE naam = '{naam}'")
        records = c.fetchall()

        conn.commit()
        conn.close()

        colour_selec = (0,1,0,1)
        colour_deselec = (1,0,0,1)

        try:
            dagen = records[0][1].replace("[", "").replace("]", "").replace("'", "").split(", ")
            for dag in dagen:
                dagen_popup.append(dag)
            
            for dag in dagen_popup:
                self.ids[dag].background_color = colour_selec
        except:
            print("Geen dagen gevonden")

    def Savedag(self, dag):
        colour_selec = (0,1,0,1)
        colour_deselec = (1,0,0,1)
        if dag in dagen_popup:
            dagen_popup.remove(dag)
            self.ids[dag].background_color = colour_deselec
        else:
            dagen_popup.append(dag)
            self.ids[dag].background_color = colour_selec

    def OW_klas(self):
        text = self.ids.naam_vakAP.text
        old_name = self.title.split(" - ")[0]

        if dagen_popup != []:
            if text != "":
                conn = sqlite3.connect('ScorroDB.db')
                c = conn.cursor()
            
                dagen = str(dagen_popup)
                c.execute("""UPDATE vakken SET
                    naam = :naam,
                    dag = :dag
                    WHERE naam = :old_name""",
                    {
                    'naam': text,
                    'dag': str(dagen_popup),
                    'old_name': old_name,
                })

                conn.commit()
                conn.close()
                print("vak opgeslagen")

                dagen_popup.clear()
                
                vakken_screen = MDApp.get_running_app().root.get_screen("vakken").ids.BoxVakken
                for vak in vakken_screen.children:
                    if vak.text == old_name:
                        vak.text = text
                
                vakken_screen.children.sort(reverse=True, key=lambda x: x.text.lower())
                self.dismiss()
            else:
                print("Geen tekst")
        else:
            print("Geen dagen")

    def verwijderKlas(self):
        naam = self.title.split(" - ")[0]

        conn = sqlite3.connect('ScorroDB.db')
        c = conn.cursor()

        c.execute(f"DELETE FROM vakken WHERE naam = '{naam}'")

        conn.commit()
        conn.close()

        vakken_screen = MDApp.get_running_app().root.get_screen("vakken").ids.BoxVakken
        
        for vak in vakken_screen.children:
            if vak.text == naam:
                vakken_screen.remove_widget(vak)
        
        self.dismiss()


class Vakken(Screen):
    def popupVak(self, naam):
        popup = PopupVak(title=f"{naam} - vak aanpassen")
        popup.ids.naam_vakAP.text = naam
        popup.open()

    def on_enter(self):
        window_size = int(Window.size[1]) / 10
        vakken_lijst = Scorro.show_klassen(self)
        self.ids.BoxVakken.clear_widgets()

        for vak in vakken_lijst:
            button = Button(text=str(vak[0]), size_hint_y=None, height=window_size)
            button.bind(on_press=lambda button: self.popupVak(button.text))
            self.ids.BoxVakken.add_widget(button)
        
        self.ids.BoxVakken.children.sort(reverse=True, key=lambda x: x.text.lower())


class PopupCF(Popup):
    def on_open(self):
        global TotCF
        vak = self.title.split(" | ")[0]
        cijfer = self.title.split(" | ")[1]
        weging = self.title.split(" | ")[2].split(" - ")[0].replace("x", "")
        self.title = vak + " - cijfer aanpassen"

        TotCF = vak + "|" + cijfer + "|" + weging
    
        conn = sqlite3.connect('ScorroDB.db')
        c = conn.cursor()

        c.execute(f"SELECT * FROM cijfers WHERE cijfer = '{cijfer}' AND weging = '{weging}' AND vak = '{vak}'")
        records = c.fetchall()

        conn.commit()
        conn.close()

        records = str(records).replace("(", "").replace(")", "").replace("[", "").replace("]", "").replace("'", "").split(", ")
        self.ids.welkCF_p.text = records[0]
        self.ids.wegingCF_p.text = records[1] + "x"
        self.ids.infoCF_p.text = records[2]
        self.ids.kiesvakCF_p.text = records[3]

    def OW_cf(self):
        Ovak = TotCF.split("|")[0]
        Ocijfer = TotCF.split("|")[1]
        Oweging = TotCF.split("|")[2]

        cf = self.ids.welkCF_p.text
        weging = self.ids.wegingCF_p.text.replace("x", "")
        info = self.ids.infoCF_p.text
        vak = self.ids.kiesvakCF_p.text

        if cf != "" and weging != "" and vak != "":
            conn = sqlite3.connect('ScorroDB.db')
            c = conn.cursor()
        
            c.execute("""UPDATE cijfers SET
                cijfer = :cijfer,
                weging = :weging,
                beschrijving = :info,
                vak = :vak
                WHERE cijfer = :Ocijfer AND vak = :Ovak AND weging = :Oweging""",
                {
                'cijfer': cf,
                'weging': weging,
                'info': info,
                'vak': vak,
                'Ocijfer': Ocijfer,
                'Oweging': Oweging,
                'Ovak': Ovak,
            })

            conn.commit()
            conn.close()
            print("vak opgeslagen")

            
            cijfers_box = MDApp.get_running_app().root.get_screen("cijfers").ids.BoxCfVak
        
            for bu in cijfers_box.children:
                if bu.text.split(" - ")[0] == Ocijfer and bu.text.split(" - ")[1] == Ovak and bu.text.split(" - ")[2] == str(Oweging + "x"):
                    bu.text = cf + " - " + vak + " - " + weging + "x"
            
            cijfers_box.children.sort(reverse=True, key=lambda x: x.text)

            MDApp.get_running_app().root.get_screen("cijfers").update_TotGem()

            self.dismiss()
        else:
            print("Je vergeet iets!")

    def verwijdercf(self):
        vak = TotCF.split("|")[0]
        cijfer = TotCF.split("|")[1]
        weging = TotCF.split("|")[2]
        
        conn = sqlite3.connect('ScorroDB.db')
        c = conn.cursor()

        c.execute(f"DELETE FROM cijfers WHERE cijfer = '{cijfer}' AND weging = '{weging}' AND vak = '{vak}'")

        conn.commit()
        conn.close()

        cijfers_box = MDApp.get_running_app().root.get_screen("cijfers").ids.BoxCfVak
        
        for cf in cijfers_box.children:
            if cf.text.split(" - ")[0] == cijfer and cf.text.split(" - ")[1] == vak and cf.text.split(" - ")[2] == str(weging + "x"):
                cijfers_box.remove_widget(cf)

        MDApp.get_running_app().root.get_screen("cijfers").update_TotGem()

        self.dismiss()

    def spinnerCFp_clicked(self):
        data = Scorro.show_klassen(self)
        spinner = self.ids.kiesvakCF_p
        spinner.values = [str(item[0]) for item in data]


class Cijfers(Screen):
    def popupCF(self, naam):
        vak = naam.split(" - ")[1]
        cijfer = naam.split(" - ")[0]
        weging = naam.split(" - ")[2]
        popup = PopupCF(title=f"{vak} | {cijfer} | {weging} - cijfer aanpassen")
        popup.open()
    
    def update_TotGem(self):
        cijferlijst = Scorro.show_cijfers(self)
        if cijferlijst != []:
            tot = 0
            weg_t = 0
            for item in cijferlijst:
                tot += float(item[0].replace(",", ".")) * float(item[1].replace(",", "."))
                weg_t += float(item[1].replace(",", "."))
            
            tot2 = tot / weg_t
            self.ids.tot_gem.text = "Totale gemiddelde: " + str(round(tot2, 1)).replace(".", ",")
            if tot2 >= 5.5:
                self.ids.tot_gem.bg_colour = (0,1,0,1)
            else:
                self.ids.tot_gem.bg_colour = (1,0,0,1)

    def on_enter(self):
        self.ids.BoxCfVak.clear_widgets()
        window_size = int(Window.size[1]) / 20
        cijferlijst = Scorro.show_cijfers(self)
        cijferlijst.sort(key=lambda x: x[3].lower())

        for item in cijferlijst:
            button = Button(text=str(item[0] + " - " + item[3] + " - " + item[1] + "x"), size_hint_y=None, height=window_size)
            button.bind(on_press=lambda button: self.popupCF(button.text))
            self.ids.BoxCfVak.add_widget(button)
        
        self.update_TotGem()


dutch_to_numeric = {'maandag': 0, 'dinsdag': 1, 'woensdag': 2, 'donderdag': 3, 'vrijdag': 4, 'zaterdag': 5, 'zondag': 6}

def get_next_weekday(current_date, target_weekday):
    days_until_target = (target_weekday - current_date.weekday() + 7) % 7
    next_weekday = current_date + timedelta(days=days_until_target)
    return next_weekday

class NieuwHuiswerk(Screen):
    def get_date(self, instance, value, date_range):
        d = str(value).split("-")
        d1 = d[2]
        d2 = d[1]
        d3 = d[0]
        date = str(d1 + "-" + d2 + "-" + d3)
        self.ids.date_picker.text = date

    def kies_datumHW(self):
        date = self.ids.date_picker.text.split("-")
        year = int(date[2])
        month = int(date[1])
        day = int(date[0])
        date_dialog = MDDatePicker(year=year, month=month, day=day)
        date_dialog.bind(on_save=self.get_date)
        date_dialog.open()
        Window.size = (1, 1)
        Window.size = (350, 600)

    def spinnerHW_clicked(self):
        data = Scorro.show_klassen(self)
        spinner = self.ids.kiesvakHW
        spinner.values = [str(item[0]) for item in data]

    def enable_date(self):
        vak = self.ids.kiesvakHW.text
        if vak != "Selecteer een vak":
            self.ids.date_picker.disabled = False
        
            conn = sqlite3.connect('ScorroDB.db')
            c = conn.cursor()

            c.execute(f"SELECT * FROM vakken WHERE naam = '{vak}'")
            records = c.fetchall()

            conn.commit()
            conn.close()
            
            records = list(records[0])
            records[1] = ast.literal_eval(records[1])

            current_date = datetime.now()

            list_dates_days = []
            for day in records[1]:
                next_instance_day = get_next_weekday(current_date, target_weekday=dutch_to_numeric[day])
                list_dates_days.append(next_instance_day)
            
            closest_date = min(list_dates_days, key=lambda date: date - current_date).strftime("%d-%m-%Y")
            self.ids.date_picker.text = closest_date


class NieuwProefwerk(Screen):
    def get_date(self, instance, value, date_range):
        d = str(value).split("-")
        d1 = d[2]
        d2 = d[1]
        d3 = d[0]
        date = str(d1 + "-" + d2 + "-" + d3)
        self.ids.date_pickerPW.text = date

    def kies_datumPW(self):
        date = self.ids.date_pickerPW.text.split("-")
        year = int(date[2])
        month = int(date[1])
        day = int(date[0])
        date_dialog = MDDatePicker(year=year, month=month, day=day)
        date_dialog.bind(on_save=self.get_date)
        date_dialog.open()
        Window.size = (1, 1)
        Window.size = (350, 600)

    def spinnerPW_clicked(self):
        data = Scorro.show_klassen(self)
        spinner = self.ids.kiesvakPW
        spinner.values = [str(item[0]) for item in data]
    
    def enable_date(self):
        vak = self.ids.kiesvakPW.text
        if vak != "Selecteer een vak":
            self.ids.date_pickerPW.disabled = False
            
            conn = sqlite3.connect('ScorroDB.db')
            c = conn.cursor()

            c.execute(f"SELECT * FROM vakken WHERE naam = '{vak}'")
            records = c.fetchall()

            conn.commit()
            conn.close()
            
            records = list(records[0])
            records[1] = ast.literal_eval(records[1])

            current_date = datetime.now()

            list_dates_days = []
            for day in records[1]:
                next_instance_day = get_next_weekday(current_date, target_weekday=dutch_to_numeric[day])
                list_dates_days.append(next_instance_day)
            
            closest_date = min(list_dates_days, key=lambda date: date - current_date).strftime("%d-%m-%Y")
            self.ids.date_pickerPW.text = closest_date


class NieuwCijfer(Screen):
    def spinnerCF_clicked(self):
        data = Scorro.show_klassen(self)
        spinner = self.ids.kiesvakCF
        spinner.values = [str(item[0]) for item in data]


class NieuwVak(Screen):
    def on_enter(self):
        for item in lijst_dagen:
            lijst_dagen.remove(item)
        self.ids.maandag.background_color = (1,0,0,1)
        self.ids.dinsdag.background_color = (1,0,0,1)
        self.ids.woensdag.background_color = (1,0,0,1)
        self.ids.donderdag.background_color = (1,0,0,1)
        self.ids.vrijdag.background_color = (1,0,0,1)
        self.ids.zaterdag.background_color = (1,0,0,1)
        self.ids.zondag.background_color = (1,0,0,1)
        
    def hide_message(self):
        self.ids.BoxMessage.remove_widget(self.ids.BoxMessage.children[0])

    def SavedVak(self):
        text = self.ids.naam_vak.text
        if lijst_dagen != []:
            if text != "":
                message = Label(text="Vak opgeslagen!")
                self.ids.BoxMessage.add_widget(message)
                Clock.schedule_once(lambda x: self.hide_message(), 1.5)

    def Savedag(self, dag):
        colour_selec = (0,1,0,1)
        colour_deselec = (1,0,0,1)
        if dag in lijst_dagen:
            lijst_dagen.remove(dag)
            self.ids[dag].background_color = colour_deselec
        else:
            lijst_dagen.append(dag)
            self.ids[dag].background_color = colour_selec


class CijferBerekenen(Screen):
    def on_enter(self):
        self.refresh()

    def spinnerCFB_clicked(self):
        data = Scorro.show_klassen(self)
        spinner = self.ids.kiesvakCFB
        spinner.values = [str(item[0]) for item in data]
    
    def refresh(self):
        self.ids.BoxCF_WE.clear_widgets()
        self.ids.kiesvakCFB.text = "Selecteer een vak"
        self.ids.CF_BH.text = ""
        self.ids.welkCFW.text = ""
        self.ids.welkWEW.text = ""


    def vak_gekozen(self):
        vak = self.ids.kiesvakCFB.text
        self.ids.BoxCF_WE.clear_widgets()

        conn = sqlite3.connect('ScorroDB.db')
        c = conn.cursor()

        c.execute(f"SELECT * FROM cijfers WHERE vak = '{vak}'")
        records = c.fetchall()

        conn.commit()
        conn.close()
        
        window_size = int(Window.size[1]) / 20
        for item in records:
            l = Label(text=item[0], color=(0,0,0,1), size_hint_y=None, height=window_size)
            e = Label(text=str(item[1] + "x"), color=(0,0,0,1), size_hint_y=None, height=window_size)
            self.ids.BoxCF_WE.add_widget(l)
            self.ids.BoxCF_WE.add_widget(e)
        
    def bereken_cf(self):
        goal = float(self.ids.welkCFW.text.replace(",", "."))
        weg = float(self.ids.welkWEW.text.replace(",", ".").replace("x", "").replace("X", ""))
        if goal != "" and weg != "":

            conn = sqlite3.connect('ScorroDB.db')
            c = conn.cursor()

            c.execute(f"SELECT * FROM cijfers WHERE vak = '{self.ids.kiesvakCFB.text}'")
            records = c.fetchall()

            conn.commit()
            conn.close()

            tot = 0
            weg_t = 0
            for item in records:
                tot += float(item[1]) * float(item[0].replace(",", "."))
                weg_t += float(item[1])
            weg_t += weg
            grade_weg = goal * weg_t - tot
            grade_to_get = grade_weg / weg

            self.ids.CF_BH.text = str(round(grade_to_get, 1)).replace(".", ",")
        else:
            print("Wat is de weging / het cijfer?")


class WindowManager(ScreenManager):
    pass

class Scorro(MDApp):
    def call_cf(self):
        self.root.current = "cijfers"

    def build(self):
        self.icon = "Images/Logo.png"
        
        conn = sqlite3.connect('ScorroDB.db')
        c = conn.cursor()

        c.execute("""CREATE TABLE if not exists vakken(
            naam text,
            dag text)
        """)

        c.execute("""CREATE TABLE if not exists cijfers(
            cijfer text,
            weging text,
            beschrijving text,
            vak text,
            date text)
        """)

        c.execute("""CREATE TABLE if not exists proefwerken(
            naam text,
            datum text,
            beschrijving text,
            vak text)
        """)

        c.execute("""CREATE TABLE if not exists huiswerk(
            naam text,
            datum text,
            beschrijving text,
            vak text)
        """)

        conn.commit()
        conn.close()

        kv = Builder.load_file('testdl.kv')
        return kv

    def on_start(self):
        self.root.current = "dashboard"

    #functies voor klassen
    def submit_klas(self):
        global lijst_dagen
        text = self.root.get_screen('nieuw vak').ids.naam_vak.text
        if lijst_dagen != []:
            if text != "":
                #connect to database
                conn = sqlite3.connect('ScorroDB.db')
                c = conn.cursor()
            
                c.execute("INSERT INTO vakken VALUES (:naam, :dag)",
                {
                    'naam': self.root.get_screen('nieuw vak').ids.naam_vak.text,
                    'dag': str(lijst_dagen),
                })

                conn.commit()
                conn.close()
                
                #reset buttons
                lijst_dagen = []
                origin = self.root.get_screen('nieuw vak')
                origin.ids.maandag.background_color = (1,0,0,1)
                origin.ids.dinsdag.background_color = (1,0,0,1)
                origin.ids.woensdag.background_color = (1,0,0,1)
                origin.ids.donderdag.background_color = (1,0,0,1)
                origin.ids.vrijdag.background_color = (1,0,0,1)
                origin.ids.zaterdag.background_color = (1,0,0,1)
                origin.ids.zondag.background_color = (1,0,0,1)

                self.root.get_screen('nieuw vak').ids.naam_vak.text = ''
                print("vak opgeslagen")

            else:
                print("Geen tekst")
        else:
            print("Geen dagen")

    def show_klassen(self):
        conn = sqlite3.connect('ScorroDB.db')
        c = conn.cursor()

        c.execute("SELECT * FROM vakken")
        records = c.fetchall()

        conn.commit()
        conn.close()
        records.sort(key=lambda x: x[0].lower())
        return records

    #functies voor cijfers
    def submit_cijfer(self):
        naam = self.root.get_screen('nieuw cijfer').ids.welkCF.text
        weging = self.root.get_screen('nieuw cijfer').ids.wegingCF.text.replace("x", "").replace("X", "")
        vak = self.root.get_screen('nieuw cijfer').ids.kiesvakCF.text
        now = datetime.now()
        if naam != "":
            if weging != "":
                if vak != "Selecteer een vak":
                    conn = sqlite3.connect('ScorroDB.db')
                    c = conn.cursor()

                    c.execute("INSERT INTO cijfers VALUES (:cijfer, :weging, :beschrijving, :vak, :date)",
                    {
                        'cijfer': naam,
                        'weging': weging,
                        'beschrijving': self.root.get_screen('nieuw cijfer').ids.infoCF.text,
                        'vak': vak,
                        'date': now,
                    })


                    self.root.get_screen('nieuw cijfer').ids.welkCF.text = ''
                    self.root.get_screen('nieuw cijfer').ids.wegingCF.text = ''
                    self.root.get_screen('nieuw cijfer').ids.infoCF.text = ''
                    self.root.get_screen('nieuw cijfer').ids.kiesvakCF.text = 'Selecteer een vak'

                    conn.commit()
                    conn.close()
                else:
                    print("Selecteer een vak")
            else:
                print("Geef je cijfer een weging")
        else:
            print("Geef je cijfer")

    def show_cijfers(self):
        conn = sqlite3.connect('ScorroDB.db')
        c = conn.cursor()

        c.execute("SELECT * FROM cijfers")
        records = c.fetchall()

        conn.commit()
        conn.close()
        return records
    

    #functies voor proefwerken
    def submit_proefwerk(self):
        naam = self.root.get_screen('nieuw proefwerk').ids.welkPW.text
        datum = self.root.get_screen('nieuw proefwerk').ids.date_pickerPW.text
        vak = self.root.get_screen('nieuw proefwerk').ids.kiesvakPW.text
        beschrijving = self.root.get_screen('nieuw proefwerk').ids.infoPW.text
        if naam != "":
            if datum != "Kies Datum":
                if vak != "Selecteer een vak":
                    conn = sqlite3.connect('ScorroDB.db')
                    c = conn.cursor()

                    c.execute("INSERT INTO proefwerken VALUES (:naam, :datum, :beschrijving, :vak)",
                    {
                        'naam': naam,
                        'datum': datum,
                        'beschrijving': beschrijving,
                        'vak': vak,
                    })


                    self.root.get_screen('nieuw proefwerk').ids.welkPW.text = ''
                    self.root.get_screen('nieuw proefwerk').ids.date_pickerPW.text = 'Kies Datum'
                    self.root.get_screen('nieuw huiswerk').ids.date_pickerPW.disabled = True
                    self.root.get_screen('nieuw proefwerk').ids.infoPW.text = ''
                    self.root.get_screen('nieuw proefwerk').ids.kiesvakPW.text = 'Selecteer een vak'

                    conn.commit()
                    conn.close()
                else:
                    print("Selecteer een vak")
            else:
                print("Geef je proefwerk een datum")
        else:
            print("Geef je proefwerk een naam")
            
            
    def show_proefwerken(self):
        conn = sqlite3.connect('ScorroDB.db')
        c = conn.cursor()

        c.execute("SELECT * FROM proefwerken")
        records = c.fetchall()

        conn.commit()
        conn.close()
        return records
    

    #functies voor huiswerk
    def submit_huiswerk(self):
        naam = self.root.get_screen('nieuw huiswerk').ids.welkHW.text
        datum = self.root.get_screen('nieuw huiswerk').ids.date_picker.text
        vak = self.root.get_screen('nieuw huiswerk').ids.kiesvakHW.text
        beschrijving = self.root.get_screen('nieuw huiswerk').ids.infoHW.text

        if naam != "":
            if datum != "Kies Datum":
                if vak != "Selecteer een vak":
                    conn = sqlite3.connect('ScorroDB.db')
                    c = conn.cursor()

                    c.execute("INSERT INTO huiswerk VALUES (:naam, :datum, :beschrijving, :vak)",
                    {
                        'naam': naam,
                        'datum': datum,
                        'beschrijving': beschrijving,
                        'vak': vak,
                    })


                    self.root.get_screen('nieuw huiswerk').ids.welkHW.text = ''
                    self.root.get_screen('nieuw huiswerk').ids.date_picker.text = 'Kies Datum'
                    self.root.get_screen('nieuw huiswerk').ids.date_picker.disabled = True
                    self.root.get_screen('nieuw huiswerk').ids.infoHW.text = ''
                    self.root.get_screen('nieuw huiswerk').ids.kiesvakHW.text = 'Selecteer een vak'

                    conn.commit()
                    conn.close()
                else:
                    print("Selecteer een vak")
            else:
                print("Geef je toets een datum")
        else:
            print("Geef je toets een naam")

    def show_huiswerk(self):
        conn = sqlite3.connect('ScorroDB.db')
        c = conn.cursor()

        c.execute("SELECT * FROM huiswerk")
        records = c.fetchall()

        conn.commit()
        conn.close()
        return records

        
Window.size = (350, 600)
#Window.size = (233, 400)

if __name__ == "__main__":
    Scorro().run()