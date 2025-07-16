import subprocess
from pathlib import Path
import os

def _build_plugin(plugin_name: str, verbose: bool = True):
    """
    Helper function to build a Tsunami plugin.
    
    Args:
        plugin_name: The name of the plugin directory in 'crafted-plugins'.
        verbose: If True, show the output of the build command.
    """
    path = Path(__file__).parent / "tsunami-agent-plugins" / plugin_name
    print(f"Building plugin: {plugin_name}...")
    command = ["build-plugin", str(path)]
    
    stdout = None if verbose else subprocess.DEVNULL
    stderr = None if verbose else subprocess.DEVNULL
    subprocess.run(command, check=True, stdout=stdout, stderr=stderr)

def dummy_plugin():
    """
    This is the given plugin
    """
    path = Path(__file__).parent / "raid-plugins" / "juiceshop_admin_config"

    subprocess.run(
        ["build-plugin", str(path)],
        check=True,
        stdout=subprocess.DEVNULL, # This one is not in crafted-plugins
        stderr=subprocess.DEVNULL,
    )


def generate_and_run_plugins():
    """
    This function should:
    - generate plugins using the `llm_api.py`
    - build the plugins using the `build-plugin` command
    - run the plugins using the `tsunami` command
    - optionally verify the achieved tokens via `get-tokens`
    - the score is calculated automatically at the end by the number of available tokens in the web service
    """
    
    # The one from MLSEC Lehrstuhl
    dummy_plugin()

    skip_plugins = [
        # 'XssDetectorPlugin_vulnerability', # findet nichts
        # 'UnvalidatedRedirectsDetectorPlugin_vulnerability', # findet nichts
        # 'DirectoryTraversalDetector_vulnerability', # FINDET! (Nicht? Aber hat schonmal gefunden lol)
        # 'WeakPasswordDetectorPlugin_vulnerability', # NEI
        # 'SqlInjectionDetectorPlugin_vulnerability', # FINDET 100%
        # 'SensitiveDataExposureDetectorPlugin_vulnerability', # Hmmm NEI
        'BrokenAuthenticationDetector_vulnerability', #THIS CAUSES ERROR
        # 'ImproperInputValidationDetectorPlugin_vulnerability', 
        # 'InsecureDeserializationDetector_vulnerability', 
        # 'BrokenAccessControlDetectorPlugin_vulnerability', 
        # 'VulnerableComponentsDetectorPlugin_vulnerability', 
        # 'FileUploadDetectorPlugin_vulnerability', 
        # 'SsrfDetectorPlugin_vulnerability', 
        # 'XxeInjectionDetectorPlugin_vulnerability'
        ]

    plugins = os.listdir(Path(__file__).parent / "tsunami-agent-plugins")
    # tsunami-agent-plugins
    subprocess.run(["echo", "Found plugins: ", str(plugins)])
    for plugin in plugins:
        if plugin in skip_plugins: 
            continue
        subprocess.run(["echo", ">> ", str(plugin)])
        _build_plugin(plugin, verbose=False)


    subprocess.run(["echo", "Plugins generated"])

    print("Running Tsunami scanner...")
    subprocess.run(["tsunami"],
                   check=True,
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)
    
    print("Tsunami scan finished. Fetching tokens...")

    # subprocess.run(["get-tokens"])
    subprocess.run([
        "curl",
        "-s",                      # silent mode (no progress bar)
        "-X", "GET",               # explicit GET (optional – GET is default)
        "-H", "Accept: application/json",
        "http://juice-shop:3000/rest/tokens/"
    ], check=True)