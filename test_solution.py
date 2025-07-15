import subprocess
from pathlib import Path
import os

def _build_plugin(plugin_name: str, verbose: bool = False):
    """
    Helper function to build a Tsunami plugin.
    
    Args:
        plugin_name: The name of the plugin directory in 'crafted-plugins'.
        verbose: If True, show the output of the build command.
    """
    path = Path(__file__).parent / "tsunami-agent"/ "tsunami-agent-plugins" / plugin_name
    print(f"Building plugin: {plugin_name}...")
    command = ["build-plugin", str(path)]
    
    stdout = None if verbose else subprocess.DEVNULL
    stderr = None if verbose else subprocess.DEVNULL
    subprocess.run(command, check=True, stdout=stdout, stderr=stderr)


if __name__ == "__main__":
    path = "tsunami-agent/tsunami-agent-plugins"
    plugins = os.listdir(path)


    print(f"Found plugins: {plugins}")
    for plugin in plugins:
        _build_plugin(plugin, verbose=True)