#!/usr/bin/python3
import kivy
import kivymd
import PyPDF2 
import pygame
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
#from kivymd.uix import MDProgressCircle
from kivymd.uix.textfield import MDTextField

from PyPDF2 import PdfReader
from gtts import gTTS
from pygame import mixer


class PDFToAudioConverterApp(MDApp):
    def build(self):
        return Builder.load_file('pdf_to_audio_converter.kv')

    def open_file_manager(self, *args):
        """Opens the file manager."""
        file_manager = MDFileManager(
            allowed_extensions=['.pdf'],
            on_file_selected=self.on_file_selected,
        )
        file_manager.open()

    def on_file_selected(self, file_path):
        """Called when a file is selected in the file manager."""
        self.root.ids.input_text.text = ''
        self.root.ids.output_text.text = ''
        self.convert_to_audio(file_path)

    def convert_to_audio(self, file_path):
        """Converts the PDF file to audio."""
        try:
            # Extract text from the PDF file.
            with open(file_path, 'rb') as file:
                pdf_reader = PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()

            # Get the language from the user.
            language = self.root.ids.language_dropdown.text

            # Convert the text to audio.
            audio = gTTS(text=text, lang=language, slow=True)

            # Save the audio file.
            if not os.path.exists('audios'):
                os.mkdir('audios')
            audio_path = 'audios/{}.mp3'.format(os.path.basename(file_path).split('.')[0])
            audio.save(audio_path)

            # Play the audio file.
            mixer.init()
            mixer.music.load(audio_path)
            mixer.music.play()

            # Update the UI.
            self.root.ids.input_text.text = ''
            self.root.ids.output_text.text = 'Audio file saved to {}'.format(audio_path)
            #self.root.ids.progress_circle.value = 100
        except Exception as e:
            self.root.ids.output_text.text = 'Error converting PDF to audio: {}'.format(str(e))


if __name__ == '__main__':
    PDFToAudioConverterApp().run()
