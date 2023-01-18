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
root.wm_minsize(width=260, height=350)
root.wm_maxsize(width=500, height=360)

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


def read_targets():
    try:
        with open(logins_dir, 'r') as file:
            content = file.read()
            content = content.split("\n")
        return content
    except FileNotFoundError:
        e = FileNotFoundError.strerror
        print(e)


class OPOGui:
    def __init__(self, **kwargs):
        root.title("One Pass Only")
        root.option_add('*tearOff', FALSE)  # The menu doesn't separate
        root.iconbitmap(icons_dir + "app_icon.ico")
        self.targets_list = None
        self.secret_entry = None
        self.password_length = None
        self.code = StringVar(root)
        self.generated_pass_label = None

    def run(self):
        # Mainframe
        mainframe = ttk.Frame(root, padding='8 8 8 8')
        mainframe.pack()


        # TODO add a menu
        # Menu
        # main_menu = Menu(root)
        # root['menu'] = main_menu
        # menu_file = Menu(main_menu)
        # menu_about = Menu(main_menu)
        # main_menu.add_cascade(menu=menu_file, label='File')
        # main_menu.add_cascade(menu=menu_about, label='About')

        # Label Frame containing the list of all logins or Known Keys and the add, remove and save buttons
        target_frame = LabelFrame(mainframe, text='Target:')
        target_frame['labelanchor'] = 'nw'
        target_frame['font'] = FONTS['default']
        target_frame.columnconfigure(1, weight=1)
        target_frame.grid(sticky="W E", pady=(0, 12))

        # Frame containing add, remove and save logins buttons
        list_btns_frame = Frame(target_frame)
        list_btns_frame.grid(column=0, row=0, sticky="N S E W")

        btn_add = Button(list_btns_frame, text="add", command=self.add_target)
        btn_add['relief'] = GROOVE
        btn_add['image'] = IMAGES.get('addknownkey')
        btn_add.grid(column=0, row=0, sticky="N", padx=3, pady=5)

        btn_remove = Button(list_btns_frame, text="remove", command=self.remove_target)
        btn_remove['relief'] = GROOVE
        btn_remove['image'] = IMAGES.get('removeknownkey')
        btn_remove.grid(column=0, row=1, sticky="N", padx=3, pady=5)

        btn_save = Button(list_btns_frame, text="save", command=self.to_file)
        btn_save['relief'] = GROOVE
        btn_save['image'] = IMAGES.get('saveknownkey')
        btn_save.grid(column=0, row=2, sticky="N", padx=3, pady=5)

        # List of all logins or Known Keys
        logins = read_targets()  # Load the saved logins
        logins_var = StringVar(value=logins)
        self.targets_list = Listbox(target_frame, height=5, listvariable=logins_var)
        self.targets_list['relief'] = FLAT
        self.targets_list['borderwidth'] = 5
        self.targets_list['activestyle'] = 'dotbox'
        self.targets_list['font'] = FONTS['listbox']
        self.targets_list.grid(column=1, row=0, pady=5, sticky="W E")
        self.targets_list.selection_set(0)

        list_scroll = Scrollbar(target_frame, orient=VERTICAL, command=self.targets_list.yview)
        self.targets_list.configure(yscrollcommand=list_scroll.set)
        list_scroll.grid(column=2, row=0, sticky="N S")

        secret_frame = LabelFrame(mainframe, text='Secret:')
        secret_frame['width'] = 330
        secret_frame['labelanchor'] = 'nw'
        secret_frame['font'] = FONTS['default']
        secret_frame.columnconfigure(1, weight=1)
        secret_frame.grid(sticky="W E", pady=(0, 12))

        # Secret Label and Secret Entry
        secret_label = Label(secret_frame, text="Key:")
        secret_label['font'] = FONTS['default']
        secret_label.grid(column=0, row=0, sticky="N W", padx=5, pady=10)

        self.secret_entry = Entry(secret_frame, show="*")
        self.secret_entry['font'] = FONTS['default']
        self.secret_entry['exportselection'] = 0
        self.secret_entry.focus()
        self.secret_entry.grid(column=1, row=0, sticky="W E", padx=10, pady=10)

        # TODO create checkbox to show Secret or not
        # self.show_secret_chbox = Checkbutton(unknownkey_frame)
        # self.show_secret_chbox.grid(column=1, row=2, sticky="N E")

        # Frame that contains the generate button and password_length spin
        generate_frame = Frame(mainframe)
        generate_frame.columnconfigure(1, weight=1)
        generate_frame.grid(sticky="W E", pady=(0, 12))

        # Length of message Label and Spinbox
        length_label = Label(generate_frame, text="Length:")
        length_label['font'] = FONTS['default']
        length_label.grid(column=0, row=0, sticky="W", padx=5)

        spin_var = StringVar(value="16")
        spin_var.set("20")
        self.password_length = Spinbox(generate_frame, from_=1, to=48, textvariable=spin_var)
        self.password_length['width'] = 6
        self.password_length['justify'] = RIGHT
        self.password_length['font'] = FONTS['default']
        self.password_length.grid(column=0, row=1, padx=5, sticky="N W")

        # Button Generate Password
        btn_generate = Button(generate_frame, text='Generate', compound=RIGHT, command=self.render_pass)
        btn_generate['font'] = FONTS['password']
        btn_generate['image'] = IMAGES['generate']
        btn_generate.grid(column=1, row=0, rowspan=2, sticky="N S E W", padx=(5, 0), pady=5)

        # Frame contaning the generated password
        password_frame = Frame(mainframe)
        password_frame['highlightbackground'] = 'black'
        password_frame['highlightthickness'] = 1
        password_frame.grid(sticky="W E", pady=(0, 12))

        self.generated_pass_label = Label(password_frame, textvariable=self.code)
        self.generated_pass_label['font'] = FONTS['pass_init']
        self.code.set(PASS_PLACEHOLDER)
        self.generated_pass_label.grid(column=1, row=0, padx=10, pady=10, sticky="W")

        def clipboard():
            """
            Copy the generated password to the clipboard
            :return: None
            """
            root.clipboard_clear()
            if self.generated_pass_label['text'] != PASS_PLACEHOLDER:
                root.clipboard_append(self.generated_pass_label['text'])
                root.update()

        btn_clipboard = Button(password_frame, text="copy", command=clipboard)
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
        target = self.targets_list.get(ACTIVE)
        secret = self.secret_entry.get()
        length = int(self.password_length.get())
        result = generator.genpass(target, secret, length=length)
        self.generated_pass_label['font'] = FONTS['password']
        self.code.set(result)

    def add_target(self):
        """
        Adds a new Known key to the list.
        :return: None
        """
        target = simpledialog.askstring("Add login", prompt="Add a known Key:")
        self.targets_list.insert(0,target)

    def remove_target(self):
        """
        Removes the current selected entry of the Listbox
        :return: None
        """
        idx = self.targets_list.curselection()
        if idx:
            answer = messagebox.askquestion("Delete", "Are you sure you want to delete the item?")
            if answer == 'yes':
                self.targets_list.delete(idx)
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
                items = self.targets_list.get(0, self.targets_list.size() - 1)
                stream = ""
                for s in items:
                    stream += s+"\n"
                with open(logins_dir, 'w') as file:
                    file.write(stream)
            except FileExistsError:
                print(FileExistsError.strerror)

