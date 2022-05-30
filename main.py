import sys
from tkinter import Tk, PhotoImage, messagebox

from assets import ThreadedTask, resource_path

from menuBar import MenuBar
from loadingPage import LoadingPage
from startPage import StartPage


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        try:
            app.socket.terminate()
        except AttributeError:
            pass
        sys.exit()


class App(Tk):
    def __init__(self):
        super().__init__()
        self.socket, self.textBox = None, None

        self.protocol("WM_DELETE_WINDOW", on_closing)

        '''____Main_Window____'''
        self.title("Mi Chat Room")                                                # App Title
        self.iconphoto(False, PhotoImage(file=resource_path(r'assets/icon.png')))              # App Icon
        self.geometry('300x400')                                          # App Position
        self.resizable(False, False)

        MenuBar(self)

        self.loadingPage = LoadingPage(self)
        self.start_loading_screen()

        ThreadedTask(StartPage, args=(self, ))

    def start_loading_screen(self):
        self.loadingPage.interrupt = False
        self.loadingPage.pack(expand=1, fill="both")
        self.loadingPage.start()

    def stop_loading_screen(self):
        self.loadingPage.pack_forget()
        self.loadingPage.interrupt = True

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
