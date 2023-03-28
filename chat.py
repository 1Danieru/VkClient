import tkinter
import tkinter.messagebox
import customtkinter
import os
import random
import json
import string
import threading
import requests
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from db import Database

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class Chat(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Configure window
        self.title("Vk Client")
        self.geometry(f"{800}x{500}")
        self.resizable(width=False, height=False)
        self.x = (self.winfo_screenwidth() - 800) / 2
        self.y = (self.winfo_screenheight() - 500) / 2
        self.wm_geometry("%dx%d+%d+%d" % (800, 500, self.x, self.y))
        self.protocol("WM_DELETE_WINDOW", self.window_chat_destroy)
        self.grab_set()
        self.font = customtkinter.CTkFont(family="Helvetica", size=18)

        # Create button
        self.button = customtkinter.CTkButton(self, text='', command=self.button_event, width=70, height=50)
        self.button.place(x=720, y=440)

        # Create frame
        self.text_frame = customtkinter.CTkFrame(self, border_width=2, fg_color='#ffffff', border_color='#b3b3b3', width=780, height=420)
        self.text_frame.place(x=10, y=10)

        # Create text box
        self.text_box = customtkinter.CTkTextbox(self.text_frame, wrap='word', fg_color='#ffffff', width=760, height=400, font=self.font)
        self.text_box.place(x=10, y=10)
        self.text_box.configure(state='disabled')

        # Create entry
        self.entry = customtkinter.CTkEntry(self, width=700, height=50, font=self.font) 
        self.entry.place(x=10, y=440)
        self.entry.bind('<Return>', self.button_event)

        # Getting information from the database
        self.db = Database()
        all_data = self.db.takes_all_data()
        self.token = all_data[0]
        self.user_id = all_data[2]

        # Authorization
        self.session = vk_api.VkApi(token=self.token)
        self.vk_session = self.session.get_api()

        # Get owner_id
        # If the "try" block fails, it prints "Wrong token"
        try:
            user_get = self.vk_session.users.get()
            user_list = user_get[0]
            self.owner_id = user_list["id"]
        except:
            self.text_box.configure(state='normal')
            self.text_box.insert('end', f'Wrong token')
            self.text_box.configure(state='disabled')            

        # Get username
        user_get = self.vk_session.users.get(user_ids=self.user_id)
        user_list = user_get[0]
        self.username = user_list["first_name"]

        # Start a separate thread
        th = threading.Thread(target=self.listener)
        th.start()

    def button_event(self, *args):
        '''Sends a message to a user
        and transfers information from the "entry" field to the "text_box" field
        '''

        # Getting Owner name
        u_get = self.vk_session.users.get()
        u_list = u_get[0]
        owner_name = u_list["first_name"]

        self.text_box.configure(state='normal')
        text_value = str(self.entry.get())

        if text_value == '':
            self.text_box.insert('end', f'{text_value}\n')
            self.entry.delete(0, 'end')
            self.text_box.configure(state = 'disabled')
        else:
            t_value = '[' + str(owner_name) + '] ' + text_value

            # Filename creation
            data = text_value.encode("utf-8", "ignore")
            rand_calll = str(''.join(random.choice(string.ascii_letters) for i in range(8)) + '.bin')
            o_id_key = str(self.owner_id) + '.pem'

            # Message encryption
            file_out = open(rand_calll, "wb")
            recipient_key = RSA.import_key(open(o_id_key).read())
            session_key = get_random_bytes(16)
            cipher_rsa = PKCS1_OAEP.new(recipient_key)
            enc_session_key = cipher_rsa.encrypt(session_key)
            cipher_aes = AES.new(session_key, AES.MODE_EAX)
            ciphertext, tag = cipher_aes.encrypt_and_digest(data)
            [ file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext) ]
            file_out.close()

            # Sending a message
            url_mess = self.vk_session.docs.getMessagesUploadServer(peer_id=self.user_id)
            url_upl = requests.post(url_mess['upload_url'], files={'file' : open(rand_calll, "rb")})
            result = json.loads(url_upl.text)
            doc_save = self.vk_session.docs.save(file=result["file"])
            doc_id = doc_save["doc"]

            att_file = 'doc' + str(self.owner_id) + '_' + str(doc_id["id"])
            self.vk_session.messages.send(user_id=self.user_id, attachment=att_file, random_id=0)
            
            self.text_box.insert('end', f'{t_value}')
            self.entry.delete(0, 'end')
            self.text_box.configure(state='disabled')

    def window_chat_destroy(self):
        '''Requests confirmation from the user to close the window'''
        y_n = tkinter.messagebox.askyesno(message="All messages will be deleted after closing. Do you want to continue?")
        if y_n is True:
            del self.db
            self.destroy()
    
    def key_exchange(self):
        '''Keys exchange'''

        def send_key():
            """Send key"""
            doc = open(str(self.user_id) + '.pem', 'r')
            url_mess = self.vk_session.docs.getMessagesUploadServer(peer_id=self.user_id)
            url_upl = requests.post(url_mess['upload_url'], files={'file' : doc}).json()
            doc_save = self.vk_session.docs.save(file=url_upl["file"])
            doc_id = doc_save["doc"]

            att_file = 'doc' + str(self.owner_id) + '_' + str(doc_id["id"])
            self.vk_session.messages.send(user_id=self.user_id, attachment=att_file, random_id=0)

        # Rename owner's public key 
        os.rename("receiver.pem", str(self.user_id) + ".pem")

        send_key()
        b = False
        for event in VkLongPoll(self.session, preload_messages=True, mode=2).listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                try:
                    u_id = event.user_id
                    att = event.attachments
                    if str(u_id) == str(self.user_id):
                        try:
                            id_att = att['attach1']
                            gHA = self.vk_session.messages.getHistoryAttachments(peer_id=self.user_id, media_type='doc')
                            ac_key = gHA['items'][0]['attachment']['doc']['access_key']
                            id_ac_key = str(id_att) + '_' + str(ac_key)
                            doc_info = self.vk_session.docs.getById(docs=id_ac_key)
                            url_att = doc_info[0]['url']
                            title_att = doc_info[0]['title']

                            filename = str(self.owner_id) + '.pem'

                            if str(title_att) == str(filename):
                                # Download user's public key
                                u_doc = requests.get(url_att, allow_redirects=True)
                                open(filename, "wb").write(u_doc.content)
                                send_key()
                                b = True
                            else:
                                tkinter.messagebox.showinfo(message='names are different.')
                        except:
                            tkinter.messagebox.showinfo(message='file is missing.')
                    else:
                        tkinter.messagebox.showinfo(message=f'User {u_id} wrote a message.')
                except:
                    tkinter.messagebox.showinfo(message='u_id or att.')

            if b is True:
                break 
        
        # Filling in the table
        db = Database()
        db.populate_data(token=self.token, owner_id=self.owner_id, user_id=self.user_id, username=self.username)

    def listener(self):
        '''Accepts new user's message'''

        for event in VkLongPoll(self.session).listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                try:
                    u_id = event.user_id
                    message_id = event.message_id
                    if str(u_id) == str(self.user_id):
                        try:
                            message_info = self.vk_session.messages.getById(message_ids=message_id)
                            url_att = message_info['items'][0]['attachments'][0]['doc']['url']

                            # Filename creation
                            rand_call = str(''.join(random.choice(string.ascii_letters) for i in range(8)) + '.bin')

                            # Download file
                            u_doc = requests.get(url_att)
                            open(rand_call, "wb").write(u_doc.content)

                            # Message decryption
                            file_in = open(rand_call, "rb")
                            private_key = RSA.import_key(open("private.pem").read())
                            enc_session_key, nonce, tag, ciphertext = \
                                [ file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1) ]
                            cipher_rsa = PKCS1_OAEP.new(private_key)
                            session_key = cipher_rsa.decrypt(enc_session_key)
                            cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
                            user_data = cipher_aes.decrypt_and_verify(ciphertext, tag)
                            file_in.close()

                            # Displaying a message
                            u_message = user_data.decode("utf-8")
                            self.text_box.configure(state='normal')
                            us_message = '[' + str(self.username) + '] ' + u_message
                            self.text_box.insert('end', f'{us_message}\n')
                            self.text_box.configure(state='disabled')

                            self.vk_session.messages.markAsRead(peer_id=self.user_id)
                        except:
                            self.vk_session.messages.markAsRead(peer_id=self.user_id)
                    else:
                        ...
                except:
                    ...