from pypresence import Presence, ActivityType
from pypresence.exceptions import DiscordNotFound, InvalidID
from dotenv import load_dotenv
import os

from godot_listener import GodotData

load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')

print("CLIENT_ID =", CLIENT_ID, type(CLIENT_ID))

class RPC:

	def __init__(self):
		self.presence = Presence(CLIENT_ID)
		self.presence.connect()

	def update(self, data: GodotData):
		try:
			self.presence.update(
				name = "Godot Engine",
				large_image = "godotdiscord.png",
				details = f"Project {data.project}",
				state = f"Edtiting scene {data.scene}",
			)
			print("updating...")
		except DiscordNotFound:
			print("Discord not Found")
		except InvalidID:
			print("Invalid Client ID")

	def clear(self):
		self.presence.clear()

	def close(self):
		self.presence.clear()
		self.presence.close()