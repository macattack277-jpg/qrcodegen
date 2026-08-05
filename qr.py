#!/usr/bin/env python3


# That's a lot of modules
import os
from tkinter import PhotoImage as photo
from tkinter import filedialog
import tkinter as tk
import qrcode as qr
import shutil
import pyperclip



qrcodewidget = None











url = ""
# Generated QR code
def displayqr(data):


    # Make sure that there's only one QR code present at once
    global qrcodewidget
    if qrcodewidget is not None:
        qrcodewidget.destroy()


    # That's a lot of globals
    global box_size1
    global border1


    
    # Make the QR code with the extra settings
    qrcode = qr.make(data, box_size=box_size1.get(), border=border1.get())
    img = qrcode.save("/tmp/qrcode.png")
    img2 = photo(file="/tmp/qrcode.png")
    qrcodewidget = tk.Label(root, image=img2)
    qrcodewidget.pack_propagate(False)
    qrcodewidget.pack()
    qrcodewidget.image = img2


# Save the QR code
def saveqr():
    filepath = filedialog.asksaveasfilename()
    shutil.copyfile("/tmp/qrcode.png", f"{filepath}")


# Open the special settings window
def specialsettings():

    global box_size1
    global border1
    box_size2 = tk.IntVar(value=box_size1)
    border2 = tk.IntVar(value=border1)

    # Specify the window's settings
    settings_window = tk.Toplevel()
    settings_window.title("Extra Settings")
    settings_window.geometry("500x500")


    # This should make it so that the user can only input numbers ideally
    def validate_numbers(P):
        try:
            if P == "":
                return True
            float(P)
        except: return False
        return True

    vcmd = settings_window.register(validate_numbers)


    # The different settings
    box_size_label = tk.Label(settings_window, text="Box size:")
    box_size_label.pack()
    box_size_setting = tk.Entry(settings_window, validate="key", width=10, textvariable=box_size1, validatecommand=(vcmd, "%P"))
    box_size_setting.pack()
    border_label = tk.Label(settings_window, text="Border size:")
    border_label.pack()
    border_setting = tk.Entry(settings_window, validate="key", width=10, textvariable=border1, validatecommand=(vcmd, "%P"))
    border_setting.pack()


    
def clipboard():
    try:
        pyperclip.copy("/tmp/qrcode.png")
    except:
        errorlabel = tk.Label(root, text="There was an error.")
        errorlabel.pack()
    

# Remove the QR code from /tmp when closing the app
def cleanup():
    try:
        os.remove("/tmp/qrcode.png")
        root.destroy()
    except:
        root.destroy()


# Base settings for the GUI
root = tk.Tk()
root.title("QR Code Generator")
root.geometry("500x500")



# Have to put this here because otherwise it tweaks out
box_size1 = tk.IntVar(value=10)
border1 = tk.IntVar(value=4)



# Enter the URL for the QR code
databutton = tk.Entry(root, width=30)
databutton.pack()


# Button to generate the QR Code
generatebutton = tk.Button(root, text="Generate QR", font=("Arial", 16), command=lambda: displayqr(databutton.get()))
generatebutton.pack()


# Button to save the QR code
saveqrbutton = tk.Button(root, text="Save", font=("Arial", 16), command=saveqr)
saveqrbutton.pack()

# Button to open the extra settings
extrasettingsbutton = tk.Button(root, text="Extra settings", font=("Arial", 16), command=lambda: specialsettings())
extrasettingsbutton.pack()

# Button to copy to clipboard
copybutton = tk.Button(root, text="Copy to clipboard", font=("Arial", 16), command=clipboard)
copybutton.pack()





# Clean the tmp folder upon closing the program
root.protocol("WM_DELETE_WINDOW", cleanup)

root.mainloop()
