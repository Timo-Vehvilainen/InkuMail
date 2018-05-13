#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from code.mainWindow import MainWindow
import os

def main():
    window = MainWindow(None)
    window.title("InkuMail 1.0")
    window.minsize(width = "590", height = "400")
    window.mainloop()
    
main()
