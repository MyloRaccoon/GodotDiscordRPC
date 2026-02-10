from godot_listener import GodotListener, GodotData
from discord_RPC import RPC
import time

def on_data_changed(rpc: RPC, data: GodotData|None):
	print(data)
	if not data:
		rpc.clear()
	else:
		rpc.update(data)

if __name__ == '__main__':
	listener = GodotListener()
	rpc = RPC()
	last_data = listener.get_last_data()
	
	if last_data:
		rpc.update(last_data)

	while True:

		new_data = listener.get_last_data()

		if new_data != last_data:
			on_data_changed(rpc, new_data)
			last_data = new_data

		time.sleep(0.5)