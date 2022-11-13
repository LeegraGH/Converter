from tkinter import *
import tkinter.ttk as ttk
import datetime
import urllib.request
import xml.dom.minidom
import locale
from dateutil.relativedelta import relativedelta
import matplotlib
import matplotlib.pyplot as plt

locale.setlocale(locale.LC_ALL, 'ru_RU.utf8')

final_val = None


def clickForConvert():
    global final_val
    currency1 = val1.get()
    currency2 = val2.get()
    value1 = ""
    value2 = ""
    nominal1 = ""
    nominal2 = ""
    val_list = dom.getElementsByTagName('Value')
    nom_list = dom.getElementsByTagName('Nominal')
    if currency1 == "Российский рубль":
        value1 = "1"
        nominal1 = 1
    if currency2 == "Российский рубль":
        value2 = "1"
        nominal2 = 1
    for i in range(len(nrub_listValues)):
        if nrub_listValues[i] == currency1:
            value1 = val_list[i].firstChild.nodeValue
            value1 = value1.replace(",", ".")
            nominal1 = nom_list[i].firstChild.nodeValue
        if nrub_listValues[i] == currency2:
            value2 = val_list[i].firstChild.nodeValue
            value2 = value2.replace(",", ".")
            nominal2 = nom_list[i].firstChild.nodeValue
    if enter.get() == "":
        return
    num = float(enter.get())
    temp1 = float(value1) / float(nominal1) * num
    temp2 = float(value2) / float(nominal2)
    final = temp1 / temp2
    if final_val is None:
        final_val = Label(tab1, text=final)
        final_val.grid(column=1, row=1)
    else:
        final_val.grid_forget()
        final_val = Label(tab1, text=final)
        final_val.grid(column=1, row=1)


def clickPeriod():
    that_period = r_var.get()
    if that_period == 1:
        choice1.grid(column=2, row=1)
        choice2.grid_forget()
        choice3.grid_forget()
        choice4.grid_forget()
    elif that_period == 2:
        choice2.grid(column=2, row=2)
        choice1.grid_forget()
        choice3.grid_forget()
        choice4.grid_forget()
    elif that_period == 3:
        choice3.grid(column=2, row=3)
        choice1.grid_forget()
        choice2.grid_forget()
        choice4.grid_forget()
    elif that_period == 4:
        choice4.grid(column=2, row=4)
        choice1.grid_forget()
        choice2.grid_forget()
        choice3.grid_forget()


def buildSchedule():
    currency = val.get()
    that_period = r_var.get()
    if that_period == 1:
        graf_day = choice1.get()[0:10]
        graf_day = graf_day.split(".")
        date_day = datetime.date(int(graf_day[2]), int(graf_day[1]), int(graf_day[0]))
        res_days = []
        res_val = []
        for i in range(7):
            write_day = date_day.strftime("%d/%m/%Y")
            graf_date = date_day.strftime("%d %b")
            date_values = urllib.request.urlopen("https://www.cbr.ru/scripts/XML_daily.asp?date_req=" + write_day)
            dom_val = xml.dom.minidom.parse(date_values)
            dom_val.normalize()
            val_list = dom_val.getElementsByTagName('Value')
            nom_list = dom_val.getElementsByTagName('Nominal')
            res_days.append(graf_date)
            for j in range(len(nrub_listValues)):
                if nrub_listValues[j] == currency:
                    value = val_list[j].firstChild.nodeValue
                    value = float(value.replace(",", "."))
                    nominal = float(nom_list[j].firstChild.nodeValue)
                    res_val.append(value / nominal)
                    break
            date_day = date_day + datetime.timedelta(days=1)
        canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=tab2)
        plot_widget = canvas.get_tk_widget()
        fig.clear()
        plt.plot(res_days, res_val, marker="o")
        plt.grid()
        plot_widget.grid(column=3, row=5, padx=10, pady=20)
    elif that_period == 2:
        month_list = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь',
                      'Ноябрь', 'Декабрь']
        graf_month = choice2.get()
        temp_date = graf_month.split()
        for i in range(len(month_list)):
            if temp_date[0] == month_list[i]:
                graf_month = i + 1
        date_month = datetime.date(int(temp_date[1]), int(graf_month), 1)
        res_month = []
        res_val = []
        for i in range(31):
            write_month = date_month.strftime("%d/%m/%Y")
            graf_date = date_month.strftime("%d")
            date_values = urllib.request.urlopen("https://www.cbr.ru/scripts/XML_daily.asp?date_req=" + write_month)
            dom_val = xml.dom.minidom.parse(date_values)
            dom_val.normalize()
            val_list = dom_val.getElementsByTagName('Value')
            nom_list = dom_val.getElementsByTagName('Nominal')
            res_month.append(graf_date)
            for j in range(len(nrub_listValues)):
                if nrub_listValues[j] == currency:
                    value = val_list[j].firstChild.nodeValue
                    value = float(value.replace(",", "."))
                    nominal = float(nom_list[j].firstChild.nodeValue)
                    res_val.append(value / nominal)
                    break
            if datetime.date.today().strftime("%B") == temp_date[0] and datetime.date.today().strftime(
                    "%d") == graf_date:
                break
            date_month = date_month + relativedelta(days=1)
            if str(date_month.month) != write_month[4:5]:
                break
        canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=tab2)
        plot_widget = canvas.get_tk_widget()
        fig.clear()
        plt.plot(res_month, res_val, marker="o")
        plt.grid()
        plot_widget.grid(column=3, row=5, padx=10, pady=20)
    elif that_period == 3:
        quarter_list = ['I', 'II', 'III', 'IV']
        graf_quarter = choice3.get()
        temp_date = graf_quarter.split()
        if temp_date[0] == quarter_list[0]:
            date_quarter = datetime.date(int(temp_date[2]), 1, 1)
            check = [1, 2, 3]
        elif temp_date[0] == quarter_list[1]:
            date_quarter = datetime.date(int(temp_date[2]), 4, 1)
            check = [4, 5, 6]
        elif temp_date[0] == quarter_list[2]:
            date_quarter = datetime.date(int(temp_date[2]), 7, 1)
            check = [7, 8, 9]
        else:
            date_quarter = datetime.date(int(temp_date[2]), 10, 1)
            check = [10, 11, 12]
        res_quarter = []
        res_val = []
        while True:
            write_month = date_quarter.strftime("%d/%m/%Y")
            graf_date = date_quarter.strftime("%d.%m")
            date_values = urllib.request.urlopen("https://www.cbr.ru/scripts/XML_daily.asp?date_req=" + write_month)
            dom_val = xml.dom.minidom.parse(date_values)
            dom_val.normalize()
            val_list = dom_val.getElementsByTagName('Value')
            nom_list = dom_val.getElementsByTagName('Nominal')
            res_quarter.append(graf_date)
            for j in range(len(nrub_listValues)):
                if nrub_listValues[j] == currency:
                    value = val_list[j].firstChild.nodeValue
                    value = float(value.replace(",", "."))
                    nominal = float(nom_list[j].firstChild.nodeValue)
                    res_val.append(value / nominal)
                    break
            date_quarter = date_quarter + relativedelta(days=5)
            if datetime.date.today().year == date_quarter.year and (
                    datetime.date.today().month < date_quarter.month or datetime.date.today().month == date_quarter.month
                    and datetime.date.today().day < date_quarter.day):
                break
            if date_quarter.month not in check:
                break
        canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=tab2)
        plot_widget = canvas.get_tk_widget()
        fig.clear()
        plt.plot(res_quarter, res_val, marker="o")
        plt.grid()
        plot_widget.grid(column=3, row=5, padx=10, pady=20)
    elif that_period == 4:
        graf_year = choice4.get()
        date_year = datetime.date(int(graf_year), 1, datetime.date.today().day)
        res_year = []
        res_val = []
        for i in range(12):
            write_year = date_year.strftime("%d/%m/%Y")
            graf_date = date_year.strftime("%b")
            date_values = urllib.request.urlopen("https://www.cbr.ru/scripts/XML_daily.asp?date_req=" + write_year)
            dom_val = xml.dom.minidom.parse(date_values)
            dom_val.normalize()
            val_list = dom_val.getElementsByTagName('Value')
            nom_list = dom_val.getElementsByTagName('Nominal')
            res_year.append(graf_date)
            for j in range(len(nrub_listValues)):
                if nrub_listValues[j] == currency:
                    value = val_list[j].firstChild.nodeValue
                    value = float(value.replace(",", "."))
                    nominal = float(nom_list[j].firstChild.nodeValue)
                    res_val.append(value / nominal)
                    break
            if datetime.date.today().strftime("%Y") == graf_year and datetime.date.today().strftime("%b") == graf_date:
                break
            date_year = date_year + relativedelta(months=1)
        canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=tab2)
        plot_widget = canvas.get_tk_widget()
        fig.clear()
        plt.plot(res_year, res_val, marker="o")
        plt.grid()
        plot_widget.grid(column=3, row=5, padx=10, pady=20)


def validate(new_value):
    if new_value in "0123456789.":
        return True
    return False


def quarterCheck(date):
    if date.month <= 3:
        return "I квартал " + date.strftime("%Y")
    if date.month <= 6:
        return "II квартал " + date.strftime("%Y")
    if date.month <= 9:
        return "III квартал " + date.strftime("%Y")
    else:
        return "IV квартал " + date.strftime("%Y")


window = Tk()
window.geometry("500x250")
window.title("Конвертер валют")
tab_control = ttk.Notebook(window)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab_control.add(tab1, text="Калькулятор валют")
tab_control.add(tab2, text="Динамика курса")
listValues = ["Российский рубль"]
nrub_listValues = []

date_req = datetime.date.today()
today = date_req.strftime("%d/%m/%Y")
todayValues = urllib.request.urlopen("https://www.cbr.ru/scripts/XML_daily.asp?date_req=" + today)
dom = xml.dom.minidom.parse(todayValues)
dom.normalize()
nodeArray = dom.getElementsByTagName('Name')
for node in nodeArray:
    listValues.append(node.firstChild.nodeValue)
    nrub_listValues.append(node.firstChild.nodeValue)
listValues.sort()

val1 = ttk.Combobox(tab1, values=listValues, state="readonly", width=25)
val1.current(0)
val1.grid(column=0, row=0, padx=10, pady=5)
val2 = ttk.Combobox(tab1, values=listValues, state="readonly", width=25)
val2.current(0)
val2.grid(column=0, row=1, padx=10, pady=20)
button_convert = ttk.Button(tab1, text="Конвертировать", command=clickForConvert)
button_convert.grid(column=3, row=0, padx=5, pady=5)
vcmd = (window.register(validate), "%S")
enter = Entry(tab1, validate='key', validatecommand=vcmd)
enter.grid(column=1, row=0, padx=10, pady=5)

val = ttk.Combobox(tab2, state="readonly", values=nrub_listValues, width=25)
val.current(0)
val.grid(column=0, row=1, padx=5, pady=5)
lbl2 = Label(tab2, text="Валюта", padx=10)
lbl2.grid(column=0, row=0)
lbl3 = Label(tab2, text="Период", padx=25)
lbl3.grid(column=1, row=0)
r_var = IntVar()
r_var.set(0)
period = ttk.Combobox(tab2, state="readonly")

listTime1 = [(date_req + datetime.timedelta(days=1, weeks=-1)).strftime(
    "%d.%m.%Y") + "-" + date_req.strftime("%d.%m.%Y"),
             (date_req + datetime.timedelta(days=1, weeks=-2)).strftime("%d.%m.%Y") + "-" + (
                     date_req + datetime.timedelta(weeks=-1)).strftime("%d.%m.%Y"),
             (date_req + datetime.timedelta(days=1, weeks=-3)).strftime("%d.%m.%Y") + "-" + (
                     date_req + datetime.timedelta(weeks=-2)).strftime("%d.%m.%Y"),
             (date_req + datetime.timedelta(days=1, weeks=-4)).strftime("%d.%m.%Y") + "-" + (
                     date_req + datetime.timedelta(weeks=-3)).strftime("%d.%m.%Y")]
choice1 = ttk.Combobox(tab2, state="readonly", values=listTime1)
choice1.current(0)
week = Radiobutton(tab2, value=1, variable=r_var, text="Неделя", command=clickPeriod)
week.grid(column=1, row=1)

listTime2 = [date_req.strftime("%B %Y"), (date_req + relativedelta(months=-1)).strftime("%B %Y"),
             (date_req + relativedelta(months=-2)).strftime("%B %Y"),
             (date_req + relativedelta(months=-3)).strftime("%B %Y")]
choice2 = ttk.Combobox(tab2, state="readonly", values=listTime2)
choice2.current(0)
month = Radiobutton(tab2, value=2, variable=r_var, text="Месяц", command=clickPeriod)
month.grid(column=1, row=2)

listTime3 = [quarterCheck(date_req), quarterCheck(date_req + relativedelta(months=-3)),
             quarterCheck(date_req + relativedelta(months=-6)), quarterCheck(date_req + relativedelta(months=-9))]
choice3 = ttk.Combobox(tab2, state="readonly", values=listTime3)
choice3.current(0)
quarter = Radiobutton(tab2, value=3, variable=r_var, text="Квартал", command=clickPeriod)
quarter.grid(column=1, row=3)

listTime4 = [date_req.strftime("%Y"), (date_req + relativedelta(years=-1)).strftime("%Y"),
             (date_req + relativedelta(years=-2)).strftime("%Y"),
             (date_req + relativedelta(years=-3)).strftime("%Y")]
choice4 = ttk.Combobox(tab2, state="readonly", values=listTime4)
choice4.current(0)
year = Radiobutton(tab2, value=4, variable=r_var, text="Год", command=clickPeriod)
year.grid(column=1, row=4)

lbl4 = Label(tab2, text="Выбор периода", padx=30)
lbl4.grid(column=2, row=0)

# График
matplotlib.use("TkAgg")
fig = plt.figure(figsize=(11, 5))
button_build = ttk.Button(tab2, text="Построить график", command=buildSchedule)
button_build.grid(column=0, row=4)

tab_control.pack(expand=1, fill="both")
window.mainloop()
