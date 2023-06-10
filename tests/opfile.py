#!/usr/bin/python3
import kivy
import kivymd 
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, NoTransition,Screen
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from pydantic import ValidationError
from pydantic.types import FilePath
from kivy.uix.filechooser import FileChooserListView

Window.size = (350,580)

class FileChooserScreen(Screen):
    file_chooser = ObjectProperty(None)

    def select_file(self, path, filename):
        # Lógica para manejar la selección del archivo
        print("Archivo seleccionado:", filename[0])

    def show_file_chooser(self):
        content = FileChooserScreen()
        popup = Popup(title="Seleccionar archivo", content=content, size_hint=(0.9, 0.9))
        popup.open()

class MainScreen(Screen):
    file_chooser_button = ObjectProperty(None)

    def show_file_chooser(self):
        file_chooser_screen = FileChooserScreen()
        popup = Popup(title="Seleccionar archivo", content=file_chooser_screen, size_hint=(0.9, 0.9))
        popup.open()    i


class HomeScreen(Screen):
    pass


class MyApp(MDApp):
    def build(self):
		screen_manager = ScreenManager()
		screen_manager.add_widget(Builder.load_file('main.kv'))
		screen_manager.add_widget(Builder.load_file('upload.kv'))
		screen_manager.add_widget(Builder.load_file('home.kv'))
		return screen_manager	



if __name__ == '__main__':
    MyApp().run()
