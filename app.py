import os
import json
import tkinter as tk  # Libreria grafica
from tkinter import filedialog
from UpVid import UpVid


class App:

    APP_PATH = os.getcwd()
    # Archivo de configuracion
    CONFG = {
        'DIRECTORIO': '/',
        'vidsToUpload': 1,
        'periodoBackup': 0
    }

    def __init__(cls):
        cls.app = tk.Tk()  # instanciacion
        cls.frameOne = tk.Frame(cls.app, borderwidth=1, relief='groove', width=380, height=200)
        cls.etiquetaUser = tk.Label(cls.app, text='User!')

        cls.etiquetaRuta = tk.Label(
            cls.frameOne, text='Seleccione ruta de respaldo', font=('Times New Roman', 10))

        cls.varStringInputDir = tk.StringVar()
        cls.input = tk.Entry(cls.frameOne)
        cls.botonOpenDir = tk.Button(cls.frameOne, text='Escoger carpeta',
                                     command=lambda: cls.openFile(cls.input))
        
        cls.etiquetaRadioButtons = tk.Label(
            cls.frameOne, text='Metodo de subida', font=('Times New Roman', 10))
        cls.radioGroupValue = tk.IntVar()
        cls.radioButton = tk.Radiobutton(cls.frameOne)
        cls.radioButton1 = tk.Radiobutton(cls.frameOne)
        
        cls.etiquetaPeriodoRespaldo = tk.Label(
            cls.frameOne, text='Respaldar cada:', font=('Times New Roman', 10))
        cls.inputPeriodo = tk.Entry(cls.frameOne)
        cls.etiquetaPeriodoRespaldo_ = tk.Label(
            cls.frameOne, text=' horas', font=('Times New Roman', 10))

        cls.botonSaveAll = tk.Button(
            cls.app, text='Guardar configuración', command=cls.saveSettings)
        cls.botonEdit = tk.Button(
            cls.app, text='Editar configuración', command=cls.editSettings)
        
        cls.botonStart = tk.Button(text='Start!', command=cls.startUpload)

    def getSettings(cls):
        if not os.path.exists('confg.json'):
            with open(os.path.join(cls.APP_PATH, 'confg.json'), 'w') as confg:
                json.dump(cls.CONFG, confg)
        else:
            with open(os.path.join(cls.APP_PATH, 'confg.json'), 'r') as confg:
                cls.CONFG = json.load(confg)
                print('aqui entro')

    def openFile(cls, input):
        input.delete(0, tk.END)
        ruta = filedialog.askdirectory(
            initialdir='/', title='Seleccione una carpeta')
        cls.varStringInputDir.set(ruta)
        # print(ruta)

    def saveSettings(cls):
        ruta = cls.input.get()
        valorRadio = cls.radioGroupValue.get()
        print(f'Esta es la ruta {ruta}')
        if ruta == '':
            print('ruta no puede ser vacia')
            return
        with open(os.path.join(cls.APP_PATH, 'confg.json'), 'r') as confg:
            cls.CONFG = json.load(confg)
            cls.CONFG['DIRECTORIO'] = ruta
            cls.CONFG['vidsToUpload'] = valorRadio
        with open(os.path.join(cls.APP_PATH, 'confg.json'), 'w') as confg:
            json.dump(cls.CONFG, confg)
        # deshabilitamos botones
        cls.radioButton.config(state='disabled')
        cls.radioButton1.config(state='disabled')
        cls.botonOpenDir.config(state='disabled')
        cls.botonSaveAll.config(state='disabled')
        cls.inputPeriodo.config(state='disabled')
        cls.botonEdit.config(state='normal')
        cls.botonStart.config(state='normal')
        
        # ob.main()

    def editSettings(cls):
        cls.botonEdit.config(state='disabled')
        # habilitar botones
        cls.botonOpenDir.config(state='active')
        cls.radioButton.config(state='normal')
        cls.radioButton1.config(state='normal')
        cls.botonOpenDir.config(state='normal')
        cls.botonSaveAll.config(state='normal')
        cls.inputPeriodo.config(state='normal')


    def startUpload(cls):
        ob = UpVid()
        ob.setSettings(cls.CONFG['DIRECTORIO'])
        ob.main()


    def setInstances(cls):
        cls.app.geometry('400x350')  # Configuracion dimensiones
        cls.app.configure()
        tk.Wm.wm_title(cls.app, "Vid Uploads - Youtube")
        #cls.frameOne.configure(width=480,height=100)
        cls.etiquetaUser.pack()
        cls.frameOne.pack()

        cls.etiquetaRuta.pack(padx=2, pady=2)

        ruta_default = cls.CONFG['DIRECTORIO'] if len(
            cls.CONFG['DIRECTORIO']) > 0 else '/'
        cls.varStringInputDir.set(ruta_default)
        cls.input.config(state='disabled', textvariable=cls.varStringInputDir)
        cls.input.configure(width=50)
        cls.input.pack()
        cls.botonOpenDir.config(state='disabled')
        cls.botonOpenDir.pack()

        cls.etiquetaRadioButtons.pack()
        vidsToUpload = cls.CONFG['vidsToUpload']
        cls.radioGroupValue.set(vidsToUpload)
        cls.radioButton.config(state='disabled',text='Vids actuales', variable=cls.radioGroupValue, value=1)
        cls.radioButton1.config(state='disabled',text='Todos', variable=cls.radioGroupValue, value=2)
        cls.radioButton.pack()
        cls.radioButton1.pack()

        cls.etiquetaPeriodoRespaldo.pack()
        cls.inputPeriodo.config(state='disabled')
        cls.inputPeriodo.configure(width=5)
        cls.inputPeriodo.pack()
        cls.etiquetaPeriodoRespaldo_.pack()

        cls.botonSaveAll.config(state='disabled')
        cls.botonSaveAll.pack()

        cls.botonEdit.pack()

        cls.botonStart.pack()

    def main(cls):
        cls.getSettings()
        cls.setInstances()
        cls.app.mainloop()


app = App()
app.main()
# Ejecucion de la ventana