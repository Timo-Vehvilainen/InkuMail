import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
import email
import code.smtplib as smtplib
from code.functions import *

'''
This class is used for producing the subwindow for requesting login information.
It also handles the sending of the newsletter.
'''

class LoginDialog(tk.Toplevel):
    
    '''
    Initializer method
        PARAMETERS:
            - the parent Tkinter object
            - the Newsletter object to be sent
    '''
    def __init__(self, parent, newsletter):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.newsletter = newsletter
        self.initialize()
        
    '''
    initialize()
    Creates all the different entry fields and buttons, and creates bindings
        PARAMETERS:
            - none
        RETURNS:
            - nothing
    '''
    def initialize(self):
        
        self.label_username = ttk.Label(self, text = "Username:")
        self.entry_username = ttk.Entry(self, textvariable = tk.StringVar())
        
        self.label_password = ttk.Label(self, text = "Password:")
        self.entry_password = ttk.Entry(self, textvariable = tk.StringVar(), show = "*")
        
        self.text_button_send = tk.StringVar()
        self.text_button_send.set("Send")
        self.button_send = ttk.Button(self, textvariable = self.text_button_send, command = self.send)
        self.button_close  = ttk.Button(self, text = "Close", command = self.destroy)
        
        self.setup_grid()
        
        self.bind('<Control-w>', self.quit)
        self.bind('<Up>', self.press_up)
        self.bind('<Down>', self.press_down)
        
        self.widgets = [self.entry_username, self.entry_password, self.button_send, self.button_close]
        for widget in self.widgets:
            widget.bind("<Return>", self.press_enter)
        
    '''
    setup_grid()
    places all the different widgets into the window
        PARAMETERS:
            - none
        RETURNS:
            - nothing
    '''
    def setup_grid(self):
        self.grid()
        self.label_username.grid(row = 0, column = 0, sticky = tk.E)
        self.entry_username.grid(row = 0, column = 1, columnspan = 2, padx = 10, pady = 10)
        self.label_password.grid(row = 1, column = 0, sticky = tk.E)
        self.entry_password.grid(row = 1, column = 1, columnspan = 2, padx = 10, pady = 10)
        self.button_send.grid(row = 2, column = 0, columnspan = 2, padx = 10, pady = 10)
        self.button_close.grid(row = 2, column = 2, padx = 10, pady = 10)
        
    '''
    press_up()
    Handles an up-arrow press
        PARAMETERS:
            - the event object given by the bind-command
        RETURNS:
            - nothing
    '''
    def press_up(self, event = None):
        event.widget.tk_focusPrev().focus()
        
    '''
    press_down()
    Handles a down-arrow press
        PARAMETERS:
            - the event object given by the bind-command
        RETURNS:
            - nothing
    '''
    def press_down(self, event = None):
        event.widget.tk_focusNext().focus()
        
        '''
    press_enter()
    Handles an 'enter' press
        PARAMETERS:
            - the event object given by the bind-command
        RETURNS:
            - nothing
    '''
    def press_enter(self, event = None):
        if event.widget in [self.button_send,self.entry_password]:
            self.send()
        elif event.widget == self.button_close:
            self.button_close.invoke()
    
    '''
    send()
    Handles the sending of the newsletter via an SMTP TLS connection. Currently
    it only snds mail through the mail.aalto.fi port.
        PARAMETERS:
            - none
        RETURNS:
            - nothing
    '''
    def send(self):
        #Change the button message to give feedback to user
        self.text_button_send.set("Sending...")
        self.button_send.update()
        
        #Fetch the file to send
        active_folderpath = get_active_folderpath(self.newsletter.get_newsletter_type())
        MIME_version_filename = os.getcwd() + active_folderpath + "MIME_version.eml"
        try:
            with open(MIME_version_filename) as MIME_version_file:
                msg = email.message_from_file(MIME_version_file)
                server = smtplib.SMTP()
                success = False
        except EnvironmentError as e:
            messagebox.showerror("Failed to send mail", e)
            self.quit()
            
        
        try:
            self.text_button_send.set("Getting connection with server...")
            self.button_send.update()

            #Fetch a connection with the server
            server = smtplib.SMTP('mail.aalto.fi', 587)
            server.ehlo()

            # If we can encrypt this session, do it
            if server.has_extn('STARTTLS'):
                server.starttls()
                server.ehlo() # re-identify ourselves over TLS connection

            self.text_button_send.set("Logging in...")
            self.button_send.update()
                
            #login    
            server.login(self.entry_username.get(), self.entry_password.get())
			
            self.text_button_send.set("Sending message...")
            self.button_send.update()
            
            #send the message
            server.sendmail(msg.get("From"), msg.get("To").split(","), msg.as_string())

            self.text_button_send.set("Archiving...")
            self.button_send.update()

            self.text_button_send.set("Closing connection...")
            self.button_send.update()
            
            #after a successful send, archive the active files
            archive_files(self.newsletter, os.getcwd() + active_folderpath)
            
            server.close()
            
            #Give user feedback
            messagebox.showinfo("Message sent", "The message was sent successfully!") 
            success = True
        except Exception as exc:
            #In case of failure, give error message
            messagebox.showerror("Failed to send mail", exc)
            server.close()
            self.quit()
        finally:
            #If the mail was sent successfully, close the entire program
            if success:
                self.parent.quit()
                
    '''
    quit()
    Destroys the subwindow
        PAREMETERS:
            - none
        RETURNS:
            - nothing
    '''
    def quit(self, event = None):
        self.destroy()
