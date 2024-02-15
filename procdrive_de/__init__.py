from typing import Callable as _Callable
from concurrent.futures import TimeoutError as _TimeoutError
import procdrive as _en
from anki.misc.lanes import _LaneType

Streckenabschnitt = _en.TrackPiece

def verbinde(fahrzeug_id: int|None=None):
    """
    Verbindet das Programm mit dem Fahrzeug.
    Diese Funktion sollte immer am Anfang des Programms ausgeführt werden.

    Parameter
    ---------
    - `fahrzeug_id` :class:`Optional[int]`
        Optionale Ganzzahl. (Kann also ausgelassen werden.)
        Eine interne Zahl anhand der man das Fahrzeug identifizieren kann.
        Für die meisten Anwendungen nicht wichtig.
    """
    return _en.connect(vehicle_id=fahrzeug_id)

def warte_auf_neuen_streckenabschnitt(wartezeit: float|None=None):
    """
    Wartet bis das Fahrzeug auf einen neuen Streckenabschnitt gefahren ist
    oder bis die angegebene Wartezeit ausläuft.

    .. note::
        Wenn die Strecke noch nicht eingescannt wurde,
        gibt diese Funktion immer :class:`None` zurück!

    Parameter
    ---------
    - `wartezeit` :class:`Optional[float]`
        Optionaler Fließkommazahl.
        Die maximale Wartezeit in Sekunden.
        Wenn gesetzt, wartet diese Funktion maximal `wartezeit` Sekunden und gibt
        gegebenenfalls :class:`None` zurück, wenn die Wartezeit ausläuft.

        Wenn keine Wartezeit gesetzt ist, wartet die Funktion potenziell unbegrenzte Zeit.
    
    Rückgabewert
    ------------
    :class:`Optional[Streckenabschnitt]`

    Gibt den Streckenabschnitt zurück auf dem das Fahrzeug jetzt ist
    oder :class:`None`, wenn die Wartezeit ausläuft.
    """
    try:
        return _en.wait_for_track_change(timeout=wartezeit)
    except _TimeoutError:
        return None

def setze_geschwindigkeit(geschwindigkeit: int, beschleunigung: int=500):
    """
    Beschleunigt oder entschleunigt das Fahrzeug auf eine gegebene Geschwindigkeit.

    Parameter
    ---------
    - `geschwindigkeit` :class:`int`
        Die Geschwindigkeit auf die das Fahrzeug beschleunigen soll in mm/s.
        
        .. warning::
            Geschwindigkeiten unter 100mm/s sind unzuverlässig.
    
    - `beschleunigung` :class:`int`
        Optionale Ganzzahl. 
        Die Beschleunigung mit der sich die Geschwindigkeit ändern soll in mm/s².

        Standardwert ist 500mm/s².
    """
    return _en.set_speed(speed=geschwindigkeit, acceleration=beschleunigung)

anhalten = _en.stop
"""
Hält das Fahrzeug an, indem die Geschwindigkeit auf 0 gesetzt wird.
"""

def spur_wechseln(
        spur: _LaneType,
        horizontale_geschwindigkeit: int=300,
        horizontale_beschleunigung: int=300
    ):
    return _en.change_lane(
        lane=spur,
        horizontal_speed=horizontale_geschwindigkeit,
        horizontal_acceleration=horizontale_beschleunigung
    )

def mittenabstand_wechseln(
        mittenabstand: float,
        horizontale_geschwindigkeit: int=300,
        horizontale_beschleunigung: int=300
    ):
    return _en.change_position(
        road_center_offset=mittenabstand,
        horizontal_speed=horizontale_geschwindigkeit,
        horizontal_acceleration=horizontale_beschleunigung
    )

def gib_spur(spurentyp: _LaneType):
    return _en.get_lane(mode=spurentyp)

def fahre_zum_start(
        geschwindigkeit: int=300,
        warten: bool=True,
        bei_ende: _Callable[[], None]|None=None
    ):
    return _en.align_to_start(
        speed=geschwindigkeit,
        blocking=warten,
        completion_callback=bei_ende
    )

gib_aktuellen_streckenabschnitt = _en.get_current_track_piece
gib_karte = _en.get_map
gib_mittenabstand = _en.get_road_offset
gib_geschwindigkeit = _en.get_speed
gib_aktuelle_spur3 = _en.get_current_lane3
gib_aktuelle_spur4 = _en.get_current_lane4
gib_fahrzeug_id = _en.get_vehicle_id
