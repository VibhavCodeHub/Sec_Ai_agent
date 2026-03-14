import os
import subprocess
import platform
import psutil
import json
import requests

def get_system_info():
    return {
        "os": platform.system(),
        "node": platform.node(),
        "cpu": platform.processor(),
        "cpu_usage": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('C:\\' if platform.system() == 'Windows' else '/').percent
    }

def list_dir(path='.'):
    try:
        return os.listdir(os.path.abspath(path))
    except PermissionError:
        return "Permission denied."

def safe_run_cmd(cmd, admin=False):
    try:
        if admin:
            # Platform-specific elevation
            sys = platform.system()
            if sys == 'Windows':
                import ctypes
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{cmd}"', None, 1)
            else:
                cmd = f'sudo {cmd}'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return result.stdout or result.stderr
    except Exception as e:
        return str(e)

def web_query(query):
    try:
        # Simple duckduckgo or weather api
        if 'weather' in query.lower():
            city = query.split()[-1]
            url = f"http://wttr.in/{city}?format=j1"
            resp = requests.get(url).json()
            return resp['current_condition'][0]['temp_C']
        else:
            url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1&skip_disambig=1"
            resp = requests.get(url).json()
            return resp.get('Abstract', 'No info.')
    except:
        return "Web error."

