import logging
import subprocess
import time
from config import Config
from utils import check_internet_connection, safe_quotes


def get_wifi_visible_list() -> list[str]:
    try:
        subprocess.check_call(['sudo', 'nmcli', 'dev', 'wifi', 'rescan'])
        output = subprocess.check_output(['nmcli', 'dev', 'wifi']).decode()
        return [line.split()[1] for line in output.splitlines() if '*' not in line]
    except subprocess.CalledProcessError:
        logging.error("Error getting WiFi visible list.")
        return []


def restart_network_manager() -> None:
    try:
        subprocess.check_call(['sudo', 'systemctl', 'restart', 'NetworkManager'])
        logging.info("Network manager restarted.")
    except subprocess.CalledProcessError:
        logging.error("Error restarting network manager.")


def connect_to_wifi(ssid: str, password: str) -> bool:
    try:
        ssid_safe = safe_quotes(ssid).strip()[:32]
        password_safe = safe_quotes(password)[:63]
        subprocess.check_call(['sudo', 'nmcli', 'dev', 'wifi', 'connect', ssid_safe, 'password', password_safe])
        logging.info(f"Connected to WiFi network: {ssid}")
        return True
    except Exception as e:
        logging.error(f"Failed to connect to WiFi network: {ssid} - {e}")
        return False


def create_wifi_hotspot(interface: str, ssid: str, password: str) -> None:
    try:
        subprocess.call(
            ['sudo', 'nmcli', 'dev', 'wifi', 'hotspot', 'ifname', interface, 'ssid', ssid, 'password', password])
        logging.info(f"Created WiFi hotspot: {ssid} on interface {interface}")
    except Exception as e:
        logging.error(f"Failed to create WiFi hotspot: {e}")


def try_to_connect_to_known_networks(config: Config, wifi_interface: str) -> str:
    for network in config.wifi_networks:
        logging.debug(f"Trying to connect to {network.ssid}")
        if connect_to_wifi(network.ssid, network.password):
            logging.info(f"Connected to {network.ssid} using {wifi_interface}")
            time.sleep(5)
            if check_internet_connection():
                return network.ssid
    return ''
