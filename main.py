from tkinter import *
from tkinter import messagebox 
import os
from winreg import *


REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"

PROXY_ADDR = {
	"HOSTEL" : "10.30.0.1",
	"LIBRARY": "10.11.0.1",
	"IT"     : "10.24.0.1",
	"ALUMNI" : "10.12.0.1"
}

PROXY_PORT = {
	"HOSTEL" : "8080",
	"LIBRARY": "8080",
	"IT"     : "8080",
	"ALUMNI" : "8080"
}

def get_cur_proxy():
	try:
		root_key=OpenKey(HKEY_CURRENT_USER, REG_PATH, 0, KEY_READ)
		[Pathname,regtype]=(QueryValueEx(root_key,"ProxyServer"))
		CloseKey(root_key)
		if (""==Pathname):
			raise WindowsError
	except WindowsError:
		return [""]

	return Pathname

def chk_proxy_state():
	try:
		root_key=OpenKey(HKEY_CURRENT_USER, REG_PATH, 0, KEY_READ)
		[Pathname,regtype]=(QueryValueEx(root_key,"ProxyEnable"))
		CloseKey(root_key)
		if (""==Pathname):
			raise WindowsError
	except WindowsError:
		return [""]

	return Pathname

def enable_proxy_state():
	try:
		# CreateKey(_winreg.HKEY_CURRENT_USER, REG_PATH)
		registry_key = OpenKey(HKEY_CURRENT_USER, REG_PATH, 0, KEY_WRITE)
		SetValueEx(registry_key, "ProxyEnable", 0, REG_DWORD, 1)
		CloseKey(registry_key)
		return True
	except WindowsError:
		return False


def disable_proxy_state():
	try:
		# CreateKey(_winreg.HKEY_CURRENT_USER, REG_PATH)
		registry_key = OpenKey(HKEY_CURRENT_USER, REG_PATH, 0, KEY_WRITE)
		SetValueEx(registry_key, "ProxyEnable", 0, REG_DWORD, 0)
		CloseKey(registry_key)
		return True
	except WindowsError:
		return False

def set_proxy(proxyValue):
	try:
		# CreateKey(_winreg.HKEY_CURRENT_USER, REG_PATH)
		registry_key = OpenKey(HKEY_CURRENT_USER, REG_PATH, 0, KEY_WRITE)
		SetValueEx(registry_key, "ProxyServer", 0, REG_SZ, proxyValue)
		CloseKey(registry_key)
		return True
	except WindowsError:
		return False

def perfAction(nameVal):
	enable_proxy_state()
	if(nameVal=="NONE"):
		disable_proxy_state()
	else:
		set_proxy(PROXY_ADDR[nameVal] + ":" + PROXY_PORT[nameVal])

	updateText()


def addButton(frLabel, txtVal, onClick):
	btn = Button(frLabel, text = txtVal, width=10, padx=5, pady=5, font=8, command = onClick)
	btn.pack()

def manualSet():
	addr = inpAddr.get()
	port = inpPr.get()

	if(len(addr.split('.'))!=4):
		messagebox.showerror("Error", "Enter Correct Proxy Address")
		disable_proxy_state()
		return
	for i in addr:
		if(i!='.' and (i<'0' or i>'9')):
			messagebox.showerror("Error", "Enter Correct Proxy Address")
			disable_proxy_state()
			return

	for i in port:
		if(i<'0' or i>'9'):
			messagebox.showerror("Error", "Enter Correct Port Value")
			disable_proxy_state()
			return

	enable_proxy_state()
	set_proxy(addr+":"+port)
	updateText()

def updateText():
	proxy_flag = chk_proxy_state()
	proxy_full = get_cur_proxy()
	proxy_addr, proxy_port = proxy_full.split(':')
	if(proxy_flag==0):
		w.delete("all")
		w.create_text(130, 40, text="NO PROXY", font="Times 19 bold")
	else:
		w.delete("all")
		w.create_text(120, 30, text="ADDRESS: " + proxy_addr, font="Times 18 bold")
		w.create_text(120, 60, text="PORT: " + proxy_port, font="Times 18 bold")



root = Tk()
root.geometry()
root.resizable(False, False)
root.title("WinProxyManager")


prFrame = LabelFrame(root, text="Choose Proxy",font=5, height=400, width=200, padx=4, pady=4)

prFrame.grid(row=0, column=2, rowspan=2)
addButton(prFrame, "No Proxy", onClick=lambda: perfAction("NONE"))
addButton(prFrame, "HOSTEL" , onClick=lambda: perfAction("HOSTEL"))
addButton(prFrame, "LIBRARY" , onClick=lambda: perfAction("LIBRARY"))
addButton(prFrame, "IT Dept" , onClick=lambda: perfAction("IT"))
addButton(prFrame, "ALUMNI Hall" , onClick=lambda: perfAction("ALUMNI"))
addButton(prFrame, "CST Dept", onClick=lambda: perfAction("NONE"))


lbFrame = LabelFrame(root, text="Current Proxy",font=5, height=230, width=200, padx=4, pady=4)
lbFrame.grid(row=0, column=0, columnspan=2)


w = Canvas(lbFrame, width=250, height=100)
w.pack()
updateText()

inFrame = LabelFrame(root, text="Manual Set",font=5, height=230, width=200, padx=4, pady=4)
inFrame.grid(row=1, column=0)

Label(inFrame, text="Address", font="Arial 14 bold").pack()
inpAddr = Entry(inFrame, width=15, font=('Arial', 13))
inpAddr.pack()

Label(inFrame, text="Proxy", font="Arial 14 bold").pack()
inpPr = Entry(inFrame, width=15, font=('Arial', 13))
inpPr.pack()

btnFrame = Frame(root)
btnFrame.grid(row=1, column=1)
Button(btnFrame, text="SET PROXY", font=13, padx=5, pady=10, command=manualSet).pack()

Label(root, text="By Arnab Sen (https://github.com/arnabsen1729)").grid(row=2, column=0, columnspan=2)

root.mainloop()

