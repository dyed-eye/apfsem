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

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']


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
                self.messages.text = ''

        def gd_choose(checkbox, value):
            if value:
                self.text_input.text = 'https://drive.google.com/'
                self.browse_button.disabled = True
                self.browse_button.opacity = 0
                self.messages.text = ''

        def confirm_path(instance):
            if source_radio.active:
                if os.path.isfile(self.text_input.text):
                    try:
                        img = Image.open(self.text_input.text)
                        if (img.format == 'JPEG') or (img.format == 'JPG')\
                                or (img.format == 'PNG') or (img.format == 'TIF'):
                            img.save('res/cached_image.png')
                            self.ids.image_preview.source = 'res/cached_image.png'
                            self.ids.image_preview.size = (img.width / img.height * self.height / 4, self.height / 4)
                            self.ids.image_preview_label.text = 'Image preview:'
                            self.messages.text = ''
                        else:
                            self.messages.text = '[color=ff1111]Error: image was not recognised[/color]'
                            print('Error: image was not recognised')
                    except:
                        self.messages.text = '[color=ff1111]Error: no file specified[/color]'
                        print('Error: no image specified')
                else:
                    self.messages.text = '[color=ff1111]Error: no file specified[/color]'
                    print('Error: no file specified')
                    # TODO: do the errors more ... (?)
            elif gd_radio.active:
                ask_google(self.text_input.text)

        def load(path, filename):
            if len(filename) == 1:
                self.text_input.text = filename[0]
                self.messages.text = ''
            else:
                self.messages.text = '[color=ff1111]Error: no file specified[/color]'
            # TODO: specify extensions (?)
            dismiss_popup()

        def dismiss_popup():
            self.pop_up.dismiss()

        def pick_path(instance):
            content = LoadDialog(load=load, cancel=dismiss_popup)
            self.pop_up = Popup(title="Select image", content=content,
                                size_hint=(0.9, 0.9))
            self.pop_up.open()

        main_l = self.ids.main_layout
        fp_l = self.ids.file_pick_layout

        source_radio = CheckBox(active=True, group='source')
        main_l.add_widget(source_radio)
        source_radio.bind(active=source_choose)
        main_l.add_widget(Label(text='Local File'))
        gd_radio = CheckBox(group='source')
        main_l.add_widget(gd_radio)
        gd_radio.bind(active=gd_choose)
        main_l.add_widget(Label(text='Google Drive link'))

        self.text_input = TextInput(text=os.path.dirname(os.path.abspath(__file__)), multiline=False)
        fp_l.add_widget(self.text_input)
        self.browse_button = Button(text='...', on_press=pick_path, size_hint_x=None, width=40)
        fp_l.add_widget(self.browse_button)
        fp_l.add_widget(Button(text='confirm', on_press=confirm_path, size_hint_x=None, width=100))
        self.messages = Label(text='', markup=True)
        fp_l.add_widget(self.messages)


class MainApp(App):
    img_prev_source = 'res/blank.png'
    img_prev_size = (0, 0)

    def build(self):
        sm = ScreenManager()
        sm.add_widget(Main(name='menu'))
        # TODO: think about other possible screens
        return sm


if __name__ == '__main__':
    MainApp().run()
