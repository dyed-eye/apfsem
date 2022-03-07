import kivy
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Rectangle, Color
from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

from PIL import Image
import os
import xml.etree.ElementTree as ET




# path example: "D:\emae\python\apfsem_examples\JACS_01.jpg"
# path has to be copied with right mouse button -> copy as path
# also we assume that metadata has path %path%_metadata.xml


class LoadDialog(GridLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


# Container class for the app's widgets
class Main(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        def ask_google(link):
            ...
            # TODO: requests to google api

        def source_choose(checkbox, value):
            if value:
                self.text_input.text = os.path.dirname(os.path.abspath(__file__))
                self.browse_button.disabled = False
                self.browse_button.opacity = 1

        def gd_choose(checkbox, value):
            if value:
                self.text_input.text = 'https://drive.google.com/'
                self.browse_button.disabled = True
                self.browse_button.opacity = 0

        def confirm_path(instance):
            if source_radio.active:
                if os.path.isfile(self.text_input.text):
                    try:
                        img = Image.open(self.text_input.text)
                        if (img.format == 'JPEG') or (img.format == 'JPG') or (img.format == 'PNG'):
                            img.save('res/cached_image.png')
                            with self.canvas:
                                self.rect = Rectangle(source='res/cached_image.png')
                                # TODO: positioning of the image
                        else:
                            print('Error: image was not recognised')
                    except:
                        print('Error: no file specified')
                else:
                    print('Error: no file specified')
                    # TODO: do the errors more ... (?)
                    # TODO: error output as a label
            elif gd_radio.active:
                ask_google(self.text_input.text)

        def load(path, filename):
            self.text_input.text = filename[0]
            # TODO: specify extensions (?)
            dismiss_popup()

        def dismiss_popup():
            self.pop_up.dismiss()

        def pick_path(instance):
            content = LoadDialog(load=load, cancel=dismiss_popup)
            self.pop_up = Popup(title="Select image", content=content,
                                size_hint=(0.9, 0.9))
            self.pop_up.open()

        l = self.ids.main_layout
        fp = self.ids.file_pick_layout
        source_radio = CheckBox(active=True, group='source')
        l.add_widget(source_radio)
        source_radio.bind(active=source_choose)
        l.add_widget(Label(text='Local File'))
        gd_radio = CheckBox(group='source')
        l.add_widget(gd_radio)
        gd_radio.bind(active=gd_choose)
        l.add_widget(Label(text='Google Drive link'))

        self.text_input = TextInput(text=os.path.dirname(os.path.abspath(__file__)), multiline=False)
        fp.add_widget(self.text_input)
        self.browse_button = Button(text='...', on_press=pick_path, size_hint_x=None, width=40)
        fp.add_widget(self.browse_button)
        fp.add_widget(Button(text='confirm', on_press=confirm_path, size_hint_x=None, width=100))


class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Main(name='menu'))
        # TODO: think about other possible screens
        return sm


if __name__ == '__main__':
    MainApp().run()
