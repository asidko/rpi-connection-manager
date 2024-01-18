import logging
from utils import load_wifi_config, get_wifi_interfaces, check_internet_connection
from actions import try_to_connect_to_known_networks, create_wifi_hotspot

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def main() -> None:
    config = load_wifi_config()
    wifi_interfaces = get_wifi_interfaces()

    if not wifi_interfaces:
        logging.info("No WiFi interfaces found.")
        return

    internet_connected = check_internet_connection()

    # Connect to internet if possible
    if not internet_connected:
        logging.info("No internet connection found. Trying to connect to known networks.")
        internet_connected = try_to_connect_to_known_networks(config, wifi_interfaces[0])

    # Create hotspot if no internet connection and possible
    if not internet_connected and wifi_interfaces:
        logging.info("No internet connection possible. Creating hotspot.")
        wifi_interface = wifi_interfaces[1] if len(wifi_interfaces) > 1 else wifi_interfaces[0]
        create_wifi_hotspot(wifi_interface, config.hotspot.ssid, config.hotspot.password)

    # Additional functionality can be added here as needed


if __name__ == "__main__":
    main()
    from api import main as api_main
    api_main()
