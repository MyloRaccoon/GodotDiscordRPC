from pystray import Icon, Menu, MenuItem
from PIL import Image
import threading
from server import Server
import os, sys

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

stop_event = threading.Event()

server = Server()

def on_quit_clicked(icon, item):
    stop_event.set()
    icon.stop()

icon = Icon(
    name='Godot RPC',
    icon= Image.open("godotdiscord.png"),
    menu=Menu(
        MenuItem("quit", on_quit_clicked)
    )
)

threading.Thread(
    target=server.run,
    args=(stop_event,),
    daemon=True
).start()

icon.run()