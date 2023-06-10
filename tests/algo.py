import os

import textract
from gtts import gTTS

# Ruta del archivo PDF
pdf_path = 'prueba.pdf'

# Extraer texto del PDF
text = textract.process(pdf_path, method='pdfminer').decode('utf-8')

# Configuración de la voz
language = 'es'  # Idioma español
slow_audio_speed = False  # Velocidad normal

# Crear objeto de conversión de texto a voz
audio = gTTS(text=text, lang=language, slow=slow_audio_speed)

# Guardar archivo de audio
audio_path = 'archivo_de_audio.mp3'
audio.save(audio_path)

# Reproducir archivo de audio
os.system('mpg321 ' + audio_path)  # Necesitarás instalar el reproductor 'mpg321'
#pip install textract
#pip install gTTSo
#pip install mpyg321
