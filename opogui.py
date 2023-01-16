from tkinter import *
from tkinter import ttk, simpledialog, messagebox
from tkinter import font
from PIL import ImageTk, Image
import os
import sys

from onepassonly import OnePassOnly

# TODO Implement the path to comply with different platforms
if sys.platform == 'win32':
    logins_dir = ".\\login\\d56b699830e77ba53855679cb1d252da"
    icons_dir = ".\\icons\\"
else:
    logins_dir = "./login/d56b699830e77ba53855679cb1d252da"
    icons_dir = "./icons/"

root = Tk()

IMAGES = {'addknownkey': ImageTk.PhotoImage(Image.open(icons_dir + "add_button.png")),
          'removeknownkey': ImageTk.PhotoImage(Image.open(icons_dir + "remove_button.png")),
          'saveknownkey': ImageTk.PhotoImage(Image.open(icons_dir + "save_button.png")),
          'generate': ImageTk.PhotoImage(Image.open(icons_dir + "generate_button.png")),
          'clipboard': ImageTk.PhotoImage(Image.open(icons_dir + "copy_button.png"))}

FONTS = {'default': font.Font(family='Arial', size=10, weight='bold'),
         'listbox': font.Font(family='Arial', size=11, weight='normal'),
         'password': font.Font(family='Arial', size=12, weight='bold'),
         'pass_init': font.Font(family='arial', size=10, weight='normal', slant='italic')}

PASS_PLACEHOLDER = '-- Click Generate --'


def read_logins():
    try:
        with open(logins_dir, 'r') as file:
            content = file.read()
            content = content.split("\n")
        return content
    except FileNotFoundError:
        e = FileNotFoundError.strerror
        print(e)


class OPOGui:
    def __init__(self, *args, **kwargs):
        root.title("One Pass Only")
        root.option_add('*tearOff', FALSE)  # The menu doesn't separate
        root.iconbitmap(icons_dir + "app_icon.ico")
        self.items_list = None
        self.secret_entry = None
        self.length = None
        self.code = StringVar(root)
        self.label_genpass = None

    def run(self):
        # Mainframe
        mainframe = ttk.Frame(root, padding='8 8 8 8')
        mainframe.grid(column=0, row=0, sticky="N W E S")

        # TODO add a menu
        # Menu
        # main_menu = Menu(root)
        # root['menu'] = main_menu
        # menu_file = Menu(main_menu)
        # menu_about = Menu(main_menu)
        # main_menu.add_cascade(menu=menu_file, label='File')
        # main_menu.add_cascade(menu=menu_about, label='About')

        # Label Frame containing the list of all logins or Known Keys and the add, remove and save buttons
        knownkey_frame = LabelFrame(mainframe, text='Know Keys:')
        knownkey_frame.grid(column=0, row=0, sticky="N S E W")
        knownkey_frame['labelanchor'] = 'nw'
        knownkey_frame['font'] = FONTS['default']

        # Frame containing add, remove and save logins buttons
        list_btns_frame = Frame(knownkey_frame)
        list_btns_frame.grid(column=0, row=0, sticky="N S E W")

        btn_add = Button(list_btns_frame, text="add", command=self.add_knownkey)
        btn_add.grid(column=0, row=0, sticky="N", padx=3, pady=5)
        btn_add['relief'] = GROOVE
        btn_add['image'] = IMAGES.get('addknownkey')

        btn_remove = Button(list_btns_frame, text="remove", command=self.remove_knownkey)
        btn_remove.grid(column=0, row=1, sticky="N", padx=3, pady=5)
        btn_remove['relief'] = GROOVE
        btn_remove['image'] = IMAGES.get('removeknownkey')

        btn_save = Button(list_btns_frame, text="save", command=self.to_file)
        btn_save.grid(column=0, row=2, sticky="N", padx=3, pady=5)
        btn_save['relief'] = GROOVE
        btn_save['image'] = IMAGES.get('saveknownkey')

        # List of all logins or Known Keys
        logins = read_logins()  # Load the saved logins
        logins_var = StringVar(value=logins)
        self.items_list = Listbox(knownkey_frame, height=5, width=30, listvariable=logins_var)
        self.items_list.grid(column=1, row=0, pady=5)
        self.items_list.selection_set(0)
        self.items_list['relief'] = FLAT
        self.items_list['borderwidth'] = 5
        self.items_list['activestyle'] = 'dotbox'
        self.items_list['font'] = FONTS['listbox']
        self.items_list.activate(0)

        list_scroll = Scrollbar(knownkey_frame, orient=VERTICAL, command=self.items_list.yview)
        list_scroll.grid(column=2, row=0, sticky="N S")
        self.items_list.configure(yscrollcommand=list_scroll.set)

        unknownkey_frame = LabelFrame(mainframe, text='Secret Key:')
        unknownkey_frame.grid(column=0, row=1, sticky="N S E W")
        unknownkey_frame['labelanchor'] = 'nw'
        unknownkey_frame['font'] = FONTS['default']
        unknownkey_frame.columnconfigure(1, weight=1)

        # Secret Label and Secret Entry
        secret_label = Label(unknownkey_frame, text="Key:")
        secret_label.grid(column=0, row=0, sticky="N W", padx=5, pady=10)
        secret_label['font'] = FONTS['default']
        self.secret_entry = Entry(unknownkey_frame, show="*", width=24)
        self.secret_entry.grid(column=1, row=0, sticky="N W E S", padx=5, pady=10)
        self.secret_entry['font'] = FONTS['default']
        self.secret_entry['exportselection'] = 0
        self.secret_entry.focus()

        # TODO create checkbox to show Secret Key or not
        # self.show_secret_chbox = Checkbutton(unknownkey_frame)
        # self.show_secret_chbox.grid(column=1, row=2, sticky="N E")

        # Frame that contains the generate button and length spin
        generate_frame = Frame(mainframe)
        generate_frame.grid(column=0, row=2, pady=10, sticky="N S E W")
        generate_frame.columnconfigure(1, weight=1)

        # Length of message Label and Spinbox
        length_label = Label(generate_frame, text="Length:")
        length_label.grid(column=0, row=0, sticky="W", padx=5)
        length_label['font'] = FONTS['default']

        spinvar = StringVar(value="16")
        spinvar.set("20")
        self.length = Spinbox(generate_frame, from_=1, to=48, textvariable=spinvar)
        self.length['width'] = 6
        self.length['justify'] = RIGHT
        self.length['font'] = FONTS['default']
        self.length.grid(column=0, row=1, padx=5, sticky="N W")

        # Button Generate Password
        btn_generate = Button(generate_frame, text='Generate', compound=RIGHT, command=self.render_pass)
        btn_generate['font'] = FONTS['password']
        btn_generate.grid(column=1, row=0, rowspan=2, sticky="N S E W", padx=(5, 0), pady=5)
        btn_generate['image'] = IMAGES['generate']

        # Frame contaning the generated password
        pass_container_frame = Frame(mainframe)
        pass_container_frame['highlightbackground'] = 'black'
        pass_container_frame['highlightthickness'] = 1
        pass_container_frame.bind()
        pass_container_frame.grid(column=0, row=3, sticky="N S E W", pady=5)
        pass_container_frame.columnconfigure(0, weight=1)

        self.label_genpass = Label(pass_container_frame, textvariable=self.code)
        self.label_genpass['font'] = FONTS['pass_init']
        self.code.set(PASS_PLACEHOLDER)
        self.label_genpass.grid(column=1, row=0, padx=10, pady=10, sticky="W")

        def clipboard():
            """
            Copy the generated password to the clipboard
            :return: None
            """
            root.clipboard_clear()
            if self.label_genpass['text'] != PASS_PLACEHOLDER:
                root.clipboard_append(self.label_genpass['text'])
                root.update()

        btn_clipboard = Button(pass_container_frame, text="copy", command=clipboard)
        btn_clipboard.grid(column=0, row=0, sticky="W", padx=5, pady=10)
        btn_clipboard['relief'] = FLAT
        btn_clipboard['image'] = IMAGES['clipboard']

        # TODO add a message line

        root.mainloop()

    def render_pass(self):
        """
        Renders the generated password.
        :return: None
        """
        generator = OnePassOnly()
        login = self.items_list.get(ACTIVE)
        secret = self.secret_entry.get()
        length = int(self.length.get())
        result = generator.genpass(login, secret, length=length)
        self.label_genpass['font'] = FONTS['password']
        self.code.set(result)

    def add_knownkey(self):
        """
        Adds a new Known key to the list.
        :return: None
        """
        login = simpledialog.askstring("Add login", prompt="Add a known Key:")
        self.items_list.insert(END, login)

    def remove_knownkey(self):
        """
        Removes the current selected entry of the Listbox
        :return: None
        """
        idx = self.items_list.curselection()
        if idx:
            answer = messagebox.askquestion("Delete", "Are you sure you want to delete the item?")
            if answer == 'yes':
                self.items_list.delete(idx)
        else:
            messagebox.showwarning("Message", "No Item selected.\nSelect an Item and try again.")

    def to_file(self):
        """
        Save the list of added logins to a file.
        :return: None
        """
        answer = messagebox.askquestion("Save", "Are you sure you want to save?")
        if answer == 'yes':
            try:
                items = self.items_list.get(0, self.items_list.size()-1)
                stream = ""
                for s in items:
                    stream += s+"\n"
                with open(logins_dir, 'w') as file:
                    file.write(stream)
            except FileExistsError:
                print(FileExistsError.strerror)

