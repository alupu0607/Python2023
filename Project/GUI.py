import tkinter as tk
from tkinter import ttk, messagebox
from redis_client import RedisClient
import sys

class FunctionalitiesGUI:
    def __init__(self, master, redis_client):
        self.master = master
        self.redis_client = redis_client

        self.functionalities_window = tk.Toplevel(self.master)
        self.functionalities_window.title('RESP GUI')
        self.functionalities_window.minsize(800, 400)
        self.functionalities_window.maxsize(800, 400)

        self.functionality_info_label = ttk.Label(self.functionalities_window, text="CRUD Operations", font=('Verdana', 10))
        self.functionality_info_label.pack(pady=5)

        self.notebook = ttk.Notebook(self.functionalities_window)

        self.create_tab("Lists")
        self.create_tab("Sets")
        self.create_tab("Hashes")
        self.create_tab("Sorted Sets")
        self.create_tab("Strings")

        self.notebook.pack(expand=1, fill="both")

        self.functionalities_window.protocol("WM_DELETE_WINDOW", self.stop)

        self.notebook = ttk.Notebook(self.functionalities_window)

        self.result_label = ttk.Label(self.functionalities_window, text="", font=('Verdana', 12), foreground='green')
        self.result_label.pack(pady=10)

        menubar = tk.Menu(self.functionalities_window)
        self.functionalities_window.config(menu=menubar)
        self.functionalities_instance = None

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Welcome GUI", command=self.open_welcome_gui)
        file_menu.add_command(label="Exit", command=self.stop)

    def execute_command(self, data_type, action, *args):
        if data_type == "Strings":
            if action == "Create":
                result = self.redis_client.strings_set(*args)
            elif action == "Read":
                result = self.redis_client.strings_get(*args)
            elif action == "Update":
                result = self.redis_client.strings_incrby(*args)
            elif action == "Delete":
                keys = args[0].split(",")
                result = self.redis_client.strings_del(*keys)
            else:
                result = "Invalid action"
        result = f"Data-type-{data_type},Action-{action}, Introduced: {args} => Response: {result}"
        self.result_label.config(text=result)

    def create_tab(self, data_type):
        frame = ttk.Frame(self.notebook)

        sub_notebook = ttk.Notebook(frame)
        for action in ["Create", "Read", "Update", "Delete"]:
            sub_frame = ttk.Frame(sub_notebook)
            sub_notebook.add(sub_frame, text=action)
            self.create_buttons(sub_frame, data_type, action)

        sub_notebook.pack(expand=1, fill="both")

        self.notebook.add(frame, text=data_type)

    def create_buttons(self, frame, data_type, action):
        if data_type == "Strings":
            if action == "Create":
                ttk.Label(frame, text="Key:").grid(row=0, column=0, padx=5, pady=5)
                name_entry = ttk.Entry(frame)
                name_entry.grid(row=0, column=1, padx=5, pady=5)

                ttk.Label(frame, text="Value:").grid(row=0, column=2, padx=5, pady=5)
                value_entry = ttk.Entry(frame)
                value_entry.grid(row=0, column=3, padx=5, pady=5)

                ttk.Button(frame, text="SET", command=lambda: self.execute_command(data_type, action, name_entry.get(),value_entry.get())).grid(row=0,column=4,padx=5,pady=5)
                ttk.Button(frame, text="❔", command=lambda: self.popup_info(data_type, action)).grid(row=0, column=5,pady=5)
            elif action == "Read":
                ttk.Label(frame, text="Key:").grid(row=0, column=0, padx=5, pady=5)
                name_entry = ttk.Entry(frame)
                name_entry.grid(row=0, column=1, padx=5, pady=5)
                ttk.Button(frame, text="GET",command=lambda: self.execute_command(data_type, action,name_entry.get(), "" )).grid(row=0,column=2,padx=5, pady=5)
                ttk.Button(frame, text="❔",command=lambda: self.popup_info(data_type, action)).grid(row=0, column=3,columnspan=3,pady=5)
            elif action == "Update":
                ttk.Label(frame, text="Key:").grid(row=0, column=0, padx=5, pady=5)
                name_entry = ttk.Entry(frame)
                name_entry.grid(row=0, column=1, padx=5, pady=5)

                ttk.Label(frame, text="Increment:").grid(row=0, column=2, padx=5, pady=5)
                value_entry = ttk.Entry(frame)
                value_entry.grid(row=0, column=3, padx=5, pady=5)

                ttk.Button(frame, text="INCRBY", command=lambda: self.execute_command(data_type, action, name_entry.get(),value_entry.get())).grid(row=0, column=4,padx=5,pady=5)
                ttk.Button(frame, text="❔", command=lambda: self.popup_info(data_type, action)).grid(row=0, column=5,pady=5)
            elif action == "Delete":
                ttk.Label(frame, text="Key(s):").grid(row=0, column=0, padx=5, pady=5)
                name_entry = ttk.Entry(frame)
                name_entry.grid(row=0, column=1, padx=5, pady=5)
                ttk.Button(frame, text="DEL",
                           command=lambda: self.execute_command(data_type, action, name_entry.get(), "")).grid(row=0,column=2,
                                                                                                               padx=5,
                                                                                                               pady=5)
                ttk.Button(frame, text="❔", command=lambda: self.popup_info(data_type, action)).grid(row=0, column=3,columnspan=3,pady=5)
        elif data_type == "Lists":
            ...
        elif data_type == "Sets":
            ...
        elif data_type == "Hashes":
            ...
        elif data_type == "Sorted Sets":
            ...

    def popup_info(self, data_type, action):
        if data_type == "Strings":
            if action == "Create":
                info_text = (f"Set key to hold the string value. If key already holds a value, it is overwritten, regardless of its type. Any previous time to live associated with the key is discarded on successful SET operation."
                            f"redis> SET mykey Hello\n\n"
                            f"OK\n\n"
                            f"redis> GET mykey\n"
                            f"Hello\n\n"
                            f"redis> SET anotherkey will expire in a minute EX 60\n\n"
                            f"OK\n\n")
                messagebox.showinfo(f"Information about {action} operation on {data_type}:",info_text)
            elif action == "Read":
                info_text = (f"Get the value of key. If the key does not exist the special value nil is returned. An error is returned if the value stored at key is not a string, because GET only handles string values.\n\n"
                            f"redis > GET  nonexisting\n\n"
                            f"(nil)\n\n"
                            f"redis > GET mykey \n\n"
                            f"Hello")
                messagebox.showinfo(f"Information about {action} operation on {data_type}:", info_text)
            elif action == "Update":
                info_text = (f"Increments the number stored at key by increment. If the key does not exist, it is set to 0 before performing the operation. An error is returned if the key contains a value of the wrong type or contains a string that can not be represented as integer. This operation is limited to 64 bit signed integers.\n\n"
                            f"redis> SET mykey 10\n\n"
                            f"OK\n\n"
                            f"redis> INCRBY mykey 5\n\n"
                            f"(integer) 15")
                messagebox.showinfo(f"Information about {action} operation on {data_type}:", info_text)
            elif action == "Delete":
                info_text = (f"Removes the specified keys. A key is ignored if it does not exist.\n\n"
                             f"Examples: redis> SET key1 Hello\n\n"
                            f"OK\n\n"
                            f"redis> SET key2 World\n\n"
                            f"OK\n\n"
                            f"redis> DEL key1 key2 key3\n\n"
                            f"(integer) 2\n\n\n\n"
                            f"USAGE GUI: COMMA SEPARATED KEYS, NO WHITESPACES"
                             )
                messagebox.showinfo(f"Information about {action} operation on {data_type}:",info_text)

    def stop(self):
        self.redis_client.close()
        self.master.destroy()
        sys.exit()

    def open_welcome_gui(self):
        if self.functionalities_instance:
            self.functionalities_instance.master.withdraw()

        self.master.deiconify()

    def open_functionalities_gui(self):
        self.master.withdraw()
        FunctionalitiesGUI(self.master, self.redis_client)



class WelcomeGUI:
    def __init__(self, master):
        self.master = master

        master.title('RESP GUI')
        master.minsize(800, 400)
        master.maxsize(800, 400)

        self.label = ttk.Label(master, text="Welcome to RESP GUI!", font=('Verdana', 15))
        self.label.grid(row=0, column=0, pady=10)

        self.description_text = tk.Text(master, wrap=tk.WORD, width=80, height=8, font=('Verdana', 12))
        self.description_text.insert(tk.END,
                                     "RESP can serialize different data types including integers, strings, and arrays. "
                                     "It also features an error-specific type. A client sends a request to the Redis server "
                                     "as an array of strings. The array's contents are the command and its arguments that "
                                     "the server should execute. The server's reply type is command-specific."
                                     "RESP is binary-safe and uses prefixed length to transfer bulk data so it does not require processing bulk data transferred from one process to another.")
        self.description_text.config(state=tk.DISABLED)
        self.description_text.grid(row=1, column=0, pady=10)

        self.status_label = ttk.Label(master, text="Check REDIS status by pressing 'PING'", font=('Verdana', 12),
                                      foreground='blue')
        self.status_label.grid(row=2, column=0, pady=10, columnspan=2)
        self.ping_button = tk.Button(master, text='PING', width=25, command=self.check_ping)
        self.ping_button.grid(row=3, column=0, pady=10)

        menubar = tk.Menu(master)
        master.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Welcome GUI", command=self.open_welcome_gui)
        file_menu.add_command(label="Open Functionalities GUI", command=self.open_functionalities_gui)

        master.grid_columnconfigure(0, weight=1)


        master.protocol("WM_DELETE_WINDOW", self.stop)
        self.redis_client = RedisClient()
        self.functionalities_instance = None

    def check_ping(self):
        try:
            ping_success = self.redis_client.ping()

            if ping_success:
                print("OK")
                self.master.withdraw()
                FunctionalitiesGUI(self.master, self.redis_client)
            else:
                print("NOT OK")

        except Exception as e:
            print(f"Error during PING: {e}")
            print("NOT OK")

    def open_welcome_gui(self):
        ...

    def open_functionalities_gui(self):
        self.master.withdraw()
        if not self.functionalities_instance:
            self.functionalities_instance = FunctionalitiesGUI(self.master, self.redis_client)
        else:
            self.functionalities_instance.master.deiconify()

    def stop(self):
        self.redis_client.close()
        self.master.destroy()
        sys.exit()

def main():
    root = tk.Tk()
    app = WelcomeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
