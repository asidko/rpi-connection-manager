from dataclasses import dataclass, field
from typing import List


@dataclass
class WiFiNetwork:
    ssid: str = "abc"
    password: str = "12345678"


@dataclass
class Config:
    wifi_networks: List[WiFiNetwork] = field(default_factory=lambda: [WiFiNetwork()])
    hotspot: WiFiNetwork = field(default_factory=lambda: WiFiNetwork(ssid="xpp", password="88888888"))