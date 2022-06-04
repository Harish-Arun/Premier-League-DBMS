import sqlite3
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

def connection():
    con=sqlite3.connect('sport.db')
    cursor=con.cursor()
    return con,cursor

# Windows
def home_away_win(tree, home):
    idx = tree.selection()[0]
    tree_item = tree.item(idx)
    f_id = tree_item['text']
    team_name = tree_item['values'][2] if home else tree_item['values'][3]
    score = tree_item['values'][4].strip()
    home_goals = int(score.split('-')[0])
    away_goals = int(score.split('-')[1])
    win = Toplevel(root)
    win.geometry('520x650')
    if home:
        if home_goals > away_goals:
            status = "(Won)"
        elif home_goals < away_goals:
            status = "(Lost)"
        else:
            status = "(Draw)"
        win.title('Home Team: ' + team_name)
    else:
        if home_goals < away_goals:
            status = "(Won)"
        elif home_goals > away_goals:
            status = "(Lost)"
        else:
            status = "(Draw)"
        win.title('Away Team: ' + team_name)

    win.iconbitmap('PLicon.ico')

    main_frame = Frame(win)
    main_frame.pack(fill=BOTH, expand=1)

    my_canvas = Canvas(main_frame)
    my_canvas.pack(side = LEFT, fill=BOTH, expand=1)

    my_scrollbar = ttk.Scrollbar(main_frame, orient = VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)
    
    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

    second_frame = Frame(my_canvas)

    my_canvas.create_window((30,0),window=second_frame,anchor="nw")

    third_frame = Frame(second_frame, bd=2, relief=GROOVE)
    third_frame.pack(fill=X, expand=1,pady=15)
    fourth_frame = Frame(third_frame)
    fourth_frame.pack()
    title_label = Label(fourth_frame,text=team_name,font=("Calibri bold", 18))
    title_label.pack(side=LEFT,pady=8)
    
    if status == '(Won)':
        match_label = Label(fourth_frame,text=status,font=("Calibri bold", 18), fg="green")
    elif status == '(Lost)':
        match_label = Label(fourth_frame,text=status,font=("Calibri bold", 18), fg="red")
    else:
        match_label = Label(fourth_frame,text=status,font=("Calibri bold", 18), fg="gray")

    match_label.pack(side=LEFT)

    playing_label = Label(second_frame,text="Playing 11:",font=("Calibri", 15))
    playing_label.pack(pady=7)
      
    table_frame = Frame(second_frame)
    table_frame.pack()
    sb = ttk.Scrollbar(table_frame)  
    tree1=ttk.Treeview(table_frame, height=7,yscrollcommand = sb.set)
    tree1["columns"]=("one","two")
    tree1.column("#0", width=100, minwidth=100, stretch=NO,anchor=CENTER)
    tree1.column("one", width=190, minwidth=100, stretch=NO,anchor=CENTER)
    tree1.column("two", width=150, minwidth=100,stretch=NO,anchor=CENTER)
    tree1.heading("#0",text="JerseyNo")
    tree1.heading("one", text="PlayerName")
    tree1.heading("two", text="Position")

    sb.config(command = tree1.yview)
    sb.pack(side = RIGHT, fill=Y)
    tree1.pack(fill=X)
    

    #inserting values to tree
    con, cur = connection()
    if home:
        lst = cur.execute(f"select a.Jersey_No, a.PlayerName, a.Pos from List_of_Players a, Homeplayers b where a.Jersey_No = b.Jersey_No and a.TeamName = b.Hometeam and b.F_id={f_id} and Playing11='yes'")
    else:
        lst = cur.execute(f"select a.Jersey_No, a.PlayerName, a.Pos from List_of_Players a, Awayplayers b where a.Jersey_No = b.Jersey_No and a.TeamName = b.Awayteam and b.F_id={f_id} and Playing11='yes'")
    i=1
    for tup in lst:
            data0,data1,data2=tup
            if i%2==0:
                tree1.insert("", "end", text=str(data0), values=(str(data1).strip(), str(data2).strip()),tags=('even',))
                tree1.tag_configure('even', background='#efefef')
            else:
                tree1.insert("", "end", text=str(data0), values=(str(data1).strip(), str(data2).strip()),tags=('odd',))
                tree1.tag_configure('odd', background='#fafafa')
            i+=1
    con.commit()
    con.close()

    Label(second_frame,text=" ").pack(pady=2)
    Subs_label = Label(second_frame,text="Substitutes:",font=("Calibri", 15))
    Subs_label.pack(pady=10)

    table_frame2 = Frame(second_frame)
    table_frame2.pack()
    sb2 = ttk.Scrollbar(table_frame2)  
    tree2=ttk.Treeview(table_frame2, height=7,yscrollcommand = sb2.set)
    tree2["columns"]=("one","two")
    tree2.column("#0", width=100, minwidth=100, stretch=NO,anchor=CENTER)
    tree2.column("one", width=190, minwidth=100, stretch=NO,anchor=CENTER)
    tree2.column("two", width=150, minwidth=100,stretch=NO,anchor=CENTER)
    tree2.heading("#0",text="JerseyNo")
    tree2.heading("one", text="PlayerName")
    tree2.heading("two", text="Position")

    sb2.config(command = tree2.yview)
    sb2.pack(side = RIGHT, fill=Y)
    tree2.pack(fill=X)
    

    #inserting values to tree
    con, cur = connection()
    if home:
        lst = cur.execute(f"select a.Jersey_No, a.PlayerName, a.Pos from List_of_Players a, Homeplayers b where a.Jersey_No = b.Jersey_No and a.TeamName = b.Hometeam and b.F_id={f_id} and Playing11='sub'")
    else:
        lst = cur.execute(f"select a.Jersey_No, a.PlayerName, a.Pos from List_of_Players a, Awayplayers b where a.Jersey_No = b.Jersey_No and a.TeamName = b.Awayteam and b.F_id={f_id} and Playing11='sub'")
    i=1
    for tup in lst:
            data0,data1,data2=tup
            if i%2==0:
                tree2.insert("", "end", text=str(data0), values=(str(data1).strip(), str(data2).strip()),tags=('even',))
                tree2.tag_configure('even', background='#efefef')
            else:
                tree2.insert("", "end", text=str(data0), values=(str(data1).strip(), str(data2).strip()),tags=('odd',))
                tree2.tag_configure('odd', background='#fafafa')
            i+=1
    con.commit()
    con.close()

    Label(second_frame,text=" ").pack(pady=2)

    Res_label = Label(second_frame,text="Reserves:",font=("Calibri", 15))
    Res_label.pack(pady=10)

    table_frame3 = Frame(second_frame)
    table_frame3.pack()
    sb3 = ttk.Scrollbar(table_frame3)  
    tree3=ttk.Treeview(table_frame3, height=5,yscrollcommand = sb3.set)
    tree3["columns"]=("one","two")
    tree3.column("#0", width=100, minwidth=100, stretch=NO,anchor=CENTER)
    tree3.column("one", width=190, minwidth=100, stretch=NO,anchor=CENTER)
    tree3.column("two", width=150, minwidth=100,stretch=NO,anchor=CENTER)
    tree3.heading("#0",text="JerseyNo")
    tree3.heading("one", text="PlayerName")
    tree3.heading("two", text="Position")

    sb3.config(command = tree3.yview)
    sb3.pack(side = RIGHT, fill=Y)
    tree3.pack(fill=X)
    
    Label(second_frame,text=" ").pack(pady=5)

    #inserting values to tree
    con, cur = connection()
    if home:
        lst = cur.execute(f"select a.Jersey_No, a.PlayerName, a.Pos from List_of_Players a, Homeplayers b where a.Jersey_No = b.Jersey_No and a.TeamName = b.Hometeam and b.F_id={f_id} and Playing11='res'")
    else:
        lst = cur.execute(f"select a.Jersey_No, a.PlayerName, a.Pos from List_of_Players a, Awayplayers b where a.Jersey_No = b.Jersey_No and a.TeamName = b.Awayteam and b.F_id={f_id} and Playing11='res'")
    i=1
    for tup in lst:
            data0,data1,data2=tup
            if i%2==0:
                tree3.insert("", "end", text=str(data0), values=(str(data1).strip(), str(data2).strip()),tags=('even',))
                tree3.tag_configure('even', background='#efefef')
            else:
                tree3.insert("", "end", text=str(data0), values=(str(data1).strip(), str(data2).strip()),tags=('odd',))
                tree3.tag_configure('odd', background='#fafafa')
            i+=1
    con.commit()
    con.close()



def fixtures_win():

    win = Toplevel(root)
    win.geometry('750x320')
    win.title('Fixtures')
    win.iconbitmap('PLicon.ico')

    title_label = Label(win,text="Fixtures",font=("Calibri bold", 18))
    title_label.pack(pady=10)

    table_frame = Frame(win)
    table_frame.pack()
    sb = ttk.Scrollbar(table_frame)  
    tree1=ttk.Treeview(table_frame,yscrollcommand = sb.set, height=5 )
    tree1["columns"]=("one","two","three","four","five")
    tree1.column("#0", width=60, minwidth=40, stretch=NO,anchor=CENTER)
    tree1.column("one", width=100, minwidth=80, stretch=NO,anchor=CENTER)
    tree1.column("two", width=100, minwidth=80,stretch=NO,anchor=CENTER)
    tree1.column("three", width=160, minwidth=80, stretch=NO,anchor=CENTER)
    tree1.column("four", width=160, minwidth=80, stretch=NO,anchor=CENTER)
    tree1.column("five", width=100, minwidth=80, stretch=NO,anchor=CENTER)
    tree1.heading("#0",text="F_ID")
    tree1.heading("one", text="Date")
    tree1.heading("two", text="Time")
    tree1.heading("three", text="HomeTeam")
    tree1.heading("four", text="AwayTeam")
    tree1.heading("five", text="Score")
    sb.config(command = tree1.yview)
    sb.pack(side = RIGHT, fill=Y)
    tree1.pack(fill=X)

    btnFrame = Frame(win)
    players_button=ttk.Button(btnFrame,text="     Home Players     ",takefocus=False, command=lambda: home_away_win(tree1,True))
    players_button.pack(padx=20,pady=20,side=LEFT)
    managers_button=ttk.Button(btnFrame,text="      Away Players     ",takefocus=False,command=lambda: home_away_win(tree1,False))
    managers_button.pack(padx= 20,side=RIGHT)
    btnFrame.pack(fill=X)

    # inserting values to tree
    con, cur = connection()
    lst = cur.execute("select * from Fixtures")
    i=1
    for tup in lst:
            data0,data1,data2,data3,data4,data5=tup
            if i%2==0:
                tree1.insert("", "end", text=str(data0), values=(str(data1).strip(), str(data2).strip(), str(data3).strip(), str(data4).strip(), str(data5).strip()),tags=('even',))
                tree1.tag_configure('even', background='#efefef')
            else:
                tree1.insert("", "end", text=str(data0), values=(str(data1).strip(), str(data2).strip(), str(data3).strip(), str(data4).strip(), str(data5).strip()),tags=('odd',))
                tree1.tag_configure('odd', background='#fafafa')
            i+=1
    con.commit()
    con.close()

def players_win(tree):
    idx = tree.selection()[0]
    tree_item = tree.item(idx)
    team_name = tree_item['text']

    win = Toplevel(root)
    win.geometry('700x340')
    win.title('Team: '+team_name)
    win.iconbitmap('PLicon.ico')

    title_label = Label(win,text=team_name,font=("Calibri bold", 18))
    title_label.pack(pady=10)

    table_frame = Frame(win)
    table_frame.pack()
    sb = ttk.Scrollbar(table_frame)  
    tree1=ttk.Treeview(table_frame, height=9,yscrollcommand = sb.set)
    tree1["columns"]=("one","two","three","four")
    tree1.column("#0", width=90, minwidth=100, stretch=NO,anchor=CENTER)
    tree1.column("one", width=190, minwidth=50, stretch=NO,anchor=CENTER)
    tree1.column("two", width=140, minwidth=100,stretch=NO,anchor=CENTER)
    tree1.column("three", width=130, minwidth=100,stretch=NO,anchor=CENTER)
    tree1.column("four", width=100, minwidth=100,stretch=NO,anchor=CENTER)
    tree1.heading("#0",text="JerseyNo")
    tree1.heading("one", text="PlayerName")
    tree1.heading("two", text="Position")
    tree1.heading("three", text="DOB")
    tree1.heading("four", text="Age")
    sb.config(command = tree1.yview)
    sb.pack(side = RIGHT, fill=Y)
    tree1.pack(fill=X)

    # inserting values to tree
    con, cur = connection()
    lst = cur.execute(f"select Jersey_No,PlayerName,Pos,DOB,Age from List_of_Players where TeamName = '{team_name}'")
    i=1
    for tup in lst:
            data0,data1,data2,data3,data4=tup
            if i%2==0:
                tree1.insert("", "end", text=str(data0), values=(str(data1).strip(), str(data2).strip(), str(data3).strip(), str(data4).strip()),tags=('even',))
                tree1.tag_configure('even', background='#efefef')
            else:
                tree1.insert("", "end", text=str(data0), values=(str(data1).strip(), str(data2).strip(), str(data3).strip(), str(data4).strip()),tags=('odd',))
                tree1.tag_configure('odd', background='#fafafa')
            i+=1
    con.commit()
    con.close()
    
def manager_win(tree):
    #manager
    idx = tree.selection()
    tree_item = tree.item(idx)
    team_name = tree_item['text']

    con, cur = connection()
    cur.execute(f"select b.ManagerName, b.Age, b.Style from List_of_Teams a, ManagerDetails b where a.M_id = b.M_id and a.TeamName = '{team_name}';")
    lst = cur.fetchall()
    formation = lst[0][2]
    ManagerName = lst[0][0]
    ManagerAge = lst[0][1]

    win1 = Toplevel(root)
    win1.geometry('600x390')
    win1.title('Manager: '+ team_name)
    win1.iconbitmap('PLicon.ico')

    title_label = Label(win1,text=team_name,font=("Calibri bold", 20))
    title_label.place(x=300,y=30)

    name_label = Label(win1,text=f"Manager Name: {ManagerName}",font=("Calibri", 16))
    age_label = Label(win1,text=f"Manager Age: {ManagerAge}",font=("Calibri", 16))
    style_label = Label(win1,text=f"Formation: {formation}",font=("Calibri", 16))
    name_label.place(x=300,y=100)
    age_label.place(x=300,y=150)
    style_label.place(x=300,y=200)

    global new_image_1
    img= (Image.open(f"{formation}.png"))
    resized_image= img.resize((272,390), Image.ANTIALIAS)
    new_image_1= ImageTk.PhotoImage(resized_image)
    Label(win1, image=new_image_1).place(x=0,y=0)

def list_teams_win():
    win = Toplevel(root)
    win.geometry('500x310')
    win.title('List of Teams')
    win.iconbitmap('PLicon.ico')

    title_label = Label(win,text="List of Teams",font=("Calibri bold", 18))
    title_label.pack(pady=10)

    table_frame = Frame(win)
    table_frame.pack()
    #sb = ttk.Scrollbar(table_frame)  
    tree1=ttk.Treeview(table_frame, height=5)#,yscrollcommand = sb.set )
    tree1["columns"]=("one",)
    tree1.column("#0", width=220, minwidth=100, stretch=NO,anchor=CENTER)
    tree1.column("one", width=220, minwidth=200,stretch=NO,anchor=CENTER)
    tree1.heading("#0",text="TeamName")
    tree1.heading("one", text="Stadium")
    #sb.config(command = tree1.yview)
    #sb.pack(side = RIGHT, fill=Y)
    tree1.pack(fill=X)

    btnFrame = Frame(win)
    players_button=ttk.Button(btnFrame,text="Players",takefocus=False, command=lambda: players_win(tree1))
    players_button.pack(padx=20,pady=20,side=LEFT)
    managers_button=ttk.Button(btnFrame,text="Manager",takefocus=False, command=lambda: manager_win(tree1))
    managers_button.pack(padx= 20,side=RIGHT)
    btnFrame.pack(fill=X)

    # inserting values to tree
    con, cur = connection()
    lst = cur.execute("select TeamName, Stadium from List_of_Teams")
    
    i=1
    for tup in lst:
            data0,data1= tup
            if i%2==0:
                tree1.insert("", "end", text=str(data0), values=(data1,),tags=('even',))
                tree1.tag_configure('even', background='#efefef')
            else:
                tree1.insert("", "end", text=str(data0), values=(data1,),tags=('odd',))
                tree1.tag_configure('odd', background='#fafafa')
            i+=1
    con.commit()
    con.close()    



# __main__
root=Tk()
root.geometry('800x600')
root.title('Premier League')
root.iconbitmap('PLicon.ico')
s = ttk.Style()
s.configure('TButton', font=('Calibri', 24))
s.configure("Treeview.Heading", font=('Calibri', 14))
s.configure('Treeview', rowheight=27, font=('Calibri', 12))

#Load an image in the script
img= (Image.open("PLimage2.png"))
resized_image= img.resize((400,200), Image.ANTIALIAS)
new_image= ImageTk.PhotoImage(resized_image)
canvas= Canvas(root, width= 600, height= 200)
canvas.create_image(0,0, anchor=NW, image=new_image)
canvas.pack(padx = 170, pady= 50)

f1=Frame(root,bd=2,relief=GROOVE)
f1.pack()

about=Frame(root,bd=2,relief=GROOVE)
about.pack(fill=X,padx = 32, pady = 20)
names_frame = Frame(about)
names_frame.pack(pady = 10)
Label(names_frame,text="Made by: ",font=("Consolas",13,'italic bold'), fg='gray').pack(side=LEFT)
Label(names_frame,text="Harish A",font=("Consolas",12,'italic')).pack(side=LEFT, padx= 40)
Label(names_frame,text="Gokulram A",font=("Consolas",12,'italic')).pack(side=LEFT, padx = 40)
Label(names_frame,text="Gokulakrishnan B",font=("Consolas",12,'italic')).pack(side=LEFT, padx = 40)

fixf = Frame(f1)
fixtures_button=ttk.Button(fixf,text="Fixtures",style="TButton",takefocus=False, command=fixtures_win)
fixtures_button.pack(pady=13)
teams_button=ttk.Button(fixf,text="Teams",style="TButton",takefocus=False, command=list_teams_win)
teams_button.pack(pady=13)
fixf.pack(padx=270,pady=27)

root.mainloop()