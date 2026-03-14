import click
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mayra.assistant import Mayra
from mayra.daemon import daemon_loop
from mayra.installer import install_auto_start
from mayra.config import load_config  # Fix import

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
            print("Mayra:", mayra.respond(query))
    else:
        print("Use --cli, --daemon, or --install")

if __name__ == "__main__":
    main()

