from tkinter import Canvas, Frame, Button, Entry, Text

from assets import *


class TextBox(Text):
    def __init__(self, master):
        super().__init__(master=master, width=280, height=270, wrap='word', exportselection=0, state='disabled')
        self.tag_configure('status', justify='center', background="#F1F5F5")
        self.tag_configure('sent', background="#B9F8D3")
        self.tag_configure("received", justify='right', background="#E8F9FD")
        self.tag_configure("space", font=("Roboto", 2 * -1))

    def status(self, message):
        self.config(state='normal')
        self.insert('end', message + "\n", "status")
        self.add_space()

    def sent(self, message):
        self.config(state='normal')
        self.insert('end', message, 'sent')
        self.add_space()

    def received(self, message):
        self.config(state='normal')
        self.insert('end', message, "received")
        self.add_space()

    def add_space(self):
        self.insert('end', "\n", "space")
        self.config(state='disabled')


class HomePage(Canvas):
    def __init__(self, master):
        super().__init__(master=master, highlightthickness=0, bg='#FFFFFF')

        image = ImageTk.PhotoImage(Image.open(resource_path(r"assets/entry2.png")))
        self.image = image
        self.create_image(10, 295, image=image, anchor='nw')

        self.msgEntry = Entry(self, font=("Roboto", 18 * -1), bd=0, highlightthickness=0)
        self.msgEntry.place(x=22, y=299, width=256, height=33)
        self.msgEntry.bind('<Return>', self.send)

        image = ImageTk.PhotoImage(Image.open(resource_path(r"assets/clear_button.png")))
        temp = Button(self, image=image, borderwidth=0, highlightthickness=0, relief="flat", command=self.clear)
        temp.img = image
        temp.place(x=10, y=350, width=135, height=40)

        image = ImageTk.PhotoImage(Image.open(resource_path(r"assets/send_button.png")))
        temp = Button(self, image=image, borderwidth=0, highlightthickness=0, relief="flat", command=self.send)
        temp.img = image
        temp.place(x=155, y=350, width=135, height=40)

        frame = Frame(self)
        frame.place(x=10, y=10, width=280, height=270)

        # image = get_thumbnail('1257860', 280)
        self.textBox = TextBox(frame)
        self.textBox.pack(side='left', expand=False)

        self.msgEntry.focus_set()

        sleep(0.2)

        self.master.stop_loading_screen()
        self.pack(fill='both', expand=1)
        self.master.socket.start(self.textBox)

    def clear(self):
        self.msgEntry.delete(0, 'end')

    def send(self, event=None):
        message = self.msgEntry.get()
        if message.isspace() or message == "":
            pass
        else:
            message = message + "\n"
            self.master.socket.send(message)
            self.clear()
