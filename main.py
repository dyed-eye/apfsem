from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

import cv2 as cv
import os
import threading

import operation as op


# path example: "D:\emae\python\apfsem_examples\JACS_01.jpg"
# path has to be copied with right mouse button -> copy as path
# also we assume that metadata has path %path%_metadata.xml


class AlignLabel(Label):
    def on_size(self, *args):
        self.text_size = self.size


class LoadDialog(GridLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class Main(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        def image_recognising(img):
            cv.imwrite('res/cached_image.png', img)
            self.ids.image_preview.source = 'res/cached_image.png'
            self.ids.image_preview.reload()
            self.ids.image_preview.size = (img.shape[1] / img.shape[0] * 160, 160)
            self.ids.image_preview_label.text = 'Image preview:'
            self.messages.text = '[color=22ff22]Success![/color]'
            APfSEMApp.img_prev_source = 'res/cached_image.png'

        def ask_google(link):
            ...
            # TODO: requests to google api (it would be cool)

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
            if self.ids.source_radio.active:
                if os.path.isfile(self.text_input.text):
                    img = cv.imread(cv.samples.findFile(self.text_input.text))
                    if img is None:
                        self.messages.text = '[color=ff1111]Error: no file specified[/color]'
                        print('Error: no image specified')
                    else:
                        image_recognising(img)
                else:
                    self.messages.text = '[color=ff1111]Error: no file specified[/color]'
                    print('Error: no file specified')
            elif self.ids.gd_radio.active:
                ask_google(self.text_input.text)

        def load(path, filename):
            if len(filename) == 1:
                self.text_input.text = filename[0]
                self.messages.text = ''
                confirm_path(None)
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

        def big_purple_button_action():
            # TODO: think about other circumstances (!)
            grain_size = 0
            try:
                grain_size = float(self.ids.grain_size_input.text)
            except:
                self.messages.text = '[color=ff1111]Error: incorrect number[/color]'
            if APfSEMApp.img_prev_source != 'res/blank.png':
                if grain_size > 0:
                    APfSEMApp.grain_size = grain_size
                    APfSEMApp.sm.current = 'process'
                else:
                    self.messages.text = '[color=ff1111]Error: size has not been stated or below zero[/color]'
            else:
                self.messages.text = '[color=ff1111]Error: choose an image[/color]'

        fp_l = self.ids.file_pick_layout

        self.ids.source_radio.bind(active=source_choose)
        self.ids.gd_radio.bind(active=gd_choose)

        self.text_input = TextInput(text=os.path.dirname(os.path.abspath(__file__)), multiline=False)
        fp_l.add_widget(self.text_input)
        self.browse_button = Button(text='...', on_press=pick_path, size_hint_x=None, width=40)
        fp_l.add_widget(self.browse_button)
        fp_l.add_widget(Button(text='confirm', on_press=confirm_path, size_hint_x=None, width=100))
        self.messages = AlignLabel(text='', markup=True, size_hint=(1.0, 1.0), halign='left', valign='middle')
        fp_l.add_widget(self.messages)

        self.ids.big_purple_button.on_press = big_purple_button_action


class Evaluate(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self, *args):
        def start_operation():
            threading.Thread(target=operation).start()

        def operation():
            self.output = op.automised(APfSEMApp.grain_size, 7)
            Clock.schedule_once(finish_operation)
            #TODO: think about possibility of changing the accuracy

        def finish_operation(args):
            APfSEMApp.sm.current = 'result'

        start_operation()


class Result(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_pre_enter(self, *args):
        self.ids.image_with_contours.source = 'res/cached_cached_image.png'

    def on_enter(self, *args):
        self.ids.image_with_contours.reload()


class Manual(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        def apply_action():
            self.ids.description.text = "Calculating... Please wait"
            threading.Thread(target=operation).start()

        def operation():
            self.count = op.manual(self.ids.blur_slider.value, self.gaus_thresh, self.ids.pixelblock_slider.value,
                              self.ids.c_slider.value, self.ids.contrast_check.active, self.ids.cliplimit_slider.value,
                              self.ids.gridsize_slider.value, self.ids.thick_slider.value)
            Clock.schedule_once(finish_operation)

        def finish_operation(args):
            self.ids.description.text = str(self.count) + ' contours'
            img = cv.imread('res/cached_cached_image.png')
            self.ids.image_editing.size = (img.shape[1] / img.shape[0] * 300, 300)
            self.ids.image_editing.reload()

        def blur_listener(instance, value):
            self.ids.blur_title.text = 'Blur (-1 to disable): ' + str(round(value, 2))

        def clip_listener(instance, value):
            self.ids.cliplimit_title.text = 'Clip Limit: ' + str(round(value, 2))

        def grid_listener(instance, value):
            self.ids.gridsize_title.text = 'Grid Size: ' + str(round(value, 2))

        def pixel_listener(instance, value):
            self.ids.pixelblock_title.text = 'Pixel Block: ' + str(round(value, 2))

        def c_listener(instance, value):
            self.ids.c_title.text = 'C: ' + str(round(value, 2))

        def th_listener(instance, value):
            self.ids.thick_title.text = 'Thickness of line: ' + str(round(value, 0))

        def mean(checkbox, value):
            if value:
                self.gaus_thresh = False

        def gaus(checkbox, value):
            if value:
                self.gaus_thresh = True

        def contrast(checkbox, value):
            if value:
                self.ids.contrast_layout.disabled = False
            else:
                self.ids.contrast_layout.disabled = True

        self.gaus_thresh = False
        self.ids.apply_button.on_press = apply_action
        self.ids.blur_slider.bind(value=blur_listener)
        self.ids.cliplimit_slider.bind(value=clip_listener)
        self.ids.gridsize_slider.bind(value=grid_listener)
        self.ids.pixelblock_slider.bind(value=pixel_listener)
        self.ids.c_slider.bind(value=c_listener)
        self.ids.mean_radio.bind(active=mean)
        self.ids.gaus_radio.bind(active=gaus)
        self.ids.contrast_check.bind(active=contrast)
        self.ids.apply_button.pos_hint = {'center_y': 0.5}
        self.ids.thick_slider.bind(value=th_listener)

    def on_pre_enter(self, *args):
        img = cv.imread('res/cached_image.png')
        cv.imwrite('res/cached_cached_image.png', img)
        self.ids.image_editing.source = 'res/cached_cached_image.png'

    def on_enter(self, *args):
        img = cv.imread('res/cached_cached_image.png')
        self.ids.image_editing.size = (img.shape[1] / img.shape[0] * 300, 300)
        self.ids.image_editing.reload()


class APfSEMApp(App):
    img_prev_source = 'res/blank.png'
    img_prev_size = (0, 0)
    grain_size = 0

    sm = ScreenManager()

    def build(self):
        self.sm.add_widget(Main(name='menu'))
        self.sm.add_widget(Evaluate(name='process'))
        self.sm.add_widget(Result(name='result'))
        self.sm.add_widget(Manual(name='manual'))
        return self.sm


if __name__ == '__main__':
    APfSEMApp().run()
