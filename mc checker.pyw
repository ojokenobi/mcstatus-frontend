import time
import json
import os
from mcstatus import JavaServer
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import threading
# The program doesnt support colors yet, so this list removes the color code characters from the description
color_codes = ['§4','§c','§6','§e','§2','§a','§b','§3','§1','§9','§d','§5','§f','§7','§8','§0','§r','§l']

def refresh():
    texLbl.config(state= NORMAL)
    texLbl.delete('1.0', END)
    texLbl.insert(END,f"--------------------------------------------------------------------------------\n")
    texLbl.config(state=DISABLED)
    try:
        for obj in json.loads(open("servers.json",'r').read()):
            try:
                server = JavaServer.lookup(obj)
                status = server.status()
                texLbl.config(state=NORMAL)
                texLbl.insert(END,f"{obj} has {status.players.online} players\n")
                texLbl.insert(END,f"The server responded in {status.latency} ms\n")
                desc = status.description
                for x in color_codes:
                    desc = desc.replace(str(x),"")
                texLbl.insert(END,f"Description: "+desc+"\n")
                texLbl.insert(END,"Players: ")
                if status.players.sample is not None:
                    texLbl.insert(END,[f"{player.name}" for player in status.players.sample])
                    texLbl.insert(END,"\n\n")
                else:
                    texLbl.insert(END,"None")
                    texLbl.insert(END,"\n\n")
                texLbl.config(state=DISABLED)
            except Exception as err:
                texLbl.config(state=NORMAL)
                texLbl.insert(END,"An error has occured, please check below for the error\n")
                texLbl.insert(END,str(err)+"\n")
                texLbl.insert(END,f"Server of cause: {obj}\n")
                texLbl.insert(END,"\n")
                texLbl.config(state=DISABLED)
    except FileNotFoundError:
        bar.place_forget()
        messagebox.showerror(parent=window,title="No servers found",message="There are no servers present in the servers.json file. Either this is the first time you have run this program, or the file has been misplaced. Check the help menu for more information.")
    texLbl.config(state=NORMAL)
    texLbl.insert(END,f"--------------------------------------------------------------------------------\n")
    texLbl.config(state=DISABLED)
    
def refresh_start():
    global refresh_thread
    refresh_thread = threading.Thread(target=refresh)
    refresh_thread.daemon = True
    refresh_thread.start()
    bar.place(x=200,y=8)
    bar.start(interval=12)
    window.after(20,check_refresh)
def check_refresh():
    if refresh_thread.is_alive():
        window.after(20,check_refresh)
    else:
        bar.stop()
        bar.place_forget()
def jsonwrite():
    noNewLines = editText.get("1.0",END)[:len(editText.get("1.0",END)) - 1].replace("\n","")
    servernamesFinal = []
    servernames = noNewLines.split(",")
    for i in servernames:
        if i.strip() != '':
            servernamesFinal.append(i)
    open("servers.json",'w').write(json.dumps(servernamesFinal))
    editwin.destroy()
def jsonedit():
    global editText,editwin
    editwin = Toplevel(window)
    editwin.title("Server List Editor")
    editwin.iconbitmap("mccheck icon.ico")
    editText = Text(editwin)
    editText.pack()
    editSubmit = Button(editwin,text="""      Submit      """,command=jsonwrite,bg='lightgreen')
    editSubmit.pack()
    try:
        for obj in json.loads(open("servers.json",'r').read()):
            editText.insert(END,obj+",")
    except FileNotFoundError:
        messagebox.showerror(parent=editwin,title="First Time",message="The server checker cannot find the servers.json file, so if this is not your first time running this program, you may have misplaced it. Check the help menu for more information.")
def helpopen(e):
    os.startfile("helpfiles\Main.html")
def closing():
    window.destroy()
    quit()
window = Tk()
window.geometry("642x450")
window.title("Minecraft Server Checker")
window.iconbitmap("mccheck icon.ico")
window.bind("<F1>",helpopen)
window.protocol("WM_DELETE_WINDOW", closing)
reBtn = Button(window,text='Refresh',command=refresh_start,bg='green',fg='white')
texLbl = Text()
texLbl.config(state= DISABLED)
jsonEdit = Button(window,text='Edit Server List',command=jsonedit,bg='cyan')
bar = ttk.Progressbar(window,orient="horizontal",mode="indeterminate", length=280)
helpbtn = Button(window,text="Help",command=lambda: helpopen(None),bg="yellow",fg='black')
texLbl.place(x=0,y=40)
reBtn.place(x=10,y=6)
jsonEdit.place(x=80,y=6)
helpbtn.place(x=600,y=6)
window.mainloop()
