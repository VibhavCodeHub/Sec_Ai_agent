import platform
import os
import subprocess
from .system_utils import safe_run_cmd

def install_auto_start():
    sys = platform.system()
    if sys == 'Windows':
        # Add to Startup folder or Task Scheduler
        startup = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
        script_path = os.path.abspath(__file__).replace('installer.py', 'main.py')
        bat = f'@python "{script_path}" --daemon\npause'
        with open(os.path.join(startup, 'mayra.bat'), 'w') as f:
            f.write(bat)
        safe_run_cmd('schtasks /create /tn Mayra /tr "python mayra/main.py --daemon" /sc onlogon /rl highest', admin=True)
        print("Windows auto-start installed (Startup + TaskScheduler).")
    elif sys == 'Linux':
        # Systemd service
        service = '[Unit]\nDescription=Mayra\n[Service]\nExecStart=/usr/bin/python3 /path/to/mayra/main.py --daemon\nRestart=always\n[Install]\nWantedBy=multi-user.target'
        # Write /etc/systemd/system/mayra.service, sudo systemctl enable
        print("Create systemd unit (manual sudo).")
    else:
        print("Mac: Add to ~/Library/LaunchAgents plist (manual).")

