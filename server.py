from godot_listener import GodotListener, GodotData
from discord_RPC import RPC
import time
from dotenv import load_dotenv
import os
from logger import log

load_dotenv()
UPDATE_FREQUENCE = float(os.getenv('UPDATE_FREQUENCE'))

class Server:

	def __init__(self):
		self.listener = GodotListener()
		self.rpc = RPC()
		self.last_data = self.listener.get_last_data()

	def on_data_changed(self, data: GodotData|None):
		if not data:
			self.rpc.clear()
			log("Godot RPC cleared")
		else:
			self.rpc.update(data)
			log(f"Godot RPC changed: {data}")

	def run(self, stop_event):

		log("Godot RPC started")
		
		if self.last_data:
			self.rpc.update(self.last_data)

		while not stop_event.is_set():

			new_data = self.listener.get_last_data()

			if new_data != self.last_data:
				self.on_data_changed(new_data)
				self.last_data = new_data

			time.sleep(UPDATE_FREQUENCE)
		
		self.rpc.close()