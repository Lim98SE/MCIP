from tkinter import *
import tkinter.messagebox as msg
import os

try:
    from mcstatus import JavaServer

except:
    os.system("pip install mcstatus")

    try:
        from mcstatus import JavaServer

    except:
        msg.showerror("MCIP Error", "Please install the Python library \"mcstatus\".")

try:
    open("mcip.txt").close()

except:
    open("mcip.txt", "w").close()

with open("mcip.txt") as mcip_list:
    ips = mcip_list.read().strip().split("\n")

def get_info(ip):
    try:
        stat = JavaServer.lookup(ip.strip())

    except:
        return {"desc": "Server Offline",
                "motd": "Server Offline",
                "online": 0,
                "max": 0,
                "players": [],
                "icon": ",iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAIAAAAlC+aJAAAAAXNSR0IArs4c6QAAAYhJREFUaIHtWcENwyAMTKtuxCiZM6MwU/qohBAxYIzhQPW9qmISrnfG4L7u+z52xhu9gF4YATSMABpGAA0jgMandcLlXPh8ep8LIIdGYHsFugjEaqDw3wqsgOYkTnA5J8jXp/fEST9bgcs5MnPE6SQnoPLD80dz6LXQwXZRoYCEIYEhuywkM+5zVk/V08kBYEFYZRuF7ULqZ55WMdUUQLloFQuJoUBg2smZhKYCEBetYqFAfmohCwC6SFkBjoueMT3eUzgL/XB6X15HHJCLFCg5NQfK65P5cHYSn96TCxVn0Wv3PziIHChYGVuzSKxSB8QoWWhyj02G7RXQqQNJ2hRE40TGyldbsb0KkG2SXOOktQYno2SwZiWOX5PrL8RfliOTDMwF6zR344cWVpOguj1UH3sMvdB09g+ZwWoWErxbBdtvo0YAjSE5IL7gCqCgAP96NaJtodOdjlfG3/JV+NTvA9XTCDlrUHF4QqG5y+z38yObsP2Vcvtt1AigYQTQMAJoGAE0jAAaX/K7u5hynbyBAAAAAElFTkSuQmCC",
                "exists": False,
                "ping": 0}
    
    server = JavaServer.lookup(ip.strip())
    status = server.status()

    server_status = {
        "desc": status.description,
        "motd": status.motd,
        "online": status.players.online,
        "max": status.players.max,
        "players": status.players.sample,
        "icon": status.icon,
        "exists": True,
        "ping": status.latency
        }

    return server_status

def add_ip():
    ip = new_ip.get().strip()

    if ip == "":
        return

    with open("mcip.txt", "a") as mcip_txt:
        mcip_txt.write("\n" + ip)

    global ips
    
    with open("mcip.txt") as mcip_list:
        ips = mcip_list.read().strip().split("\n")

    global servers
    servers.delete(0, END)

    for i in ips:
        servers.insert(END, i)

def refresh_info():
    get_selected_info(0)
        
def get_selected_info(event):
    for i in servers.curselection():
        server = servers.get(i)
    
    info = get_info(server)

    global server_ip
    global icon

    try:
        motd = info["motd"].to_plain()

    except:
        motd = info["motd"]

    text = server
    text += "\n\n" + motd + "\n"
    text += f"\n{info['online']}/{info['max']}"
    text += "\n\nPing: " + str(round(info["ping"], 2)) + "ms\n"

    text += "\nOnline Players:\n\n"

    if info["players"] is None:
        info["players"] = []

    for i in info["players"]:
        text += i.name + "\n"

    icon.config(data = info["icon"].split(",")[1])

    server_icon.config(image = icon)

    server_ip.config(state=NORMAL)

    server_ip.delete("1.0", END)

    server_ip.insert("1.0", text)

    server_ip.config(state=DISABLED)
    

window = Tk()
window.geometry("800x800")
window.resizable(0,0)
window.title("MCIP - Server Status App")

window_icon_b64 = "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"

window_icon = PhotoImage(data = window_icon_b64)

window.iconphoto(False, window_icon)

scrollbar = Scrollbar(window)
scrollbar.pack(side=RIGHT, fill=Y)

servers = Listbox(window, yscrollcommand = scrollbar.set, font = ("Consolas", 20))
servers.bind("<Button-1>", get_selected_info)

for i in ips:
    servers.insert(END, i)

servers.pack(anchor = N, fill = X)
scrollbar.config(command = servers.yview)

server_ip = Text(window, font = ("Consolas", 20))
server_ip.insert(f"1.0", "Select an IP!")
server_ip.config(state=DISABLED)
icon = PhotoImage()
server_icon = Label(window, justify="left")

new_ip = Entry(window, font = ("Consolas", 20))
new_ip.pack(anchor = N, fill = X)

add_btn = Button(window, text = "Add IP", command = add_ip, font = ("Consolas", 20))
add_btn.pack(anchor = N, fill = X)

refresh_btn = Button(window, text = "Refresh", command = refresh_info, font = ("Consolas", 20))
refresh_btn.pack(anchor = N, fill = X)

server_icon.pack()
server_ip.pack()
mainloop()
