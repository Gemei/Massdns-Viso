from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os, pathlib
from Util import *

class Tkinter_GUI_Handler:

	#master is root
	def __init__(self, master):
		self.current_working_dir = os.getcwd()
		util = Util(master)
		util.center(master, "Massdns Viso")
		self.master = master	

	def options_menu(self):
		menu = Menu(self.master)
		self.master.config(menu=menu)

		subMenu = Menu(menu)
		menu.add_cascade(label="file", menu=subMenu)
		subMenu.add_command(label="massdns ndjson output file", command=self.massdns_file)
		subMenu.add_command(label="amass output file", command=self.amass_file)

	def massdns_file(self):
		filename = self.file_explorer()
		if self.is_not_blank(filename):
			util = Util(self.master)
			util.pass_file(filename,"massdns_file")

	def amass_file(self):
		filename = self.file_explorer()
		if self.is_not_blank(filename):
			util = Util(self.master)
			util.pass_file(filename,"amass_file")

	def file_explorer(self):
		self.master.option_add('*foreground', 'red')
		self.master.filename = filedialog.askopenfilename(initialdir = self.current_working_dir, title = "Select file", filetypes = (("all files","*"),("txt files","*.txt")))
		if self.is_not_blank(self.master.filename):
			self.current_working_dir = pathlib.Path(self.master.filename).parent.absolute()
			return self.master.filename

	def is_not_blank(self, s):
		return bool(s and s.strip())