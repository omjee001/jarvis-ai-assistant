import subprocess

def open_app(app_name):
    try:
        subprocess.run(["open", "-a", app_name], check=True)
        return f"Opening {app_name}..."
    except subprocess.CalledProcessError:
        return f"Couldn't find {app_name}."