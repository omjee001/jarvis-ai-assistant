import subprocess


def run_terminal_command(command):
    """
    Executes safe terminal commands or opens the terminal.
    """
    cmd = command.strip()

    if not cmd or cmd.lower() in ["open terminal", "terminal"]:
        subprocess.run(["open", "-a", "Terminal"])
        return "Opening Terminal."

    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
        output = result.stdout.strip() or result.stderr.strip()
        if output:
            lines = output.splitlines()
            # Truncate to first 3 lines for voice clarity
            voice_summary = " ".join(lines[:3])
            return f"Command output: {voice_summary}"
        return "Command completed with no output."
    except subprocess.TimeoutExpired:
        return "Command timed out."
    except Exception as e:
        return f"Failed to execute command: {e}"
