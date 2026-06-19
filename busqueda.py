from __future__ import annotations

from abc import ABC, abstractmethod


class EstrategiaBusqueda(ABC):
    @abstractmethod
    def coincide(self, obj: object, consulta: str) -> bool:
        raise NotImplementedError


class BuscarPorId(EstrategiaBusqueda):
    def coincide(self, obj: object, consulta: str) -> bool:
        q = consulta.strip().lower()
        if not q:
            return False

        for attr in ("id_persona", "id_curso", "id_inscripcion"):
            if hasattr(obj, attr):
                value = str(getattr(obj, attr)).strip().lower()
                if value == q:
                    return True
        return False


class BuscarPorNombre(EstrategiaBusqueda):
    def coincide(self, obj: object, consulta: str) -> bool:
        q = consulta.strip().lower()
        if not q:
            return False
        if hasattr(obj, "nombre"):
            return q in str(getattr(obj, "nombre")).strip().lower()
        return False


class BuscarPorEmail(EstrategiaBusqueda):
    def coincide(self, obj: object, consulta: str) -> bool:
        q = consulta.strip().lower()
        if not q:
            return False
        if hasattr(obj, "email"):
            return q in str(getattr(obj, "email")).strip().lower()
        return False

class BuscarPorLegajo(EstrategiaBusqueda):
    def coincide(self, obj: object, consulta: str) -> bool:
        q = consulta.strip().lower()
        if not q:
            return False
        if hasattr(obj, "legajo"):
            return q == str(getattr(obj, "legajo")).strip().lower()
        return False

class Buscador:
    def __init__(self, estrategia: EstrategiaBusqueda):
        self._estrategia = estrategia

    def set_estrategia(self, estrategia: EstrategiaBusqueda) -> None:
        self._estrategia = estrategia

    def buscar(self, items: list[object], consulta: str) -> list[object]:
        return [x for x in items if self._estrategia.coincide(x, consulta)]
