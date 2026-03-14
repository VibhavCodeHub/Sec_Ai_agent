import click
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


# from mayra.utils import load_config  # Fixed path issue

from assistant import Mayra
from daemon import daemon_loop
from installer import install_auto_start
def load_config():
    import json
    with open('mayra/config.json', 'r') as f:
        return json.load(f)

@click.command()
@click.option('--cli', is_flag=True, help='CLI mode')
@click.option('--daemon', is_flag=True, help='Daemon mode')
@click.option('--install', is_flag=True, help='Install auto-start')
def main(cli, daemon, install):
    config = load_config()
    mayra = Mayra(config)
    
    if install:
        install_auto_start()
        return
    
    if daemon:
        daemon_loop()
        return
    
    if cli:
        while True:
            query = input("You: ")
            if query.lower() == 'exit':
                break
            try:
                from voice import response_tone
                response_tone()
            except:
                pass
            print("Mayra:", mayra.respond(query))
    else:
        print("Use --cli, --daemon, or --install")

if __name__ == "__main__":
    main()

