"""
Deutsche Übersetzungen für Fehler, die die Library selber raisen kann

Sind teils auch mit den library-eigenen englischen Exceptions aus core-package verwandt
"""


class WertFehler(ValueError):
    """ValueError aber deutsch :clown face:"""


class InventarFeldLeerFehler(KeyError):
    """Repräsentiert core.InventoryFieldEmptyError"""
