from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
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
		layout = BoxLayout(orientation='vertical')

		self.run_button = Button(text='Run splash_page.yamlish')
		self.run_button.bind(on_press=self.run_splash_page)
		layout.add_widget(self.run_button)

		self.start_button = Button(text='Start Server')
		self.start_button.bind(on_press=self.start_server)
		layout.add_widget(self.start_button)

		self.stop_button = Button(text='Stop Server')
		self.stop_button.bind(on_press=self.stop_server)
		layout.add_widget(self.stop_button)

		self.server_process = None
		self.temp_dir = None

		return layout

	def run_splash_page(self, instance):
		self.temp_dir = tempfile.mkdtemp()
		splash_page_path = 'splash_page.yamlish'
		shutil.copy(splash_page_path, self.temp_dir)
		print(f'splash_page.yamlish copied to {self.temp_dir}')

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

