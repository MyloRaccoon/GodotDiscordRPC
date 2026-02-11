import psutil, win32gui, win32process
from psutil import Process

class GodotData:

	def __init__(self, project, scene):
		self.project = project
		self.scene = scene

	def __str__(self):
		return f"Editing scene {self.scene} for project {self.project}"

	def __eq__(self, value):
		if not isinstance(value, GodotData): return False
		return self.project == value.project and self.scene == value.scene

class GodotListener:

	def __init__(self):
		self.process: Process = None

	def find_godot_process(self) -> Process|None:
		for proc in psutil.process_iter(['name', 'exe', 'cmdline']):
			try:
				name_is_godot = "godot" in (proc.info['name'] or "").lower()
				name_in_exe = "godot" in (proc.info['exe'] or "").lower()
				cmdline = " ".join(proc.info['cmdline'] or [])
				is_in_editor = "--editor" in cmdline or " -e" in cmdline

				if name_is_godot and name_in_exe and is_in_editor:
					return proc
			
			except (psutil.NoSuchProcess, psutil.AccessDenied):
				pass

		return None

	def update_process(self):
		if self.process is None or not psutil.pid_exists(self.process.pid):
			self.process = self.find_godot_process()

	def get_window_title(self) -> str|None:
		titles = []

		def enum_callback(hwnd, _):
			if not win32gui.IsWindow(hwnd): return
			_, win_pid = win32process.GetWindowThreadProcessId(hwnd)
			if win_pid == self.process.pid:
				title = win32gui.GetWindowText(hwnd)
				if not title: return
				if title in ("MSCTFIME UI", "Default IME"): return
				if title and "godot" in title.lower() and not "(DEBUG)" in title:
					titles.append(title)

		win32gui.EnumWindows(enum_callback, None)
		if len(titles) == 0: return None
		return titles[0]

	def get_last_data(self) -> GodotData|None:
		self.update_process()
		if not self.process: return None
		window_title = self.get_window_title()
		if not window_title: return None
		items = window_title.split('-')
		scene = items[0].strip()
		project = items[1].strip()
		return GodotData(project, scene)