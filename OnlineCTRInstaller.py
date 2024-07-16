import tkinter as tk
import threading
import requests
import pyxdelta
import os
from os import path
import py7zr
import zipfile

CWD = os.getcwd()
INSTALL_PATH = path.join(CWD, 'OnlineCTR')

def install(framerate, output, fps30button, fps60button):
    try:
        fps30button.config(state=tk.DISABLED)
        fps60button.config(state=tk.DISABLED)

        ROM_PATH = path.join(INSTALL_PATH, 'ctr.bin')
        if not path.exists(ROM_PATH):
            output.config(text=f'No se encontró la ROM del CTR. Descargándola...')
            response = requests.get('https://ia601900.us.archive.org/6/items/ctr-crash-team-racing-usa-1999-ps1/CTR%20-%20Crash%20Team%20Racing%20%28USA%29.7z')

            if not path.exists(INSTALL_PATH):
                os.mkdir(INSTALL_PATH)

            ZIPPED_ROM_PATH = path.join(INSTALL_PATH, 'ctr.7z')

            file = open(ZIPPED_ROM_PATH, 'wb')
            file.write(response.content)
            file.close()

            output.config(text=f'Extrayendo la ROM comprimida...')

            archive = py7zr.SevenZipFile(ZIPPED_ROM_PATH, mode='r')
            archive.extractall(path=INSTALL_PATH)
            archive.close()

            os.remove(path.join(INSTALL_PATH, 'ctr.7z'))
            os.remove(path.join(INSTALL_PATH, 'CTR - Crash Team Racing (USA).cue'))
            os.rename(path.join(INSTALL_PATH, 'CTR - Crash Team Racing (USA).bin'), path.join(INSTALL_PATH, 'ctr.bin'))
        else:
            output.config(text=f'Ya tiene la ROM del CTR. Se omitirá su instalación...')

        output.config(text=f'Descargando el parche...')
        response = requests.get(f'https://online-ctr.com/wp-content/uploads/onlinectr_patches/ctr-u_Online{framerate}.xdelta')

        PATCH_PATH = path.join(INSTALL_PATH, f'ctr-u_Online{framerate}.xdelta')

        file = open(PATCH_PATH, 'wb')
        file.write(response.content)
        file.close()

        if path.exists(path.join(INSTALL_PATH, 'OnlineCTR.bin')):
            os.remove(path.join(INSTALL_PATH, 'OnlineCTR.bin'))

        output.config(text=f'Parcheando la ROM...')
        pyxdelta.decode(ROM_PATH, PATCH_PATH, path.join(INSTALL_PATH, 'OnlineCTR.bin'))

        os.remove(path.join(INSTALL_PATH, path.join(INSTALL_PATH, f'ctr-u_Online{framerate}.xdelta')))

        output.config(text=f'Descargando el cliente...')
        CLIENT_PATH = path.join(INSTALL_PATH, 'client.zip')

        response = requests.get('https://online-ctr.com/wp-content/uploads/onlinectr_patches/client.zip')
        
        file = open(CLIENT_PATH, 'wb')
        file.write(response.content)
        file.close()

        output.config(text=f'Extrayendo el cliente comprimido...')
        archive = zipfile.ZipFile(CLIENT_PATH, 'r')
        archive.extractall(path=INSTALL_PATH)
        archive.close()

        os.remove(CLIENT_PATH)

        output.config(text=f'Descargando la configuración del juego...')
        CONFIG_PATH = path.expanduser(path.join('~', 'Documents', 'DuckStation', 'gamesettings', 'SCUS-94426.ini'))

        if path.exists(CONFIG_PATH):
            os.remove(CONFIG_PATH)

        response = requests.get('https://online-ctr.com/wp-content/uploads/onlinectr_patches/SCUS-94426.ini')

        file = open(CONFIG_PATH, 'wb')
        file.write(response.content)
        file.close()

        output.config(text=f'OnlineCTR se ha instalado correctamente. Cierra esta ventana para salir.')
    except Exception as e:
        output.config(text=f'Ocurrió un {type(e).__name__}. Cierra esta ventana para salir.', fg='#e06c75')

root = tk.Tk()

root.title('OnlineCTR Installer')
root.configure(
    background='#030712'
)
root.geometry('720x480')
root.resizable(False, False)

heading = tk.Label(root, text='OnlineCTR Installer', font=('', 32, 'bold'), fg='#e5c07b', bg='#030712')
heading.place(relx=0.5, rely=0.32, anchor='center')

question = tk.Label(root, text='¿Qué versión quieres instalar?', font=('', 16, 'bold'), fg='#ffffff', bg='#030712')
question.place(relx=0.5, rely=0.42, anchor='center')

fps30button = tk.Button(root, text='30 FPS', command=lambda: threading.Thread(target=install, args=('30', output, fps30button, fps60button)).start(), bg='#111827', fg='#61afef', font=('', 20, 'bold'))
fps30button.place(relx=0.40, rely=0.54, anchor='center')

fps60button = tk.Button(root, text='60 FPS', command=lambda: threading.Thread(target=install, args=('60', output, fps30button, fps60button)).start(), bg='#111827', fg='#98c379', font=('', 20, 'bold'))
fps60button.place(relx=0.60, rely=0.54, anchor='center')

output = tk.Label(root, text='', font=('', 14, 'bold'), fg='#98c379', bg='#030712')
output.place(relx=0.5, rely=0.68, anchor='center')

root.mainloop()

