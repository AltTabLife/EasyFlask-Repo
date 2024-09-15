from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
import shutil
import tempfile
import subprocess
import threading
import os
import signal

# Import the road_map function
from EasyFlask.road_map import full_road_map

class MyApp(App):
	def build(self):
		main_layout = BoxLayout(orientation='vertical')

		file_input_layout = BoxLayout(orientation='horizontal')
		self.file_input = TextInput(hint_text='Enter .yamlish file path', multiline=False)
		file_input_layout.add_widget(self.file_input)

		self.file_button = Button(text='Browse')
		self.file_button.bind(on_press=self.open_file_chooser)
		file_input_layout.add_widget(self.file_button)

		process_button_layout = BoxLayout(orientation='horizontal')
		self.process_button = Button(text='Process .yamlish File')
		self.process_button.bind(on_press=self.process_yamlish_file)
		process_button_layout.add_widget(self.process_button)

		file_input_and_process_layout = BoxLayout(orientation='vertical')
		file_input_and_process_layout.add_widget(file_input_layout)
		file_input_and_process_layout.add_widget(process_button_layout)

		horizontal_layout = BoxLayout(orientation='horizontal')
		horizontal_layout.add_widget(file_input_and_process_layout)

		self.run_button = Button(text='Run splash_page.yamlish', size_hint_y=None, height=100)
		self.run_button.bind(on_press=self.run_splash_page)
		horizontal_layout.add_widget(self.run_button)

		main_layout.add_widget(horizontal_layout)

		self.start_button = Button(text='Start Server')
		self.start_button.bind(on_press=self.start_server)
		main_layout.add_widget(self.start_button)

		self.stop_button = Button(text='Stop Server')
		self.stop_button.bind(on_press=self.stop_server)
		main_layout.add_widget(self.stop_button)

		self.server_process = None
		self.temp_dir = None

		return main_layout

	def open_file_chooser(self, instance):
		content = BoxLayout(orientation='vertical')
		filechooser = FileChooserListView()
		content.add_widget(filechooser)

		select_button = Button(text='Select')
		select_button.bind(on_press=lambda x: self.select_file(filechooser.selection))
		content.add_widget(select_button)

		self.popup = Popup(title='Select a .yamlish file', content=content, size_hint=(0.9, 0.9))
		self.popup.open()

	def select_file(self, selection):
		if selection:
			self.file_input.text = selection[0]
		self.popup.dismiss()

	def process_yamlish_file(self, instance):
		if self.temp_dir:
			shutil.rmtree(self.temp_dir)
		self.temp_dir = tempfile.mkdtemp()

		yamlish_file_path = self.file_input.text
		if not os.path.isfile(yamlish_file_path):
			print(f"File not found: {yamlish_file_path}")
			return

		shutil.copy(yamlish_file_path, self.temp_dir)
		print(f'{yamlish_file_path} copied to {self.temp_dir}')

		# Run the road_map function
		full_road_map(yamlish_file_path, self.temp_dir)
		print(f'road_map function executed with {yamlish_file_path} and {self.temp_dir}')

	def run_splash_page(self, instance):
		if self.temp_dir:
			shutil.rmtree(self.temp_dir)
		self.temp_dir = tempfile.mkdtemp()

		splash_page_path = 'splash_page.yamlish'
		if not os.path.isfile(splash_page_path):
			print(f"File not found: {splash_page_path}")
			return

		shutil.copy(splash_page_path, self.temp_dir)
		print(f'{splash_page_path} copied to {self.temp_dir}')

		# Run the road_map function
		full_road_map(splash_page_path, self.temp_dir)
		print(f'road_map function executed with {splash_page_path} and {self.temp_dir}')

	def start_server(self, instance):
		if self.server_process is None and self.temp_dir is not None:
			self.server_thread = threading.Thread(target=self.run_flask_server, args=(self.temp_dir,))
			self.server_thread.start()

	def run_flask_server(self, working_dir):
		try:
			self.server_process = subprocess.Popen(['flask', 'run'], cwd=working_dir, preexec_fn=os.setsid)
			self.server_process.wait()
		except Exception as e:
			print(f"Error starting Flask server: {e}")

	def stop_server(self, instance):
		if self.server_process is not None:
			os.killpg(os.getpgid(self.server_process.pid), signal.SIGTERM)
			self.server_process = None
			print("Flask server stopped")

if __name__ == '__main__':
	MyApp().run()