import tkinter as tk
import threading
import requests
import pyxdelta
import os
from os import path
import py7zr
import zipfile

INSTALL_PATH = path.join(os.getcwd(), 'OnlineCTR')

def download_file(url, path, output_object):
    message = output_object['text']

    res = requests.get(url, stream=True)

    # Obtén el tamaño total del archivo
    total_size = int(res.headers.get('content-length', 0))

    # Inicializa una variable para llevar la cuenta de los datos descargados hasta ahora
    downloaded_size = 0

    with open(path, 'wb') as file:
        for chunk in res.iter_content(chunk_size=1024):
            if chunk:
                downloaded_size += len(chunk)

                percent = downloaded_size / total_size * 100

                output_object.config(text=f'{message} ({int(percent)}%)')

                file.write(chunk)

def install(framerate, output, fps30button, fps60button, duck_checkbox_value):
    try:
        fps30button.config(state=tk.DISABLED)
        fps60button.config(state=tk.DISABLED)
        duck_checkbox.config(state=tk.DISABLED)

        # rom verification and download

        ROM_PATH = path.join(INSTALL_PATH, 'ctr.bin')

        if not path.exists(ROM_PATH):
            output.config(text=f'No se encontró la ROM del CTR. Descargándola...')

            if not path.exists(INSTALL_PATH):
                os.mkdir(INSTALL_PATH)

            ZIPPED_ROM_PATH = path.join(INSTALL_PATH, 'ctr.7z')
            download_file('https://drive.usercontent.google.com/download?id=1HePT1AUTv-UUYhyl3n12xaVRxiZqgKzM&export=download&authuser=0&confirm=t&uuid=d566728c-bcfb-4fd9-bd5e-fa28eda20cc5&at=APZUnTXueQvUe7SoI5QAOZwvZ_uL%3A1721740758809', ZIPPED_ROM_PATH, output)

            output.config(text=f'Extrayendo la ROM comprimida...')

            archive = py7zr.SevenZipFile(ZIPPED_ROM_PATH, mode='r')
            archive.extractall(path=INSTALL_PATH)
            archive.close()

            os.remove(path.join(INSTALL_PATH, 'ctr.7z'))
        else:
            output.config(text=f'Ya tiene la ROM del CTR. Se omitirá su instalación...')

        # downloading patch and applying it to the rom

        output.config(text=f'Descargando el parche...')

        PATCH_PATH = path.join(INSTALL_PATH, f'ctr-u_Online{framerate}.xdelta')
        download_file(f'https://online-ctr.com/wp-content/uploads/onlinectr_patches/ctr-u_Online{framerate}.xdelta', PATCH_PATH, output)

        if path.exists(path.join(INSTALL_PATH, 'OnlineCTR.bin')):
            os.remove(path.join(INSTALL_PATH, 'OnlineCTR.bin'))

        output.config(text=f'Parcheando la ROM...')
        pyxdelta.decode(ROM_PATH, PATCH_PATH, path.join(INSTALL_PATH, 'OnlineCTR.bin'))

        os.remove(path.join(INSTALL_PATH, path.join(INSTALL_PATH, f'ctr-u_Online{framerate}.xdelta')))

        # downloading client

        output.config(text=f'Descargando el cliente...')

        CLIENT_PATH = path.join(INSTALL_PATH, 'client.zip')
        download_file('https://online-ctr.com/wp-content/uploads/onlinectr_patches/client.zip', CLIENT_PATH, output)

        output.config(text=f'Extrayendo el cliente comprimido...')

        archive = zipfile.ZipFile(CLIENT_PATH, 'r')
        archive.extractall(path=INSTALL_PATH)
        archive.close()

        os.remove(CLIENT_PATH)

        # downloading config file

        output.config(text=f'Descargando la configuración del juego...')

        GAMESETTINGS_PATH = path.expanduser(path.join('~', 'Documents', 'DuckStation', 'gamesettings'))
        CONFIG_PATH = path.join(GAMESETTINGS_PATH, 'SCUS-94426.ini')

        if not path.exists(GAMESETTINGS_PATH):
            os.makedirs(GAMESETTINGS_PATH)

        if path.exists(CONFIG_PATH):
            os.remove(CONFIG_PATH)

        download_file('https://online-ctr.com/wp-content/uploads/onlinectr_patches/SCUS-94426.ini', CONFIG_PATH, output)

        # duckstation installation

        if duck_checkbox_value.get() == 1:
            output.config(text=f'Descargando DuckStation...')

            DUCKSTATION_PATH = path.join(INSTALL_PATH, 'duck.zip')
            download_file('https://github.com/stenzek/duckstation/releases/download/latest/duckstation-windows-x64-release.zip', DUCKSTATION_PATH, output)

            output.config(text=f'Extrayendo DuckStation...')

            archive = zipfile.ZipFile(DUCKSTATION_PATH, 'r')
            archive.extractall(path=path.join(INSTALL_PATH, 'duckstation'))
            archive.close()

            os.remove(DUCKSTATION_PATH)

        output.config(text=f'OnlineCTR se ha instalado correctamente. Cierra esta ventana para salir.')
    except Exception as e:
        output.config(text=f'Ocurrió un {type(e).__name__}. Cierra esta ventana para salir.', foreground='#e06c75')

root = tk.Tk()

root.title('OnlineCTR Installer')
root.configure(
    background='#030712'
)
root.geometry('720x480')
root.resizable(False, False)

heading = tk.Label(root, text='OnlineCTR Installer', font=('', 32, 'bold'), foreground='#e5c07b', background='#030712')
heading.place(relx=0.5, rely=0.34, anchor='center')

question = tk.Label(root, text='¿Qué versión quieres instalar?', font=('', 16, 'bold'), foreground='#ffffff', background='#030712')
question.place(relx=0.5, rely=0.42, anchor='center')

fpsButtonImage = tk.PhotoImage(file="style/fpsButton.png") 
fpsButtonHoverImage = tk.PhotoImage(file="style/fpsButtonHover.png") 
 
fps30button = tk.Button(root, text='30 FPS', command=lambda: threading.Thread(target=install, args=('30', output, fps30button, fps60button, duck_checkbox_value)).start(), image=fpsButtonImage, width=104, height=42, background='#030712', foreground='#000000', highlightthickness = 0, bd = 0, activebackground='#030712', font=('', 16, 'bold'), compound="center")
fps30button.bind("<Enter>", lambda _: fps30button.config(image=fpsButtonHoverImage))
fps30button.bind("<Leave>", lambda _: fps30button.config(image=fpsButtonImage))
fps30button.place(relx=0.40, rely=0.55, anchor='center')  
 
fps60button = tk.Button(root, text='60 FPS', command=lambda: threading.Thread(target=install, args=('60', output, fps30button, fps60button, duck_checkbox_value)).start(), image=fpsButtonImage, width=104, height=42, background='#030712', foreground='#000000', highlightthickness = 0, bd = 0, activebackground='#030712', font=('', 16, 'bold'), compound="center")
fps60button.bind("<Enter>", lambda _: fps60button.config(image=fpsButtonHoverImage))
fps60button.bind("<Leave>", lambda _: fps60button.config(image=fpsButtonImage))
fps60button.place(relx=0.60, rely=0.55, anchor='center') 

duck_checkbox_value = tk.IntVar()
duck_checkbox = tk.Checkbutton(root, text='Instalar también DuckStation', variable=duck_checkbox_value, background='#030712', foreground='#ffffff', highlightthickness = 0, bd = 0, activebackground='#030712', activeforeground='#ffffff', selectcolor='#030712', font=('', 11, 'bold'))
duck_checkbox.place(relx=0.5, rely=0.66, anchor='center')

output = tk.Label(root, text='', font=('', 14, 'bold'), foreground='#98c379', background='#030712')
output.place(relx=0.5, rely=0.80, anchor='center')

root.mainloop()

