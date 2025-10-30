import tkinter as tk
from tkinter import *

varNames = ["Rent", "LowesHD", "Electrical", "Phone", "Internet", "Cable", "Server", "Cell",
            "Computer", "OfficeSup", "Travel", "Hotel", "CarIns", "CarRepair", "Gas", "HealthC",
            "SMarket", "Food", "Clothing", "Tuition", "Books", "Bank", "QBOnline", "MoneyIn", "MoneyOut",
            "FLTaxes"]
for n in varNames:
    globals()['lable_{}'.format(n)] = ""
    globals()['edit_{}'.format(n)] = ""

class NewWindow(tk.Toplevel):
    def __init__(self, parent):
        global varNames
        super().__init__(parent)
        self.title("Open Search Filters")
        self.geometry("1180x900")

        r = 0
        c = 0
        root = self

        menubar = Menu(root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save", command=root.save)
        filemenu.add_command(label="Close", command=root.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        f_var = open("fileval.txt", "r")
        f_content = f_var.read()

        for n in varNames:
            vVar_l = "lable_" + n
            vVar_e = "edit_" + n

            globals()[vVar_l] = tk.Label(self, text=n)
            globals()[vVar_l].grid(row=r, column=c)
            globals()[vVar_e] = tk.Text(self, width=47, height=4)
            globals()[vVar_e].grid(row=r + 1, column=c, padx=5, pady=5)

            for f_arr in f_content.split(";"):
                f_arr1 = f_arr.split("=")
                if f_arr1[0] == n:
                    globals()[vVar_e].insert(tk.END, f_arr1[1])

            c += 1
            if c == 3:
                c = 0
                r += 2

        root.config(menu=menubar)
        root.mainloop()

    def save(self):
        global varNames
        semi = ";"
        v_cnt = 1
        f_Var = open("fileval.txt", "w")
        f_Var.close()
        f_Var = open("fileval.txt", "a")
        for n in varNames:
            vVar_e = "edit_" + n
            txtbox = globals()[vVar_e].get("1.0", 'end-1c')
            if v_cnt == len(varNames):
                semi = ""
            box_var = n + "=" + txtbox + semi
            f_Var.write(box_var)
            v_cnt += 1
        f_Var.close()