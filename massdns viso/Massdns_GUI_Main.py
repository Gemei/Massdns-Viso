from Tkinter_GUI_Handler import *

class Main:
	def start_gui(self):
		root = Tk()
		gui_handler = Tkinter_GUI_Handler(root)
		gui_handler.options_menu()
		#gui_handler.init_tree_view()
		root.mainloop()
		
main = Main()
main.start_gui()