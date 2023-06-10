import os
import PyPDF2
from gtts import gTTS
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pygame
from tkinter import ttk

def convertir_a_audio():
    # Obtener la ruta del archivo PDF seleccionado
    pdf_path = filedialog.askopenfilename(filetypes=[("Archivos PDF", "*.pdf")])

    if pdf_path:
        try:
            # Extraer texto del PDF
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()

            # Obtener el idioma seleccionado
            language = idiomas_codigos[combo_idiomas.get()]

            # Crear objeto de conversión de texto a voz
            audio = gTTS(text=text, lang=language, slow=slow_audio_speed)

            # Guardar archivo de audio
            audio_path = 'archivo_de_audio.mp3'
            audio.save(audio_path)

            # Reproducir archivo de audio con pygame
            pygame.mixer.init()
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()

            # Actualizar los controles de reproducción
            btn_pause.config(state=tk.NORMAL)
            btn_resume.config(state=tk.DISABLED)

            # Obtener la duración del archivo de audio
            audio_info = pygame.mixer.Sound(audio_path)
            duration = audio_info.get_length()

            # Iniciar la barra de progreso
            progress_bar.config(maximum=duration)
            actualizar_barra_progreso()

            messagebox.showinfo("Éxito", "La conversión se ha completado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error durante la conversión: {str(e)}")
    else:
        messagebox.showwarning("Advertencia", "No se ha seleccionado ningún archivo PDF.")

def actualizar_barra_progreso():
    current_time = pygame.mixer.music.get_pos() / 1000  # Obtener el tiempo actual en segundos
    progress_bar.config(value=current_time)
    if pygame.mixer.music.get_busy():
        window.after(1000, actualizar_barra_progreso)  # Actualizar la barra cada segundo

def pausar_reproduccion():
    pygame.mixer.music.pause()
    btn_pause.config(state=tk.DISABLED)
    btn_resume.config(state=tk.NORMAL)

def reanudar_reproduccion():
    pygame.mixer.music.unpause()
    btn_pause.config(state=tk.NORMAL)
    btn_resume.config(state=tk.DISABLED)

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
slow_audio_speed = True  # Cambiar a False para una velocidad más rápida

# Crear la ventana de la interfaz
window = tk.Tk()
window.title("Conversor de PDF a Audio")

# Agregar una lista desplegable de idiomas con nombres completos
idiomas_codigos = {v: k for k, v in idiomas.items()}  # Invertir el diccionario para obtener los códigos de idioma
combo_idiomas = ttk.Combobox(window, values=list(idiomas.values()))
combo_idiomas.current(0)  # Establecer el idioma predeterminado
combo_idiomas.pack(pady=10)

# Agregar un botón para seleccionar el archivo PDF y realizar la conversión
btn_convertir = tk.Button(window, text="Seleccionar PDF", command=convertir_a_audio)
btn_convertir.pack(pady=20)

# Agregar botones para pausar y reanudar la reproducción
btn_pause = tk.Button(window, text="Pausar", state=tk.DISABLED, command=pausar_reproduccion)
btn_pause.pack(pady=10)

btn_resume = tk.Button(window, text="Reanudar", state=tk.DISABLED, command=reanudar_reproduccion)
btn_resume.pack(pady=10)

# Agregar una barra de progreso para mostrar el avance de la reproducción
progress_bar = ttk.Progressbar(window, orient='horizontal', mode='determinate')
progress_bar.pack(pady=10)

# Ejecutar la interfaz
window.mainloop()
