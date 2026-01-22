#!/usr/bin/env python3
import time
import psutil
from pypresence import Presence

#   CONFIGURATION HERE!! LOOK AT THIS.
#   Go to https://discord.com/developers/applications
#   Create a new app, customize it, then copy the "Application ID" here.
CLIENT_ID = "123456767676969"

#   What process(s) are we looking for?
#   you can find this by running "top" or "htop" in your terminal.
#   add multiple names to cover different versions (e.g., 'firefox', 'firefox.exe')
PROCESS_NAMES = ["1", "2", "3", "4"]

#   what should the status say?
RPC_DETAILS = {
    "details": "Playing a Game",       # top line
    "state": "custom rpc by Asa-DB on github",    # bottom line
    "large_image": "main_logo",        # name of image in 'art assets'
    "large_text": "Cool Game",      # hover text for large image
    "small_image": "playing_icon",     # name of image in 'art Assets' (optional)
    "small_text": "In Game"            # hover text for small image
}

# REFRESH RATE how often (in seconds) to check if the app is running
POLL_INTERVAL = 15

def is_process_running():
    """Scans running processes for any name in PROCESS_NAMES."""
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] in PROCESS_NAMES:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def main():
    print(f"Waiting for {PROCESS_NAMES}...")

    rpc = Presence(CLIENT_ID)
    connected = False
    start_time = None

    while True:
        try:
            if not connected:
                try:
                    rpc.connect()
                    connected = True
                    print("connected to discord!")
                except Exception:
                    time.sleep(5)
                    continue

            if is_process_running():
                if start_time is None:
                    start_time = int(time.time())
                    print(f"Detected {PROCESS_NAMES}! updating status...")

                    rpc.update(
                        details=RPC_DETAILS["details"],
                        state=RPC_DETAILS["state"],
                        large_image=RPC_DETAILS["large_image"],
                        large_text=RPC_DETAILS["large_text"],
                        small_image=RPC_DETAILS["small_image"],
                        small_text=RPC_DETAILS["small_text"],
                        start=start_time
                    )
            else:
                if start_time is not None:
                    print("Process closed. Clearing status.")
                    rpc.clear()
                    start_time = None

        except Exception as e:
            print(f"Error: {e}. Reconnecting...")
            connected = False
            start_time = None

        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
