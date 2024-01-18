# RPI Connection manager

This project has a simple purpose: to make sure you can always connect to your RPI device event when there's no known WiFi available.

It creates a service that will start on boot and check:

- If there's a known WiFi available, it will connect to it
- If there's no known WiFi available, it will create a hotspot

Additionally, it creates a simple web interface that allows you to:
- See the current IP and visible WiFi networks
- Manually change mode (hotspot or WiFi)
- Manually change WiFi network

<img alt="Interface | Get IP" src="https://github.com/asidko/asidko/assets/22843881/6bf3c22e-3b87-445a-bd8a-d764dce3dc45">

## Installation

1. Clone this repository
2. Run `sudo ./install.sh`

To uninstall, run `sudo ./uninstall.sh`

## Configuration

After the installation (first run) configuration file `config.yaml` will be automatically created in project directory. You can edit it to change the default settings.

There are two main sections there, 'hotspot' to set up hotspot name and password, and 'wifi' to set up known WiFi networks to connect to.

Example config:
```yaml
hotspot:
  password: 88888888
  ssid: xpp
wifi_networks:
- password: sKNUv9NgjfixKLf1
  ssid: abc
```

## Usage

Go to `http://<your_rpi_ip>:8080` to see the interface.

<img alt="Interface | Wifi list" src="https://github.com/asidko/asidko/assets/22843881/ac29104e-1f08-488f-beb4-5f737c174cbe">

Go to `http://<your_rpi_ip>:8080/docs` to check the API endpoints.

<img  alt="Open API" src="https://github.com/asidko/asidko/assets/22843881/35397bf6-9ebb-48c2-abd7-4ad9d72f21a1">


**FAQ**

How do I know my RPI IP to open web interface?
    
If it's connected to a WiFi, you can check the IP in your router settings at the connected devices list page.

If a device is in hotspot mode, connect to it and check the IP in your network settings, in my case it's: 10.42.0.1

