import json, subprocess
from tkinter import *
from tkinter import ttk

class Massdns_Parser:
	def __init__(self, master, massdns_file):
		self.master = master
		self.init_tree_view()
		last_query_name = ""
		file = open(massdns_file, 'r') 
		lines = file.readlines() 
		for line in lines:
			split = line.split(",")
			query_name = split[0].split(":")[1].replace('"', '').replace(' ', '')
			query_type = split[1].split(":")[1].replace('"', '').replace(' ', '')
			resp_name = split[2].split(":")[1].replace('"', '').replace(' ', '')
			resp_type = split[3].split(":")[1].replace('"', '')
			data = split[4].split(":")[1].replace('"', '').replace('}', '').rstrip("\n\r")
			if query_name is not last_query_name:
				self.add_new_node_to_tree(query_name)
				self.add_sub_node_to_tree(query_name,query_type,resp_name,resp_type,data)
				last_query_name = query_name
			else:
				self.add_sub_node_to_tree(query_name,query_type,resp_name,resp_type,data)


	def init_tree_view(self):
		self.tree = ttk.Treeview(self.master)

		self.vsb = ttk.Scrollbar(orient="vertical",command=self.tree.yview)
		self.tree.configure(yscrollcommand=self.vsb.set)
		self.search_box_entry = Entry(self.master)
		self.search_button = Button(self.master, text='Search', command=self.search_tree)

		self.tree["columns"] = ("query_type", "resp_name", "resp_type","data")
		self.tree.column("query_type", width=50, stretch=NO)
		self.tree.column("resp_name", width=150)
		self.tree.column("resp_type", width=50, stretch=NO)
		self.tree.column("data", width=150)
		self.tree.heading("query_type", text="Query Type")
		self.tree.heading("resp_name", text="Response Name")
		self.tree.heading("resp_type", text="Response Type")
		self.tree.heading("data", text="Data")
		self.tree.bind('<ButtonRelease-1>', self.selectItem)

		self.vsb.pack(side='right', fill='y')
		self.search_box_entry.pack(side='top', anchor="w", padx=2, pady=2)
		self.search_button.pack(side='top', anchor="w", padx=2, pady=2)
		self.tree.pack(side='left', expand=1, fill=BOTH)

	def add_new_node_to_tree(self, query_name):
		try:
			self.tree.insert("", "end", query_name, text=query_name)
		except:
			pass

	def add_sub_node_to_tree(self, query_name, query_type, resp_name, resp_type, data):
		try:
			self.tree.insert(query_name, "end", text=query_name, values=(query_type, resp_name, resp_type, data))
		except:
			pass

	def selectItem(self, event):
		curItem = self.tree.item(self.tree.focus())
		col = self.tree.identify_column(event.x)
		try:
			if col == '#0':
				cell_value = curItem['text']
			elif col == '#1':
				cell_value = curItem['values'][0]
			elif col == '#2':
				cell_value = curItem['values'][1]
			elif col == '#3':
				cell_value = curItem['values'][2]
			elif col == '#4':
				cell_value = curItem['values'][3]

			item_text = cell_value.replace("'", "")
			self.copy_to_clipboard(item_text)
		except:
			pass

	def copy_to_clipboard(self, data):
	    p = subprocess.Popen(['xclip','-selection','clipboard'], stdin=subprocess.PIPE)
	    p.stdin.write(data.encode('utf-8'))
	    p.stdin.close()
	    retcode = p.wait()

	def search_tree(self, item=''):
		pattern = self.search_box_entry.get()
		#avoid search on empty string
		if len(pattern) > 0:
			children = self.tree.get_children(item)
		for child in children:
			text = self.tree.item(child, 'text')
			if text.lower().startswith(pattern.lower()):
				self.tree.selection_set(child)
				self.tree.see(child)
				return True
			else:
				res = self.search_tree(child)
				if res:
					return True
		else:
			pass