import random # random ist eine eingebaute Bibliothek in Python, die Funktionen für die Erzeugung von Zufallszahlen und -ereignissen bereitstellt. In unserem Fall verwenden wir sie, um zufällige Ladegeschwindigkeiten, zufällige Ereignisse während der Sortierung (z.B. Überhitzung) und zufällige Gewichte für die Pakete zu generieren. Das macht unsere Simulation realistischer und spannender, da nicht immer alles nach Plan läuft.
import time # time ist eine eingebaute Bibliothek in Python, die Funktionen für die Zeitmessung und -manipulation bereitstellt. In unserem Fall verwenden wir sie, um den Ladevorgang des Roboters zu simulieren, indem wir eine kurze Pause einlegen, damit es realistischer wirkt.
import uuid # UUID (Universally Unique Identifier) ist eine eingebaute Bibliothek in Python, die es uns ermöglicht, eindeutige Identifikatoren zu erstellen. In unserem Fall verwenden wir sie, um jedem Roboter eine einzigartige ID zu geben, damit wir sie auch dann unterscheiden können, wenn sie den gleichen Namen haben. Das ist besonders wichtig in einem Szenario mit mehreren Robotern oder wenn wir den Zustand eines Roboters über die Zeit verfolgen wollen.
import xml.etree.ElementTree as ET # ET steht für ElementTree und ist eine eingebaute Bibliothek in Python, die es uns ermöglicht, XML-Daten zu erstellen, zu bearbeiten und zu speichern. In unserem Fall verwenden wir sie, um den Zustand des Fließbands in einer XML-Datei zu speichern und wieder zu laden. Das ist besonders nützlich, weil XML eine strukturierte und leicht lesbare Art der Datenspeicherung bietet, die auch von anderen Programmen oder System
from enum import Enum # Enum ist eine spezielle Klasse, die eine Gruppe von konstanten Werten definiert. In unserem Fall verwenden wir sie, um die möglichen Ergebnisse einer Arbeitsschicht zu beschreiben (z.B. ob die Sortierung erfolgreich war oder ob es Probleme gab). Das macht unseren Code lesbarer und weniger fehleranfällig, da wir nicht mit willkürlichen Strings oder Zahlen arbeiten müssen
from typing import Final #  Final ist eine Typ-Hinweis, der anzeigt, dass eine Variable nach ihrer Initialisierung nicht mehr geändert werden soll. Es ist eine Art "Konstante" in Python, die hilft, unbeabsichtigte Änderungen zu vermeiden und den Code lesbarer zu machen.
from dataclasses import dataclass #Dataclass ist eine praktische Funktion, um Klassen zu erstellen, die hauptsächlich Daten speichern. Sie generiert automatisch Methoden wie __init__ und __repr__, damit wir uns auf die Logik konzentrieren können, anstatt viel Boilerplate-Code zu schreiben.

# --- DOMAIN LAYER: Definitionen ---

class ShiftResult(Enum):
    """Beschreibt den Status nach einer Arbeitsschicht (Domain Status)."""
    COMPLETED = "completed"
    BATTERY_EMPTY = "battery_empty"
    EMERGENCY_OVERHEAT = "emergency_overheat"
    EMERGENCY_BELT_DEFECT = "emergency_belt_defect"

@dataclass(frozen=True)
class Package: 
    """
    DDD Value Object: Ein Paket ist nur durch seinen Wert (Gewicht) definiert.
    'frozen=True' macht es unveränderbar (immutable), wie eine Zahl oder ein String.
    """
    weight: int 
    
    def __repr__(self) -> str:
        return f"[{self.weight}kg]"

class WarehouseRobot:
    """
    DDD Entity: Ein Roboter hat eine eindeutige Identität (_id), 
    die über die Zeit gleich bleibt, auch wenn sich sein Akku oder Name ändert.
    """
    def __init__(self, name: str, starting_battery: int = 50) -> None:
        # Final stellt sicher, dass die ID nach der Erzeugung nicht mehr geändert wird.
        self._id: Final[uuid.UUID] = uuid.uuid4() # Jede Instanz bekommt eine einzigartige ID, damit wir sie eindeutig identifizieren können, auch wenn sie den gleichen Namen haben.
        self._name: Final[str] = name # Der Name ist ebenfalls final, da er sich nicht ändern soll. In einem echten Szen
        self._battery: int = starting_battery # Der Akku ist veränderlich, da er sich durch die Arbeit entleert und durch das Aufladen wieder füllt.
        self._is_active: bool = True # Ein einfacher Status, um zu wissen, ob der Roboter arbeiten kann oder nicht. Er könnte z.B. durch Überhitzung oder Defekte inaktiv werden.
        self._packages_sorted: int = 0 # Zählt, wie viele Pakete der Roboter bereits sortiert hat. Das ist eine Metrik für seine Leistung.

    def recharge(self) -> None:
        """Simuliert den Ladevorgang mit einer Kontrollschleife."""
        print(f"\n🔌 Ladevorgang startet (Aktueller Stand: {self._battery}%)...")
        
        for sekunde in range(1, 21): # Maximal 20 Sekunden Ladezeit, um nicht ewig zu warten
            if self._battery >= 100: # Sobald 100% erreicht sind, können wir den Ladevorgang beenden
                print(f"✅ Voll geladen nach {sekunde-1} Sekunden.")
                break # 'break' beendet die Schleife vorzeitig, wenn 100% erreicht sind
            
            # Zufällige Ladegeschwindigkeit pro Sekunde
            self._battery += random.randint(5, 15)
            if self._battery > 100:
                self._battery = 100
            
            time.sleep(0.1) # Kurze Pause zur Simulation
            
        self._is_active = True

    def sort_packages(self, belt: list[Package]) -> ShiftResult:
        """
        Der Kern-Algorithmus: Bubble Sort.
        Vergleicht benachbarte Pakete und schiebt schwere 'nach hinten'.
        """
        if not self._is_active: # Wenn der Roboter nicht aktiv ist, kann er nicht arbeiten.
           return ShiftResult.BATTERY_EMPTY    # Wir nehmen an, dass der Roboter nur inaktiv ist, wenn der Akku leer ist. In einem echten Szenario könnte es auch andere Gründe geben, aber für unsere Simulation reicht das als Annahme.
       
        n = len(belt) # Anzahl der Pakete auf dem Fließband
        
        # Äußere Schleife: Geht durch das gesamte Band
        for i in range(n):
            swapped = False # Optimierung: Wenn nichts getauscht wird, ist alles sortiert
            
            # Innere Schleife: Vergleicht Nachbarn. 
            # Mit jedem 'i' wandert das schwerste verbliebene Paket ans Ende.
            for j in range(0, n - i - 1):
                
                # 1. ZUFALLS-EVENTS (Domain Hazards)
                if random.random() < 0.02:
                    self._is_active = False
                    return ShiftResult.EMERGENCY_OVERHEAT

                # 2. ENERGIE-CHECK (Grundverbrauch für den Vergleich)
                if self._battery < 1:
                    self._is_active = False
                    return ShiftResult.BATTERY_EMPTY
                self._battery -= 1
                
                left_pkg = belt[j]
                right_pkg = belt[j + 1]
                
                #Bubble Sort: Die innere Schleife vergleicht immer j und j+1. Ist das linke Paket schwerer, 
                # "blubbert" es eine Position nach rechts.

                # 3. VERGLEICH & TAUSCH (Der eigentliche Bubble Sort)
                if left_pkg.weight > right_pkg.weight:
                    # Tauschkosten sind abhängig vom Gewicht des Pakets
                    if self._battery < left_pkg.weight:
                        self._is_active = False
                        return ShiftResult.BATTERY_EMPTY
                    
                    self._battery -= left_pkg.weight # Energie für körperliche Arbeit abziehen
                    belt[j], belt[j + 1] = belt[j + 1], belt[j] # Tausch der Pakete in der Liste 
                    swapped = True
                
            # Wenn in einem Durchlauf kein Tausch stattfand -> Fertig!
            if not swapped:
                break
                
        return ShiftResult.COMPLETED

# --- INFRASTRUCTURE LAYER: Datenspeicherung ---

class XmlPackageRepository: # Ein Repository, das sich um das Laden und Speichern von Paketen in einer XML-Datei kümmert. Es trennt die Logik der Datenspeicherung von der Logik des Roboters, was eine gute Praxis in der Softwarearchitektur ist (Separation of Concerns).
    """Repository-Pattern: Trennt die Logik (Sortieren) von der Speicherung (XML)."""
    
    def load_manifest(self, filename: str) -> list[Package]: # Lädt den aktuellen Zustand des Fließbands aus einer XML-Datei.
        packages: list[Package] = [] # Wir erstellen eine leere Liste, die wir mit Paketen füllen werden.
        try:
            tree = ET.parse(filename) # Wir versuchen, die XML-Datei zu öffnen und zu lesen. Wenn die Datei nicht existiert oder beschädigt ist, wird eine Ausnahme ausgelöst.
            root = tree.getroot() # Wir bekommen das Wurzel-Element der XML-Struktur. In unserem Fall ist das <Delivery>.
            for pkg in root.findall("Package"): # Wir suchen alle <Package>-Elemente unter <Delivery> und gehen sie einzeln durch.
                weight = int(pkg.get("weight", 0)) # Wir lesen das 'weight'-Attribut jedes <Package>-Elements aus. Wenn es nicht vorhanden ist, verwenden wir 0 als Standardwert. Wir wandeln den Wert in eine ganze Zahl um.
                packages.append(Package(weight)) # Wir erstellen ein neues Package-Objekt mit dem gelesenen Gewicht und fügen es unserer Liste 'packages' hinzu.
            print(f"📦 {len(packages)} Pakete aus {filename} geladen.") 
        except (FileNotFoundError, ET.ParseError): # Wenn die Datei nicht gefunden wird oder die XML-Struktur ungültig ist, fangen wir die Ausnahme ab.
            # FEHLERTOLERANZ: Falls Datei fehlt, erstellen wir Testdaten und starten trotzdem
            print(f"⚠️ Datei fehlt. Erstelle 10 zufällige Pakete für den Start.")
            packages = [Package(random.randint(5, 50)) for _ in range(10)] # Wir generieren 10 Pakete mit zufälligen Gewichten zwischen 5 und 50 kg, damit der Roboter etwas zu tun hat.
        return packages

    def save_manifest(self, packages: list[Package], filename: str) -> None: 
        """Schreibt den aktuellen Zustand des Fließbands zurück in die XML."""
        root = ET.Element("Delivery")
        for pkg in packages:
            ET.SubElement(root, "Package", weight=str(pkg.weight))
        tree = ET.ElementTree(root)
        tree.write(filename, encoding="utf-8", xml_declaration=True)

# --- APPLICATION LAYER: Ablaufsteuerung ---

if __name__ == "__main__":
    repo = XmlPackageRepository() # Wir erstellen eine Instanz unseres Repositories, um mit der XML-Datei zu arbeiten. Das Repository kümmert sich um das Laden und Speichern der Pakete.
    robot = WarehouseRobot("Sort-O-Matic", starting_battery=20) # Wir erstellen unseren Roboter mit einem Namen und einem Start-Akku von 20%. Das ist eine Herausforderung, damit er nicht sofort leer ist.
    
    # 1. Daten laden
    current_belt = repo.load_manifest("belt_state.xml")
    
    shift_counter = 0
    is_fully_sorted = False
    
    # 2. Hauptschleife: Der Roboter arbeitet in Schichten, bis alles sortiert ist
    while not is_fully_sorted:
        shift_counter += 1
        print(f"\n--- SCHICHT {shift_counter} STARTET ---")
        
        # Roboter für die Schicht fit machen
        robot.recharge() # Wir laden den Akku vor jeder Schicht auf, damit der Roboter genug Energie hat, um zu arbeiten. Das ist wichtig, da er sonst sofort leer wäre.
        
        # Arbeit ausführen
        result = robot.sort_packages(current_belt) # Wir rufen die Sortierfunktion auf, die den Bubble Sort Algorithmus implementiert. Sie gibt uns ein ShiftResult zurück, das uns sagt, ob die Schicht erfolgreich war oder ob es Probleme gab (z.B. Akku leer oder Überhitzung).
        
        # Ergebnis auswerten (Match-Statement für saubere Fallunterscheidung)
        match result:
            case ShiftResult.COMPLETED:
                print("✨ Sortierung erfolgreich abgeschlossen!")
                is_fully_sorted = True
            case ShiftResult.BATTERY_EMPTY:
                print("🪫 Akku leer. Feierabend für heute.")
            case _:
                print(f"🚨 KRITISCHER FEHLER: {result.name}. Techniker gerufen.")
                # Hier könnte man die Schleife auch mit 'break' abbrechen
        
        # 3. Fortschritt sichern (Persistence)
        repo.save_manifest(current_belt, "belt_state.xml") # Wir speichern den aktuellen Zustand des Fließbands nach jeder Schicht, damit wir im nächsten Durchlauf dort weitermachen können, wo wir aufgehört haben. Das ist wichtig für die Fehlertoleranz und um den Fortschritt zu dokumentieren.

    print(f"\n🏁 ZIEL ERREICHT: Alle Pakete in {shift_counter} Schichten sortiert.")