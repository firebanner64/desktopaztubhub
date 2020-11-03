import aiohttp
import json
import asyncio
import tkinter
import tkinter.filedialog
from pyperclip import copy
class Gui(tkinter.Tk):
    def __init__(self):
        super().__init__()

        self.title("AztupBrew Client")
        self.options_menu = ObfuscationOptionsMenu(self)
        self.text_field_frame = TextFieldFrame(self, self.options_menu)
        
class ObfuscationOptionsMenu(tkinter.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.pack(side=tkinter.RIGHT, fill=tkinter.NONE, expand=tkinter.FALSE)

        self.AddMemes = tkinter.BooleanVar()
        tkinter.Checkbutton(self, text='Add memes', var=self.AddMemes).pack(anchor=tkinter.W)

        self.PreserveLineInfo = tkinter.BooleanVar()
        tkinter.Checkbutton(self, text='Preserve Line Info (Debug)', var=self.PreserveLineInfo).pack(anchor=tkinter.W)

        self.NoControlFlow = tkinter.BooleanVar()
        tkinter.Checkbutton(self, text='No Control Flow', var=self.NoControlFlow).pack(anchor=tkinter.W)

        self.EncryptAllStrings = tkinter.BooleanVar()
        tkinter.Checkbutton(self, text='Encrypt All Strings', var=self.EncryptAllStrings).pack(anchor=tkinter.W)

        self.EncryptImportantStrings = tkinter.BooleanVar()
        tkinter.Checkbutton(self, text='Encrypt Important Strings', var=self.EncryptImportantStrings).pack(anchor=tkinter.W)

        self.NoBytecodeCompress = tkinter.BooleanVar()
        tkinter.Checkbutton(self, text='No Bytecode Compress',  var=self.NoBytecodeCompress).pack(anchor=tkinter.W)

        self.Uglify = tkinter.BooleanVar()
        tkinter.Checkbutton(self, text='Uglify', var=self.Uglify).pack(anchor=tkinter.W)

        self.CustomVarName = tkinter.StringVar()
        tkinter.Entry(self).pack(anchor=tkinter.W)
        self.CustomVarName.set("Custom Variable")
    
    def get_options_state(self):

        return {"AddMemes":bool(self.AddMemes),"PreserveLineInfo":bool(self.PreserveLineInfo),"NoControlFlow":bool(self.NoControlFlow),"EncryptStrings":bool(self.EncryptAllStrings),"EncryptImportantStrings":bool(self.EncryptImportantStrings),"NoBytecodeCompress":bool(self.NoBytecodeCompress),"Uglify":bool(self.Uglify)}

    def get_custom_var(self):
        var_string = str(self.CustomVarName)
        
        if var_string not in ["Custom Variable", ""]:
            return var_string
        else:
            return False

class TextFieldFrame(tkinter.Frame):

    def __init__(self, parent, options_menu):
        super().__init__(parent)

        self.pack(side=tkinter.BOTTOM)

        self.pack(side=tkinter.LEFT)
        self.text_field = TextField(self)
        self.text_field_buttons = TextFieldButtons(self, TextFieldActions(self.text_field, options_menu))

class TextField(tkinter.Text):

    def __init__(self, parent):
        super().__init__(parent, width=60, height=20)
        self.pack()
    
    def get_text(self):
        return self.get(1.0, tkinter.END)
    
    def set_text(self, new_text):
        self.delete(1.0, tkinter.END)
        self.insert(tkinter.END, new_text)

class TextFieldButtons(tkinter.Frame):

    def __init__(self, parent, text_field_actions):
        super().__init__(parent)

        self.pack(side=tkinter.BOTTOM, anchor=tkinter.W)
        tkinter.Button(self, command=text_field_actions.obfuscate_init,text='Obfuscate').pack(side='left')
        tkinter.Button(self, text='Open file', command=text_field_actions.open_file).pack(side='left')
        tkinter.Button(self, text='Clear text', command=text_field_actions.clear_text).pack(side='left')
        tkinter.Button(self, text='Copy text', command=text_field_actions.copy_text).pack(side='left')
class TextFieldActions():

    def __init__(self, text_field: TextField, options_menu: ObfuscationOptionsMenu):
        
        self.text_field = text_field
        self.options_menu = options_menu

    def open_file(self):
        script_directory = tkinter.filedialog.askopenfilename(initialdir = "/",title = "Select script", filetypes=(("Text files",".txt .lua"),))

        try: self.text_field.set_text(open(script_directory, mode='r').read())
        except: return

    def obfuscate_init(self):
        asyncio.run(self.obfuscate())
    
    async def obfuscate(self):
        text = self.text_field.get_text()

        custom_var = self.options_menu.get_custom_var()

        if not custom_var:
            data = {'script':text, "options":self.options_menu.get_options_state()}
        else:
            data = {'script':text, "options":merge_two_dicts(self.options_menu.get_options_state(), {'CustomVarName':custom_var})}
            print('with custom var')

        async with aiohttp.ClientSession().post('https://obfuscator.aztupscripts.xyz/api/v1/obfuscate', json=data) as response:
            response_json = await response.json()

        try:
            self.text_field.set_text(response_json['script'])
        except:
            try:
                self.text_field.set_text(response_json['message'])
            except:
                try:
                    self.text_field.set_text(response_json['error'])
                except:
                    pass
        
    def clear_text(self):
        self.text_field.set_text('')
    
    def copy_text(self):
        copy(self.text_field.get_text())
        


def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

if __name__ == '__main__':
    gui = Gui()
    gui.mainloop()






    

