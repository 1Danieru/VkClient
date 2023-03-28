import tkinter
import tkinter.messagebox
import customtkinter
import webbrowser
import ctypes
import os
from chat import Chat
from db import Database
from keys_generation import Keys

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # configure window
        self.title("Vk Client")
        self.geometry(f"{600}x{300}")
        self.resizable(width=False, height=False)
        self.x = (self.winfo_screenwidth() - 600) / 2
        self.y = (self.winfo_screenheight() - 300) / 2
        self.wm_geometry("%dx%d+%d+%d" % (600, 300, self.x, self.y))
        self.font = customtkinter.CTkFont(family="Helvetica", size=12)

        # create label and entry for user's id
        self.user_id_label = customtkinter.CTkLabel(self,  justify='center', text='USER ID', width=240, height=20, font=self.font)
        self.user_id_label.place(x=80, y=50)
        self.user_id_entry = customtkinter.CTkEntry(self, justify='left', width=240, height=30, font=self.font)
        self.user_id_entry.place(x=80, y=70)

        # create label and entry for user's token
        self.token_label = customtkinter.CTkLabel(self, justify='center', text='TOKEN', width=240, height=20, font=self.font)
        self.token_label.place(x=80, y=100)
        self.token_entry = customtkinter.CTkEntry(self, justify='left', width=240, height=30, font=self.font)
        self.token_entry.place(x=80, y=120)

        # create button 'connect'
        self.btn_connect = customtkinter.CTkButton(self, text='Connect', cursor="hand2", width=100, height=60, command=self.btn_connect_event)
        self.btn_connect.place(x=350, y=80)

        # create button 'Clean'
        self.btn_clean = customtkinter.CTkButton(self, text='Clean', cursor="hand2", width=100, height=60, command=self.btn_clean_event)
        self.btn_clean.place(x=150, y=210)

        # create button 'Chat'
        self.btn_chat = customtkinter.CTkButton(self, text='Chat', cursor="hand2", width=100, height=60, command=self.btn_chat_event)
        self.btn_chat.place(x=350, y=210)

        # create button '?'
        self.btn_info = customtkinter.CTkButton(self, fg_color='#ebebeb', text_color='blue', text='?', cursor="hand2", width=20, height=25, command=self.btn_info_event)
        self.btn_info.place(x=0, y=0)

        # create button 'GET TOKEN'
        self.btn_get_token = customtkinter.CTkButton(self, fg_color='#ebebeb', text_color='blue', text='GET TOKEN', cursor="hand2", width=100, height=20, command=self.get_token_event)
        self.btn_get_token.place(x=5, y=275)

    def btn_connect_event(self):
        """Getting user_id and token"""
        token = self.token_entry.get()
        self.token_entry.delete(0, 'end')
        user_id = self.user_id_entry.get()
        self.user_id_entry.delete(0, 'end')

        if not user_id or not token:
            tkinter.messagebox.showinfo(message='Insert TOKEN and USER_ID.')
        else:
            # Creating database
            db = Database()
            db.create_database()
            db.add_token_and_user_id(token=token, user_id=user_id)
            del db

            # Generating keys
            key_gen = Keys()
            key_gen_ = key_gen.key_generation()
            del key_gen, key_gen_

            chat = Chat()
            chat_ = chat.key_exchange()
            del chat_

    def btn_clean_event(self):
        """Deleting .db .pem .bin files"""
        y_n = tkinter.messagebox.askyesno(message="Files .db .bin .pem will be deleted. Do you want to continue?")
        if y_n is True:
            dir_name = os.getcwd()
            files = os.listdir(dir_name)
            for filename in files:
                if filename.endswith('.bin'):
                    os.remove(os.path.join(dir_name, filename))
                elif filename.endswith('.pem'):
                    os.remove(os.path.join(dir_name, filename))
                elif filename.endswith('.db'):
                    os.remove(os.path.join(dir_name, filename))

    def btn_chat_event(self):
        '''Create chat window'''
        Chat()
            
    def btn_info_event(self):
        '''Redirects to the github.com'''
        y_n = tkinter.messagebox.askyesno(message="All instructions are on github.\nRedirect to https://github.com/1Danieru/VkClient?")
        if y_n is True:
            webbrowser.open(url="https://github.com/1Danieru/VkClient", new=2) 

    def get_token_event(self):
        '''Redirects to the site to get the token'''
        y_n = tkinter.messagebox.askyesno(message="Redirect to vkhost.github.io?")
        if y_n is True:
            webbrowser.open(url="https://vkhost.github.io", new=2) 


if __name__ == "__main__":
    if ctypes.windll.shell32.IsUserAnAdmin():
        app = App()
        app.mainloop()
    else:
        tkinter.messagebox.showinfo(message='Admin mode is required, please run as administrator and try again...')