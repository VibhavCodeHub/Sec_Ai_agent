import click
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import load_config
from daemon import main_loop as daemon_loop
from installer import install_auto_start
from live_listener import start_listener
from assistant import respond
from voice import speak

@click.command()
@click.option('--cli', is_flag=True, help='CLI mode (blocking)')
@click.option('--daemon/--no-daemon', default=True, help='Live daemon mode (default)')
@click.option('--live', is_flag=True, help='Live always-listen CLI mode')
@click.option('--install', is_flag=True, help='Install auto-start')
def main(cli, daemon, live, install):
    config = load_config()
    
    if install:
        install_auto_start()
        return
    
    if daemon:
        daemon_loop()
        return
    
    print("🚀 Mayra Live AI ready!")
    
    if live:
        # Live CLI with always-listener
        listener = start_listener()
        try:
            while True:
                query = input("💭 You: ")
                if 'exit' in query.lower():
                    break
                resp = respond(query)
                print("Mayra:", resp)
        finally:
            listener.stop()
    elif cli:
        # Legacy blocking CLI
        while True:
            query = input("💭 You: ")
            if 'exit' in query.lower():
                break
            resp = respond(query)
            print("Mayra:", resp)
    else:
        print("Use --daemon (default), --live, --cli, or --install.")

if __name__ == "__main__":
    main()
