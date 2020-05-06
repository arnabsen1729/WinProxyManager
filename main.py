from tkinter import *
import os
from winreg import *


REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"

PROXY_LIST = {
	"HOSTEL" : "10.30.0.1:8080",
	"LIBRARY": "10.11.0.1:8080",
	"IT"     : "10.24.0.1:8080",
	"ALUMNI" : "10.12.0.1:8080"
}

def set_reg(name, value):
	try:
		CreateKey(_winreg.HKEY_CURRENT_USER, REG_PATH)
		registry_key = OpenKey(_winreg.HKEY_CURRENT_USER, REG_PATH, 0, 
									   _winreg.KEY_WRITE)
		SetValueEx(registry_key, name, 0, _winreg.REG_SZ, value)
		CloseKey(registry_key)
		return True
	except WindowsError:
		return False

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
		set_proxy(PROXY_LIST[nameVal])

	updateText()


def addButton(frLabel, txtVal, onClick):
	btn = Button(frLabel, text = txtVal, width=10, padx=5, pady=5, font=8, command = onClick)
	btn.pack()

def updateText():
	proxy_flag = chk_proxy_state()
	proxy_full = get_cur_proxy()
	proxy_addr = proxy_full[:-5]
	proxy_port = proxy_full[-4:]
	if(proxy_flag==0):
		w.delete("all")
		w.create_text(150, 90, text="NO PROXY", font="Times 20 bold")
	else:
		w.delete("all")
		w.create_text(150, 80, text="ADDRESS: " + proxy_addr, font="Times 20 bold")
		w.create_text(150, 120, text="PORT: " + proxy_port, font="Times 20 bold")



root = Tk()
root.geometry()
root.resizable(False, False)
root.title("WinProxyManager")

root.iconbitmap('icon.ico')

prFrame = LabelFrame(root, text="Choose Proxy",font=5, height=400, width=200, padx=4, pady=4)

prFrame.grid(row=0, column=1)
addButton(prFrame, "No Proxy", onClick=lambda: perfAction("NONE"))
addButton(prFrame, "HOSTEL" , onClick=lambda: perfAction("HOSTEL"))
addButton(prFrame, "LIBRARY" , onClick=lambda: perfAction("LIBRARY"))
addButton(prFrame, "IT Dept" , onClick=lambda: perfAction("IT"))
addButton(prFrame, "ALUMNI Hall" , onClick=lambda: perfAction("ALUMNI"))
addButton(prFrame, "CST Dept", onClick=lambda: perfAction("NONE"))


lbFrame = LabelFrame(root, text="Current Proxy",font=5, height=230, width=200, padx=4, pady=4)
lbFrame.grid(row=0, column=0)


w = Canvas(lbFrame, width=300, height=237)
w.pack()
updateText()

author = Label(root, text="By Arnab Sen (https://github.com/arnabsen1729)")
# author2 = Label(root, text="https://github.com/arnabsen1729", )


author.grid(row=1, column=0)
# author2.grid(row=1, column=1)

root.mainloop()

