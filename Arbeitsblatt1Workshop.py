"""
Arbeitsblatt 1: JSON, Enums und Exceptions
Dein Ziel: Den Roboter-Status in ein Dictionary (Telefonbuch) packen, sicher speichern (Postweiche) und beim Laden Fehler abfangen (Sicherheitsnetz).
"""
import random
import time
import json
import yaml
import xml.etree.ElementTree as ET
from enum import Enum
from typing import Final, Any

# TODO 1: Erstelle ein Enum namens 'SaveFormat' (Dein Dropdown-Menü)
# Es soll aktuell nur einen Wert geben: JSON = "json"
class SaveFormat(Enum):
    JSON = "json"
    XML = "xml"
    YAML = "yaml"

class WarehouseRobot:
    def __init__(self, name: str, max_battery: int = 100) -> None:
        self._name: Final[str] = name
        self._battery: int = max_battery
        self._is_active: bool = True
        self._packages_sorted: int = 0

    def sort_packages(self) -> None:
        if not self._is_active: return
        cost = random.randint(10, 25)
        if self._battery >= cost:
            self._battery -= cost
            self._packages_sorted += 1
            print(f"✅ Paket sortiert. Akku: {self._battery}%")
        else:
            self._is_active = False

    def save_state(self, base_filename: str, format_type: SaveFormat) -> None:
        """Speichert den Zustand auf der Festplatte."""
        # TODO 2: Erstelle ein Dictionary 'state' mit den Schlüsseln
        # "name", "battery" und "packages_sorted". (Wie ein Telefonbuch)
        state: dict[str, Any] = {
            "name": self._name,
            "battery": self._battery,
            "packages_sorted": self._packages_sorted} # <-- Hier anpassen

        full_filename = f"{base_filename}.{format_type.value}"

        # TODO 3: Baue die Postweiche (Match-Case) auf Basis von 'format_type'
        # case SaveFormat.JSON:
        #    öffne die Datei ('w' für schreiben) und nutze json.dump(state, file)
        match format_type:
            case SaveFormat.JSON:
                with open(full_filename, 'w') as file:
                    json.dump(state, file, indent=4)
                print(f"write succesfull: {full_filename}")
                
            case SaveFormat.YAML:
                with open(full_filename, "w") as file:
                    yaml.dump(state, file, default_flow_style=False)
                print(f"write succesfull: {full_filename}")  
                  
            case SaveFormat.XML:
                root = ET.Element("RobotState")
                ET.SubElement(root, "Name").text = str(state["name"])
                ET.SubElement(root, "Battery").text = str(state["battery"])
                ET.SubElement(root, "Packages").text = str(state["packages_sorted"])
                tree = ET.ElementTree(root)
                tree.write(full_filename, encoding="utf-8", xml_declaration=True)
                print(f"write succesfull: {full_filename}") 
              
                pass
            
            case _: # Das fängt alles andere ab
                print(f"Format {format_type} does not exist yet.")
                    
                    
                    

    def load_state(self, filename: str) -> None:
        """Lädt den Zustand aus einer Datei."""
        # TODO 4: Baue ein Sicherheitsnetz (try-except Block)!
        # PLAN A (try): Öffne die Datei ('r' für lesen) und lade sie mit json.load(file).
        # Aktualisiere self._battery und self._packages_sorted mit den gelesenen Daten!
        try:
            with open(filename, 'r') as file:
                state = json.load(file)
                self._battery = state.get("battery", 100)
                self._packages_sorted = state.get("packages_sorted")
                print(f"State Loaded! Previously sorted {self._packages_sorted}")
        except FileNotFoundError:
            # PLAN B (except FileNotFoundError): Gib eine nette Warnung aus ("Tagebuch fehlt, starte neu"), anstatt abzustürzen.
            print("⚠️ Tagebuch fehlt, starte neu")

if __name__ == "__main__":
    bot = WarehouseRobot("Wall-E")

    # Lade das Gedächtnis
    bot.load_state("savegame.json")

    # Arbeite
    bot.sort_packages()
    bot.sort_packages()

    # Speichere als JSON
    bot.save_state("savegame", SaveFormat.JSON) # <-- Einkommentieren, wenn TODOs fertig!
    bot.save_state("savegame", SaveFormat.YAML)
    bot.save_state("savegame", SaveFormat.XML)
  