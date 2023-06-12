#!/usr/bin/python3
import os
import time
import PyPDF2
import gtts
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pygame
from tkinter import ttk
from PIL import  ImageTk, Image # Image,
from tkdocviewer import *
#print(os.getcwd())
audio_path = 'archivo_de_audiof.mp3'
def convertir_a_audio():
    # Obtener la ruta del archivo PDF seleccionado
    global pdf_path
    pdf_path = filedialog.askopenfilename(filetypes=[("Archivos PDF", "*.pdf")])

    if (pdf_path) and (os.path.getsize(pdf_path) <=6000000):
        try:
            # Extraer texto del PDF
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
            #print(text)
        
            # Obtener el idioma seleccionado
            language = idiomas_codigos[combo_idiomas.get()]
            #print(idiomas_codigos)
            #print(type(language))

            # Crear objeto de conversión de texto a voz
            audio = gtts.gTTS(text=text, lang=language, slow=slow_audio_speed)
            time.sleep(10)
            audio_info = pygame.mixer.Sound(audio_path)
            duration = audio_info.get_length()
            #print(audio)
            
            # Guardar archivo de audio
            print('si')
            time.sleep(2)
            audio.save(audio_path)
            print('n')

            # Reproducir archivo de audio con pygame
            #pygame.init()
            #pygame.mixer.init()
            #pygame.mixer.music.load(audio_path)
            #pygame.mixer.music.play(1)
            

            # Actualizar los controles de reproducción
            #btn_reproducir.config(state=tk.NORMAL)
            #btn_pause.config(state=tk.NORMAL)
            #btn_resume.config(state=tk.DISABLED)

            # Obtener la duración del archivo de audio

            # Iniciar la barra de progreso
            progress_bar.config(maximum=duration)
            actualizar_barra_progreso()
            print('listo')

            messagebox.showinfo("Éxito", "La conversión se ha completado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error durante la conversión: {str(e)}")
    else:
        messagebox.showwarning("Advertencia", "No se ha seleccionado ningún archivo PDF o Tu archivo es muy pesado.")
    

#def actualizar_barra_progreso():
#    current_time = pygame.mixer.music.get_pos() / 1000  # Obtener el tiempo actual en segundos
#    progress_bar.config(value=current_time)
#    if pygame.mixer.music.get_busy():
#        window.after(1000, actualizar_barra_progreso)  # Actualizar la barra cada segundo
def actualizar_barra_progreso():
    current_time = pygame.mixer.music.get_pos() / 1000#Obtener el tiempo actual en segundos
    style = ttk.Style()
    style.configure('my.Progressbar', troughcolor='black', bordercolor='white', foreground='white', relief='flat')
    progress_bar.config(value=current_time,style='my.Progressbar')
    if pygame.mixer.music.get_busy():
	    window.after(1000, actualizar_barra_progreso)#Actualizar la barra cada segundo

def pausar_reproduccion():
    pygame.mixer.music.pause()
    btn_pause.config(state=tk.DISABLED)
    btn_resume.config(state=tk.NORMAL)
    btn_reproducir.config(state=tk.NORMAL)

def reanudar_reproduccion():
    pygame.mixer.music.unpause()
    btn_pause.config(state=tk.NORMAL)
    btn_resume.config(state=tk.DISABLED)
    btn_reproducir.config(state=tk.NORMAL)

def iniciar_reproduccion():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()
    btn_pause.config(state=tk.NORMAL)
    btn_resume.config(state=tk.DISABLED)
def visualizador_pdf():
    if not hasattr(visualizador_pdf, 'v') or visualizador_pdf.v is None:
        visualizador_pdf.v = DocViewer(ventana_secundaria)
        visualizador_pdf.v.place(x=250, y=150, height=500, width=550)
    # Display some document
        visualizador_pdf.v.display_file(pdf_path)
        btn_viewer.config(text='Regresame al Inicio')
    else:
    # Close the viewer
        visualizador_pdf.v.pack_forget()
        visualizador_pdf.v = None
        btn_viewer.config(text='Visualizar')
    
    
    


def destroy():
    try:
       os.remove(audio_path)
       print("El archivo se ha eliminado con éxito.")   
    except FileNotFoundError:
       print("El archivo no existe:.")
    pygame.mixer.quit()

def funcion():
    if (pdf_path) and (os.path.getsize(pdf_path) <= 6000000):
        global btn_reproducir
        global btn_pause
        global btn_resume
        global ventana_secundaria
        global btn_viewer
        ventana_secundaria = tk.Toplevel()
        ventana_secundaria.configure(bg='blue')
        ventana_secundaria.geometry('1000x1000')
        ventana_secundaria.title("Reproductor")
        ventana_secundaria.config(width=1000, height=1000)

        # Establecer la imagen "v1.jpg" como fondo usando un Canvas
        canvas = tk.Canvas(ventana_secundaria, width=ventana_secundaria.winfo_screenwidth(), height=ventana_secundaria.winfo_screenheight(),highlightthickness=0)
        canvas.pack()

        background_image = Image.open('/home/sistemas/projects/temporal_pdf/app/images/v6.jpg')
        background_image = background_image.resize((ventana_secundaria.winfo_screenwidth(), ventana_secundaria.winfo_screenheight()))
        background = ImageTk.PhotoImage(background_image)

        canvas.create_image(0, 0, anchor='nw', image=background)

    
         #Cargar las imágenes de los botones "Pausar" y "Reanudar"
        pausar_image = ImageTk.PhotoImage(file="/home/sistemas/projects/temporal_pdf/app/images/pause.jpeg")
        reanudar_image = ImageTk.PhotoImage(file="/home/sistemas/projects/temporal_pdf/app/images/r.png")
        play_image = ImageTk.PhotoImage(file="/home/sistemas/projects/temporal_pdf/app/images/play.jpeg")
        home_image = ImageTk.PhotoImage(file="/home/sistemas/projects/temporal_pdf/app/images/home.jpeg")

	

        btn_reproducir = tk.Button(ventana_secundaria,image=play_image,state=tk.NORMAL ,command=iniciar_reproduccion, bd=1)
        btn_reproducir.place(x=300, y=0)

        btn_pause = tk.Button(ventana_secundaria,image=pausar_image,state=tk.NORMAL ,command=pausar_reproduccion,bd=2)
        btn_pause.place(x=350, y=0)

        btn_resume = tk.Button(ventana_secundaria, image=reanudar_image,state=tk.DISABLED ,command=reanudar_reproduccion,bd=3)
        btn_resume.place(x=400, y=0)

        btn_viewer = tk.Button(ventana_secundaria,text='view',state=tk.NORMAL, command=visualizador_pdf,bd=4)
        btn_viewer.place(x=800, y=0)

        btn_destroy = tk.Button(ventana_secundaria,text='go back',image=home_image,state =tk.NORMAL ,command=lambda:[destroy(),ventana_secundaria.destroy()])
        btn_destroy.place(x=600, y=0)

        btn_reproducir.config(state=tk.NORMAL)
        btn_pause.config(state=tk.NORMAL)
        btn_resume.config(state=tk.NORMAL)
        ventana_secundaria.mainloop()


# Diccionario de idiomas
idiomas = {
    'es': 'Español',
    'en': 'Inglés',
    'fr': 'Francés',
    'pt': 'Portugués',
    'zh': 'Chino',
    'it': 'Italiano'
}

# Configuración de la velocidad de reproducción
slow_audio_speed = False  # Cambiar a False para una velocidad más rápida

# Crear la ventana de la interfaz
window = tk.Tk()
window.title("Conversor de PDF a Audio")
window.configure(bg='white')

#Subir imagen de logo
print("aaaa")

image = Image.open('/home/sistemas/projects/temporal_pdf/app/images/logo.jpeg')
logo_image_path = ImageTk.PhotoImage(image)
#logo_image = ImageTk.PhotoImage(file='images/logo.jpeg') 
#image = Image.open('images/logo.jpeg')
#print("aaab")
label_title = tk.Label(window, image=logo_image_path,bg='red')
label_title.pack(pady=20)


# Agregar una lista desplegable de idiomas con nombres completos
idiomas_codigos = {v: k for k, v in idiomas.items()}  # Invertir el diccionario para obtener los códigos de idioma
combo_idiomas = ttk.Combobox(window, values=list(idiomas.values()))
combo_idiomas.current(0)  # Establecer el idioma predeterminado
combo_idiomas.pack(pady=10)

#Cargar la imagen del botón "Subir PDF"
subir_pdf_image = ImageTk.PhotoImage(file="/home/sistemas/projects/temporal_pdf/app/images/subir_pdf.jpeg")

# Agregar un botón para seleccionar el archivo PDF y realizar la conversión
btn_convertir = tk.Button(window,image=subir_pdf_image ,text="Seleccionar PDF", command=lambda:[convertir_a_audio(),funcion()])#convertir_a_audio()
btn_convertir.pack(pady=10)
#Agregar una barra de progreso para mostrar el avance de la reproducción
progress_bar = ttk.Progressbar(window, orient='horizontal', mode='determinate')
progress_bar.pack(pady=10)

canvas = tk.Canvas(window, width=window.winfo_screenwidth(), height=window.winfo_screenheight(),highlightthickness=0)
canvas.pack()

background_image = Image.open('/home/sistemas/projects/temporal_pdf/app/images/v11.jpg')
background_image = background_image.resize((window.winfo_screenwidth(), window.winfo_screenheight()))
background = ImageTk.PhotoImage(background_image)

canvas.create_image(0, 0, anchor='nw', image=background)









#Agregar un bóton para iniciar la reproducción
#btn_reproducir = tk.Button(ventana_secundaria, text="Reproducir", state=tk.NORMAL, command=iniciar_reproduccion)
#btn_reproducir.pack(pady=10)
# Agregar botones para pausar y reanudar la reproducción
#btn_pause = tk.Button(ventana_secundaria, text="Pausar", state=tk.DISABLED, command=pausar_reproduccion)
#btn_pause.pack(pady=10)

#btn_resume = tk.Button(ventana_secundaria, text="Reanudar", state=tk.DISABLED, command=reanudar_reproduccion)
#btn_resume.pack(pady=10)



# Ejecutar la interfaz
window.mainloop()