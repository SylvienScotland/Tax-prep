import fitz # this is pymupdf
import datetime as tmx
import tkinter as tk
import taxWin as mwin
import taxXL as xlwb
import tkinter.messagebox as tkmsg
from tkinter.filedialog import askopenfilename
from tkinter import ttk
import os
from csv import reader

date_f = "%m/%d/%Y"
line_flg = 0
float_cnt = 0
text_line = ""
text_month = ""
month_sel = 0
m_onths = ["--", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
month_sel = ""
box_dict = {}
text_box = ""
xl_file = ""
window = tk.Tk()

def load_boxdict():
    global box_dict
    box_dict = {"Rent": "", "LowesHD": "", "Electrical": "", "Phone": "", "Internet": "", "Cable": "", "Server": "",
                "Cell": "", "Computer": "", "OfficeSup": "", "Travel": "", "Hotel": "", "CarIns": "", "CarRepair": "",
                "Gas": "", "HealthC": "", "SMarket": "", "Food": "", "Clothing": "", "Tuition": "", "Books": "",
                "Bank": "", "QBOnline": "", "MoneyIn": "", "MoneyOut": "", "FLTaxes": ""}

def hello(msg):
   tkmsg.messagebox.showinfo("Message Box", msg)

def open_mywin():
    mwin.NewWindow(window)

def open_xlfile():
    """Open a Exel Work Book file for processing."""
    global xl_file
    xl_file = askopenfilename(filetypes=[("EXEL Spread Sheet", "*.xlsx")])
    if not xl_file:
        return
    fileName = os.path.basename(xl_file)
    btn_openxl.config(text="Exel: "+fileName)

def open_file():
    """Open a file for processing."""
    filepath = askopenfilename(filetypes=[("PDF Files", "*.pdf"),("CSV Files", "*.csv"),("All Files", "*.*")])
    if not filepath:
        return
    txt_edit.delete(1.0, tk.END)
    root_ext = os.path.splitext(filepath)
    if root_ext[1] == ".pdf":
        prep_pdf(filepath)
    else:
        if root_ext[1] == ".csv":
            prep_csv(filepath)

    window.title(f"Simple PDF Bank Taxes Processor - {filepath}")
    msglabel.config(text="")

def run_taxes():
    """Run the Taxes for a month"""
    global var_Names, text_box, box_dict
    line_no_mt = ""
    f_var = open("fileval.txt", "r")
    f_content = f_var.read()
    f_var.close()
    load_boxdict()
    dict_prnt = ""
    for tbox_line in text_box.lower().split("++"):
        for f_line in f_content.split(";"):
            l_arr = f_line.split("=")
            a_inx = l_arr[0]
            a_val = l_arr[1]
            mt = 0
            cnt = 0
            if a_val.count(",") > 0:
                a_val = a_val.lower().split(",")
                for l_str in a_val:
                     if tbox_line.find(l_str) > 0:
                        box_dict[a_inx] = box_dict[a_inx] + "+" + proc_amt(tbox_line)
                        mt = 1
                        break
                     else:
                        """l_strArr = l_str.split()
                        if len(l_strArr) > 1:
                            if tbox_line.find(l_strArr[0]) > 0 and tbox_line.find(l_strArr[1]) > 0:
                                box_dict[a_inx] = box_dict[a_inx] + "+" + proc_amt(tbox_line)
                                mt = 1
                                break"""
                        cnt += 1
            else:
                if a_val != "" and tbox_line.find(a_val) > 0:
                        box_dict[a_inx] = box_dict[a_inx] + "+" + proc_amt(tbox_line)
                        mt = 1
                        break
            if mt == 1:
                break
        if mt == 0:
            line_no_mt += tbox_line
    for x, y in box_dict.items():
        dict_prnt += x + "=" + y + "\n"
    dict_prnt += "\n"
    txt_edit.delete(1.0, tk.END)
    txt_edit.insert(tk.END, dict_prnt)
    txt_edit.insert(tk.END, line_no_mt)

def run_xls():
    """Run the Exel Spread Sheet"""
    global box_dict, xl_file
    xlw = xlwb.xlwbook()
    xlw.f_name = xl_file
    xlw.month_sel = month_sel.lower()
    xlw.w_dict = box_dict
    xlw.openbook()
    fin_msg = 'Done Running Exel for : ' + month_sel
    msglabel.config(text=fin_msg, foreground="red")

def proc_amt(f_text):
    #s_pos = f_text.find("$") + 1
    #e_pos1 = f_text.find("$", s_pos) - 1
    price_arr = f_text.split("$")
    return price_arr[1]

def fin():
    exit()

def run_search():
    """Run the search for a text"""
    txt_edit.tag_remove('found', '1.0', 'end-1c')
    s_str = txt_search.get("1.0", 'end-1c')
    if s_str:
        idx = '1.0'
        while 1:
            idx = txt_edit.search(s_str, idx, nocase=1, stopindex='end-1c')
            if not idx: break
            lastidx = '%s+%dc' % (idx, len(s_str))
            txt_edit.tag_add('found', idx, lastidx)
            idx = lastidx
        txt_edit.tag_config('found', foreground='red', font=("bold"))
        #msglabel.config(text="Search String Found",foreground="red")
    txt_edit.focus_set()

def validate(date_x):
    date_err = 0
    try:
        tmx.datetime.strptime(date_x, date_f)
    except:
        date_err = 1
    return date_err

def prep_csv(filepath):
    """Opens & Read csv File Line by Line and Display on Screen"""
    global line_flg, float_cnt, text_line
    text_line = ""
    with open(filepath, 'r') as f_var:
        csv_content = reader(f_var)
        header = next(csv_content)
        if header != None:
           for row in csv_content:
               row[3] = row[3].replace("$", "")
               dobj = tmx.datetime.strptime(row[0], "%m/%d/%Y").date()
               row[0] = dobj.strftime("%m/%d/%Y")
               text_line += row[0]+" "+row[1]+" "+row[3]+" "+row[4]+"++\n"

    text_line = text_line.replace("$+", "$")
    text_line = text_line.replace("(", "")
    text_line = text_line.replace(")", "")
    txt_edit.insert(tk.END, text_line)

def prep_pdf(filepath):
    """Opens & Read PDF File Line by Line and Display on Screen"""
    global line_flg, float_cnt, text_line
    text_line = ""
    with fitz.open(filepath) as doc:
        for page in doc:
            page_txt = page.getText()
            line_flg = 0
            float_cnt = 0
            for line_txt in page_txt.splitlines():
                if line_flg == 1:
                   if line_txt.find('$') != -1:
                      float_cnt += 1
                   if float_cnt == 2:
                      text_line += " " + line_txt + "++\n"
                      line_flg = 0
                      float_cnt = 0
                   else:
                       text_line += " " + line_txt
                else:
                    val_date = validate(line_txt)
                    if val_date == 0:
                       text_line += line_txt
                       line_flg = 1
                       float_cnt= 0
    txt_edit.insert(tk.END, text_line)

def proc_month(event):
    """Listing by Month In COMBOBOX"""
    global text_box, month_sel
    if m_sel.get() == "--":
       txt_edit.delete(1.0, tk.END)
       txt_edit.insert(tk.END, text_line)
    else:
        mnth_obj = tmx.datetime.strptime(m_sel.get(), "%b")
        mnth_sel = mnth_obj.month
        month_sel = m_sel.get()
        month_line = ""

        for line_txt in text_line.splitlines():
            line_month = line_txt[0:10]
            #print(mnth_sel)

            date_obj = tmx.datetime.strptime(line_month, date_f)
            if date_obj.month == mnth_sel:
                month_line += line_txt + "\n"
        txt_edit.delete(1.0, tk.END)
        txt_edit.insert(tk.END, month_line)
        text_box = txt_edit.get("1.0", 'end-1c')
        msglabel.config(text="")


"""******************** Main Screen Setup Routines **********************"""

window.title("Tax Preparation")
window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=800, weight=1)
window.geometry("1200x850")

h = tk.Scrollbar(window, orient='horizontal')
h.pack(side=tk.BOTTOM, fill=tk.X)

v = tk.Scrollbar(window)
v.pack(side=tk.RIGHT, fill=tk.Y)

txt_edit = tk.Text(window, width=1200, height=850, wrap=tk.NONE,xscrollcommand=h.set,yscrollcommand=v.set)

h.config(command=txt_edit.xview)
v.config(command=txt_edit.yview)

""" Set the frame window """
fr_buttons = tk.Frame(window, height=50, relief=tk.RAISED, bd=2)

""" Set the widgets for the combobox """
m_sel = ttk.Combobox(fr_buttons, width=8, values=m_onths)
m_sel.current(0)
m_sel.bind("<<ComboboxSelected>>", proc_month)

""" Set the widgets to the frame window """
btn_prop = tk.Button(fr_buttons, text="Open Search Filters", command=open_mywin)
btn_open = tk.Button(fr_buttons, text="Open a Bank File", command=open_file)
btn_openxl = tk.Button(fr_buttons, text="Open Exel Spread Sheet", command=open_xlfile)
label = tk.Label(fr_buttons, text="Select a Month:")
btn_runtax = tk.Button(fr_buttons, text="Run Taxes", command=run_taxes)
btn_runxls = tk.Button(fr_buttons, text="Run XL Spread Sheet", command=run_xls)
txt_search = tk.Text(fr_buttons, width=20, height=1)
btn_search = tk.Button(fr_buttons, text="Search", command=run_search)
msglabel = tk.Label(fr_buttons, text="")

btn_prop.grid(row=0, column=0, padx=5, pady=5)
btn_open.grid(row=0, column=1, padx=5, pady=5)
btn_openxl.grid(row=0, column=2, padx=5, pady=5)
label.grid(row=0, column=3)
m_sel.grid(row=0, column=4)
btn_runtax.grid(row=0, column=5, padx=10)
btn_runxls.grid(row=0, column=6, padx=10)
txt_search.grid(row=0, column=7, padx=10)
btn_search.grid(row=0, column=8, padx=5)
msglabel.grid(row=0, column=9, padx=20)

fr_buttons.pack(fill=tk.X)
txt_edit.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

window.mainloop()