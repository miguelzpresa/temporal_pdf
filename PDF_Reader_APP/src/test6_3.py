#!/usr/bin/python3

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label 
from kivy.uix.textinput import TextInput
from pydantic import ValidationError
from pydantic.types import FilePath



class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)

        # BoxLayout principal
        main_layout = BoxLayout(orientation='vertical')

        # BoxLayout para el título
        title_layout = BoxLayout(size_hint=(0.5, 0.5))
        welcome_label = Label(text='PDF_Readeer', font_size=40)
        title_layout.add_widget(welcome_label)

        # BoxLayout para usuario y contraseña
        input_layout = BoxLayout(size_hint=(0.3, 0.5), padding=(20, 0))
        user_label = Label(text='Usuario:', font_size=20, halign='left', valign='middle')
        user_input = TextInput(multiline=False)
        pass_label = Label(text='Contraseña:', font_size=20, halign='left', valign='middle')
        pass_input = TextInput(multiline=False, password=True)
        input_layout.add_widget(user_label)
        input_layout.add_widget(user_input)
        input_layout.add_widget(pass_label)
        input_layout.add_widget(pass_input)

        # BoxLayout para el botón
        button_layout = BoxLayout(size_hint=(1, 0.2), padding=(20, 0))
        welcome_button = Button(text='Ingresar', font_size=30, size_hint=(0.5, 1))
        welcome_button.bind(on_press=self.switch_to_file_screen)
        button_layout.add_widget(welcome_button)

        # Agregar los BoxLayouts al BoxLayout principal
        main_layout.add_widget(title_layout)
        main_layout.add_widget(input_layout)
        main_layout.add_widget(button_layout)

        self.add_widget(main_layout)



    def switch_to_file_screen(self, *args):
        self.manager.current = 'file'

class FileScreen(Screen):
    def __init__(self, **kwargs):
        super(FileScreen, self).__init__(**kwargs)
        layout = BoxLayout()
        file_chooser = FileChooserListView()
        select_button = Button(text='Select', size_hint=(None, 0.2), width=100)
        select_button.bind(on_press=lambda x: self.upload_file(file_chooser.path))
        file_chooser.size_hint_y = 0.8
        layout.add_widget(file_chooser)
        layout.add_widget(select_button)
        self.add_widget(layout)



    def upload_file(self, path):
        print(path)
    try:
        # validar que el archivo es un PDF
        FilePath(strict=True, endswith='.pdf').__get_validators__()[0](path)

        with open(path, 'rb') as f:
            # ejecutar la función pdf_metamorfosis con el archivo como argumento
            pdf_metamorfosis(f.read())
    except ValidationError:
        print('El archivo no es un PDF')
    except FileNotFoundError:
        print('El archivo no existe')
    except Exception as e:
        print('Ocurrió un error inesperado:', e)       
class MyApp(App):

    def build(self):
        screen_manager = ScreenManager()
        welcome_screen = WelcomeScreen(name='welcome')
        file_screen = FileScreen(name='file')
        screen_manager.add_widget(welcome_screen)
        screen_manager.add_widget(file_screen)
        return screen_manager


if __name__ == '__main__':
    MyApp().run()

