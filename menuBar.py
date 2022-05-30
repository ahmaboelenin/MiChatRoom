from tkinter import Menu, messagebox


class MenuBar(Menu):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.infoMenu = Menu(self, tearoff=0)
        self.infoMenu.add_command(label="Credits",
                                  command=lambda: messagebox.showinfo("Credits",
                                                                      "This Simple App was Created By Ahmed Aboelenin"))
        self.add_cascade(label="Info", menu=self.infoMenu)
        self.master.configure(menu=self)
