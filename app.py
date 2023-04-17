import tkinter as tk #Libreria grafica
from tkinter import filedialog
from UpVid import UpVid

def openFile(input):
    ruta = filedialog.askdirectory(initialdir = '/', title= 'Seleccione una carpeta')
    input.insert(0, ruta)
    #print(ruta)

def saveSettings():
    #botonSaveAll.config(state='disabled') desactivamos el boton
    ob = UpVid()
    ruta = input.get()
    print(f'Esta es la ruta {ruta}')
    ob.setDir(ruta)
    ob.main()

app = tk.Tk() # instanciacion
app.geometry('500x200') # Configuracion dimensiones
app.configure()

tk.Wm.wm_title(app, "Vid Uploads - Youtube")

etiquetaUser = tk.Label(app)

etiquetaUser.pack()
etiquetaRuta = tk.Label(app, 
                        text='Seleccione ruta de respaldo',
                        font=('Helvetica',14))
""" etiquetaRuta.grid(row=0, column=1) """
etiquetaRuta.pack(padx = 2, pady=2)

input = tk.Entry(app)
input.pack()

boton = tk.Button(app, text='Escoger carpeta', command= lambda: openFile(input))
boton.pack()

botonSaveAll = tk.Button(app, text='Guardar!', command= saveSettings)
botonSaveAll.pack()

app.mainloop()# Ejecucion de la ventana