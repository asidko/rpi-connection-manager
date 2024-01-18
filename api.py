import os

from fastapi import FastAPI, HTTPException
from starlette.staticfiles import StaticFiles

from typing import Optional

from actions import try_to_connect_to_known_networks, create_wifi_hotspot, connect_to_wifi, get_wifi_visible_list, \
    restart_network_manager
from utils import load_wifi_config, get_wifi_interfaces
from utils import get_local_ip, get_public_ip
from fastapi.responses import FileResponse

app = FastAPI()

current_dir = os.path.dirname(os.path.realpath(__file__))
app.mount("/ui", StaticFiles(directory=os.path.join(current_dir, 'static')), name="ui")


@app.get("/")
async def read_index():
    return FileResponse('ui/index.html')


@app.get("/switch_to_wifi")
async def switch_to_wifi():
    config = load_wifi_config()
    wifi_interfaces = get_wifi_interfaces()
    if not wifi_interfaces:
        raise HTTPException(status_code=400, detail="No WiFi interfaces found.")
    ssid = try_to_connect_to_known_networks(config, wifi_interfaces[0])
    return {"message": f"Switched to WiFi {ssid}"}


@app.get("/get_wifi_list")
async def get_wifi_list():
    wifi_list = get_wifi_visible_list()
    return {"wifi_list": wifi_list}


@app.get("/restart_network_manager")
async def do_restart_network_manager():
    restart_network_manager()
    return {"message": "Network manager restarted."}


@app.get("/switch_to_hotspot")
async def switch_to_hotspot():
    config = load_wifi_config()
    wifi_interfaces = get_wifi_interfaces()
    wifi_interface = wifi_interfaces[1] if len(wifi_interfaces) > 1 else wifi_interfaces[0]
    create_wifi_hotspot(wifi_interface, config.hotspot.ssid, config.hotspot.password)
    return {"message": f"Switched to Hotspot mode. Look for SSID: {config.hotspot.ssid}"}


@app.get("/connect_to_wifi")
async def do_connect_to_wifi(ssid: Optional[str] = None, password: Optional[str] = None):
    if not ssid or not password:
        raise HTTPException(status_code=400, detail="SSID and password required")
    connected = connect_to_wifi(ssid, password)
    return {"message": f"Connected to {ssid}" if connected else f"Failed to connect to {ssid}"}


@app.get("/get_ip_addresses")
async def get_ip_addresses():
    return {
        "local_ip": get_local_ip(),
        "public_ip": get_public_ip()
    }


def main():
    import uvicorn

    print("Starting the server. Swagger UI available at http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == '__main__':
    main()
