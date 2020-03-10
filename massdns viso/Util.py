from Massdns_Scanner import *
from Tkinter_GUI_Handler import *
from PyQt4 import QtGui
from Massdns_Parser import *
import os, pathlib

class Util:

	def __init__(self, master):
		self.master = master

	def pass_file(self, file_path, file_type):
		self.file_path = file_path
		if file_type is "massdns_file":
			self.read_massdns_output(file_path)
		elif file_type is "amass_file":
			self.start_massdns_scanner(file_path)
		else:
			print("Wrong File Type!")

	def start_massdns_scanner(self, amass_file):
		popup = self.popup_window("Massdns scanning in progress...", "Please Wait")
		massdns_scanner = Massdns_Scanner(amass_file)
		results = massdns_scanner.do_scan()
		self.save_massdns_scan_results(results)
		popup.destroy()

	def save_massdns_scan_results(self, scan_results):
		current_dir = pathlib.Path(self.file_path).parent.absolute()
		massdns_filepath = str(current_dir)+"/massdns_scan_results"
		file = open(massdns_filepath,"w+")
		file.write(scan_results)
		file.close()
		self.read_massdns_output(massdns_filepath)

	def read_massdns_output(self, massdns_file):
		#print("Reading massdns file")
		massdns_parser = Massdns_Parser(self.master, massdns_file)


	def disable_popup_exit(self):
		pass

	def popup_window(self, popup_text, title):
		popup = Toplevel()
		popup.protocol("WM_DELETE_WINDOW", self.disable_popup_exit)
		popup.option_add('*foreground', 'white')
		popup.wm_title(title)
		label = Label(popup, text=popup_text, font=(None, 12)).grid(row=0,column=0)
		popup.pack_slaves()
		self.center(popup, title)
		return popup

	def center(self, master, title):
		master.update_idletasks()
		# Tkinter way to find the screen resolution
		# screen_width = toplevel.winfo_screenwidth()
		# screen_height = toplevel.winfo_screenheight()

		# PyQt way to find the screen resolution
		app = QtGui.QApplication([])
		screen_width = app.desktop().screenGeometry().width()
		screen_height = app.desktop().screenGeometry().height()

		size = tuple(int(_) for _ in master.geometry().split('+')[0].split('x'))
		x = screen_width/2 - size[0]/2
		y = screen_height/2 - size[1]/2
		
		master.geometry("+%d+%d" % (x, y))
		master.title(title)