from tkinter import *
import api
import constants
import threading

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
get_balance = Button(frame_center, text='Balance', width=14)
show_ad = Button(frame_center, text='Show Ads', width=14)
add_ad = Button(frame_center, text='Add Ad', width=14)
edit_ad = Button(frame_center, text='Edit Ad', width=14)
show_mess = Button(frame_center, text='Show Messages', width=14)
reply_mess = Button(frame_center, text='Answer Messages', width=14)
show_notif = Button(frame_center, text='Show notifications', width=14)

answer = Text(frame_bottom, height=14, width=98, font=16)
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
show_ad.grid(row=0, column=1)
add_ad.grid(row=0, column=2)
edit_ad.grid(row=0, column=3)
show_mess.grid(row=0, column=4)
reply_mess.grid(row=0, column=5)
show_notif.grid(row=0, column=6)

#end gui

def pre_balance(event):
	answer.config(state=NORMAL)
	answer.insert(END,'Sending request to api...\n')
	answer.config(state=DISABLED)
	threading.Thread(target=get_balance_fun).start()

def get_balance_fun():
	name_of_acc = select.get(ACTIVE)
	for i in accounts:
		if name_of_acc == i.name:
			hmac_key = i.hmac_key
			hmac_secret = i.hmac_secret
			break
	conn = api.hmac(hmac_key, hmac_secret)
	s = conn.call('GET', '/api/wallet/').json()
	try:
		answer.config(state=NORMAL)
		answer.insert(END,"Balance on {}: {}\n".format(name_of_acc, s['data']['total']['balance'])+'\n-----------------------\n')
		answer.config(state=DISABLED)
	except KeyError:
		answer.config(state=NORMAL)
		answer.insert(END,'Something went wrong. Maybe your hmac or hmack secret is incorrect.\n-----------------------\n')
		answer.config(state=DISABLED)

def pre_show_ad(event):
	answer.config(state=NORMAL)
	answer.insert(END,'Sending request to api...\n')
	answer.config(state=DISABLED)
	threading.Thread(target=show_ad_fun).start()

def show_ad_fun():
	name_of_acc = select.get(ACTIVE)
	for i in accounts:
		if name_of_acc == i.name:
			key = i.hmac_key
			key_secret = i.hmac_secret
			break
	conn = api.hmac(key, key_secret)
	s = conn.call('GET', '/api/ads/').json()
	try:
		s = s['data']['ad_list']
		if s:
			st=''
			for ind, i in enumerate(s):
				try:
					acc_inf = i['data']['account_info']
				except KeyError:
					acc_inf = '(phone number: {}) '.format(i['data']['account_details']['phone_number'])
				st += '{}) username: {}; feedback: {}; trades: {}; last online: {};\n\
				trade type: {}; ad id: {}; bank name: {}; payment window minutes: {}; account info: {}; \
				country: {}; currency: {}; created at: {}; max amount available: {}; message: {}; volume coeficient BTC: {}; view at: {}; edit: {}\n'.format(ind+1, i['data']['profile']['username'],
					i['data']['profile']['feedback_score'], i['data']['profile']['trade_count'], i['data']['profile']['last_online'], i['data']['trade_type'], 
					i['data']['ad_id'],'\"'+i['data']['bank_name']+'\"', i['data']['payment_window_minutes'],acc_inf,i['data']['location_string'],
					i['data']['currency'], i['data']['created_at'], i['data']['max_amount_available'], '\"' + i['data']['msg'] + '\"', i['data']['volume_coefficient_btc'],
					i['actions']['public_view'], i['actions']['html_form'])
			answer.config(state=NORMAL)
			answer.insert(END,'Ads for ' + name_of_acc + ' {\n' + st + '\n}\n-----------------------\n')
			answer.config(state=DISABLED)
		else:
			answer.config(state=NORMAL)
			answer.insert(END,'You have no ads.\n-----------------------\n')
			answer.config(state=DISABLED)
			return 0
	except KeyError:
		answer.config(state=NORMAL)
		answer.insert(END,'Something went wrong. Maybe your hmac or hmack secret is incorrect.\n-----------------------\n')
		answer.config(state=DISABLED)
		return 0

def pre_show_notif(event):
	answer.config(state=NORMAL)
	answer.insert(END,'Sending request to api...\n')
	answer.config(state=DISABLED)
	threading.Thread(target=show_notif_fun).start()

def show_notif_fun():
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
		answer.insert(END,'Something went wrong. Maybe your hmac or hmack secret is incorrect.\n-----------------------\n')
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

def add_ad_window(event):
	add_ad = Toplevel(root)
	add_ad.title('Adding account')
	add_ad.resizable(width=False,height=False)

def edit_ad_window(event):
	edit_ad = Toplevel(root)
	edit_ad.title('Adding account')
	edit_ad.resizable(width=False,height=False)

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
del_button.bind('<Button-1>', del_acc)
get_balance.bind('<Button-1>', pre_balance)
show_ad.bind('<Button-1>', pre_show_ad)
add_ad.bind('<Button-1>', add_ad_window)
edit_ad.bind('<Button-1>', edit_ad_window)
show_notif.bind('<Button-1>', pre_show_notif)
root.mainloop()
