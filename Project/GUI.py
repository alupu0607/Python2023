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

    def execute_command(self, data_type, action, value):
        result = f"Executing {action} on {data_type} with value {value}..."
        print(result)
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
                ttk.Label(frame, text="Value:").grid(row=0, column=0, padx=5, pady=5)
                value_entry = ttk.Entry(frame)
                value_entry.grid(row=0, column=1, padx=5, pady=5)
                ttk.Button(frame, text="Create",command=lambda: self.execute_command(data_type, action, value_entry.get())).grid(row=0,column=2,padx=5,pady=5)
                ttk.Button(frame, text="❔", command=lambda: self.popup_info(data_type, action)).grid(row=0, column=3, columnspan=3, pady=5)
            elif action == "Read":
                pass
            elif action == "Update":
                pass
            elif action == "Delete":
                pass

    def popup_info(self, data_type, action):
        info_text = f"Information about {action} operation on {data_type}:\n\n"  # Add your information here
        messagebox.showinfo(f"{action} {data_type} Info", info_text)
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
