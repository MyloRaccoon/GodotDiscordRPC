from pypresence import Presence, ActivityType
from pypresence.exceptions import DiscordNotFound, InvalidID
from pypresence.types import ActivityType
from dotenv import load_dotenv
from logger import log
import os

from godot_listener import GodotData

load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')

class RPC:

	def __init__(self):
		self.presence = Presence(CLIENT_ID)
		self.connected = False
		self.try_connect()

	def try_connect(self):
		try:
			self.presence.connect()
			self.connected = True
		except DiscordNotFound:
			log("ERROR: counld't connect to discord")

	def update(self, data: GodotData):
		if not self.connected: self.try_connect()
		if not self.connected: 
			log("Couldn't update RPC: not connected")
			return
		try:
			resp = self.presence.update(
				name = "Godot Engine",
				activity_type=ActivityType.PLAYING,
				large_image = "godotdiscord.png",
				details = f"Project {data.project}",
				state = f"Edtiting scene {data.scene}",
			)
			log(f"updating: {resp}")
		except DiscordNotFound:
			log("Discord not Found")
		except InvalidID:
			log("Invalid Client ID")

	def clear(self):
		if not self.connected: 
			log("Couldn't clear RPC: not connected")
			return
		self.presence.clear()

	def close(self):
		if not self.connected: 
			log("Couldn't close RPC: not connected")
			return
		self.presence.clear()
		self.presence.close()