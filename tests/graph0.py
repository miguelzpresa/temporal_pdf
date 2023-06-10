#!/home/sistemas/kivy_venv/bin/python
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

class LoginScreen(Screen):
    pass


class HomeScreen(Screen):
    pass


class MyApp(MDApp):
    def build(self):
	
        self.manager = ScreenManager(transition = NoTransition())
        self.manager.add_widget(Builder.load_file("graph0.kv"))

        self.manager.add_widget(LoginScreen(name='login'))  # <-- Correct indentation
        self.manager.add_widget(HomeScreen(name='home'))
        return self.manager
    def open_f(self):
   		pass


if __name__ == '__main__':
    MyApp().run()
