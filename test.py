
import tkinter as tk
from tkinter import font as ft
import mysql.connector as mysql
from tkinter import ttk
import os
import math
from PIL import ImageTk, Image
from tkinter import messagebox
info = messagebox.showinfo 
from numpy import array as ar
import tkinter.messagebox as msg
import time
import tkinter.filedialog as filedialog
import pickle

try:
    with open('raw','r') as f: 
        cc = f.read()
except:
    with open('raw','w') as f:
        f.write('1')

try:
    with open('penality.txt','r') as f: 
        cc = f.read()
except:
    with open('penality.txt','w') as f:
        f.write('1')


class intel_ui(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry("%dx%d+0+0" % (w, h))
        self.title("top_secret")
        self.configure(bg='#A2FD9F')
        self._frame = None  
        self.justforsuspect = 0
        self.justforsuspect2 = [[0]]
        self.justfornetwork = 0
        self.justfornetwork2 = 0
        self.id = 0
        self.last_frame=0

        #for connecting with mysql
        self.command = ""
        self.con = mysql.connect(host="sql12.freemysqlhosting.net", user="sql12344028", password="3lgjXwAmtj", database="sql12344028",port=3306)
        self.cursor = self.con.cursor()
        self.switch_frame(LoginScreen)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class LoginScreen(tk.Frame):
    
    def login_check(self):
        id1 = self.login_id.get()
        pswd = self.login_pswd.get()
        if id1 == "login id" and pswd == "password":
            self.master.switch_frame(HomeScreen)
        elif id1 == "login id1" and pswd == "password":
            self.master.switch_frame(DataEntry)
        else:
            
            tk.Label(self, text="wrong attempt no. {}!".format(self.limit), font=('times', 12, "bold"),fg="red", bg="#A2FD9F", height=0,  border=0).place(relx=1,x=-810,y=350)
            self.limit += 1
            if (self.limit == 5):
                with open("penality.txt","w") as f:
                    self.penality = f.write(str(int(time.time()+60*10)))
                info("error", "too many wrong attempts shutting service for 10 minutes.. ")
                exit()


    def __init__(self, master):

        with open("penality.txt","r") as f:
            self.penality = f.read()

        if int(time.time()) < int(self.penality):
            info("error", "sorry try after some time")
            exit()

        
        
        self.limit = 1
        #for starting the frame
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='#A2FD9F')
        self.pack(expand=True, fill=tk.BOTH)
 
        
        #for input prompt
        self.login_id = tk.Entry(self, border=0, width = 25)
        self.login_id.place(relx=1,x=-810,y=300)
        self.login_id.insert(0,"login id")
        
        #for input prompt
        self.login_pswd = tk.Entry(self, border=0, width = 25, show="*")
        self.login_pswd.place(relx=1,x=-810,y=330)
        self.login_pswd.insert(0,"password")

        #for button to insert
        login_button=tk.Button(self, text="Login", command=self.login_check, bg="#D1ABFF", activebackground="#D6F9FF", fg="#383838",  border=0)
        login_button.place(relx = 1, x =-660, y = 370, anchor = tk.NE)
        login_button['font']=ft.Font(size=16, family="serif", weight="bold") 




class HomeScreen(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='#A2FD9F')
        self.pack(expand=True, fill=tk.BOTH)

        #the buttons in the home page
        tk.Button(self, text="..",bg="#A2FD9D",command=lambda: master.switch_frame(LoginScreen), border=0).place(relx=1,x=-60,y=10)
        
        but_spe_op=tk.Button(text="Special Intel", command=lambda: master.switch_frame(SpecialIntel), bg="#D1ABFF", activebackground="#D6F9FF", fg="#383838", height=3, width=16, border=0)
        but_spe_op.place(relx = 1, x =-884, y = 100, anchor = tk.NE)
        but_spe_op['font']=ft.Font(size=28, family="serif", weight="bold") 
        but_spe_op=tk.Button(text="Special Ops", command=lambda: master.switch_frame(SpecialOps), bg="#FACDB6", activebackground="#D6F9FF", fg="#383838", height=3, width=16, border=0)
        but_spe_op.place(relx = 1, x =-140, y = 100, anchor = tk.NE)
        but_spe_op['font']=ft.Font(size=28, family="serif", weight="bold") 
        but_spe_op=tk.Button(text="Suspects", command=lambda: master.switch_frame(Suspects), bg="#BFF4EA", activebackground="#D6F9FF", fg="#383838", height=2, width=13, border=0)
        but_spe_op.place(relx = 1, x =-985, y = 305, anchor = tk.NE)
        but_spe_op['font']=ft.Font(size=25, family="serif") 
        but_spe_op=tk.Button(text="Network", command=lambda: master.switch_frame(Network), bg="#BFF4EA", activebackground="#D6F9FF", fg="#383838", height=2, width=13, border=0)
        but_spe_op.place(relx = 1, x =-983, y = 440, anchor = tk.NE)
        but_spe_op['font']=ft.Font(size=25, family="serif") 
        but_spe_op=tk.Button(text="Dominion", command=lambda: master.switch_frame(Dominion), bg="#BFF4EA", activebackground="#D6F9FF", fg="#383838", height=2, width=13, border=0)
        but_spe_op.place(relx = 1, x =-981, y = 570, anchor = tk.NE)
        but_spe_op['font']=ft.Font(size=25, family="serif") 
        

class SpecialIntel(tk.Frame):
    #opening media afer getting media_id
    def openmedia(self):
        self.binary=0
        self.master.id = int(self.media_no.get().strip())
        self.master.id = self.catched_rows[self.master.id-1][0]
        self.command="SELECT media_blob from Media where media_id = "+str(self.master.id)
        self.cursor.execute(self.command)
        self.binary = self.cursor.fetchall( )
        self.binary = self.binary[0][0]

        #writing got file to temp, so that can access
        with open('raw','wb') as file:
            file.write(self.binary)
        
        #will work if you are on linux and have vlc or chanege the above path and open file manually...

        os.system('vlc raw')
        
    #function supporting taking keywords from prompt and searching view oneview with it
    def insert(self):
        self.kw = self.e_keywords.get()
        self.kw = self.kw.split(",")
        
        #for putting kws in the list kw without whitespace
        for i in range(len(self.kw)):
            self.kw[i]=self.kw[i].strip()

        #the skeleton for query command
        self.command = """SELECT*FROM oneview WHERE """  + "feature LIKE \"%"+self.kw[0]+"%\" " + "or oname LIKE \"%"+self.kw[0]+"%\" " + "or pname LIKE \"%"+self.kw[0]+"%\" " 
        #the body for query command        
        for i in self.kw[1:]:
            self.command += "OR feature LIKE \"%"+i+"%\" " + "or oname LIKE \"%"+i+"%\" " + "or pname LIKE \"%"+i+"%\" " 
        self.command += ";"

        #executing uery command
        self.cursor.execute(self.command)

        #for catching data rows
        self.catched_rows = self.cursor.fetchall()
        
        #for making table
        if len(self.catched_rows)%2:
            col ='#E7B7A0'
        else:
            col = '#F6A57C'
            
        ttk.Style().configure("Treeview", background=col, foreground="white", fieldbackground=col)
        self.tv=ttk.Treeview(self, columns = (1,2,3,4,5), show="headings", height="24")
        self.tv.place(relx=1, x=-1300, y=120)
        self.tv.heading(1,text="no.")
        self.tv.heading(2,text="id")
        self.tv.heading(3,text="name")
        self.tv.heading(4,text="organisation")
        self.tv.heading(5,text="feature")
        self.tv.column(5, minwidth=0, width=700, stretch=tk.NO)
        self.tv.column(1, minwidth=0, width=50, stretch=tk.NO)
        self.tv.column(2, minwidth=0, width=50, stretch=tk.NO)

        self.tv.tag_configure('odd', background='#F6A57C')
        self.tv.tag_configure('even', background='#E7B7A0')

        #inserting scroll
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tv.yview)
        vsb.place(relx=1, x=-100, y=120, height=500)
        self.tv.configure(yscrollcommand=vsb.set)

    
        #printing to table
        count=0
        for i in self.catched_rows:
            if count%2:
                tag = "even"
            else:
                tag = "odd"
            self.tv.insert('', 'end', values=(count,)+tuple(i),tags=(tag,))
            count+=1
            a=len(i[3])
            if a > 100:
                no = math.floor(a/100)
                #to manage multiple lines
                for j in range(1,no-1):
                    self.tv.insert('', 'end', values=("","","",(count,)+i[3][100*j:100*(j+1)]), tags=(tag,))
                self.tv.insert('', 'end', values=("","","",(count,)+i[3][100*(no):]), tags=(tag,))



        #to open media
        insert = tk.Button(self, text="open media",  font=('roboto',10),activebackground="#D6F9FF", fg="#383838", bg='#A2FD9F', command=self.openmedia, border=0)
        insert.place(relx=1,x=-660, y=650) 
        self.media_no = tk.Entry(self, border=0)
        self.media_no.place(relx=1,x=-840,y=655)

    def __init__(self, master):
        #for connecting with mysql
        self.command = ""
        self.con = mysql.connect(host="sql12.freemysqlhosting.net", user="sql12344028", password="3lgjXwAmtj", database="sql12344028",port=3306)
        self.cursor = self.con.cursor()

        #for starting the frame
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='#D1ABFF')
        self.pack(expand=True, fill=tk.BOTH)
        
        #for heading
        l1 = tk.Label(self, text="Special Intel", font=('times', 27, "bold"),fg="white", bg="#A2FD9F", height=0, width=16, border=0).place(relx=1,x=-1300,y=60)
        tk.Button(self, text="..",bg="#A2FD9F",command=lambda: master.switch_frame(HomeScreen), border=0).place(relx=1,x=-60,y=10)
        
        #for working with input keywords
        self.e_keywords=0
        self.kw = 0

        #for input prompt
        self.e_keywords = tk.Entry(self, border=0)
        self.e_keywords.place(relx=1,x=-520,y=65)

        #for button to insert
        insert = tk.Button(self, text="search keywords",  font=('roboto',10),activebackground="#D6F9FF", fg="#383838", bg='#A2FD9F', command=self.insert, border=0)
        insert.place(relx=1,x=-340, y=60)



class SpecialOps(tk.Frame):
      
        
    #function supporting taking keywords from prompt and searching view twoview with it
    def insert(self):
        self.list = self.e_keywords.get().split(",")
        self.list2 = self.e_keywords2.get().split(",")
        self.list3 = self.e_keywords3.get().split(",")

        #for putting kws in the list kw without whitespace
        for i in range(len(self.list)):
            self.list[i]=self.list[i].strip()
        for i in range(len(self.list2)):
            self.list2[i]=self.list2[i].strip()
        for i in range(len(self.list3)):
            self.list3[i]=self.list3[i].strip()

        #the skeleton for query command
        self.command = "SELECT*FROM twoview " 
        is_first_iteration = True
        
        #the body for query command
        if self.list[0]:
            for i in self.list:
                if is_first_iteration:
                    self.command += "WHERE oname LIKE \"%"+i+"%\" " + "OR pname LIKE \"%"+i+"%\" " 
                    is_first_iteration=False
                else:
                    self.command += "OR oname LIKE \"%"+i+"%\" " + "OR pname LIKE \"%"+i+"%\" " 
        if self.list2[0]:
            for i in self.list2:
                if is_first_iteration:
                    self.command += "WHERE date LIKE \"%"+i+"%\" " 
                    is_first_iteration=False
                else:
                    self.command += "OR date LIKE \"%"+i+"%\" " 
        if self.list3[0]:
            for i in self.list3:
                if is_first_iteration:
                    self.command += "WHERE operation LIKE \"%"+i+"%\" "
                    is_first_iteration=False
                else:
                    self.command += "OR operation LIKE \"%"+i+"%\" " 
        self.command += ";"


        #executing uery command
        self.cursor.execute(self.command)

        #for catching data rows
        self.catched_rows = self.cursor.fetchall()

        #for making table
        if len(self.catched_rows)%2:
            col ='#99C6B1'
        else:
            col = '#ABD0B5'
        self.tv=ttk.Treeview(self, columns = (1,2,3,4,5,6),  show="headings", height="24")
        ttk.Style().configure("Treeview", background=col, foreground="white", fieldbackground=col)
        self.tv.place(relx=1, x=-1300, y=200)
        self.tv.tag_configure('odd', background='#ABD0B5')
        self.tv.tag_configure('even', background='#99C6B1')

        #inserting scroll
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tv.yview)
        vsb.place(relx=1, x=-50, y=200, height=500)
        self.tv.configure(yscrollcommand=vsb.set)

        #inserting columns
        self.tv.heading(1,text="no")
        self.tv.column(1, minwidth=0, width=50, stretch=tk.NO)
        self.tv.heading(2,text="id")
        self.tv.column(2, minwidth=0, width=50, stretch=tk.NO)
        self.tv.heading(3,text="operation")
        self.tv.column(3, minwidth=0, width = 550)
        self.tv.heading(4,text="name")
        self.tv.heading(5,text="organisation")
        self.tv.heading(6,text="date")

        #printing to table
        count=0
        for i in self.catched_rows:
            if count%2:
                tag = "even"
            else:
                tag = "odd"
            self.tv.insert('', 'end', values=(count,)+tuple(i),tags=(tag,))
            count+=1
            a=len(i[3])
            if a > 100:
                no = math.floor(a/100)
                #to manage multiple lines
                for j in range(1,no-1):
                    self.tv.insert('', 'end', values=("","","",(count,)+i[3][100*j:100*(j+1)]), tags=(tag,))
                self.tv.insert('', 'end', values=("","","",(count,)+i[3][100*(no):]), tags=(tag,))


    def __init__(self, master):
        #for connecting with mysql
        self.command = ""
        self.con = mysql.connect(host="sql12.freemysqlhosting.net", user="sql12344028", password="3lgjXwAmtj", database="sql12344028",port=3306)
        self.cursor = self.con.cursor()

        #for working with input keywords
        self.list=[]
        self.list2=[]
        self.list3=[]
        self.e_keywords=0
        self.e_keywords2=0
        self.e_keywords2=0
        self.kw = 0

        #for starting the frame
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='#FACDB6')
        self.pack(expand=True, fill=tk.BOTH)
        
        #for heading
        l1 = tk.Label(self, text="Special Ops", font=('times', 27, "bold"),fg="white", bg="#A2FD9F", height=0, width=16, border=0).place(relx=1,x=-1300,y=60)
        tk.Button(self, text="..",bg="#A2FD9F",command=lambda: master.switch_frame(HomeScreen), border=0).place(relx=1,x=-60,y=10)
        
        #to input organ
        self.e_keywords = tk.Entry(self, border=0)
        self.e_keywords.place(relx=1,x=-380,y=65)

        #to filter organ
        insert = tk.Button(self, text="filter target",  font=('roboto',10),activebackground="#D6F9FF", fg="#383838", bg='#A2FD9F', command=self.insert, border=0)
        insert.place(relx=1,x=-200, y=60) 

        #to input person
        self.e_keywords2 = tk.Entry(self, border=0)
        self.e_keywords2.place(relx=1,x=-380,y=95)

        #to filter person
        insert2 = tk.Button(self, text="filter date",  font=('roboto',10),activebackground="#D6F9FF", fg="#383838", bg='#A2FD9F',  command=self.insert, border=0)
        insert2.place(relx=1,x=-200, y=90) 

        #to input date
        self.e_keywords3 = tk.Entry(self, border=0, width=60)
        self.e_keywords3.place(relx=1,x=-920,y=120)

        #to filter date
        insert2 = tk.Button(self, text="search",  font=('roboto',10),activebackground="#D6F9FF", fg="#383838",  bg='#A2FD9F', command=self.insert, border=0)
        insert2.place(relx=1,x=-700, y=144) 
        

        
class Suspects(tk.Frame):

    def check_right_input_then_jump(self):
        self.master.id = int(self.master.justforsuspect.get())
        if self.master.id > len(self.master.justforsuspect2) or self.master.id <=0 :
            info("Oops","wrong entry")
        else:
            self.master.switch_frame(suspect_detail)

        

    #function supporting taking keywords from prompt and searching view threeview with it
    def insert(self):
        self.list = self.e_keywords.get().split(",")
        self.list2 = self.e_keywords2.get().split(",")

        #for putting kws in the list kw without whitespace
        for i in range(len(self.list)):
            self.list[i]=self.list[i].strip()
        for i in range(len(self.list2)):
            self.list2[i]=self.list2[i].strip()

        #the skeleton for query command
        self.command = "SELECT*FROM threeview " 
        is_first_iteration = True


        #the body for query command
        if self.list[0]:
            for i in self.list:
                if is_first_iteration:
                    self.command += "WHERE pname LIKE \"%"+i+"%\" " 
                    is_first_iteration=False
                else:
                    self.command += "OR pname LIKE \"%"+i+"%\" " 
        if self.list2[0]:
            for i in self.list2:
                if is_first_iteration:
                    self.command += "WHERE oname LIKE \"%"+i+"%\" " 
                    is_first_iteration=False
                else:
                    self.command += "OR oname LIKE \"%"+i+"%\" " 
        self.command += ";"

        #executing uery command
        self.cursor.execute(self.command)

        #for catching data rows
        self.catched_rows = self.cursor.fetchall()
        self.master.justforsuspect2 = self.catched_rows

        #for making table
        if len(self.catched_rows)%2:
            col ='#9AB083'
        else:
            col = '#A1BC88'
            
        ttk.Style().configure("Treeview", background=col, foreground="white", fieldbackground=col)
        self.tv=ttk.Treeview(self, columns = (1,2,3,4,5,6), show="headings", height="24")
        self.tv.place(relx=1, x=-1300, y=200)
        self.tv.heading(1,text="no")
        self.tv.heading(2,text="id")
        self.tv.heading(3,text="name")
        self.tv.heading(4,text="organisation")
        self.tv.heading(5,text="country")
        self.tv.heading(6,text="soc/eco status")
        self.tv.column(1, minwidth=0, width=50, stretch=tk.NO)
        self.tv.column(2, minwidth=0, width=50, stretch=tk.NO)
        self.tv.column(3, minwidth=0, width = 550)

        self.tv.tag_configure('odd', background='#A1BC88')
        self.tv.tag_configure('even', background='#9AB083')

        #inserting scroll
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tv.yview)
        vsb.place(relx=1, x=-50, y=200, height=500)
        self.tv.configure(yscrollcommand=vsb.set)


    
        #printing to table
        count=0
        for i in self.catched_rows:
            if count%2:
                tag = "even"
            else:
                tag = "odd"
            self.tv.insert('', 'end', values=(count,)+tuple(i),tags=(tag,))
            count+=1
            
    
        #to show details
        tk.Button(self, text="",command=lambda: self.master.switch_frame(suspect_detail), border=0)
        
        self.master.justforsuspect = tk.Entry(self, border=0)
        self.master.justforsuspect.place(relx=1,x=-840,y=710)
        self.master.last_frame = Suspects
        insert = tk.Button(self, text="show_detail",  font=('roboto',10),activebackground="#D6F9FF", fg="#383838", bg='#A2FD9F', command=self.check_right_input_then_jump, border=0)
        insert.place(relx=1,x=-660, y=705) 


    def __init__(self, master):
        #for connecting with mysql
        self.command = ""
        self.con = mysql.connect(host="sql12.freemysqlhosting.net", user="sql12344028", password="3lgjXwAmtj", database="sql12344028",port=3306)
        self.cursor = self.con.cursor()

        #for starting the frame
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='#BFF4EA')
        self.pack(expand=True, fill=tk.BOTH)
        l1 = tk.Label(self, text="Suspects", font=('times', 27, "bold"), bg="#A2FD9F", fg="white",height=0, width=16, border=0).place(relx=1,x=-1300,y=60)
        tk.Button(self, text="..",bg="#A2FD9F",command=lambda: master.switch_frame(HomeScreen), border=0).place(relx=1,x=-60,y=10)

        #for working with input keywords
        self.e_keywords=0
        self.kw = 0

        #to input name
        self.e_keywords = tk.Entry(self, border=0, width=60)
        self.e_keywords.place(relx=1,x=-920,y=120)

        #to search name
        insert2 = tk.Button(self, text="search",  font=('roboto',10),activebackground="#D6F9FF", fg="#383838",  bg='#A2FD9F', command=self.insert, border=0)
        insert2.place(relx=1,x=-700, y=144) 

        #to input organisation
        self.e_keywords2 = tk.Entry(self, border=0)
        self.e_keywords2.place(relx=1,x=-380,y=95)

        #to filter organisation
        insert2 = tk.Button(self, text="filter organisation",  font=('roboto',10),activebackground="#D6F9FF", fg="#383838", bg='#A2FD9F',  command=self.insert, border=0)
        insert2.place(relx=1,x=-200, y=90) 

            

class suspect_detail(tk.Frame):
    def crime_table(self):
        #the skeleton for query command
        self.command = """SELECT `Action`.action_id, `Action`.name FROM Person JOIN criminal_record ON criminal_record.person_id = Person.person_id JOIN `Action` ON `Action`.action_id = criminal_record.action_id WHERE Person.person_id={} ;""".format(self.ind)

        #executing uery command
        self.master.cursor.execute(self.command)

        #for catching data rows
        self.catched_rows = self.master.cursor.fetchall()
        
        
        #for making table
        if len(self.catched_rows)%2:
            col ='#A2D9A0'
        else:
            col = '#9BCB98'
        
        ttk.Style().configure("Treeview", background=col, foreground="white", fieldbackground=col)
        self.tv=ttk.Treeview(self, columns = (1,2), show="headings", height="18")
        self.tv.place(relx=1, x=-380, y=320)
        self.tv.heading(1,text="no.")
        self.tv.heading(2,text="crime")
        self.tv.column(1, minwidth=0, width=50, stretch=tk.NO)
        self.tv.column(2, minwidth=0, width=300, stretch=tk.NO)


        self.tv.tag_configure('odd', background='#9BCB98')
        self.tv.tag_configure('even', background='#A2D9A0')
        
        #inserting scroll
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tv.yview)
        vsb.place(relx=1, x=-30, y=320, height=380)
        self.tv.configure(yscrollcommand=vsb.set)
        
    
        #printing to table
        count=0
        for i in self.catched_rows:
            if count%2:
                tag = "even"
            else:
                tag = "odd"
            self.tv.insert('', 'end', values=(count,)+i[1:],tags=(tag,))
            count+=1
           

    def __init__(self, master):
        self.catched_rows=0
        self.ind=0

        #creating frame
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='#B3D9CA')
        self.pack(expand=True, fill=tk.BOTH)

        #heading
        l1 = tk.Label(self, text="suspect_detail", font=('times', 27, "bold"), bg="#A2FD9F", fg="white", height=0, width=16, border=0).place(relx=1,x=-1300,y=60)
        tk.Button(self, text="..",bg="#A2FD9F",command=lambda: master.switch_frame(master.last_frame), border=0).place(relx=1,x=-50,y=20)
        
        #entry from suspect show detail button
               
        
       
        
        self.ind = master.justforsuspect2[master.id-1][0]

        command = """SELECT firstset.id, firstset.pname, firstset.dob, firstset.mb, firstset.oname, firstset.status, 
        firstset.city, firstset.state, firstset.country, secondset.crime FROM ( select Person.person_id AS id, Person.name AS pname
        , Person.dob AS dob, Media.media_blob AS mb, Organisation.name AS oname, Person.citizen_status AS status, 
        Location.city AS city, Location.state AS state,  Country.name AS country FROM  Person JOIN Media on 
        Media.media_id=Person.media_id JOIN Organisation ON Person.organ_id = Organisation.organ_id JOIN Location on 
        Person.location_id=Location.location_id	JOIN Country ON Country.country_id=Location.country_id WHERE person_id={}  ) AS 
        firstset INNER JOIN (SELECT  IFNULL(person_id, {}) AS id, COUNT(person_id) AS crime FROM criminal_record WHERE person_id={} ) AS 
        secondset ON firstset.id=secondset.id;""".format(self.ind, self.ind, self.ind)

        #executing uery command
        master.cursor.execute(command)

        #for catching data rows
        self.catched_rows = master.cursor.fetchall()

    
    
        self.pic = self.catched_rows[0][3]
        self.data = self.catched_rows[0][:3]+self.catched_rows[0][4:]


        
        #writing got file to temp, so that can access
        with open('raw','wb') as file:
            file.write(self.pic)
        
        #showing photo
        self.canv1 = tk.Canvas(self, width = 200, height = 220)         
        self.canv1.place(relx=1, x=-280, y=80)
        self.new_img = ImageTk.PhotoImage(Image.open(r"raw"))
        self.item1 = self.canv1.create_image(100, 100, image = self.new_img)
        self.canv1.image = self.new_img

        #showing rest of data
        
        name = tk.Label(self, text="Name", font=('times', 20), bg="#CEBE9A", height=0, width=16, border=0).place(relx=1,x=-1300 + 40,y=300 - 80) 
        name = tk.Label(self, text="Dob", font=('times', 20), bg="#CEBE9A", height=0, width=16, border=0).place(relx=1,x=-1300 + 40,y=360 - 80) 
        name = tk.Label(self, text="Organisation", font=('times', 20), bg="#CEBE9A", height=0, width=16, border=0).place(relx=1,x=-1300 + 40,y=420 - 80) 
        name = tk.Label(self, text="Status", font=('times', 20), bg="#CEBE9A", height=0, width=16, border=0).place(relx=1,x=-1300 + 40,y=480 - 80) 
        name = tk.Label(self, text="City", font=('times', 20), bg="#CEBE9A", height=0, width=16, border=0).place(relx=1,x=-1300 + 40,y=540 - 80) 
        name = tk.Label(self, text="State", font=('times', 20), bg="#CEBE9A", height=0, width=16, border=0).place(relx=1,x=-1300 + 40,y=600 - 80) 
        name = tk.Label(self, text="Country", font=('times', 20), bg="#CEBE9A", height=0, width=16, border=0).place(relx=1,x=-1300 + 40,y=660 - 80) 
        name = tk.Label(self, text="Crime record", font=('times', 20), bg="#CEBE9A", height=0, width=16, border=0).place(relx=1,x=-1300 + 40,y=720 - 80) 


        name = tk.Label(self, text = self.data[1], font=('roboto', 14), justify=tk.LEFT, anchor="w", bg="#CEBE9A", height=0, width=45, border=0).place(relx=1,x=-1000 + 40,y=300 - 80) 
        name = tk.Label(self, text = self.data[2], font=('roboto', 14), justify=tk.LEFT, anchor="w", bg="#CEBE9A", height=0, width=45, border=0).place(relx=1,x=-1000 + 40,y=360 - 80) 
        name = tk.Label(self, text = self.data[3], font=('roboto', 14), justify=tk.LEFT, anchor="w", bg="#CEBE9A", height=0, width=45, border=0).place(relx=1,x=-1000 + 40,y=420 - 80) 
        name = tk.Label(self, text = self.data[4], font=('roboto', 14), justify=tk.LEFT, anchor="w", bg="#CEBE9A", height=0, width=45, border=0).place(relx=1,x=-1000 + 40,y=480 - 80) 
        name = tk.Label(self, text = self.data[5], font=('roboto', 14), justify=tk.LEFT, anchor="w", bg="#CEBE9A", height=0, width=45, border=0).place(relx=1,x=-1000 + 40,y=540 - 80) 
        name = tk.Label(self, text = self.data[6], font=('roboto', 14), justify=tk.LEFT, anchor="w", bg="#CEBE9A", height=0, width=45, border=0).place(relx=1,x=-1000 + 40,y=600 - 80) 
        name = tk.Label(self, text = self.data[7], font=('roboto', 14), justify=tk.LEFT, anchor="w", bg="#CEBE9A", height=0, width=45, border=0).place(relx=1,x=-1000 + 40,y=660 - 80) 
        name = tk.Label(self, text = self.data[8], font=('roboto', 14), justify=tk.LEFT, anchor="w", bg="#CEBE9A", height=0, width=40, border=0).place(relx=1,x=-1000 + 40,y=720 - 80) 
        
        if self.data[8]:
            tk.Button(self, text="detail",bg="#B3D9CA",command=self.crime_table, border=0).place(relx=1,x=-470,y=640)

        


class Network(tk.Frame):

    def check_right_input_then_jump(self):
        self.master.id = int(self.master.justfornetwork.get())
        if self.master.id > len(self.master.justfornetwork2) or self.master.id <=0 :
            info("Oops","wrong entry")     
        else:
            self.master.switch_frame(network_detail)

    #function supporting taking keywords from prompt and searching view threeview with it
    def insert(self):
        self.list = self.e_keywords.get().split(",")
        self.list2 = self.e_keywords2.get().split(",")

        #for putting kws in the list kw without whitespace
        for i in range(len(self.list)):
            self.list[i]=self.list[i].strip()
        for i in range(len(self.list2)):
            self.list2[i]=self.list2[i].strip()

        #the skeleton for query command
        self.command = "SELECT*FROM fourview " 
        is_first_iteration = True


        #the body for query command
        if self.list[0]:
            for i in self.list:
                if is_first_iteration:
                    self.command += "WHERE oname LIKE \"%"+i+"%\" " 
                    is_first_iteration=False
                else:
                    self.command += "OR oname LIKE \"%"+i+"%\" " 
        if self.list2[0]:
            for i in self.list2:
                if is_first_iteration:
                    self.command += "WHERE otype LIKE \"%"+i+"%\" " 
                    is_first_iteration=False
                else:
                    self.command += "OR otype LIKE \"%"+i+"%\" " 
        self.command += ";"

        #executing uery command
        self.cursor.execute(self.command)

        #for catching data rows
        self.catched_rows = self.cursor.fetchall()
        self.master.justfornetwork2 = self.catched_rows

        #for making table
        if len(self.catched_rows)%2:
            col ='#9AB083'
        else:
            col = '#A1BC88'
            
        ttk.Style().configure("Treeview", background=col, foreground="white", fieldbackground=col)
        self.tv=ttk.Treeview(self, columns = (1,2,3,4,5,6,7), show="headings", height="24")
        self.tv.place(relx=1, x=-1300, y=200)
        self.tv.heading(1,text="no")
        self.tv.heading(2,text="id")
        self.tv.heading(3,text="type")
        self.tv.heading(4,text="organisation")
        self.tv.heading(5,text="city")
        self.tv.heading(6,text="state")
        self.tv.heading(7,text="country")
        self.tv.column(1, minwidth=0, width=50, stretch=tk.NO)
        self.tv.column(2, minwidth=0, width=50, stretch=tk.NO)
        self.tv.column(4, minwidth=0, width=500, stretch=tk.NO)
        for i in range(5,8):
            self.tv.column(i, minwidth=0, width=150, stretch=tk.NO)
        
        

        self.tv.tag_configure('odd', background='#A1BC88')
        self.tv.tag_configure('even', background='#9AB083')

        #inserting scroll
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tv.yview)
        vsb.place(relx=1, x=-50, y=200, height=500)
        self.tv.configure(yscrollcommand=vsb.set)


    
        #printing to table
        count=0
        for i in self.catched_rows:
            if count%2:
                tag = "even"
            else:
                tag = "odd"
            self.tv.insert('', 'end', values=(count,)+(i[0],)+i[2:4]+i[7:11],tags=(tag,))
            count += 1
            
    
        #to show details
        tk.Button(self, text="",command=lambda: self.master.switch_frame(network_detail), border=0)
        
        self.master.justfornetwork = tk.Entry(self, border=0)
        self.master.justfornetwork.place(relx=1,x=-840,y=710)
        insert = tk.Button(self, text="show_detail",  font=('roboto',10),activebackground="#D6F9FF", fg="#383838", bg='#A2FD9F', command=self.check_right_input_then_jump, border=0)
        insert.place(relx=1,x=-660, y=705) 


    def __init__(self, master):
        #for connecting with mysql
        self.command = ""
        self.con = mysql.connect(host="sql12.freemysqlhosting.net", user="sql12344028", password="3lgjXwAmtj", database="sql12344028",port=3306)
        self.cursor = self.con.cursor()

        #for starting the frame
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='#BFF4EA')
        self.pack(expand=True, fill=tk.BOTH)
        l1 = tk.Label(self, text="Network", font=('times', 27, "bold"), bg="#A2FD9F", fg="white",height=0, width=16, border=0).place(relx=1,x=-1300,y=60)
        tk.Button(self, text="..",bg="#A2FD9F",command=lambda: master.switch_frame(HomeScreen), border=0).place(relx=1,x=-60,y=10)

        #for working with input keywords
        self.e_keywords=0
        self.kw = 0

        #to input name
        self.e_keywords = tk.Entry(self, border=0, width=60)
        self.e_keywords.place(relx=1,x=-920,y=120)

        #to search name
        insert2 = tk.Button(self, text="search",  font=('roboto',10),activebackground="#D6F9FF", fg="#383838",  bg='#A2FD9F', command=self.insert, border=0)
        insert2.place(relx=1,x=-700, y=144) 

        #to input type
        self.e_keywords2 = tk.Entry(self, border=0)
        self.e_keywords2.place(relx=1,x=-380,y=95)

        #to filter type
        insert2 = tk.Button(self, text="filter type",  font=('roboto',10),activebackground="#D6F9FF", fg="#383838", bg='#A2FD9F',  command=self.insert, border=0)
        insert2.place(relx=1,x=-200, y=90) 


           

class network_detail(tk.Frame):
    

    #to help showing leader data
    def check_right_input_then_jump(self):
        if self.master.id > len(self.master.justforsuspect2) or self.master.id <=0 :
            info("Oops","wrong entry")
        else:
            self.master.switch_frame(suspect_detail)
    
    def __init__(self, master):
        self.data=0

        #creating frame
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='#B3D9CA')
        self.pack(expand=True, fill=tk.BOTH)

        #heading
        l1 = tk.Label(self, text="network_detail", font=('times', 27, "bold"), bg="#A2FD9F", fg="white", height=0, width=16, border=0).place(relx=1,x=-1300,y=60)
        tk.Button(self, text="..",bg="#A2FD9F",command=lambda: master.switch_frame(Network), border=0).place(relx=1,x=-50,y=20)
        
        #entry from suspect show detail button

        
        self.ind = master.justfornetwork2[master.id-1][0]

        self.data = master.justfornetwork2[master.id-1]

        
        #showing rest of data
        
        headings=['','id', 'type', 'name', 'worth', 'leader', 'security level', 'city', 'state', 'country', 'no of guaards', 'duty change', 'cameras', 'blockade' ]

        j=0
        for i in [1,2,3,4,6,7,8,5,9,10,11,12,13]:
            tk.Label(self, text=headings[i], font=('times', 20), bg="#CEBE9A", height=0, width=16, border=0).place(relx=1,x=-1300 + 40,y=250 +(42*j) - 80) 
            tk.Label(self, text = self.data[i], font=('roboto', 14), justify=tk.LEFT, anchor="w", bg="#CEBE9A", height=0, width=45, border=0).place(relx=1,x=-1000 + 40,y=250+(42*j) - 80) 
            j+=1
        
        #to show leader detail (jumping to suspect)
        master.justforsuspect2 = ar(master.justfornetwork2)
        master.last_frame = network_detail
        insert = tk.Button(self, text="show_detail",  font=('roboto',10),activebackground="#D6F9FF", fg="#383838", bg='#A2FD9F', command=self.check_right_input_then_jump, border=0)
        insert.place(relx=1,x=-520, y=335) 
               
        

class Dominion(tk.Frame):

    def jump(self):

        self.master.switch_frame(suspect_detail)


    def show_detail(self):
        
        ind = int(self.master.justfornetwork.get())

        if ind> len(self.master.justfornetwork2) or ind<=0 :
            info("Oops","wrong entry")
            return

        ind = self.master.justfornetwork2[ind-1][0]
        


        self.command = """SELECT Location.location_id, Location.state, Person.person_id, Person.name FROM Country
	    JOIN Person ON Person.person_id = Country.leader
		JOIN Location ON Location.location_id = Country.capital WHERE Country.country_id={};""".format(ind)

        #executing uery command
        self.cursor.execute(self.command)

        #for catching data rows
        self.catched_rows1 = self.cursor.fetchall()

        headings=['','capital ->','', 'leader ->']

        self.master.id = 1
        self.master.justforsuspect2[0][0] = self.catched_rows1[0][2]

        j=0
        for i in [1,3]:
            tk.Label(self, text=headings[i], font=('times', 20), bg="#DFD4BB", height=0, width=16, border=0).place(relx=1,x=-1300 +500 + 40,y=220 +(42*j)) 
            tk.Label(self, text = self.catched_rows1[0][i], font=('roboto', 14), justify=tk.LEFT, anchor="w", bg="#DFD4BB", height=0, width=30, border=0).place(relx=1,x=-1050 +500+ 40,y=220+(42*j)) 
            j+=1


        self.command = """SELECT Country.name FROM country_alias
	JOIN Country ON Country.country_id = country_alias.alias_id
		WHERE country_alias.country_id = {};""".format(ind)
        #executing query command
        self.cursor.execute(self.command)
        #for catching data rows
        self.alias = self.cursor.fetchall()

        

        self.command = """SELECT Country.name FROM country_enemy
	JOIN Country ON Country.country_id = country_enemy.enemy_id
		WHERE country_enemy.country_id = {};""".format(ind)
        #executing query command
        self.cursor.execute(self.command)
        #for catching data rows
        self.enemies = self.cursor.fetchall()

        

        len1 = len(self.alias)
        len2 = len(self.enemies)
        finlen = len1-len2
        if len1>len2:
            self.enemies += [('',)]*finlen
        else:
            finlen = len2-len1
            self.alias += [('',)]*finlen

        #for making table
        if len(self.catched_rows)%2:
            col ='#BCD99C'
        else:
            col = '#B0CC96'
            
        ttk.Style().configure("Treeview", background=col, foreground="white", fieldbackground=col)
        self.tv=ttk.Treeview(self, columns = (1,2), show="headings", height="18")
        self.tv.place(relx=1, x=-520, y=300)
        self.tv.heading(1,text="allies")
        self.tv.heading(2,text="enemies")
        self.tv.column(1, minwidth=0, width=200, stretch=tk.NO)
        self.tv.column(2, minwidth=0, width=200, stretch=tk.NO)
        
        

        self.tv.tag_configure('odd', background='#B0CC96')
        self.tv.tag_configure('even', background='#BCD99C')

        #inserting scroll
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tv.yview)
        vsb.place(relx=1, x=-120, y=300, height=385)
        self.tv.configure(yscrollcommand=vsb.set)


    
        #printing to table
        count=0
        for i in range(finlen):
            if count%2:
                tag = "even"
            else:
                tag = "odd"
            self.tv.insert('', 'end', values=self.alias[i]+self.enemies[i],tags=(tag,))


        #to show leader detail (jumping to suspect)
        self.master.last_frame = Dominion
        insert = tk.Button(self, text="more detail",  font=('roboto',10),activebackground="#D6F9FF", fg="#383838", bg='#A2FD9F', command=self.jump, border=0)
        insert.place(relx=1,x=-248,y=260)


        weap = ['nuclear', 'biological', 'chemical']
        self.weap = [0,0,0]

        for i in range(3):
            self.command = """SELECT Weapons.NUMBER FROM country_weapon
            JOIN Country ON Country.country_id = country_weapon.country_id
                JOIN Weapons ON Weapons.weapon_id = country_weapon.{}_id
                    WHERE Country.country_id = {};""".format(weap[i], ind)
            #executing query command
            self.cursor.execute(self.command)
            #for catching data rows
            num = self.cursor.fetchall()
            if num:
                self.weap[i] = num[0][0]
            


        tk.Label(self, text="Weapons :", font=('times', 20), bg="#DFD4BB", height=0, width=16, border=0).place(relx=1,x=-1300 +500 + 40,y=420 -50 ) 

        tex = ['nuclear :', 'chemical :', 'biological :']
        j=0
        for i in range(3):
            tk.Label(self, text=tex[i], font=('times', 20), bg="#DFD4BB", height=0, width=10, border=0).place(relx=1,x=-1300 +500 + 80,y=420 +(42*j)) 
            j+=1
            tk.Label(self, text=self.weap[i], font=('times', 20), bg="#DFD4BB", height=0, width=10, border=0).place(relx=1,x=-1300 +500 + 80,y=420 +(42*j)) 
            j+=1
      


    #function supporting taking keywords from prompt and searching view threeview with it
    def insert(self):
        self.list = self.e_keywords.get().split(",")

        #for putting kws in the list kw without whitespace
        for i in range(len(self.list)):
            self.list[i]=self.list[i].strip()

        #the skeleton for query command
        self.command = "SELECT*FROM Country " 
        is_first_iteration = True


        #the body for query command
        if self.list[0]:
            for i in self.list:
                if is_first_iteration:
                    self.command += "WHERE name LIKE \"%"+i+"%\" " 
                    is_first_iteration=False
                else:
                    self.command += "OR continent LIKE \"%"+i+"%\" " 
        self.command += ";"

        #executing uery command
        self.cursor.execute(self.command)

        #for catching data rows
        self.catched_rows = self.cursor.fetchall()
        self.master.justfornetwork2 = self.catched_rows

        #for making table
        if len(self.catched_rows)%2:
            col ='#BCD99C'
        else:
            col = '#B0CC96'
            
        ttk.Style().configure("Treeview", background=col, foreground="white", fieldbackground=col)
        self.tv=ttk.Treeview(self, columns = (1,2,3,4), show="headings", height="24")
        self.tv.place(relx=1, x=-1300, y=200)
        self.tv.heading(1,text="no")
        self.tv.heading(2,text="id")
        self.tv.heading(3,text="country")
        self.tv.heading(4,text="continent")
        self.tv.column(1, minwidth=0, width=40, stretch=tk.NO)
        self.tv.column(2, minwidth=0, width=40, stretch=tk.NO)
        self.tv.column(3, minwidth=0, width=185, stretch=tk.NO)
        self.tv.column(4, minwidth=0, width=185, stretch=tk.NO)
        
        

        self.tv.tag_configure('odd', background='#B0CC96')
        self.tv.tag_configure('even', background='#BCD99C')

        #inserting scroll
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tv.yview)
        vsb.place(relx=1, x=-850, y=200, height=500)
        self.tv.configure(yscrollcommand=vsb.set)


    
        #printing to table
        count=0
        for i in self.catched_rows:
            if count%2:
                tag = "even"
            else:
                tag = "odd"
            self.tv.insert('', 'end', values=(count,)+(i[0],)+i[1:3],tags=(tag,))
            count+=1
        
        #to show details
        
        self.master.justfornetwork = tk.Entry(self, border=0)
        self.master.justfornetwork.place(relx=1,x=-1240,y=710)
        insert = tk.Button(self,command=self.show_detail, text="show_detail",  font=('roboto',10),activebackground="#D6F9FF", fg="#383838", bg='#A2FD9F', border=0)
        insert.place(relx=1,x=-1060, y=705) 



        


    def __init__(self, master):
        #for connecting with mysql
        self.command = ""
        self.con = mysql.connect(host="sql12.freemysqlhosting.net", user="sql12344028", password="3lgjXwAmtj", database="sql12344028",port=3306)
        self.cursor = self.con.cursor()

        #for starting the frame
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='#BFF4EA')
        self.pack(expand=True, fill=tk.BOTH)
        l1 = tk.Label(self, text="Dominion", font=('times', 27, "bold"), bg="#A2FD9F", fg="white",height=0, width=16, border=0).place(relx=1,x=-1300,y=60)
        tk.Button(self, text="..",bg="#A2FD9F",command=lambda: master.switch_frame(HomeScreen), border=0).place(relx=1,x=-60,y=10)

        #for working with input keywords
        self.e_keywords=0
        self.kw = 0

        #to input name
        self.e_keywords = tk.Entry(self, border=0, width=60)
        self.e_keywords.place(relx=1,x=-920,y=120)

        #to search name
        insert2 = tk.Button(self, text="search",  font=('roboto',10),activebackground="#D6F9FF", fg="#383838",  bg='#A2FD9F', command=self.insert, border=0)
        insert2.place(relx=1,x=-700, y=144) 



class ScrollFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master) # create a frame (self)

        self.canvas = tk.Canvas(self, borderwidth=0, background="#A2E3C3")          #place canvas on self
        self.viewPort = tk.Frame(self.canvas, background="#A2E3C3")                    #place a frame on the canvas, this frame will hold the child widgets 
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview) #place a scrollbar on self 
        self.canvas.configure(yscrollcommand=self.vsb.set)                          #attach scrollbar action to scroll of canvas

        self.vsb.pack(side="right", fill="y")                                       #pack scrollbar to right of self
        self.canvas.pack(side="left", fill="both", expand=True)                     #pack canvas to left of self and expand to fil
        self.canvas_window = self.canvas.create_window((4,4), window=self.viewPort, anchor="nw",            #add view port frame to canvas
                                  tags="self.viewPort")

        self.viewPort.bind("<Configure>", self.onFrameConfigure)                       #bind an event whenever the size of the viewPort frame changes.
        self.canvas.bind("<Configure>", self.onCanvasConfigure)                       #bind an event whenever the size of the viewPort frame changes.

        self.onFrameConfigure(None)                                                 #perform an initial stretch on render, otherwise the scroll region has a tiny border until the first resize

    def onFrameConfigure(self, event):                                              
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))                 #whenever the size of the frame changes, alter the scroll region respectively.

    def onCanvasConfigure(self, event):
        '''Reset the canvas window to encompass inner frame when required'''
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width = canvas_width)            #whenever the size of the canvas changes alter the window region respectively.



class DataEntry(tk.Frame):
    
    def browsefunc(self):
        self.addr = filedialog.askopenfilename()
        self.add_spe_intel[2].insert(0, self.addr)

    def browsefunc1(self):
        self.picadr = filedialog.askopenfilename()
        self.special_for_person.insert(0, self.picadr)

    def insert_special_intel_by_person(self):


        cmd = "select person_id from Person where person_id = {};".format(self.add_spe_intel[0].get())
        self.cursor.execute(cmd)
        flag = self.cursor.fetchall()
        
        if flag == []:
            info("error", "id doesn't exist")
            return



    
        

        def convertToBinaryData(filename):
            # Convert digital data to binary format
            with open(filename, 'rb') as file:
                binaryData = file.read()
            return binaryData

        sql_insert_blob_query = """ INSERT INTO Media
                            (media_blob) VALUES (%s)"""

        empPicture = convertToBinaryData(self.addr)

        # Convert data into tuple format
        insert_blob_tuple = (empPicture, )
        self.cursor.execute(sql_insert_blob_query, insert_blob_tuple)
        self.con.commit()



    

        self.cursor.execute("""INSERT INTO Features(feature) VALUES("{}");""".format(self.add_spe_intel[1].get()))
        self.con.commit()

        #add
        

        self.cursor.execute("select max(media_id) from Media;")
        media_id_here = self.cursor.fetchall()

        self.cursor.execute("select max(feature_id) from Feature;")
        feature_id_here = self.cursor.fetchall()



        #add


        self.cursor.execute("""INSERT INTO media_features(media_id, feature_id) VALUES({}, {}) ;""".format(media_id_here, media_id_here))
        self.con.commit()


        self.cursor.execute("""INSERT INTO special_intel(media_id, person_id) VALUES({}, {});""".format(media_id_here, self.add_spe_intel[0].get()))
        self.con.commit()


    def insert_special_intel_by_organ(self):
        
        cmd = "select organ_id from Organisation where organ_id = {};".format(self.add_spe_intel[0].get())
        self.cursor.execute(cmd)
        flag = self.cursor.fetchall()
        
        if flag == []:
            info("error", "id doesn't exist")
            return



        def convertToBinaryData(filename):
            # Convert digital data to binary format
            with open(filename, 'rb') as file:
                binaryData = file.read()
            return binaryData

        sql_insert_blob_query = """ INSERT INTO Media
                            (media_blob) VALUES (%s)"""

        empPicture = convertToBinaryData(self.addr)

        # Convert data into tuple format
        insert_blob_tuple = (empPicture, )
        self.cursor.execute(sql_insert_blob_query, insert_blob_tuple)

        self.con.commit()
        


        self.cursor.execute("""INSERT INTO Features(feature) VALUES("{}");""".format(self.add_spe_intel[1].get()))
        self.con.commit()

        #add
        

        self.cursor.execute("select max(media_id) from Media;")
        media_id_here = self.cursor.fetchall()

        self.cursor.execute("select max(feature_id) from Feature;")
        feature_id_here = self.cursor.fetchall()



        #add


        self.cursor.execute("""INSERT INTO media_features(media_id, feature_id) VALUES({}, {}) ;""".format(media_id_here, feature_id_here))
        self.con.commit()


        self.cursor.execute("""INSERT INTO special_intel(media_id, organ_id) VALUES({}, {});""".format(media_id_here, self.add_spe_intel[0].get()))
        self.con.commit()



    def insert_special_ops_by_person(self):

        person_id_here = self.add_spe_ops[0].get()
        info_here = self.add_spe_ops[1].get()
        date_here = self.add_spe_ops[2].get()

        

        
        cmd = "select person_id from Person where person_id = {};".format(self.add_spe_ops[0].get())
        self.cursor.execute(cmd)
        flag = self.cursor.fetchall()
        
        if flag == []:
            info("error", "id doesn't exist")
            return



        sql_insert_blob_query = """ INSERT INTO Action
                            (name, date) VALUES ("{}", "{}");""".format(info_here, date_here)


        # Convert data into tuple format
        self.cursor.execute(sql_insert_blob_query)
        self.con.commit()


        #add
        

        self.cursor.execute("select max(action_id) from Action;")
        action_id_here = self.cursor.fetchall()[0][0]


        #add


        self.cursor.execute("""INSERT INTO special_ops(action_id, person_id) VALUES({}, {}) ;""".format(action_id_here, person_id_here))
        self.con.commit()


    def insert_special_ops_by_organ(self):

        organ_id_here = self.add_spe_ops[0].get()
        info_here = self.add_spe_ops[1].get()
        date_here = self.add_spe_ops[2].get()

        

        
        cmd = "select organ_id from Organisation where organ_id = {};".format(self.add_spe_ops[0].get())
        self.cursor.execute(cmd)
        flag = self.cursor.fetchall()
        
        if flag == []:
            info("error", "id doesn't exist")
            return



        sql_insert_blob_query = """ INSERT INTO Action
                            (name, date) VALUES ("{}", "{}");""".format(info_here, date_here)


        # Convert data into tuple format
        self.cursor.execute(sql_insert_blob_query)
        self.con.commit()


        #add
        

        self.cursor.execute("select max(action_id) from Action;")
        action_id_here = self.cursor.fetchall()[0][0]


        #add


        self.cursor.execute("""INSERT INTO special_ops(action_id, organ_id) VALUES({}, {}) ;""".format(action_id_here, organ_id_here))
        self.con.commit()




    def insert_person(self):
        
        name_here = self.add_person[0].get()
        dob_here = self.add_person[1].get()
        status_here = self.add_person[2].get()
        organ_id_here = self.add_person[3].get()
        location_id_here = self.add_person[4].get()

        

        def convertToBinaryData(filename):
            # Convert digital data to binary format
            with open(filename, 'rb') as file:
                binaryData = file.read()
            return binaryData

        sql_insert_blob_query = """ INSERT INTO Media
                            (media_blob) VALUES (%s)"""

        empPicture = convertToBinaryData(self.picadr)

        # Convert data into tuple format
        insert_blob_tuple = (empPicture, )
        self.cursor.execute(sql_insert_blob_query, insert_blob_tuple)
        self.con.commit()


        #add
        

        self.cursor.execute("select max(media_id) from Media;")
        media_id_here = self.cursor.fetchall()[0][0]



        #add


        self.cursor.execute("""INSERT INTO Person(name, dob, citizen_status, organ_id, location_id, media_id) VALUES("{}", "{}", "{}", {}, {}, {}) ;""".format(name_here, dob_here, status_here, organ_id_here, location_id_here, media_id_here))
        self.con.commit()



    def insert_crime_of_person(self):

        person_id_here = self.add_crime[0].get()
        date_here = self.add_crime[1].get()
        details_here = self.add_crime[2].get()

        cmd = "select person_id from Person where person_id = {};".format(person_id_here)
        self.cursor.execute(cmd)
        flag = self.cursor.fetchall()
        
        if flag == []:
            info("error", "id doesn't exist")
            return





    

        self.cursor.execute("""INSERT INTO Action(date, name) VALUES("{}","{}");""".format(date_here, details_here))
        self.con.commit()

        #add
        

        self.cursor.execute("select max(action_id) from Action;")
        action_id_here = self.cursor.fetchall()[0][0]



        #add


        self.cursor.execute("""INSERT INTO criminal_record(action_id, person_id) VALUES({}, {}) ;""".format(action_id_here, person_id_here))
        self.con.commit()



    def insert_ally_by_country(self):

        country_id_here = self.add_allies[0].get()
        ally_id_here = self.add_allies[1].get()
        
        

        
        cmd = "select country_id from Country where country_id = {};".format(country_id_here)
        self.cursor.execute(cmd)
        flag = self.cursor.fetchall()
        
        if flag == []:
            info("error", "id doesn't exist")
            return

        cmd = "select country_id from Country where country_id = {};".format(ally_id_here)
        self.cursor.execute(cmd)
        flag = self.cursor.fetchall()
        
        if flag == []:
            info("error", "ally id error")
            return

        
        cmd = "select enemy_id from country_enemy where country_id = {} and enemy_id={};".format(country_id_here, ally_id_here)
        self.cursor.execute(cmd)
        flag = self.cursor.fetchall()
        
        if flag != []:
            info("error", "said ally is enemy")
            return

        
        


        self.cursor.execute("""INSERT INTO country_alias(country_id, alias_id) VALUES({}, {}) ;""".format(country_id_here, ally_id_here))
        self.con.commit()

        
    

    def insert_enemy_by_country(self):

        country_id_here = self.add_allies[0].get()
        enemy_id_here = self.add_allies[2].get()
        
        

        
        cmd = "select country_id from Country where country_id = {};".format(country_id_here)
        self.cursor.execute(cmd)
        flag = self.cursor.fetchall()
        
        if flag == []:
            info("error", "id doesn't exist")
            return

        cmd = "select country_id from Country where country_id = {};".format(enemy_id_here)
        self.cursor.execute(cmd)
        flag = self.cursor.fetchall()
        
        if flag == []:
            info("error", "enemy id error")
            return

        
        cmd = "select alias_id from country_alias where country_id = {} and alias_id={};".format(country_id_here, enemy_id_here)
        self.cursor.execute(cmd)
        flag = self.cursor.fetchall()
        
        if flag != []:
            info("error", "said enemy is ally")
            return

        
        


        self.cursor.execute("""INSERT INTO country_enemy(country_id, enemy_id) VALUES({}, {}) ;""".format(country_id_here, enemy_id_here))
        self.con.commit()

        



    def delete_ally_by_country(self):

        country_id_here = self.delete_allies[0].get()
        ally_id_here = self.delete_allies[1].get()
        
        

        
        cmd = "select country_id from Country where country_id = {};".format(country_id_here)
        self.cursor.execute(cmd)
        flag = self.cursor.fetchall()
        
        if flag == []:
            info("error", "id doesn't exist")
            return

        cmd = "select country_id from Country where country_id = {};".format(ally_id_here)
        self.cursor.execute(cmd)
        flag = self.cursor.fetchall()
        
        if flag == []:
            info("error", "ally id error")
            return

        
        cmd = "select alias_id from country_alias where country_id = {} and alias_id={};".format(country_id_here, ally_id_here)
        self.cursor.execute(cmd)
        flag = self.cursor.fetchall()
        
        if flag == []:
            info("error", "ally doesn't exist")
            return

        
        


        self.cursor.execute("""delete from country_alias where country_id={} and alias_id={} ;""".format(country_id_here, ally_id_here))
        self.con.commit()

        
    

    def delete_enemy_by_country(self):

        country_id_here = self.delete_allies[0].get()
        enemy_id_here = self.delete_allies[2].get()
        
        

        
        cmd = "select country_id from Country where country_id = {};".format(country_id_here)
        self.cursor.execute(cmd)
        flag = self.cursor.fetchall()
        
        if flag == []:
            info("error", "id doesn't exist")
            return

        cmd = "select country_id from Country where country_id = {};".format(enemy_id_here)
        self.cursor.execute(cmd)
        flag = self.cursor.fetchall()
        
        if flag == []:
            info("error", "enemy id error")
            return

        
        cmd = "select enemy_id from country_enemy where country_id = {} and enemy_id={};".format(country_id_here, enemy_id_here)
        self.cursor.execute(cmd)
        flag = self.cursor.fetchall()
        
        if flag == []:
            info("error", "enemy doesn't exist")
            return

        
        


        self.cursor.execute("""delete from country_enemy where country_id={} and enemy_id={}; """.format(country_id_here, enemy_id_here))
        self.con.commit()

        



    def update_status_by_person_id(self):

        person_id_here = self.update_person[0].get()
        status_here = self.update_person[1].get()
        
       
        cmd = "select person_id from Person where person_id = {};".format(person_id_here)
        self.cursor.execute(cmd)
        flag = self.cursor.fetchall()
        
        if flag == []:
            info("error", "id doesn't exist")
            return

        self.cursor.execute("""update Person set citizen_status = "{}" where person_id ={}; """.format(status_here
        , person_id_here))

        self.con.commit()




    def update_organ_by_person_id(self):

        person_id_here = self.update_person[0].get()
        organ_id_here = self.update_person[2].get()
        
    
        cmd = "select person_id from Person where person_id = {};".format(person_id_here)
        self.cursor.execute(cmd)
        flag = self.cursor.fetchall()
        
        if flag == []:
            info("error", "id doesn't exist")
            return


        cmd = "select organ_id from Organisation where organ_id = {};".format(organ_id_here)
        self.cursor.execute(cmd)
        flag = self.cursor.fetchall()
        
        if flag == []:
            info("error", "organ id error")
            return

        self.cursor.execute("""update Person set organ_id = "{}" where person_id ={}; """.format(organ_id_here
        , person_id_here))

        self.con.commit()

    
    def update_leader_by_organ_id(self):

        organ_id_here = self.update_organ[0].get()
        person_id_here = self.update_organ[1].get()
        
        cmd = "select organ_id from Organisation where organ_id = {};".format(organ_id_here)
        self.cursor.execute(cmd)
        flag = self.cursor.fetchall()
        
        if flag == []:
            info("error", "id doesn't exist")
            return

        cmd = "select person_id from Person where person_id = {};".format(person_id_here)
        self.cursor.execute(cmd)
        flag = self.cursor.fetchall()
        
        if flag == []:
            info("error", "leader id error")
            return

        self.cursor.execute("""update Organisation set leader = "{}" where organ_id ={}; """.format(person_id_here
        , organ_id_here))

        self.con.commit()

    

    def update_weapon_by_country_id(self):
        
        country_id_here = int(self.update_country[0].get())
        nukes_here = int(self.update_country[1].get())
        chem_here = int(self.update_country[2].get())
        bio_here = int(self.update_country[3].get())
        print("=============",nukes_here,"===========")

        
        
        cmd = "select country_id from Country where country_id = {};".format(country_id_here)
        self.cursor.execute(cmd)
        flag = self.cursor.fetchall()
        
        if flag == []:
            info("error", "id doesn't exist")
            return

        
       
        cmd = "select * from country_weapon where country_id = {};".format(country_id_here)
        self.cursor.execute(cmd)
        nbc_id = self.cursor.fetchall()

        if nbc_id == []:
            if nukes_here != -1:
                cmd = "insert into Weapons (NUMBER) values ({}); ".format(nukes_here)
                self.cursor.execute(cmd)
                self.con.commit()

                #add
                

                self.cursor.execute("select max(weapon_id) from Weapons;")
                nukes_id_here = self.cursor.fetchall()[0][0]

            else:
                nukes_id_here = 0



            if chem_here != -1:
                cmd = "insert into Weapons (NUMBER) values ({}); ".format(chem_here)
                self.cursor.execute(cmd)
                self.con.commit()

                #add
                

                self.cursor.execute("select max(weapon_id) from Weapons;")
                chem_id_here = self.cursor.fetchall()[0][0]
            else:
                chem_id_here = 0



            if bio_here != -1:
                cmd = "insert into Weapons (NUMBER) values ({}); ".format(bio_here)
                self.cursor.execute(cmd)
                self.con.commit()

                #add
                

                self.cursor.execute("select max(weapon_id) from Weapons;")
                bio_id_here = self.cursor.fetchall()[0][0]

            else:
                bio_id_here = 0



            self.cursor.execute("""insert into country_weapon values ({},{},{},{}); """.format(country_id_here,nukes_id_here,bio_id_here,chem_id_here)) 
            self.con.commit()

            return



        nbc_id = list(nbc_id[0][1:])


        old_nbc = (nbc_id[0], nbc_id[1], nbc_id[2])

        if nukes_here != -1:
            cmd = "insert into Weapons (NUMBER) values ({}); ".format(nukes_here)
            self.cursor.execute(cmd)
            

            self.con.commit()
            #add
            self.cursor.execute("select max(weapon_id) from Weapons;")
            nbc_id[0] = self.cursor.fetchall()[0][0]
        
        if chem_here != -1:
            cmd = "insert into Weapons (NUMBER) values ({}); ".format(chem_here)
            self.cursor.execute(cmd)
            

            self.con.commit()
            #add
            self.cursor.execute("select max(weapon_id) from Weapons;")
            nbc_id[1] = self.cursor.fetchall()[0][0]



        if bio_here != -1:
            cmd = "insert into Weapons (NUMBER) values ({}); ".format(bio_here)
            self.cursor.execute(cmd)
            

            self.con.commit()
            #add
            self.cursor.execute("select max(weapon_id) from Weapons;")
            nbc_id[2] = self.cursor.fetchall()[0][0]




        print("==",nbc_id,"==")
            
        self.cursor.execute("""update country_weapon set nuclear_id = {}, biological_id={}, chemical_id = {} where country_id ={}; 
        """.format(nbc_id[0], nbc_id[1], nbc_id[2], country_id_here))

        self.con.commit()

        if nukes_here != -1:
            cmd = "delete from Weapons where weapon_id = {}; ".format(old_nbc[0])
            self.cursor.execute(cmd)
        if chem_here != -1:
            cmd = "delete from Weapons where weapon_id = {}; ".format(old_nbc[1])
            self.cursor.execute(cmd)
        if bio_here != -1:
            cmd = "delete from Weapons where weapon_id = {}; ".format(old_nbc[2])
            self.cursor.execute(cmd)
        

        self.con.commit()

    



    def __init__(self, master):
        
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='#A2E3C3')
        self.pack(expand=True, fill=tk.BOTH)
        

        self.scrollFrame = ScrollFrame(self) # add a new scrollable frame.
        
        # Now add some controls to the scrollframe. 
        # NOTE: the child controls are added to the view port (scrollFrame.viewPort, NOT scrollframe itself)
        
        # when packing the scrollframe, we pack scrollFrame itself (NOT the viewPort)
        self.scrollFrame.pack(expand=True, fill=tk.BOTH)
        #self.scrollFrame.configure(self,bg='#ABE1DD')

        #for connecting with mysql
        self.command = ""
        self.con = mysql.connect(host="sql12.freemysqlhosting.net", user="sql12344028", password="3lgjXwAmtj", database="sql12344028",port=3306)
        self.cursor = self.con.cursor()



         #heading
        tk.Label(self.scrollFrame.viewPort, text=" ",bg="#A2E3C3", border=0, height=2).grid(row=1, column=1)
        tk.Button(self.scrollFrame.viewPort, text="..",bg="#A2FD9F",command=lambda: master.switch_frame(LoginScreen), border=0).grid(row=1, column=7)
        tk.Label(self.scrollFrame.viewPort, text=" "*4,bg="#A2E3C3", border=0).grid(row=2, column=1)
        l1 = tk.Label(self.scrollFrame.viewPort, text="Data Entry", font=('times', 27, "bold"), bg="#8AEDA4", fg="white", height=0, width=10, border=0).grid(row=2, column=2)
        for i in range(3,10):
            tk.Label(self.scrollFrame.viewPort, text=" "*25,bg="#A2E3C3", border=0, width=24).grid(row=2, column=i)
        
        tk.Label(self.scrollFrame.viewPort, text=" ",bg="#A2E3C3", border=0, height=4).grid(row=3, column=3)
        tk.Label(self.scrollFrame.viewPort, text="Intel :",bg="#8AEDA4",font=('times', 18), border=0, height=1).grid(row=4, column=1)


        #all inputs for special intel
        self.addr = ""

        self.add_spe_intel = [1,2,3,4,5, 6]        
        for i in range(3):
            self.add_spe_intel[i] = tk.Entry(self.scrollFrame.viewPort, border=0)
            self.add_spe_intel[i].grid(row=5, column=2+i)
        self.add_spe_intel[3] = tk.Button(self.scrollFrame.viewPort, text="address of intel",bg="#D1ABFF", font=40, command=self.browsefunc, border=0)
        self.add_spe_intel[3].grid(row=5, column=5)

        self.add_spe_intel[0].insert(0,"person id/ organ id")
        self.add_spe_intel[1].insert(0,"about the intel")

        tk.Label(self.scrollFrame.viewPort, text=" ",bg="#A2E3C3", border=0, height=1).grid(row=6, column=1)

        self.add_spe_intel[4] = tk.Button(self.scrollFrame.viewPort, text="insert by person id",bg="#A8C8ED", command = self.insert_special_intel_by_person, font=40, border=0)
        self.add_spe_intel[4].grid(row=7, column=3)
        self.add_spe_intel[5] = tk.Button(self.scrollFrame.viewPort, text="insert by organ id",bg="#A8C8ED", command = self.insert_special_intel_by_organ,font=40, border=0)
        self.add_spe_intel[5].grid(row=7, column=4)

        tk.Label(self.scrollFrame.viewPort, text=" ",bg="#A2E3C3", border=0, height=4).grid(row=8, column=3)
        tk.Label(self.scrollFrame.viewPort, text="Ops:",bg="#8AEDA4",font=('times', 18), border=0, height=1).grid(row=9, column=1)
        


        #all inputs for special operations
        self.addr = ""

        self.add_spe_ops = [1,2,3,4,5,6]
        for i in range(3):
            self.add_spe_ops[i] = tk.Entry(self.scrollFrame.viewPort, border=0)
            self.add_spe_ops[i].grid(row=10, column=2+i)

        self.add_spe_ops[0].insert(0,"person id/ organ id")
        self.add_spe_ops[1].insert(0,"about the operation")
        self.add_spe_ops[2].insert(0,"date in YYYY-MM-DD")

        tk.Label(self.scrollFrame.viewPort, text=" ",bg="#A2E3C3", border=0, height=1).grid(row=11, column=1)

        self.add_spe_ops[4] = tk.Button(self.scrollFrame.viewPort,command=self.insert_special_ops_by_person , text="insert by person id",bg="#A8C8ED", font=40, border=0)
        self.add_spe_ops[4].grid(row=12, column=3)
        self.add_spe_ops[5] = tk.Button(self.scrollFrame.viewPort, command=self.insert_special_ops_by_organ, text="insert by organ id",bg="#A8C8ED", font=40, border=0)
        self.add_spe_ops[5].grid(row=12, column=4)
        
        tk.Label(self.scrollFrame.viewPort, text=" ",bg="#A2E3C3", border=0, height=4).grid(row=13, column=3)
        tk.Label(self.scrollFrame.viewPort, text="Person:",font=('times', 18),bg="#8AEDA4", border=0, height=1).grid(row=14, column=1)
       
        

        
        #all inputs of person
        self.picadr = "/demo.png"
        self.add_person = [1,2,3,4,5,6,7,8]
        
        for i in range(5):
            self.add_person[i] = tk.Entry(self.scrollFrame.viewPort, border=0)
            self.add_person[i].grid(row=15, column=2+i)
        
        self.special_for_person = tk.Entry(self.scrollFrame.viewPort, border=0)
        self.special_for_person.grid(row=15, column=7)

        

        self.add_person[0].insert(0,"name")
        self.add_person[1].insert(0,"1900-01-01")
        self.add_person[2].insert(0,"f--")
        self.add_person[3].insert(0,"0")
        self.add_person[4].insert(0,"0")
        self.special_for_person.insert(0,"/demo.png")


        tk.Label(self.scrollFrame.viewPort, text=" ",bg="#A2E3C3", border=0, height=1).grid(row=16, column=1)

        self.add_person[7] = tk.Button(self.scrollFrame.viewPort, command=self.insert_person, text="insert ",bg="#A8C8ED", font=40, border=0)
        self.add_person[7].grid(row=17, column=3)

        self.special_for_person2 = tk.Button(self.scrollFrame.viewPort, text="pic",bg="#D1ABFF", font=40, command=self.browsefunc1, border=0)
        self.special_for_person2.grid(row=17, column=7)


        tk.Label(self.scrollFrame.viewPort, text=" ",bg="#A2E3C3", border=0, height=4).grid(row=18, column=3)
        tk.Label(self.scrollFrame.viewPort, text="Crime:",font=('times', 18),bg="#8AEDA4", border=0, height=1).grid(row=19, column=1)
       
       

        
        #all inputs of crime
        self.addr = ""

        self.add_crime = [1,2,3,4,5]
        for i in range(3):
            self.add_crime[i] = tk.Entry(self.scrollFrame.viewPort, border=0)
            self.add_crime[i].grid(row=20, column=2+i)

        self.add_crime[0].insert(0,"person id")
        self.add_crime[1].insert(0,"date in YYYY-MM-DD")
        self.add_crime[2].insert(0,"crime details")

        tk.Label(self.scrollFrame.viewPort, text=" ",bg="#A2E3C3", border=0, height=1).grid(row=21, column=1)

        self.picadr = "/demo.png"

        self.add_crime[3] = tk.Button(self.scrollFrame.viewPort, command = self.insert_crime_of_person, text="insert ",bg="#A8C8ED", font=40, border=0)
        self.add_crime[3].grid(row=22, column=3)

        tk.Label(self.scrollFrame.viewPort, text=" ",bg="#A2E3C3", border=0, height=4).grid(row=23, column=3)
        tk.Label(self.scrollFrame.viewPort, text="Country:",font=('times', 18),bg="#8AEDA4", border=0, height=1).grid(row=24, column=1)
       
       


        
        #all inputs of country
        self.addr = ""

        self.add_allies = [1,2,3,4,5]
        for i in range(3):
            self.add_allies[i] = tk.Entry(self.scrollFrame.viewPort, border=0)
            self.add_allies[i].grid(row=25, column=2+i)

        self.add_allies[0].insert(0,"country id")
        self.add_allies[1].insert(0,"ally id")
        self.add_allies[2].insert(0,"enemy id")

        tk.Label(self.scrollFrame.viewPort, text=" ",bg="#A2E3C3", border=0, height=1).grid(row=26, column=1)

        self.picadr = "/demo.png"

        self.add_allies[3] = tk.Button(self.scrollFrame.viewPort, command = self.insert_ally_by_country, text="insert ally",bg="#A8C8ED", font=40, border=0)
        self.add_allies[3].grid(row=27, column=3)
        self.add_allies[4] = tk.Button(self.scrollFrame.viewPort, command = self.insert_enemy_by_country, text="insert enemy",bg="#A8C8ED", font=40, border=0)
        self.add_allies[4].grid(row=27, column=4)

        tk.Label(self.scrollFrame.viewPort, text=" ",bg="#A2E3C3", border=0, height=1).grid(row=28, column=3)
        

        #for deeleting allies/enemies
        self.addr = ""

        self.delete_allies = [1,2,3,4,5]
        for i in range(3):
            self.delete_allies[i] = tk.Entry(self.scrollFrame.viewPort, border=0)
            self.delete_allies[i].grid(row=29, column=2+i)

        self.delete_allies[0].insert(0,"country id")
        self.delete_allies[1].insert(0,"ally id")
        self.delete_allies[2].insert(0,"enemy id")

        tk.Label(self.scrollFrame.viewPort, text=" ",bg="#A2E3C3", border=0, height=1).grid(row=30, column=1)

        self.picadr = "/demo.png"

        self.delete_allies[3] = tk.Button(self.scrollFrame.viewPort, command = self.delete_ally_by_country, text="delete ally",bg="#A8C8ED", font=40, border=0)
        self.delete_allies[3].grid(row=31, column=3)
        self.delete_allies[4] = tk.Button(self.scrollFrame.viewPort, command = self.delete_enemy_by_country, text="delete enemy",bg="#A8C8ED", font=40, border=0)
        self.delete_allies[4].grid(row=31, column=4)

        tk.Label(self.scrollFrame.viewPort, text=" ",bg="#A2E3C3", border=0, height=4).grid(row=32, column=3)
        tk.Label(self.scrollFrame.viewPort, text="Person:",font=('times', 18),bg="#8AEDA4", border=0, height=1).grid(row=33, column=1)
       
    


        #for updating person data 
        self.addr = ""

        self.update_person = [1,2,3,4, 5]
        for i in range(3):
            self.update_person[i] = tk.Entry(self.scrollFrame.viewPort, border=0)
            self.update_person[i].grid(row=34, column=2+i)

        self.update_person[0].insert(0,"person id")
        self.update_person[1].insert(0,"status")
        self.update_person[2].insert(0,"organ id")

        tk.Label(self.scrollFrame.viewPort, text=" ",bg="#A2E3C3", border=0, height=1).grid(row=35, column=1)

        self.picadr = "/demo.png"

        self.update_person[4] = tk.Button(self.scrollFrame.viewPort, command = self.update_status_by_person_id, text="update status ",bg="#A8C8ED", font=40, border=0)
        self.update_person[4].grid(row=36, column=3)

        self.update_person[3] = tk.Button(self.scrollFrame.viewPort, command = self.update_organ_by_person_id, text="update organ id ",bg="#A8C8ED", font=40, border=0)
        self.update_person[3].grid(row=36, column=4)

        tk.Label(self.scrollFrame.viewPort, text=" ",bg="#A2E3C3", border=0, height=4).grid(row=37, column=3)
        tk.Label(self.scrollFrame.viewPort, text="Organisation:",font=('times', 18),bg="#8AEDA4", border=0, height=1).grid(row=38, column=1)
       


        #for updating organisation data 
        self.addr = ""

        self.update_organ = [1,2,3]
        for i in range(2):
            self.update_organ[i] = tk.Entry(self.scrollFrame.viewPort, border=0)
            self.update_organ[i].grid(row=39, column=2+i)

        self.update_organ[0].insert(0,"organ id")
        self.update_organ[1].insert(0,"leader id")

        tk.Label(self.scrollFrame.viewPort, text=" ",bg="#A2E3C3", border=0, height=1).grid(row=40, column=1)

        self.picadr = "/demo.png"

        self.update_organ[2] = tk.Button(self.scrollFrame.viewPort, command = self.update_leader_by_organ_id, text="update leader ",bg="#A8C8ED", font=40, border=0)
        self.update_organ[2].grid(row=41, column=3)

        tk.Label(self.scrollFrame.viewPort, text=" ",bg="#A2E3C3", border=0, height=4).grid(row=42, column=3)
        tk.Label(self.scrollFrame.viewPort, text="Country:",font=('times', 18),bg="#8AEDA4", border=0, height=1).grid(row=43, column=1)
       



        #for updating country data 
        self.addr = ""

        self.update_country = [1,2,3,4,5]
        for i in range(4):
            self.update_country[i] = tk.Entry(self.scrollFrame.viewPort, border=0)
            self.update_country[i].grid(row=44, column=2+i)

        self.update_country[0].insert(0,"country id")
        self.update_country[1].insert(0,"nukes count (def:-1)")
        self.update_country[2].insert(0,"chem. wep count(def:-1)")
        self.update_country[3].insert(0,"bio. wep count(def:-1)")


        tk.Label(self.scrollFrame.viewPort, text=" ",bg="#A2E3C3", border=0, height=1).grid(row=45, column=1)

        self.picadr = "/demo.png"

        self.update_country[4] = tk.Button(self.scrollFrame.viewPort, command = self.update_weapon_by_country_id, text="update count ",bg="#A8C8ED", font=40, border=0)
        self.update_country[4].grid(row=46, column=3)



intel_ui().mainloop()

