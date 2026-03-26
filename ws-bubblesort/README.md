# Warehouse Robot - Der schwere Algorithmus (Bubble Sort & DDD)

Willkommen zum Workshop-Repository! In diesem Projekt bauen wir die intelligente Steuerungssoftware für einen autonomen Logistik-Roboter.

## Lernziele dieses Workshops

- **Domain-Driven Design (DDD)**: Saubere Trennung und Implementierung von Entitäten (Roboter mit eindeutiger `UUID`) und Wertobjekten (`@dataclass` für Pakete).
- **Algorithmen**: Verständnis und Implementierung eines Bubble Sorts, erweitert um variable, dynamische Energiekosten.
- **Kontrollstrukturen**: Intelligentes Aufladen durch `for`-Schleifen und break, sowie die finale Schichtauswertung mit `match...case`.
- **Datenpersistenz**: Einlesen und manipulationssicheres Speichern des Lagerzustands mittels XML (`xml.etree.ElementTree`).
---
## Systemvoraussetzungen
- **Betriebssystem**: Ubuntu 24.04 LTS (oder vergleichbares Linux/macOS)
- **Python**: Version 3.13
- **IDE**: Visual Studio Code (VSCode) empfohlen
---
## Setup & Installation
1. **Repository klonen & in den Workshop-Ordner navigieren:**
    Lade dir zuerst das Repository des Dualis-Instituts herunter und wechsle direkt in den richtigen Arbeitsordner:
    `git clone https://github.com/DualisInstitut/p2-python-dice-game-student.git`
    `cd p2-python-dice-game-student/ws-bubblesort`


2. **Virtuelle Umgebung (venv) erstellen & aktivieren:**
    Damit wir unser System sauber halten, arbeiten wir in einer isolierten Umgebung:
    `python3.13 -m venv.venv`
    `source.venv/bin/activate`

3. **Vorbereitungsdaten prüfen:**
    Die benötigte XML-Datei (`belt_state.xml`) sowie dein Arbeitsblatt (`robot_sorting_exercise.py`) liegen bereits fertig vorbereitet in diesem Ordner. Schau dir die XML-Datei kurz in VSCode an, um zu sehen, welche Paketgewichte auf den Roboter warten!
---
## Ausführung
Sobald du die TODOs in deinem Arbeitsblatt erfolgreich gelöst hast, kannst du die Simulation starten:
`python robot_sorting_exercise.py`

Beobachte die Ausgaben im Terminal. Der Roboter wird in Etappen arbeiten müssen. Schau dir nach Abschluss des Skripts (oder nach einem Notaus) die `belt_state.xml` an, um zu sehen, wie der Roboter den Zustand im Repository gesichert und überschrieben hat!
---
## Projektarchitektur (Separation of Concerns)
- *Package*: Ein unveränderliches Wertobjekt (Value Object). Sein einziger Zweck ist es, ein Gewicht zu transportieren.
- *WarehouseRobot*: Unsere Kern-Entität mit eindeutiger Identität, Geschäftslogik und Zustandsmanagement (Akkustand).
- *XmlPackageRepository*: Der Infrastruktur-Code (Architekt). Er ist komplett von der Logik isoliert und kümmert sich ausschließlich um das Einlesen und Speichern der XML-Dateien.