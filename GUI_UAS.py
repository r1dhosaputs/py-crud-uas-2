# ======================
# imports
# ======================
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import Spinbox
import ToolTip as tt
from threading import Thread
from time import sleep
from queue import Queue
from tkinter import filedialog as fd
from os import path, makedirs
from tkinter import messagebox as mBox
from GUI_MySQL_class import MySQL

# Module level GLOBALS
GLOBAL_CONST = 42
fDir = path.dirname(__file__)
netDir = fDir + "\\Backup"
if not path.exists(netDir):
    makedirs(netDir, exist_ok=True)
WIDGET_LABEL = " Widgets Frame "


# ===================================================================
class OOP:
    def __init__(self):
        # Create instance
        self.win = tk.Tk()

        # Add a title
        self.win.title("Python GUI")

        # Disable resizing the window
        self.win.resizable(0, 0)

        # Create a Queue
        self.guiQueue = Queue()

        self.createWidgets()

        # populate Tab 2 Entries
        self.defaultFileEntries()

        # create MySQL instance
        self.mySQL = MySQL()
        
        self.msg = mBox

    def defaultFileEntries(self):
        self.fileEntry.delete(0, tk.END)
        self.fileEntry.insert(0, "Z:\\")  # bogus path
        self.fileEntry.config(state="readonly")

        self.netwEntry.delete(0, tk.END)
        self.netwEntry.insert(0, "Z:\\Backup")  # bogus path

    # Exit GUI cleanly
    def _quit(self):
        self.win.quit()
        self.win.destroy()
        exit()

    # Button callback
    def showData(self):
        show = self.mySQL.showData()
        self.tree.delete(*self.tree.get_children())

        for no, row in enumerate(show, start=1):
            # Mengabaikan kolom ID (indeks 0)
            row_str = "\t".join(map(str, row[1:]))
            # Menambahkan nomor urut sebagai prefix jadi nomor tambah hasil row
            row_with_number = f"{no}. {row_str}"
            # self.scr_txt.insert(tk.END, row_with_number + "\n")
            self.tree.insert(
                "", "end", values=row_with_number, tags=(row[0])
            )  # tags buat id biar tersembunyi dari read show
            
    def insertData(self):
        # title = self.bookTitle.get()
        # page = self.pageNumber.get()
        # quote = self.quote.get(1.0, tk.END)
        # print(title)
        # print(quote)
        # self.mySQL.insertBooks(title, page, quote)
        nama = self.enama.get()
        nim = self.enim.get()
        j_kelamin = self.j_kelamin.get()
        prodi = self.prodi_var.get()
        # print(nama, nim, gender, prodi)
        if nama and nim and j_kelamin and prodi :
            data = {
                "nama" : nama,
                "nim" :nim,
                "j_kelamin": j_kelamin,
                "prodi":prodi
            }
            
            self.mySQL.insertData(data)
            self.showData()
            
    def deleteSelected(self):
        selected = self.tree.selection()
        if selected:
            confirmation = self.msg.askyesno("Konfirmasi", "Yakin Ingin Menghapus?")
            if confirmation:
                item = self.tree.item(selected, "tags")
                id = item[0]
                self.mySQL.deleteData(id)
                self.showData()
                self.msg.showinfo("Info", "Data berhasil dihapus.")
            else:
                self.msg.showinfo("Info", "Baiklah")
        else:
            self.msg.showerror("Error", "Data Tidak Valid/Ditemukan")
            
    def updateSelected(self):
        # print('halo')
        selected = self.tree.selection()
        if selected:
            item_info = self.tree.item(selected)

            item_values = item_info["values"]
            item_tags = item_info["tags"]

            id = item_tags[0]
            nama = self.enama.get()
            nim = self.enim.get()
            j_kelamin = self.j_kelamin.get()
            prodi = self.prodi_var.get()

            # jika tidak di isi salah satu isi dengan yang lama
            if not nim:
                nim = item_values[1]
            
            if not nama:
                nama = item_values[2]

            if not j_kelamin:
                j_kelamin = item_values[3]

            if not prodi:
                prodi = item_values[4]
            
            data = {
                "id": id,
                "nama" : nama,
                "nim" :nim,
                "j_kelamin": j_kelamin,
                "prodi":prodi
            }

            if data:
                # print(name, nim, gender)
                # print(data)
                query = self.mySQL.updateData(data)
                if query == True:
                    self.msg.showinfo("Info", "Data Berhasil Diubah.")
                    self.showData()
            else:
                self.msg.showerror("Error", "Data Tidak Valid/Ditemukan")
        
           
    # Button callback
    # def getQuote(self):
    #     allBooks = self.mySQL.showBooks()
    #     print(allBooks)
    #     self.quote.insert(tk.INSERT, allBooks)

    # # Button callback
    # def modifyQuote(self):
    #     raise NotImplementedError(
    #         "This still needs to be implemented for the SQL command."
    #     )

    def new_DB(self):
        self.mySQL.createGuiDB()
        
    def new_Table(self):
        self.mySQL.createTables()
    
    #####################################################################################
    def createWidgets(self):
        # Tab Control introduced here --------------------------------------
        tabControl = ttk.Notebook(self.win)  # Create Tab Control

        tab1 = ttk.Frame(tabControl)  # Create a tab
        tabControl.add(tab1, text="MySQL")  # Add the tab

        tab2 = ttk.Frame(tabControl)  # Add a second tab
        tabControl.add(tab2, text="Widgets")  # Make second tab visible

        tabControl.pack(expand=1, fill="both")  # Pack to make visible
        # ~ Tab Control introduced here -----------------------------------------

        # We are creating a container frame to hold all other widgets
        self.mySQL = ttk.LabelFrame(tab1, text=" Data Mahasiswa ")
        self.mySQL.grid(column=0, row=0, padx=8, pady=4)

        # Creating a Label
        ttk.Label(self.mySQL, text="NIM").grid(column=0, row=0, sticky="W")

        # Adding a Textbox Entry widget
        nim = tk.StringVar()
        self.enim = ttk.Entry(self.mySQL, width=50, textvariable=nim)
        self.enim.grid(column=1, row=0, sticky="W", pady=10)

        # Creating a Label
        ttk.Label(self.mySQL, text="NAMA").grid(column=0, row=1, sticky="W")

        # Adding a Textbox Entry widget
        nama = tk.StringVar()
        self.enama = ttk.Entry(self.mySQL, width=50, textvariable=nama)
        self.enama.grid(column=1, row=1, sticky="W", pady=5)

        # Radio buttons for gender
        self.label_j_kelamin = ttk.Label(self.mySQL, text="J. Kelamin:")
        self.label_j_kelamin.grid(column=0, row=2, pady=5, sticky="W")

        self.j_kelamin = tk.StringVar()
        self.radio_male = ttk.Radiobutton(
            self.mySQL, text="Laki-Laki", variable=self.j_kelamin, value="Laki-Laki"
        )
        self.radio_male.grid(column=1, row=2, padx=5, pady=5, sticky="W")

        self.radio_female = ttk.Radiobutton(
            self.mySQL, text="Perempuan", variable=self.j_kelamin, value="Perempuan"
        )
        self.radio_female.grid(column=1, row=3, padx=5, pady=5, sticky="W")


        # Membuat Select Box dengan tk.StringVar untuk PRODI
        # Creating a Label
        ttk.Label(self.mySQL, text="Prodi").grid(column=0, row=4, sticky="W")
        options = [ "TI", "SI" ]
        self.prodi_var = tk.StringVar()
        self.select_box = ttk.Combobox(self.mySQL, values=options, width=50, textvariable=self.prodi_var)
        self.select_box.grid(row=4, column=1, pady=10,sticky="W")
        
        # Adding a Button
        self.action = ttk.Button(self.mySQL, text="Insert", command=self.insertData)
        self.action.grid(column=0, row=5)
        
        self.action2 = ttk.Button(self.mySQL, text="Update", command=self.updateSelected)
        self.action2.grid(column=1, row=5)
        
        self.action3 = ttk.Button(self.mySQL, text="Delete", command=self.deleteSelected)
        self.action3.grid(column=2, row=5)

        # # Adding a Button
        # self.action2 = ttk.Button(self.mySQL, text="Delete", command=self.modifyQuote)
        # self.action2.grid(column=2, row=5)

        # Add some space around each widget
        # for child in self.mySQL.winfo_children():
        #     child.grid_configure(padx=2, pady=4)

        # quoteFrame = ttk.LabelFrame(tab1, text=" Data ")
        # quoteFrame.grid(column=0, row=1, padx=8, pady=4)

        # Using a scrolled Text control
        # quoteW = 40
        # quoteH = 6
        # self.quote = scrolledtext.ScrolledText(
        #     quoteFrame, width=quoteW, height=quoteH, wrap=tk.WORD
        # )
        # self.quote.grid(column=0, row=8, sticky="WE", columnspan=3)

        # tabel pakai tree gabisa pakai scr text ulun pak :(
        # self.tree_col = ("No", "NIM", "NAMA", "Kelamin", "Prodi")
        self.tree_col = ("NO","NIM", "NAMA", "Kelamin", "Prodi")
        self.tree = ttk.Treeview(
            self.mySQL, columns=self.tree_col, show="headings", selectmode="browse"
        )
        
        for col in self.tree_col:
            self.tree.heading(col, text=col)
        self.tree.grid(row=8, column=0, columnspan=125, padx=10, pady=10, sticky="WE")

        # Add some space around each widget
        # for child in quoteFrame.winfo_children():
        #     child.grid_configure(padx=2, pady=4)











        # ======================================================================================================
        # Tab Control 2
        # ======================================================================================================
        # We are creating a container frame to hold all other widgets -- Tab2
        self.mySQL2 = ttk.LabelFrame(tab2, text=WIDGET_LABEL)
        self.mySQL2.grid(column=0, row=0, padx=8, pady=4)

        # Using a scrolled Text control
        scrolW = 40
        scrolH = 1
        self.scr = scrolledtext.ScrolledText(
            self.mySQL2, width=scrolW, height=scrolH, wrap=tk.WORD
        )
        self.scr.grid(column=0, row=8, sticky="WE", columnspan=3)

        # Create Manage Files Frame ------------------------------------------------
        mngFilesFrame = ttk.LabelFrame(tab2, text=" Manage Files: ")
        mngFilesFrame.grid(column=0, row=1, sticky="WE", padx=10, pady=5)

        # Button Callback
        def getFileName():
            print("hello from getFileName")
            fDir = path.dirname(__file__)
            fName = fd.askopenfilename(parent=self.win, initialdir=fDir)
            print(fName)
            self.fileEntry.config(state="enabled")
            self.fileEntry.delete(0, tk.END)
            self.fileEntry.insert(0, fName)

            if len(fName) > self.entryLen:
                self.fileEntry.config(width=len(fName) + 3)

        # Add Widgets to Manage Files Frame
        lb = ttk.Button(mngFilesFrame, text="Browse to File...", command=getFileName)
        lb.grid(column=0, row=0, sticky=tk.W)

        # -----------------------------------------------------
        file = tk.StringVar()
        self.entryLen = scrolW - 4
        self.fileEntry = ttk.Entry(
            mngFilesFrame, width=self.entryLen, textvariable=file
        )
        self.fileEntry.grid(column=1, row=0, sticky=tk.W)

        # -----------------------------------------------------
        logDir = tk.StringVar()
        self.netwEntry = ttk.Entry(
            mngFilesFrame, width=self.entryLen, textvariable=logDir
        )
        self.netwEntry.grid(column=1, row=1, sticky=tk.W)

        def copyFile():
            import shutil

            src = self.fileEntry.get()
            file = src.split("/")[-1]
            dst = self.netwEntry.get() + "\\" + file
            try:
                shutil.copy(src, dst)
                mBox.showinfo("Copy File to Network", "Succes: File copied.")
            except FileNotFoundError as err:
                mBox.showerror(
                    "Copy File to Network",
                    "*** Failed to copy file! ***\n\n" + str(err),
                )
            except Exception as ex:
                mBox.showerror(
                    "Copy File to Network", "*** Failed to copy file! ***\n\n" + str(ex)
                )

        cb = ttk.Button(mngFilesFrame, text="Copy File To :   ", command=copyFile)
        cb.grid(column=0, row=1, sticky=tk.E)

        # Add some space around each label
        for child in mngFilesFrame.winfo_children():
            child.grid_configure(padx=6, pady=6)

        # Creating a Menu Bar ==========================================================
        menuBar = Menu(tab1)
        self.win.config(menu=menuBar)
        
        # Add menu items
        fileMenu = Menu(menuBar, tearoff=0)
        fileMenu.add_command(label="New", command=self.new_DB)
        fileMenu.add_separator()
        fileMenu.add_command(label="New Table", command=self.new_Table)
        fileMenu.add_separator()
        fileMenu.add_command(label="Show Data", command=self.showData)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=self._quit)
        menuBar.add_cascade(label="File", menu=fileMenu)

        # Add another Menu to the Menu Bar and an item
        helpMenu = Menu(menuBar, tearoff=0)
        helpMenu.add_command(label="About")
        menuBar.add_cascade(label="Help", menu=helpMenu)

        # Change the main windows icon
        self.win.iconbitmap("pyc.ico")

        # Using tkinter Variable Classes
        strData = tk.StringVar()
        strData.set("Hello StringVar")

        # It is not necessary to create a tk.StringVar()
        strData = tk.StringVar()
        # strData = self.spin.get()

        # Place cursor into name Entry
        self.enim.focus()

        # Add a Tooltip to the Spinbox
        # tt.create_ToolTip(self.spin, 'This is a Spin control.')

        # Add Tooltips to more widgets
        tt.create_ToolTip(self.enim, "NIM.")
        # tt.create_ToolTip(self.action, "This is a Button control.")
        # tt.create_ToolTip(self.scr, "This is a ScrolledText control.")


# ======================
# Start GUI
# ======================
oop = OOP()
oop.win.mainloop()
