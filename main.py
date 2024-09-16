from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
import shutil
import tempfile
import subprocess
import threading
import os
import signal
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Import the road_map function
from EasyFlask.road_map import full_road_map

class YamlishFileHandler(FileSystemEventHandler):
    def __init__(self, app):
        self.app = app

    def on_modified(self, event):
        if event.src_path == self.app.yamlish_file_path:
            self.app.restart_server_with_new_yamlish()

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        main_layout = BoxLayout(orientation='vertical')

        file_input_layout = BoxLayout(orientation='horizontal')
        self.file_input = TextInput(hint_text='Enter .yamlish file path', multiline=True, size_hint_y=None, height=100)
        file_input_layout.add_widget(self.file_input)

        self.file_button = Button(text='Browse')
        self.file_button.bind(on_press=self.open_file_chooser)
        file_input_layout.add_widget(self.file_button)

        process_button_layout = BoxLayout(orientation='horizontal')
        self.process_button = Button(text='Live Debug')
        self.process_button.bind(on_press=self.open_debug_window)
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
        self.yamlish_file_path = None
        self.observer = None

        self.add_widget(main_layout)

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

    def open_debug_window(self, instance):
        self.manager.current = 'debug'

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

    def start_server_on_port(self, port):
        if self.server_process is None and self.temp_dir is not None:
            self.server_thread = threading.Thread(target=self.run_flask_server, args=(self.temp_dir, port))
            self.server_thread.start()

    def run_flask_server(self, working_dir, port='5000'):
        try:
            self.server_process = subprocess.Popen(['flask', 'run', '--port', port], cwd=working_dir, preexec_fn=os.setsid)
            self.server_process.wait()
        except Exception as e:
            print(f"Error starting Flask server: {e}")

    def stop_server(self, instance):
        if self.server_process is not None:
            os.killpg(os.getpgid(self.server_process.pid), signal.SIGTERM)
            self.server_process = None
            print("Flask server stopped")

    def stop_server_on_port(self, port):
        if self.server_process is not None:
            os.killpg(os.getpgid(self.server_process.pid), signal.SIGTERM)
            self.server_process = None
            print(f"Flask server on port {port} stopped")

    def restart_server_with_new_yamlish(self):
        # Step 1: Kill the current process
        self.stop_server(None)

        # Step 2: Delete the old files in the temp directory (or start a new temp directory and delete the old one)
        if self.temp_dir:
            shutil.rmtree(self.temp_dir)
        self.temp_dir = tempfile.mkdtemp()

        # Step 3: Reprocess the new yamlish file version
        shutil.copy(self.yamlish_file_path, self.temp_dir)
        print(f'{self.yamlish_file_path} copied to {self.temp_dir}')
        full_road_map(self.yamlish_file_path, self.temp_dir)
        print(f'road_map function executed with {self.yamlish_file_path} and {self.temp_dir}')

        # Step 4: Start the new Flask server
        self.start_server(None)

    def on_stop(self):
        if self.observer is not None:
            self.observer.stop()
            self.observer.join()
        self.stop_server(None)  # Ensure the Flask server is stopped when the application stops

class DebugScreen(Screen):
    def __init__(self, **kwargs):
        super(DebugScreen, self).__init__(**kwargs)
        main_layout = BoxLayout(orientation='horizontal')

        # Column 1

        column1 = BoxLayout(orientation='vertical')

        self.back_button = Button(text='Back to Main Menu')
        self.back_button.bind(on_press=self.confirm_stop_server)
        column1.add_widget(self.back_button)

        self.current_path_label = Label(text='Current Flask Input Path: \nTemp Directory:')
        column1.add_widget(self.current_path_label)

        self.ports_label = Label(text='Current Running Flask Ports and PIDs:')
        column1.add_widget(self.ports_label)

        self.port_input = TextInput(hint_text='Enter port number', multiline=False)
        column1.add_widget(self.port_input)

        self.start_button = Button(text='Start Server')
        self.start_button.bind(on_press=self.start_server_on_port)
        column1.add_widget(self.start_button)

        self.stop_button = Button(text='Stop Server')
        self.stop_button.bind(on_press=self.stop_server_on_port)
        column1.add_widget(self.stop_button)



        main_layout.add_widget(column1)

        # Column 2
        column2 = BoxLayout(orientation='vertical')
        self.debug_output = TextInput(hint_text='Debug Data Output', multiline=True, readonly=True)
        scroll_view = ScrollView()
        scroll_view.add_widget(self.debug_output)
        column2.add_widget(scroll_view)

        main_layout.add_widget(column2)

        self.add_widget(main_layout)

        # Schedule the update of the ports and PIDs list every 5 seconds
        Clock.schedule_interval(self.update_ports_and_pids, 5)

    def start_server_on_port(self, instance):
        port = self.port_input.text or '5000'
        self.manager.get_screen('main').start_server_on_port(port)

    def stop_server_on_port(self, instance):
        port = self.port_input.text or '5000'
        self.manager.get_screen('main').stop_server_on_port(port)

    def update_ports_and_pids(self, dt):
        ports_and_pids = self.get_flask_ports_and_pids()
        self.ports_label.text = f'Current Running Flask Ports and PIDs:\n{ports_and_pids}'

    def get_flask_ports_and_pids(self):
        result = subprocess.run(['lsof', '-i', '-P', '-n'], stdout=subprocess.PIPE)
        output = result.stdout.decode('utf-8')
        flask_ports_and_pids = []
        for line in output.split('\n'):
            if 'flask' in line:
                parts = line.split()
                pid = parts[1]
                port = parts[8].split(':')[-1]
                flask_ports_and_pids.append(f'Port: {port}, PID: {pid}')
        return '\n'.join(flask_ports_and_pids)

    def confirm_stop_server(self, instance):
        if self.manager.get_screen('main').server_process is not None:
            content = BoxLayout(orientation='vertical')
            content.add_widget(Label(text='A server is currently running. It will be stopped if you return to the main menu.'))
            button_layout = BoxLayout(orientation='horizontal')
            yes_button = Button(text='Yes')
            yes_button.bind(on_press=self.stop_server_and_return)
            button_layout.add_widget(yes_button)
            no_button = Button(text='No')
            no_button.bind(on_press=lambda x: self.popup.dismiss())
            button_layout.add_widget(no_button)
            content.add_widget(button_layout)
            self.popup = Popup(title='Confirm', content=content, size_hint=(0.8, 0.4))
            self.popup.open()
        else:
            self.manager.current = 'main'

    def stop_server_and_return(self, instance):
        self.manager.get_screen('main').stop_server(None)
        self.popup.dismiss()
        self.manager.current = 'main'

class MyApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        self.main_screen = MainScreen(name='main')
        self.debug_screen = DebugScreen(name='debug')

        self.screen_manager.add_widget(self.main_screen)
        self.screen_manager.add_widget(self.debug_screen)

        return self.screen_manager

    def on_stop(self):
        self.main_screen.on_stop()

if __name__ == '__main__':
    MyApp().run()