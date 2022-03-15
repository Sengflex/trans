import sys

from googletrans import LANGUAGES as AvailableLangs
from googletrans import Translator
from tkinter import Tk, messagebox
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk


# Thanks to sloth at stackoverflow.com
# Font: https://stackoverflow.com/questions/12298159/tkinter-how-to-create-a-combo-box-with-autocompletion
class AutocompleteCombobox(ttk.Combobox):

        def set_completion_list(self, completion_list):
                """Use our completion list as our drop down selection menu, arrows move through menu."""
                self._completion_list = sorted(completion_list, key=str.lower) # Work with a sorted list
                self._hits = []
                self._hit_index = 0
                self.position = 0
                self.bind('<KeyRelease>', self.handle_keyrelease)
                self['values'] = self._completion_list  # Setup our popup menu

        def autocomplete(self, delta=0):
                """autocomplete the Combobox, delta may be 0/1/-1 to cycle through possible hits"""
                if delta: # need to delete selection otherwise we would fix the current position
                        self.delete(self.position, tk.END)
                else: # set position to end so selection starts where textentry ended
                        self.position = len(self.get())
                # collect hits
                _hits = []
                for element in self._completion_list:
                        if element.lower().startswith(self.get().lower()): # Match case insensitively
                                _hits.append(element)
                # if we have a new hit list, keep this in mind
                if _hits != self._hits:
                        self._hit_index = 0
                        self._hits=_hits
                # only allow cycling if we are in a known hit list
                if _hits == self._hits and self._hits:
                        self._hit_index = (self._hit_index + delta) % len(self._hits)
                # now finally perform the auto completion
                if self._hits:
                        self.delete(0,tk.END)
                        self.insert(0,self._hits[self._hit_index])
                        self.select_range(self.position,tk.END)

        def handle_keyrelease(self, event):
                """event handler for the keyrelease event on this widget"""
                if event.keysym == "BackSpace":
                        self.delete(self.index(tk.INSERT), tk.END)
                        self.position = self.index(tk.END)
                if event.keysym == "Left":
                        if self.position < self.index(tk.END): # delete the selection
                                self.delete(self.position, tk.END)
                        else:
                                self.position = self.position-1 # delete one character
                                self.delete(self.position, tk.END)
                if event.keysym == "Right":
                        self.position = self.index(tk.END) # go to end (no selection)
                if len(event.keysym) == 1:
                        self.autocomplete()
                # No need for up/down, we'll jump to the popup
                # list at the position of the autocompletion

def GUITranslate(translator):
    root = tk.Tk()
    root.title("Tk Tranalator - By Paioniu")
    root.iconbitmap('trans.ico')
    root.geometry("600x380")
   
    def translateIt():    
        Dest=dest_lang_combo.get().split(',')[1]  
        
        if Dest == '':
            Dest = 'en'

        to = translator.translate(in_text.get('1.0', tk.END), dest=Dest, src='auto')
        out_text.delete('1.0', tk.END)
        out_text.insert(tk.INSERT, to.text)
     
    # Input Text 
    in_text_label = tk.Label(root, text = 'Text to translate', font=('calibre',10, 'bold'))
    
    in_text = scrolledtext.ScrolledText(root, 
                                      wrap = tk.WORD, 
                                      width = 40, 
                                      height = 6, 
                                      font = ("calibre",
                                              15))                                              
    
    out_text_label = tk.Label(root, text = 'Translated text', font=('calibre',10, 'bold'))

    # Output Text 
    out_text = scrolledtext.ScrolledText(root, 
                                      wrap = tk.WORD, 
                                      width = 40, 
                                      height = 6, 
                                      font = ("calibre",
                                              15))
    
    # Destination language 
    dest_lang_label = tk.Label(root, text = 'Dest Lang', font = ('calibre',10,'bold'))
    
    alangs = []

    for alang in AvailableLangs:
        alangs.append(AvailableLangs[alang] + ',' + alang)

    dest_lang_combo = AutocompleteCombobox(root)
    dest_lang_combo.set_completion_list(alangs)
    
    # Translate button 
    trans_btn=tk.Button(root,text = 'Translate', command = translateIt)

    # Layout widgets
    in_text_label.grid(row=0,column=0)
    in_text.grid(row=0,column=1)
    dest_lang_label.grid(row=1,column=0)
    dest_lang_combo.grid(row=1,column=1)
    out_text_label.grid(row=2,column=0)
    out_text.grid(row=2,column=1)
    trans_btn.grid(row=3,column=1)

    root.mainloop()


translator = Translator()

argslen = len(sys.argv)

if argslen < 2:
    GUITranslate(translator)
    sys.exit()

Text = sys.argv[1]
Src  = None
Dest = None

if argslen > 2:
    Src = sys.argv[2]
if argslen > 3:
    Dest = sys.argv[3]

Src = Src or 'auto'
Dest = Dest or 'en'

if Src == '-':
    Src = 'auto'

to = translator.translate(Text, dest=Dest, src=Src)

messagebox.showinfo("Translation Result", to.text)
