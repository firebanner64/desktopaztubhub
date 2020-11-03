import aiohttp
import json
import asyncio
import tkinter
import tkinter.filedialog




class gui(tkinter.Frame):

    def __init__(self, parent):   
        super().__init__(parent)

        self.AddMemes = tkinter.BooleanVar()
        tkinter.Checkbutton(self, text='Add memes', var=self.AddMemes).pack()

        self.PreserveLineInfo = tkinter.BooleanVar()
        tkinter.Checkbutton(self, text='Preserve Line Info (Debug)', var=self.PreserveLineInfo).pack()

        self.NoControlFlow = tkinter.BooleanVar()
        tkinter.Checkbutton(self, text='No Control Flow', var=self.NoControlFlow).pack()

        self.EncryptAllStrings = tkinter.BooleanVar()
        tkinter.Checkbutton(self, text='Encrypt All Strings', var=self.EncryptAllStrings).pack()

        self.EncryptImportantStrings = tkinter.BooleanVar()
        tkinter.Checkbutton(self, text='Encrypt Important Strings', var=self.EncryptImportantStrings).pack()

        self.NoBytecodeCompress = tkinter.BooleanVar()
        tkinter.Checkbutton(self, text='No Bytecode Compress',  var=self.NoBytecodeCompress).pack()

        self.Uglify = tkinter.BooleanVar()
        tkinter.Checkbutton(self, text='Uglify', var=self.Uglify).pack()

        self.entry = tkinter.Text(self, width=60, height=20)
        self.entry.pack(side=tkinter.LEFT)

        tkinter.Button(self, command=self.file_dialog_handler,text='Open File').pack(side='right')

        tkinter.Button(self, command=self.obfuscate_init,text='Obfuscate').pack(side='right')

    def get_text(self):
        return self.entry.get(1.0, tkinter.END)
    
    def set_text(self, new_text):
        self.entry.delete(1.0,tkinter.END)
        self.entry.insert(tkinter.END, new_text)
    
    def file_dialog_handler(self):
        script_directory = tkinter.filedialog.askopenfilename(initialdir = "/",title = "Select script", filetypes=(("Text files",".txt"),))

        self.set_text(open(script_directory, mode='r').read())
    
    def obfuscate_init(self):
        asyncio.run(self.obfuscate())
    
    async def obfuscate(self):
        text = self.get_text()
        data = {'script':text, "options":{"AddMemes":bool(self.AddMemes),"PreserveLineInfo":bool(self.PreserveLineInfo),"NoControlFlow":bool(self.NoControlFlow),"EncryptStrings":bool(self.EncryptAllStrings),"EncryptImportantStrings":bool(self.EncryptImportantStrings),"NoBytecodeCompress":bool(self.NoBytecodeCompress),"Uglify":bool(self.Uglify)}}

        async with aiohttp.ClientSession().post('https://obfuscator.aztupscripts.xyz/api/v1/obfuscate', json=data) as response:
            response_json = await response.json()
        

        try:
            self.set_text(response_json['script'])
        except:
            try:
                self.set_text(response_json['message'])
            except:
                try:
                    self.set_text(response_json['error'])
                except:
                    pass
    


if __name__ == '__main__':
    root = tkinter.Tk()
    application = gui(root).pack(side='top',fill='both',expand=True)
    root.mainloop()