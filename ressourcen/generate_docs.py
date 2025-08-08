"""
Dieses Skript extrahiert die Dokumentation aus der Bibliothek und speichert sie in einer Textdatei.
Das Ergebnis ist nicht dafür gedacht, von Menschen direkt gelesen zu werden, 
sondern soll einem LLM zur Verfügung gestellt werden, damit es die Bibliothek verstehen kann.

So kann ein LLM auf Basis der Dokumentation Code generieren, ohne dass es auf diese Bibliothek trainiert wurde.

Das Skript kann direkt hier ausgeführt werden. Stelle nur sicher, dass die Bibliothek
in der Python Umgebung installiert ist.

Ironischerweise ist das Skript selbst größtenteils von einer KI generiert und nur leicht von uns
für die Formatierung angepasst worden.

Beispiel Prompt, den du vor das Einfügen der generierten Dokumentation setzen kannst:

Ich gebe dir die API reference einer python library, mit dem namen sk_minecraft die du nicht kennst.

Bitte antworte alle folgenden fragen basierend auf dem was du nun über die library weißt.
Stelle sicher, dass du KEINE neuen Funktionen erfindest.

Alle funktionen und Objekte sind direkt über sk_minecraft.<objekt> erreichbar, 
 achte auch darauf, dass du alle imports richtig setzt.
 Bitte bevorzuge den modul import über den objekt import.

Der server ist immer localhost und der port standardmäßig 12345.

Die Dokumentaton lautet:
[Docs einfügen]
"""


import inspect
import importlib
from typing import Any, TextIO


BIBLIOTHEK_NAME = 'sk_minecraft'
modul = importlib.import_module(BIBLIOTHEK_NAME)


def extrahiere_informationen(objekt: Any, objekt_name: str, ausgabe_datei: TextIO, ebene: int = 0) -> None:
    """Schreibt Signatur und Dokumentation eines Objekts in die Ausgabedatei.

    - Ermittelt nach Möglichkeit die Signatur
    - Hängt vorhandene Docstrings an

    Args:
        objekt: Zu inspizierendes Objekt (Funktion, Klasse, Methode, Modul)
        objekt_name: Anzeigename des Objekts
        ausgabe_datei: Geöffnete Textdatei für die Ausgabe
        ebene: Einzugsebene zur hierarchischen Darstellung
    """
    einrückung = '    ' * ebene
    try:
        signatur = str(inspect.signature(objekt))
    except (TypeError, ValueError):
        signatur = '(...)'

    dokumentation = inspect.getdoc(objekt) or ''

    ausgabe_datei.write(f"{einrückung}{objekt_name}{signatur}\n")
    if dokumentation:
        ausgabe_datei.write(f"{einrückung}    Dokumentation:\n{einrückung}    {dokumentation}\n")
    ausgabe_datei.write("\n\n----\n\n")


def verarbeite_modul(modul_objekt: Any, ausgabe_datei: TextIO, ebene: int = 0) -> None:
    """Durchläuft ein Modul und schreibt alle öffentlichen Symbole unseres Pakets in die Ausgabedatei.

    Es werden nur Mitglieder berücksichtigt, deren `__module__` mit unserem Bibliotheksnamen beginnt.

    Args:
        modul_objekt: Importiertes Modulobjekt, das inspiziert werden soll
        ausgabe_datei: Geöffnete Textdatei für die Ausgabe
        ebene: Einzugsebene zur hierarchischen Darstellung
    """
    for name, objekt in inspect.getmembers(modul_objekt):
        if name.startswith('_'):
            continue

        # Nur Mitglieder berücksichtigen, die in unserer Bibliothek definiert sind
        objekt_modul = getattr(objekt, '__module__', '')
        if not objekt_modul.startswith(BIBLIOTHEK_NAME):
            continue

        if inspect.isfunction(objekt) or inspect.isclass(objekt):
            extrahiere_informationen(objekt, name, ausgabe_datei, ebene)

            if inspect.isclass(objekt):
                for methoden_name, methode in inspect.getmembers(objekt, inspect.isfunction):
                    if methoden_name.startswith('_'):
                        continue
                    if getattr(methode, '__module__', '').startswith(BIBLIOTHEK_NAME):
                        extrahiere_informationen(methode, f"{name}.{methoden_name}", ausgabe_datei, ebene + 1)

        elif inspect.ismodule(objekt) and objekt.__name__.startswith(BIBLIOTHEK_NAME):
            ausgabe_datei.write(f"{'    '*ebene}Modul: {name}\n\n")
            verarbeite_modul(objekt, ausgabe_datei, ebene + 1)


def schreibe_dokumentation(ausgabedatei_pfad: str = 'library_documentation.txt') -> None:
    """Erstellt die Bibliotheksdokumentation als Textdatei.

    Args:
        ausgabedatei_pfad: Pfad der Ausgabedatei
    """
    with open(ausgabedatei_pfad, 'w', encoding='utf-8') as datei:
        datei.write(f"Dokumentation für Bibliothek: {BIBLIOTHEK_NAME}\n\n")
        verarbeite_modul(modul, datei)


# Standardverhalten: Beim direkten Ausführen die Dokumentation erstellen
schreibe_dokumentation()
