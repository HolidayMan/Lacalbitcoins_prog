from tkinter import *
import api
import constants

accounts = []

with open('accounts.txt','r') as f:
	for i in f.readlines():
		a,b,c = i.split('|')
		accounts.append(constants.Account(a,b,c.replace('\n', '')))

names = [i.name for i in accounts]
names.sort()
pre_acc = []
for i in names:
	for j in accounts:
		if j.name == i:
			pre_acc.append(j)
			break
accounts = pre_acc
with open('accounts.txt', 'w') as f:
		for i in accounts:
			f.write('{}|{}|{}\n'.format(i.name,i.hmac_key,i.hmac_secret))

# gui

root = Tk()
root.title('Localbitcoin')
root.resizable(width=False, height=False)
root.geometry('1000x600')
# root.iconbitmap('favicon.ico')


frame_top = Frame(root)
frame_acc = Frame(root)
frame_center = Frame(root)
frame_bottom = Frame(root)
frame_del = Frame(root)

scrollbar_2 = Scrollbar(frame_acc)
select = Listbox(frame_acc, height=4, yscrollcommand=scrollbar_2.set)
scrollbar_2.config(command=select.yview)
for i in accounts:
    select.insert(END, i.name)


inf_lb = Label(frame_top, text='It\'s a localbitcoin program', bg='light green',font=15,width=100)

del_button = Button(frame_del, bg='red', text='Delete Account', height=1)

add_account = Button(root, text='Add account', width=20, font=15, bg='light blue')
get_balance = Button(frame_center, text='Balance', width=17)
show_notif = Button(frame_center, text='Show Notifications', width=17)
add_notif = Button(frame_center, text='Add Notifications', width=17)
edit_notif = Button(frame_center, text='Edit Notifications', width=17)
show_mess = Button(frame_center, text='Show Messages', width=17)
reply_mess = Button(frame_center, text='Answer Messages', width=17)

answer = Text(frame_bottom, height=14, width=98, font=15)
answer.config(state=DISABLED)

scrollbar = Scrollbar(frame_bottom)


frame_top.pack(side=TOP)
inf_lb.pack(side=TOP, anchor='center')
add_account.pack(pady=50)
frame_acc.pack()
select.pack(side=LEFT)
frame_del.pack()
del_button.pack(pady=1)
scrollbar_2.pack(side=RIGHT, fill=Y)
frame_bottom.pack(side=BOTTOM, anchor='center', fill=X)
frame_center.pack(side=BOTTOM, anchor='center', pady=10)



answer.pack(side=LEFT)
scrollbar.pack(side=RIGHT, fill=Y)
scrollbar.config(command = answer.yview)
answer.config(yscrollcomman=scrollbar.set)



get_balance.grid(row=0, column=0)
show_notif.grid(row=0, column=1)
add_notif.grid(row=0, column=2)
edit_notif.grid(row=0, column=3)
show_mess.grid(row=0, column=4)
reply_mess.grid(row=0, column=5)

#end gui

def pre_balance(event):
	name_of_acc = select.get(ACTIVE)
	for i in accounts:
		if name_of_acc == i.name:
			key = i.hmac_key
			key_secret = i.hmac_secret
			break
	get_balance_fun(name_of_acc, key, key_secret)

def get_balance_fun(name, hmac_key, hmac_secret):
	conn = api.hmac(hmac_key, hmac_secret)
	s = conn.call('GET', '/api/wallet/').json()
	try:
		answer.config(state=NORMAL)
		answer.insert(END,"Balance on {}: {}\n".format(name, s['data']['total']['balance']))
		answer.config(state=DISABLED)
	except KeyError:
		answer.config(state=NORMAL)
		answer.insert(END,'Something went wrong. Maybe your hmac or hmack secret are incorrect.\n-----------------------\n')
		answer.config(state=DISABLED)

def show_notif_fun(event):
	name_of_acc = select.get(ACTIVE)
	for i in accounts:
		if name_of_acc == i.name:
			key = i.hmac_key
			key_secret = i.hmac_secret
			break
	conn = api.hmac(key, key_secret)
	s = conn.call('GET', '/api/notifications/').json()
	ins = []
	try:
		for i in s['data']:
			st = ''
			time = i['created_at'][:i['created_at'].index('T')] + ' at ' + i['created_at'][i['created_at'].index('T')+1:i['created_at'].index('+')]
			st = '\"{}\"; recieved: {}; {}\n'.format(i['msg'], time, 'READ' if i['read'] else 'NOT READ')
			ins.append(st)
	except KeyError:
		answer.config(state=NORMAL)
		answer.insert(END,'Something went wrong. Maybe your hmac or hmack secret are incorrect.\n-----------------------\n')
		answer.config(state=DISABLED)
		return 0
	ins = ''.join(ins[::-1])
	answer.config(state=NORMAL)
	answer.insert(END, 'Notifications at {}:\n{}-----------------------\n'.format(name_of_acc, ins))
	answer.config(state=DISABLED)

def del_acc(event):
	name_of_acc = select.get(ACTIVE)
	select.delete('active')
	for i in accounts:
		if name_of_acc == i.name:
			del accounts[accounts.index(i)]
	with open('accounts.txt', 'w') as f:
		for i in accounts:
			f.write('{}|{}|{}\n'.format(i.name,i.hmac_key,i.hmac_secret))

def add_account_window(event):
	add_acc = Toplevel(root)
	add_acc.title('Adding account')
	add_acc.resizable(width=False,height=False)
	add_acc.geometry('300x240')
	frame_entry = Frame(add_acc)

	name = Entry(frame_entry)
	pbkey = Entry(frame_entry)
	sckey = Entry(frame_entry)

	namelb = Label(frame_entry, text='Name:', font=15)
	pbkeylb = Label(frame_entry, text='Public key:', font=15)
	sckeylb = Label(frame_entry, text='Secret key:', font=15)

	add = Button(frame_entry, text='Add', font=15, width=10)

	def add_account_fun(event):
		global accounts
		if name.get() and pbkey.get() and sckey.get():	
			with open('accounts.txt', 'a') as f:
				f.write(name.get()+'|'+pbkey.get()+'|'+sckey.get()+'\n')
			accounts.append(constants.Account(name.get(),pbkey.get(),sckey.get().replace('\n','')))
			global select
			names = [i.name for i in accounts]
			names.sort()
			pre_acc = []
			for i in names:
				for j in accounts:
					if j.name == i:
						pre_acc.append(j)
						break
			accounts = pre_acc
			with open('accounts.txt', 'w') as f:
					for i in accounts:
						f.write('{}|{}|{}\n'.format(i.name,i.hmac_key,i.hmac_secret))
			select.delete(0,END)
			for i in accounts:
				select.insert(END, i.name)
			add_acc.destroy()

	add.bind('<Button-1>', add_account_fun)
	frame_entry.pack(side=TOP, anchor='center', pady=50)
	namelb.grid(row=0,column=0)
	name.grid(row=0,column=1)
	pbkeylb.grid(row=1,column=0, sticky=E, pady=1)
	pbkey.grid(row=1,column=1, pady=1)
	sckeylb.grid(row=2,column=0, sticky=E, pady=1)
	sckey.grid(row=2,column=1, pady=1)
	add.grid(row=3, columnspan=2, pady=10)



add_account.bind('<Button-1>', add_account_window)
get_balance.bind('<Button-1>', pre_balance)
show_notif.bind('<Button-1>', show_notif_fun)
del_button.bind('<Button-1>', del_acc)
root.mainloop()