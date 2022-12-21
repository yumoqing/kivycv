from kivy.uix.boxlayout import BoxLayout
from camera4kivy import Preview
from kivyblocks.utils import blocksImage, CSize
from kivyblocks.clickable import ClickableImage
from kivy.app import App
from kivy.utils import platform
from kivy.clock import Clock

class NewCamera(BoxLayout):
	def __init__(self, **kw):
		super().__init__(orientation='vertical')
		self.preview = Preview(**kw)
		self.add_widget(self.preview)
		box = BoxLayout(orientation='horizontal',
									size_hint_y=None,
									height=CSize(2))
		self.camera = ClickableImage(size_hint=[None, None],
									height=CSize(1.6),
									width=CSize(1.6),
									pos_hint={
										'x':self.width/2 - CSize(1.6),
										'y':0
									},
									source=blocksImage('photo.png'),
									img_kw={
										'size_hint':[None,None],
										'height':CSize(1.5),
										'width':CSize(1.5)
									})

		self.lensid = ClickableImage(size_hint=[None, None],
									height=CSize(1.6),
									width=CSize(1.6),
									pos_hint={
										'x':self.width/2,
										'y':0
									},
									source=blocksImage('lensid.png'),
									img_kw={
										'size_hint':[None,None],
										'height':CSize(1.5),
										'width':CSize(1.5)
									})

		self.camera.bind(on_press=self.take_a_pic)
		self.lensid.bind(on_press=self.change_lensid)
		box.add_widget(self.camera)
		box.add_widget(self.lensid)
		self.add_widget(box)
		# self.bind(size=self.change_btn_position)
		Clock.schedule_once(self.open_camera, 0.5)

	def open_camera(self, *args):
		self.preview.connect_camera(aspect_ratio='16:9', 
								filepath_callback=self.photo_saved)

	def photo_saved(self, path:str):
		print(f'{path} saved')

	def change_lensid(self, *args):
		if platform not in [ 'android', 'ios' ]:
			return
		if self.preview.preview.index == 0:
			self.preview.select_camera("1")
		else:
			self.preview.select_camera("0")

	def change_btn_position(self, *args):
		self.camera.pos_hint = {
			'x':self.width/2 - CSize(1.6),
			'y':0
		}
		self.lensid.pos_hint = {
			'x':self.width/2,
			'y':0
		}

	def take_a_pic(self, o):
		self.preview.capture_photo()

class C4KApp(App):
	def build(self):
		x = NewCamera()
		return x

if __name__ == '__main__':
	C4KApp().run()
