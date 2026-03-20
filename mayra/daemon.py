import threading
import keyboard
import time
import signal
import sys
from utils import load_config, query_queue, response_queue, pop_queue
from assistant import respond
from voice import activate_tone
from live_listener import start_listener

def hotkey_listener(config):
    print(f"⌨️ Hotkey '{config['hotkey']}' active")
    while True:
        if keyboard.is_pressed(config['hotkey']):
            query = input("💭 Mayra (hotkey): ")
            query_queue.put(query)
        time.sleep(0.05)

def main_loop():
    config = load_config()
    print("🚀 Mayra Live Responsive Daemon started!")
    print("👂 Always-listening for '{}', hotkey: {}".format(config['wake_word'], config['hotkey']))
    
    activate_tone()

    # Start always-listener
    listener = start_listener()

    # Start hotkey thread
    hotkey_thread = threading.Thread(target=hotkey_listener, args=(config,), daemon=True)
    hotkey_thread.start()

    try:
        while True:
            # Poll query queue (non-blocking responsive)
            try:
                query = query_queue.get(timeout=0.2)
                print(f"📤 Processing: {query}")
                threading.Thread(target=respond, args=(query,), daemon=True).start()
            except:
                pass  # No query

            # Check response queue for speak/print
            try:
                resp = response_queue.get_nowait()
                print(f"📥 Response: {resp}")
                # Speak in thread to not block
                threading.Thread(target=lambda r=resp: print("🎤 Speaking:", r), daemon=True).start()
            except:
                pass

            time.sleep(0.05)  # Responsive poll
    except KeyboardInterrupt:
        print("\n🛑 Stopping...")
        listener.stop()
    finally:
        listener.stop()
        sys.exit(0)

if __name__ == '__main__':
    main_loop()
