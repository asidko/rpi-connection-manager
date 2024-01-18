import logging
import subprocess
from dataclasses import asdict

import yaml
from config import Config, WiFiNetwork


def load_wifi_config() -> Config:
    try:
        with open('config.yaml', 'r') as file:
            config_dict = yaml.safe_load(file)
            wifi_networks = [WiFiNetwork(**nw) for nw in config_dict['wifi_networks']]
            hotspot = WiFiNetwork(**config_dict['hotspot'])
            return Config(wifi_networks=wifi_networks, hotspot=hotspot)
    except FileNotFoundError:
        logging.debug("config.yaml not found, creating a default config.")
        config = Config()
        with open('config.yaml', 'w') as file:
            yaml.dump(asdict(config), file)
        return config


def check_internet_connection() -> bool:
    try:
        subprocess.check_call(['ping', '-c', '1', 'google.com'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        logging.debug("Internet connection successful.")
        return True
    except subprocess.CalledProcessError:
        logging.debug("No internet connection.")
        return False


def get_wifi_interfaces() -> list[str]:
    try:
        output = subprocess.check_output(['iwconfig'], stderr=subprocess.STDOUT).decode()
        return [line.split()[0] for line in output.splitlines() if 'IEEE 802.11' in line]
    except subprocess.CalledProcessError:
        logging.debug("Error getting WiFi interfaces.")
        return []


def get_public_ip():
    return subprocess.check_output(['curl', 'ifconfig.me']).decode().strip()


def get_local_ip():
    try:
        return subprocess.check_output(['hostname', '-I']).decode().strip()
    except subprocess.CalledProcessError:
        try:
            return subprocess.check_output(['ipconfig', 'getifaddr', 'en0']).decode().strip()
        except subprocess.CalledProcessError:
            return "No local IP found"


def safe_quotes(s: str) -> str:
    # Remove ' quotes if present + wrap with ' quotes
    fixed_str = s.replace("'", "")
    return "'" + fixed_str + "'" if fixed_str else ""
