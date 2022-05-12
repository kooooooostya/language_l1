import time
from tkinter import *
from tkinter.filedialog import askopenfilename

from dictionary_helper import DictionaryHelper
from striprtf.striprtf import rtf_to_text

root = Tk()

txt = StringVar()
res = StringVar()

Tk().withdraw()


def choose_file():
    filename = askopenfilename()

    # reading txt rtf files
    text = ""
    if filename.__contains__("rtf"):
        with open(filename) as infile:
            content = infile.read()
            text = rtf_to_text(content)
        print(text)
    else:
        f = open(filename, "r")
        text = f.read()
        print(text)

    start_time = time.time()
    handler = DictionaryHelper(text)
    content = handler.get_full_dictionary_string()
    res.set(res.get() + "\n" + content)
    print("--- %s seconds ---" % (time.time() - start_time))


def open_file():
    filename = askopenfilename()

    # reading txt rtf files
    text = ""
    if filename.__contains__("lang"):
        with open(filename) as infile:
            content = infile.read()
            res.set(content)
        print(text)


def write_file():
    with open('C:/Users/Mi Book/Desktop/lang_l1.lang', 'w') as f:
        f.write(res.get())


root.title("Sentence analyzer")
root.geometry("900x600")

choose_file_button = Button(text="Choose file", command=choose_file)
choose_file_button.place(relx=.5, rely=.1, anchor="c")

open_file_button = Button(text="Open file", command=open_file)
open_file_button.place(relx=.8, rely=.1, anchor="c")

save_file_button = Button(text="Save file", command=write_file)
save_file_button.place(relx=.2, rely=.1, anchor="c")


resultlabel = Label(textvariable=res, justify=LEFT)
resultlabel.place(relx=.5, rely=.2, anchor="n")

root.mainloop()
