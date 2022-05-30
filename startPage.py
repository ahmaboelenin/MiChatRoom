from tkinter import Canvas, Button, Entry, messagebox

from homePage import HomePage

from server import Server, Client

from assets import *


def check_connect_parameters(host, port, pin):
    if host in ['', 'Enter IP Address'] or port in ['', 'Enter Port']:
        messagebox.showwarning("Warning", "Please Enter IP Address, Port to Connect")
        return
    else:
        if is_valid_host(host):
            # Validates the entered ip address
            if port.isdigit():
                # Validates the entered port
                respond = messagebox.askquestion("askquestion", f"Are you sure to connect to {host}:{port} without Pin?") \
                    if pin in ['', 'Enter Pin'] \
                    else messagebox.askquestion("askquestion", f"Are you sure to connect to {host}:{port} with {pin} as Pin?")
                return 1 if respond == 'yes' else 0
            else:
                messagebox.showwarning("Warning", "Port Must be a Digit.")
        else:
            messagebox.showwarning("Warning", "Please Enter Valid IP Address.")


def check_host_parameters(pin):
    if pin in ['', 'Enter Pin']:
        respond = messagebox.askquestion("askquestion", "Are you sure to Host without Pin?")
        if respond == 'yes':
            return ""
    else:
        respond = messagebox.askquestion("askquestion", f"Are you sure to Host with '{pin}' as your Pin?")
        if respond == 'yes':
            return pin


class StartPage(Canvas):
    def __init__(self, master):
        super().__init__(master=master, highlightthickness=0, bg='#FFFFFF')
        entry_image = ImageTk.PhotoImage(Image.open(resource_path(r"assets/entry.png")))
        clear_image = ImageTk.PhotoImage(Image.open(resource_path(r"assets/clear_button.png")))
        generate_image = ImageTk.PhotoImage(Image.open(resource_path(r"assets/generate_button.png")))
        host_image = ImageTk.PhotoImage(Image.open(resource_path(r"assets/host_button.png")))
        connect_image = ImageTk.PhotoImage(Image.open(resource_path(r"assets/connect_button.png")))

        self.image = entry_image
        self.create_image(10, 20, image=entry_image, anchor='nw')
        self.create_image(10, 190, image=entry_image, anchor='nw')
        self.create_image(10, 240, image=entry_image, anchor='nw')
        self.create_image(10, 290, image=entry_image, anchor='nw')

        """____Entries____"""
        self.pinEntry = Entry(self, font=("Roboto", 18 * -1), bd=0, highlightthickness=0)
        self.pinEntry.place(x=22, y=24, width=256, height=33)

        self.ipEntry = Entry(self, font=("Roboto", 18 * -1), bd=0, highlightthickness=0)
        self.ipEntry.place(x=22, y=194, width=256, height=33)

        self.portEntry = Entry(self, font=("Roboto", 18 * -1), bd=0, highlightthickness=0)
        self.portEntry.place(x=22, y=244, width=256, height=33)

        self.pin2Entry = Entry(self, font=("Roboto", 18 * -1), bd=0, highlightthickness=0)
        self.pin2Entry.place(x=22, y=294, width=256, height=33)

        self.pinEntry.insert(0, "Enter Pin")
        self.ipEntry.insert(0, "Enter IP Address")
        self.portEntry.insert(0, "Enter Port")
        self.pin2Entry.insert(0, "Enter Pin")

        self.pinEntry.bind('<Button-1>', self.reset_pin)
        self.ipEntry.bind('<Button-1>', self.reset_ip)
        self.portEntry.bind('<Button-1>', self.reset_port)
        self.pin2Entry.bind('<Button-1>', self.reset_pin2)

        self.pinEntry.bind('<Return>', self.host_button)
        self.pin2Entry.bind('<Return>', self.connect_button)

        """____Buttons____"""
        temp = Button(self, text="", image=clear_image, borderwidth=0, highlightthickness=0, relief="flat",
                      command=self.host_clear)
        temp.image = clear_image
        temp.place(x=10, y=70, width=135, height=40)

        temp = Button(self, image=generate_image, borderwidth=0, highlightthickness=0, relief="flat",
                      command=self.generate_pin)
        temp.img = generate_image
        temp.place(x=155, y=70, width=135, height=40)

        temp = Button(self, image=host_image, borderwidth=0, highlightthickness=0, relief="flat",
                      command=self.host_button)
        temp.img = host_image
        temp.place(x=10, y=120, width=280, height=40)

        temp = Button(self, image=clear_image, borderwidth=0, highlightthickness=0, relief="flat",
                      command=self.conn_clear)
        temp.img = clear_image
        temp.place(x=10, y=340, width=135, height=40)

        temp = Button(self, image=connect_image, borderwidth=0, highlightthickness=0, relief="flat",
                      command=self.connect_button)
        temp.img = connect_image
        temp.place(x=155, y=340, width=135, height=40)

        sleep(0.2)
        self.master.stop_loading_screen()
        self.pack(fill='both', expand=1)

    def reset_pin(self, event=None):
        self.pinEntry.delete(0, 'end')
        self.pinEntry.unbind('<Button-1>')

    def reset_ip(self, event=None):
        self.ipEntry.delete(0, 'end')
        self.ipEntry.unbind('<Button-1>')

    def reset_port(self, event=None):
        self.portEntry.delete(0, 'end')
        self.portEntry.unbind('<Button-1>')

    def reset_pin2(self, event=None):
        self.pin2Entry.delete(0, 'end')
        self.pin2Entry.unbind('<Button-1>')

    def host_clear(self):
        self.pinEntry.delete(0, 'end')
        self.pinEntry.insert(0, "Enter Pin")
        self.pinEntry.bind('<Button-1>', self.reset_pin)

    def conn_clear(self):
        self.ipEntry.delete(0, 'end')
        self.portEntry.delete(0, 'end')
        self.pin2Entry.delete(0, 'end')
        self.ipEntry.insert(0, "Enter IP Address")
        self.portEntry.insert(0, "Enter Port")
        self.pin2Entry.insert(0, "Enter Pin")
        self.ipEntry.bind('<Button-1>', self.reset_ip)
        self.portEntry.bind('<Button-1>', self.reset_port)
        self.pin2Entry.bind('<Button-1>', self.reset_pin2)

    def generate_pin(self):
        self.pinEntry.unbind('<Button-1>')
        self.pinEntry.delete(0, 'end')
        self.pinEntry.insert(0, generate_pin())

    """____Socket_Func____"""

    def connect_button(self, event=None):
        ThreadedTask(self.connect)
        self.pack_forget()
        self.master.start_loading_screen()

    def connect(self):
        host, port, pin = self.ipEntry.get(), self.portEntry.get(), self.pin2Entry.get()
        if check_connect_parameters(host, port, pin):
            self.master.socket = Client()
            self.master.socket.initialize()

            self.master.socket.connect(host, port, pin)
            if self.master.socket.state == 'Running':
                self.next_page()
            else:
                messagebox.showwarning("Warning", "Error in Connecting.")
                self._return()
        else:
            self._return()

    def host_button(self, event=None):
        pin = self.pinEntry.get()
        pin = check_host_parameters(pin)
        if pin is not None:
            ThreadedTask(self.host, (pin,))
            self.pack_forget()
            self.master.start_loading_screen()

    def host(self, pin):
        self.master.socket = Server(pin)
        self.master.socket.initialize('public',)
        if self.master.socket.state == 'Running':
            self.next_page()
        else:
            messagebox.showwarning("Warning", "Error in Hosting.")
            self._return()

    def _return(self):
        sleep(0.2)
        self.master.stop_loading_screen()
        self.pack(fill='both', expand=1)

    def next_page(self):
        ThreadedTask(HomePage, (self.master,))
        self.destroy()
        self.master.start_loading_screen()
