"""
Workshop Aufgabe: BubbleSort & DDD (90 Min)
Ziel: Value Objects (@dataclass), Entitäten (UUID), XML laden, Break, Bubble Sort.
"""
from fileinput import filename
import random
import time
import uuid
import xml.etree.ElementTree as ET
from enum import Enum
from typing import Final
# WICHTIG: Importiere dataclass
from dataclasses import dataclass

class ShiftResult(Enum):
    COMPLETED = "completed"
    BATTERY_EMPTY = "battery_empty"
    EMERGENCY_OVERHEAT = "emergency_overheat"
    EMERGENCY_BELT_DEFECT = "emergency_belt_defect"

# TODO 1: Value Object (Wertobjekt) erstellen
# Nutze den Decorator @dataclass(frozen=True) über der Klasse 'Package'.
# Schreibe als einzige Zeile in die Klasse: weight: int
@dataclass(frozen=True)
class Package:
    weight: int 
    
    def __repr__(self) -> str:
        return f"[{self.weight}kg]"

class WarehouseRobot:
    def __init__(self, name: str, starting_battery: int = 50) -> None:
        # TODO 2: Die Identität der Entität (Der Ausweis)
        self._id: Final[uuid] = uuid.uuid4()
        self._name: Final[str] = name
        self._battery: int = starting_battery
        self._is_active: bool = True
        # Erzeuge eine UUID mit uuid.uuid4() und weise sie der internen 
        # Variable self._id zu. (Typisierung: Final)
        
        self._name: Final[str] = name
        self._battery: int = starting_battery
        self._is_active: bool = True

    def recharge(self) -> None:
        print(f"\n🔌 Ladevorgang startet (Akku: {self._battery}%)...")
        
        # TODO 4: Das intelligente Aufladen (For-Schleife & Break)
        # 1. Baue eine for-Schleife für 20 Sekunden: for sekunde in range(1, 21):
        for sekunde in range(1, 21):
            if self._battery >= 100:
                self._battery = 100
                print(f"100% erreicht! Ladevorgang gestoppt nach {sekunde -1} Sekunden.")
            self._battery += random.randint(1, 5)
            if self._battery > 100:
                self._battery = 100
                print(f"100% erreicht! Ladevorgang gestoppt nach {sekunde} Sekunden.")
            time.sleep(1,0) # Simuliere die Ladezeit mit time.sleep(1)
        self._is_active = True
        print(f"Ladevorgang beendet.")

    def sort_packages(self, belt: list[Package]) -> ShiftResult:
        if not self._is_active:
           return ShiftResult.BATTERY_EMPTY    
       
        n = len(belt)
        print(f"{self._name} startet die Sortierung von {n} Paketen ")
        # TODO 5: Bubble Sort Schleifen bauen.
        # Outer Loop: for i in range(n)
        # Inner Loop: for j in range(0, n - i - 1)
        
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                
                # ZUFALLS-EVENTS (Notaus)
                hazard = random.random()
                if hazard < 0.01:
                    self._is_active = False
                    return ShiftResult.EMERGENCY_OVERHEAT
                elif hazard < 0.02:
                    self._is_active = False
                    return ShiftResult.EMERGENCY_BELT_DEFECT

                # TODO 6: Energie für den VGL prüfen
                if self._battery < 1:
                    self._is_active = False
                    return ShiftResult.BATTERY_EMPTY
                
                self._battery -= 1
                # Wenn _battery < 1, setze _is_active auf False und 
                # gib ShiftResult.BATTERY_EMPTY zurück!
                # Sonst: Ziehe 1 von _battery ab.
                left_pkg = belt[j]
                right_pkg = belt[j + 1]

                # TODO 7: Der schwere Tausch
                if left_pkg.weight > right_pkg.weight:
                    if self._battery < left_pkg.weight:
                        swap_cost = left_pkg.weight
                        if self._battery < swap_cost:
                            self._is_active = False
                            return ShiftResult.BATTERY_EMPTY
                    self._battery -= left_pkg.weight
                    belt[j], belt[j + 1] = belt[j + 1], belt[j]
                    swapped = True
                    
                # WENN das Gewicht von left_pkg > right_pkg ist:
                #   1. Prüfe, ob _battery < left_pkg.weight ist (Wenn ja -> BATTERY_EMPTY)
                #   2. Ziehe left_pkg.weight vom _battery ab.
                #   3. Tausche die Pakete im 'belt' (belt[j], belt[j+1] = belt[j+1], belt[j])
                #   4. Setze swapped auf True
                
                
            if not swapped:
                return ShiftResult.COMPLETED
                
        return ShiftResult.COMPLETED

class XmlPackageRepository:
    def load_manifest(self, filename: str) -> list[Package]:
        packages: list[Package] = [ET.parse(filename)]
        try:
            tree = ET.parse(filename)
            root = tree.getroot()
            for pkg in root.findall("Package"):
                weight_str = pkg.get("weight")
                if weight_str is not None:
                    try:
                        weight = int(weight_str)
                        packages.append(Package(weight))
                    except ValueError:
                        print(f"Ungültiges Gewicht '{weight_str}' in XML. Paket übersprungen.")
                else:
                    print("Fehlendes 'weight' Attribut in einem Package. Paket übersprungen.")
        except FileNotFoundError:
            print(f"Fehler: Datei {filename} nicht gefunden.")
        except ET.ParseError:
            print(f"Fehler: XML-Format in {filename} ist korrupt.")
        

        # TODO 3: Lade die XML mit ET.parse(), suche alle "Package" Tags.
        # Hole das Attribut 'weight', wandle es in einen 'int' um und 
        # füge ein neues Package(weight) zur Liste hinzu. (Nutze try-except!)
        return packages

    def save_manifest(self, packages: list[Package], filename: str) -> None:
        root = ET.Element("Delivery")
        for pkg in packages:
            ET.SubElement(root, "Package", weight=str(pkg.weight))
        tree = ET.ElementTree(root)
        tree.write(filename, encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    repo = XmlPackageRepository()
    robot = WarehouseRobot("Sort-O-Matic", starting_battery=20)
    current_belt = repo.load_manifest("belt_state.xml")
    
    shift_counter = 0
    is_fully_sorted = False
    
    while not is_fully_sorted:# Baue eine 'while not is_fully_sorted:' Schleife.
        shift_counter += 1# 1. Zähle shift_counter hoch.
    # 2. Lade den Roboter auf (recharge).
        robot.recharge()
    # 3. Rufe result = robot.sort_packages(current_belt) auf.
        result = robot.sort_packages(current_belt)
    # 4. Baue einen 'match result:' Block:
    match result:
        case ShiftResult.COMPLETED:
            is_fully_sorted = True
    #    case ShiftResult.COMPLETED: Setze is_fully_sorted = True
        case ShiftResult.BATTERY_EMPTY: print("Akku leer!")
    #    case ShiftResult.BATTERY_EMPTY: Print "Akku leer!"
        case ShiftResult.EMERGENCY_OVERHEAT: print("Überhitzung!") 
    #    case ShiftResult.EMERGENCY_OVERHEAT: Print "Überhitzung!"
        case ShiftResult.EMERGENCY_BELT_DEFECT: print("Band defekt!")
    #    case ShiftResult.EMERGENCY_BELT_DEFECT: Print "Band defekt!"
    
    # 5. Speichere current_belt via repo.save_manifest ab!
    repo.save_manifest(current_belt, "belt_state.xml")

    print(f"\n🎉 FEIERABEND! Alle Pakete in {shift_counter} Schichten sortiert.")