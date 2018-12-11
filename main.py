from Tkinter import *
from lbcapi import api

# gui

root = Tk()
root.title('Localbitcoin')
root.resizable(width=False, height=False)
root.geometry('1000x600')

frame_top = Frame(root)
frame_center = Frame(root)
frame_entry = Frame(root)
frame_bottom= Frame(root)

name = Entry(frame_entry)
pbkey = Entry(frame_entry)
sckey = Entry(frame_entry)

inf_lb = Label(frame_top, text='It\'s a localbitcoin program', bg='light green',font=15,width=100)

namelb = Label(frame_entry, text='name:', font=15)
pbkeylb = Label(frame_entry, text='public key:', font=15)
sckeylb = Label(frame_entry, text='secret key:', font=15)

get_balance = Button(frame_center, text='Balance', width=17)
show_notif = Button(frame_center, text='Show Notifications', width=17)
add_notif = Button(frame_center, text='Add Notifications', width=17)
edit_notif = Button(frame_center, text='Edit Notifications', width=17)
show_mess = Button(frame_center, text='Show Messages', width=17)
reply_mess = Button(frame_center, text='Answer Messages', width=17)

answer = Text(frame_bottom, height=17, width=123)
scrollbar = Scrollbar(frame_bottom)

frame_top.pack(side=TOP)
inf_lb.pack(side=TOP, anchor='center')
frame_entry.pack(side=TOP, anchor='center', pady=100)
frame_center.pack(side=TOP, anchor='center', pady=10)
frame_bottom.pack(side=BOTTOM, anchor='center', fill=X)

answer.pack(side=LEFT)
scrollbar.pack(side=RIGHT, fill=Y)
scrollbar.config(command = answer.yview)
answer.config(yscrollcomman=scrollbar.set)

namelb.grid(row=0,column=0)
name.grid(row=0,column=1)
pbkeylb.grid(row=1,column=0, sticky=E, pady=1)
pbkey.grid(row=1,column=1, pady=1)
sckeylb.grid(row=2,column=0, sticky=E, pady=1)
sckey.grid(row=2,column=1, pady=1)

get_balance.grid(row=0, column=0)
show_notif.grid(row=0, column=1)
add_notif.grid(row=0, column=2)
edit_notif.grid(row=0, column=3)
show_mess.grid(row=0, column=4)
reply_mess.grid(row=0, column=5)

#end gui

def pre_balance(event):
	key = pbkey.get()
	key_secret = sckey.get()
	get_balance_fun(key, key_secret)
	
def get_balance_fun(hmac_key,hmac_secret):
	from lbcapi import api
	conn = api.hmac(hmac_key, hmac_secret)
	s = conn.call('GET', '/api/wallet/').json()
	answer.insert(END,"Balance on {}: {}\n".format(name.get(), s['data']['total']['balance']))

get_balance.bind('<Button-1>', pre_balance)
root.mainloop()