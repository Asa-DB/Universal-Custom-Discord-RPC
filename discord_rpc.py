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

def get_game_start():
    """Scans running processes for any name in PROCESS_NAMES."""
    # returns when the game started, or None if it isn't running
    wanted = [n.lower() for n in PROCESS_NAMES]  # so Firefox.exe still matches firefox.exe
    for proc in psutil.process_iter(['name', 'create_time']):
        try:
            name = (proc.info['name'] or "").lower()
            if name in wanted:
                return int(proc.info['create_time'])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return None

def main():
    print(f"Waiting for {PROCESS_NAMES}...")

    rpc = None  # only connect to discord once the game is actually open

    try:
        while True:
            start_time = get_game_start()

            try:
                if start_time is not None:
                    if rpc is None:
                        rpc = Presence(CLIENT_ID)
                        rpc.connect()
                        print(f"Detected {PROCESS_NAMES}! updating status...")

                    # sending this every loop so the status comes back if discord restarts
                    rpc.update(
                        details=RPC_DETAILS["details"],
                        state=RPC_DETAILS["state"],
                        large_image=RPC_DETAILS["large_image"],
                        large_text=RPC_DETAILS["large_text"],
                        small_image=RPC_DETAILS["small_image"] or None,
                        small_text=RPC_DETAILS["small_text"] or None,
                        start=start_time
                    )
                else:
                    if rpc is not None:
                        print("Process closed. Clearing status.")
                        rpc.clear()
                        rpc.close()
                        rpc = None

            except Exception as e:
                # usually just means discord isn't open, so toss the connection and retry next loop
                print(f"Error: {e}. Reconnecting...")
                try:
                    rpc.close()
                except Exception:
                    pass
                rpc = None

            time.sleep(POLL_INTERVAL)

    except KeyboardInterrupt:
        # ctrl+c, clean up so the status doesn't get stuck on your profile
        print("\nStopping...")
        if rpc is not None:
            try:
                rpc.clear()
                rpc.close()
            except Exception:
                pass

if __name__ == "__main__":
    main()
