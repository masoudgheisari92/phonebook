import sqlite3
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox


class PhoneBook:
    def __init__(self, window, con):
        self.con = con
        self.cursor = self.con.cursor()
        self.window = window
        self.clear(self.window)
        self.main_page_gui()
        self.show_contacts()
        self.window.mainloop()

    def clear(self, window):
        x = window.winfo_children()
        for i in x:
            i.destroy()

    def show_contacts(self):
        search = self.search_entry.get()
        try:
            self.tree.delete(*self.tree.get_children())
            if not search:
                self.cursor.execute("SELECT * FROM CONTACTS_TABLE ORDER BY Name ASC")
            else:
                self.cursor.execute(
                    f"SELECT * FROM CONTACTS_TABLE WHERE Mobile_Number LIKE '%{search}%' OR NAME LIKE '%{search}%'"
                )

            fetch = self.cursor.fetchall()
            for data in fetch:
                self.tree.insert("", "end", values=(data))
        except tk.TclError:
            pass

    def edit_contact(self):
        if not self.tree.selection():
            tkMessageBox.showwarning(
                "Error : No contact selected",
                "Please select a contact first!",
                icon="warning",
            )
        else:
            cur_item = self.tree.focus()
            contents = self.tree.item(cur_item)
            selected_item = contents["values"]
            self.tree.delete(cur_item)
            self.cursor.execute(
                f"SELECT * FROM CONTACTS_TABLE WHERE Mobile_Number = {selected_item[1]} OR Mobile_Number = '0{selected_item[1]}'"
            )
            fetch = self.cursor.fetchall()[0]

            self.mobile_before_edit = selected_item[1]

            self.edit_contact_gui(fetch)

    def delete_contact(self):
        if not self.tree.selection():
            result = tkMessageBox.showwarning(
                "Error : No Contact Selected",
                "Please Select Something First!",
                icon="warning",
            )
        else:
            result = tkMessageBox.askquestion(
                "Warning",
                "Are you sure you want to delete this record?",
                icon="warning",
            )
            if result == "yes":
                curItem = self.tree.focus()
                contents = self.tree.item(curItem)
                selecteditem = contents["values"]
                self.tree.delete(curItem)
                self.cursor.execute(
                    f"DELETE FROM CONTACTS_TABLE WHERE Mobile_Number = {selecteditem[1]} OR Mobile_Number = '0{selecteditem[1]}'"
                )
                self.con.commit()
                self.show_contacts()

    def check_int(self, num):
        for i in num:
            if ord(i) > 57 or ord(i) < 48:
                return False
        return True

    def init_call(self):
        self.__init__(self.window, self.con)

    def edit_contact_in_db(self, mobile):
        mobile = self.mobile_before_edit
        self.cursor.execute(
            f"DELETE FROM CONTACTS_TABLE WHERE Mobile_Number = {mobile} OR Mobile_Number = '0{mobile}'"
        )
        self.save_contact_to_db()

    def save_contact_to_db(self):
        name = self.name.get()
        mobile = self.mobile.get()
        phone1 = self.phone1.get()
        phone2 = self.phone2.get()
        email = self.email.get()
        notes = self.E6.get("1.0", "end-1c")

        if name == "" or mobile == "":
            result = tkMessageBox.showwarning(
                "Error : All Fields Not Filled",
                "Please Complete The Required Fields",
                icon="warning",
            )
        if (
            self.check_int(mobile) == False
            or self.check_int(phone1) == False
            or self.check_int(phone2) == False
        ):
            result = tkMessageBox.showwarning(
                "Error : Invalid Mobile or Phone Number",
                "Please Check The Mobile or Phone Number. No special Characters or Letters allowed.",
                icon="warning",
            )

        else:
            self.cursor.execute(
                f"SELECT * FROM CONTACTS_TABLE WHERE Mobile_Number = {mobile} OR Mobile_Number = '0{mobile}'"
            )
            res = self.cursor.fetchall()
            if len(res) == 0:
                self.cursor.execute(
                    f"""INSERT INTO CONTACTS_TABLE VALUES(
                                '{name}','{mobile}','{phone1}','{phone2}','{email}','{notes}')
                                """
                )
                self.con.commit()

                self.clear(self.window)
                self.__init__(self.window, self.con)
                self.show_contacts()
            else:
                result = tkMessageBox.showwarning(
                    "Error : Contact Exists",
                    "A Contact Card with this Mobile Number Already Exists. Please Check.",
                    icon="warning",
                )

    def main_page_gui(self):
        width = 1000
        height = 500
        self.window.title("PhoneBook")
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.window.geometry("%dx%d+%d+%d" % (width, height, x, y))
        self.window.resizable(0, 0)
        self.window.config(bg="#4bfdc8")
        self.style = ttk.Style(self.window)
        self.style.theme_use("default")
        self.style.configure(
            "Treeview",
            background="#B3c1bd",
            fieldbackground="#Ecdcec",
            foreground="#000000",
        )
        self.style.configure(
            "Treeview.Heading", background="#F0FFF4", font=("Arial", 10)
        )

        self.titlelable = tk.Label(
            self.window,
            text="My PhoneBook",
            font=("Arial", 17),
            bg="#4bfdc8",
            fg="#14213d",
        )
        self.titlelable.pack(pady=20, padx=50, side=tk.TOP, anchor=tk.W)

        self.search_entry_text = tk.Label(
            self.window,
            text="Enter name or mobile",
            font=("Arial", 10),
            bg="#4bfdc8",
            fg="#14213d",
        )
        self.search_entry_text.place(x=300, y=10)
        self.search_entry = tk.Entry(self.window, width=50)
        self.search_entry.place(x=300, y=30)

        self.search_button = tk.Button(
            self.window,
            text="Search",
            relief=tk.FLAT,
            activebackground="#1BFF1E",
            font=("Arial", 10),
            bg="#8AFF1B",
            fg="#14213d",
            command=self.show_contacts,
        )
        self.search_button.place(x=610, y=26)

        self.add_button = tk.Button(
            self.window,
            text="Add",
            relief=tk.FLAT,
            activebackground="#1BFF1E",
            font=("Arial", 10),
            bg="#8AFF1B",
            fg="#14213d",
            command=self.add_new_contact_gui,
        )
        self.add_button.place(x=800, y=20)

        self.edit_button = tk.Button(
            self.window,
            text="Edit",
            relief=tk.FLAT,
            activebackground="#Fdd04b",
            font=("Arial", 10),
            bg="#Fdd04b",
            fg="#14213d",
            command=self.edit_contact,
        )
        self.edit_button.place(x=850, y=20)

        self.delete_button = tk.Button(
            self.window,
            text="Delete",
            relief=tk.FLAT,
            activebackground="#FF200E",
            activeforeground="#FFFFFF",
            font=("Arial", 10),
            bg="#FF2525",
            fg="#FFFFFF",
            command=self.delete_contact,
        )
        self.delete_button.place(x=900, y=20)

        self.scrollbarx = tk.Scrollbar(self.window, orient=tk.HORIZONTAL)
        self.scrollbary = tk.Scrollbar(self.window, orient=tk.VERTICAL)
        self.tree = ttk.Treeview(
            self.window,
            height=500,
            yscrollcommand=self.scrollbary.set,
            xscrollcommand=self.scrollbarx.set,
        )

        self.scrollbary.config(command=self.tree.yview)
        self.scrollbary.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbarx.config(command=self.tree.xview)
        self.scrollbarx.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree["columns"] = ("1", "2", "3", "4", "5", "6")
        self.tree["show"] = "headings"
        self.tree.column("1", width=170, anchor="center")
        self.tree.column("2", width=150, anchor="center")
        self.tree.column("3", width=150, anchor="center")
        self.tree.column("4", width=200, anchor="center")
        self.tree.column("5", width=150, anchor="center")
        self.tree.column("6", width=250, anchor="center")

        self.tree.heading("1", text="Name")
        self.tree.heading("2", text="Mobile")
        self.tree.heading("3", text="Phone1")
        self.tree.heading("4", text="Phone2")
        self.tree.heading("5", text="Email")
        self.tree.heading("6", text="Notes")

        self.tree.pack()

    def edit_contact_gui(self, contact_data):
        self.clear(self.window)
        self.window.config(bg="#4bfdc8")
        self.window.title("Edit Contact")

        # variables
        self.name = tk.StringVar()
        self.name.set(contact_data[0])
        self.mobile = tk.StringVar()
        self.mobile.set(contact_data[1])
        self.phone1 = tk.StringVar()
        self.phone1.set(contact_data[2])
        self.phone2 = tk.StringVar()
        self.phone2.set(contact_data[3])
        self.email = tk.StringVar()
        self.email.set(contact_data[4])

        # labels and buttons
        self.TitleLabel = tk.Label(
            self.window,
            text="Edit Contact",
            font=("Arial", 18),
            bg="#4bfdc8",
            fg="#14213d",
        )
        self.TitleLabel.pack()
        self.L1 = tk.Label(
            self.window,
            text="Name",
            font=("Arial", 10),
            bg="#4bfdc8",
            fg="#14213d",
        )
        self.E1 = tk.Entry(
            self.window,
            textvariable=self.name,
            width=40,
            relief=tk.FLAT,
            font=("Arial", 10),
        )
        self.L2 = tk.Label(
            self.window,
            text="Mobile Number",
            font=("Arial", 10),
            bg="#4bfdc8",
            fg="#14213d",
        )
        self.E2 = tk.Entry(
            self.window,
            textvariable=self.mobile,
            width=40,
            relief=tk.FLAT,
            font=("Arial", 10),
        )
        self.L3 = tk.Label(
            self.window,
            text="Phone Number 1",
            font=("Arial", 10),
            bg="#4bfdc8",
            fg="#14213d",
        )
        self.E3 = tk.Entry(
            self.window,
            textvariable=self.phone1,
            width=40,
            relief=tk.FLAT,
            font=("Arial", 10),
        )
        self.L4 = tk.Label(
            self.window,
            text="Phone Number 2",
            font=("Arial", 10),
            bg="#4bfdc8",
            fg="#14213d",
        )
        self.E4 = tk.Entry(
            self.window,
            textvariable=self.phone2,
            width=40,
            relief=tk.FLAT,
            font=("Arial", 10),
        )
        self.L5 = tk.Label(
            self.window,
            text="Email",
            font=("Arial", 10),
            bg="#4bfdc8",
            fg="#14213d",
        )
        self.E5 = tk.Entry(
            self.window,
            textvariable=self.email,
            width=40,
            relief=tk.FLAT,
            font=("Arial", 10),
        )
        self.L6 = tk.Label(
            self.window,
            text="Notes",
            font=("Arial", 10),
            bg="#4bfdc8",
            fg="#14213d",
        )
        self.E6 = tk.Text(
            self.window,
            width=40,
            height=4,
            relief=tk.FLAT,
            font=("Arial", 10),
        )
        self.E6.insert(tk.END, contact_data[5])

        self.B1 = tk.Button(
            self.window,
            text="Edit",
            relief=tk.FLAT,
            activebackground="#1BFF1E",
            font=("Arial", 10),
            bg="#1BFF1E",
            fg="#14213d",
            command=lambda: self.edit_contact_in_db(self.mobile_before_edit),
        )
        self.B2 = tk.Button(
            self.window,
            text="Cancel",
            relief=tk.FLAT,
            activebackground="#FF200E",
            activeforeground="#FFFFFF",
            font=("Arial", 10),
            bg="#FF2525",
            fg="#FFFFFF",
            command=self.init_call,
        )
        # placement
        self.L1.place(x=10, y=60)
        self.E1.place(x=170, y=60)
        self.L2.place(x=10, y=100)
        self.E2.place(x=170, y=100)
        self.L3.place(x=10, y=140)
        self.E3.place(x=170, y=140)
        self.L4.place(x=10, y=180)
        self.E4.place(x=170, y=180)
        self.L5.place(x=10, y=220)
        self.E5.place(x=170, y=220)
        self.L6.place(x=10, y=260)
        self.E6.place(x=170, y=260)
        self.B1.place(x=240, y=380)
        self.B2.place(x=300, y=380)

    def add_new_contact_gui(self):
        self.clear(self.window)
        self.window.config(bg="#4bfdc8")
        self.window.title("New Contact")

        # variables
        self.name = tk.StringVar()
        self.mobile = tk.StringVar()
        self.phone1 = tk.StringVar()
        self.phone2 = tk.StringVar()
        self.email = tk.StringVar()

        # labels and buttons
        self.TitleLabel = tk.Label(
            self.window,
            text="New Contact",
            font=("Arial", 18),
            bg="#4bfdc8",
            fg="#14213d",
        )
        self.TitleLabel.pack()
        self.L1 = tk.Label(
            self.window,
            text="Name",
            font=("Arial", 10),
            bg="#4bfdc8",
            fg="#14213d",
        )
        self.L1.place(x=10, y=60)
        self.E1 = tk.Entry(
            self.window,
            textvariable=self.name,
            width=40,
            relief=tk.FLAT,
            font=("Arial", 10),
        )
        self.E1.place(x=170, y=60)
        self.L2 = tk.Label(
            self.window,
            text="Mobile Number",
            font=("Arial", 10),
            bg="#4bfdc8",
            fg="#14213d",
        )
        self.L2.place(x=10, y=100)
        self.E2 = tk.Entry(
            self.window,
            textvariable=self.mobile,
            width=40,
            relief=tk.FLAT,
            font=("Arial", 10),
        )
        self.E2.place(x=170, y=100)
        self.L3 = tk.Label(
            self.window,
            text="Phone Number 1",
            font=("Arial", 10),
            bg="#4bfdc8",
            fg="#14213d",
        )
        self.L3.place(x=10, y=140)
        self.E3 = tk.Entry(
            self.window,
            textvariable=self.phone1,
            width=40,
            relief=tk.FLAT,
            font=("Arial", 10),
        )
        self.E3.place(x=170, y=140)
        self.L4 = tk.Label(
            self.window,
            text="Phone Number 2",
            font=("Arial", 10),
            bg="#4bfdc8",
            fg="#14213d",
        )
        self.L4.place(x=10, y=180)
        self.E4 = tk.Entry(
            self.window,
            textvariable=self.phone2,
            width=40,
            relief=tk.FLAT,
            font=("Arial", 10),
        )
        self.E4.place(x=170, y=180)
        self.L5 = tk.Label(
            self.window,
            text="Email",
            font=("Arial", 10),
            bg="#4bfdc8",
            fg="#14213d",
        )
        self.L5.place(x=10, y=220)
        self.E5 = tk.Entry(
            self.window,
            textvariable=self.email,
            width=40,
            relief=tk.FLAT,
            font=("Arial", 10),
        )
        self.E5.place(x=170, y=220)
        self.L6 = tk.Label(
            self.window,
            text="Notes",
            font=("Arial", 10),
            bg="#4bfdc8",
            fg="#14213d",
        )
        self.L6.place(x=10, y=260)
        self.E6 = tk.Text(
            self.window,
            width=40,
            height=4,
            relief=tk.FLAT,
            font=("Arial", 10),
        )
        self.E6.place(x=170, y=260)
        self.B1 = tk.Button(
            self.window,
            text="Save",
            relief=tk.FLAT,
            activebackground="#1BFF1E",
            font=("Arial", 10),
            bg="#1BFF1E",
            fg="#14213d",
            command=self.save_contact_to_db,
        )
        self.B1.place(x=240, y=380)
        self.B2 = tk.Button(
            self.window,
            text="Cancel",
            relief=tk.FLAT,
            activebackground="#FF200E",
            activeforeground="#FFFFFF",
            font=("Arial", 10),
            bg="#FF2525",
            fg="#FFFFFF",
            command=self.init_call,
        )
        self.B2.place(x=300, y=380)


def load_dataset():
    con = sqlite3.connect("Contacts.db")
    cur = con.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS CONTACTS_TABLE(
                Name varchar(50),
                Mobile_Number varchar(50) PRIMARY KEY,
                Phone_Number_1 int,
                Phone_Number_2 int,
                Email varchar(100),
                Notes longtext)           
                """
    )
    cur.execute("SELECT * FROM CONTACTS_TABLE")
    fetch = cur.fetchall()
    if not fetch:
        cur.execute(
            """INSERT INTO CONTACTS_TABLE VALUES
        ("Test1","09123456789",12345678,12345678,"test1@example.com","A Test Contact Card."),
        ("Test2","09123456788",12345678,12345678,"test2@example.com","A Test Contact Card.")
        """
        )
    return con


root = tk.Tk()
con = load_dataset()
cur = PhoneBook(root, con)
