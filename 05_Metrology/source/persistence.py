# Klipper Metrology Extension
# Persistence operations

from typing import Dict, Any, Optional
import json
import os

def save_config(machine, filepath: str) -> bool:
    """
    Save machine configuration to file.

    Args:
        machine: Machine object to save
        filepath (str): Path to save the configuration

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        config_data = {
            "bed_origin": machine.bed_origin.as_dict(),
            "bed_size": machine.bed_size.as_dict(),
            "tool_offsets": {
                name: offset.as_dict()
                for name, offset in machine.tool_offsets.items()
            },
            "reference_tool": machine.reference_tool,
            "devices": {
                name: device.position.as_dict()
                for name, device in machine.devices.items()
            }
        }

        with open(filepath, 'w') as f:
            json.dump(config_data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False

def load_config(filepath: str) -> Optional[Dict[str, Any]]:
    """
    Load machine configuration from file.

    Args:
        filepath (str): Path to load the configuration from

    Returns:
        Optional[Dict[str, Any]]: Loaded configuration data or None if failed
    """
    try:
        if not os.path.exists(filepath):
            return None

        with open(filepath, 'r') as f:
            config_data = json.load(f)

        return config_data
    except Exception as e:
        print(f"Error loading config: {e}")
        return None
