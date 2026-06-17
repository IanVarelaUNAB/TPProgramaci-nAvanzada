from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from modelos import Curso, Docente, Estudiante, Inscripcion


class RepositorioAcademico:
    def __init__(self) -> None:
        self.estudiantes: list[Estudiante] = []
        self.docentes: list[Docente] = []
        self.cursos: list[Curso] = []
        self.inscripciones: list[Inscripcion] = []

    def _es_id_numerico(self, value: str) -> bool:
        return value.isdigit()

    def _validar_id_numerico(self, value: str, etiqueta: str) -> None:
        if not value:
            raise ValueError(f"{etiqueta} no puede estar vacío")
        if not self._es_id_numerico(value):
            raise ValueError(f"{etiqueta} debe ser numérico (solo dígitos, sin letras)")

    def _next_id(self, ids: list[str]) -> str:
        if not ids:
            return "1"
        nums = [int(x) for x in ids if x.isdigit()]
        if not nums:
            return "1"
        return str(max(nums) + 1)

    def next_id_estudiante(self) -> str:
        return self._next_id([e.id_persona for e in self.estudiantes])

    def next_legajo_estudiante(self) -> str:
        return self._next_id([e.legajo for e in self.estudiantes])

    def next_id_docente(self) -> str:
        return self._next_id([d.id_persona for d in self.docentes])

    def next_id_curso(self) -> str:
        return self._next_id([c.id_curso for c in self.cursos])

    def next_id_inscripcion(self) -> str:
        return self._next_id([i.id_inscripcion for i in self.inscripciones])

    def docente_tiene_cursos(self, id_docente: str) -> bool:
        for c in self.cursos:
            if c.id_docente == id_docente:
                return True
        return False

    def curso_tiene_inscripciones(self, id_curso: str) -> bool:
        for i in self.inscripciones:
            if i.id_curso == id_curso:
                return True
        return False

    def estudiante_tiene_inscripciones(self, id_estudiante: str) -> bool:
        for i in self.inscripciones:
            if i.id_estudiante == id_estudiante:
                return True
        return False

    def eliminar_inscripcion(self, id_inscripcion: str) -> None:
        for idx, insc in enumerate(self.inscripciones):
            if insc.id_inscripcion == id_inscripcion:
                self.inscripciones.pop(idx)
                return
        raise ValueError("La inscripción no existe")

    def eliminar_estudiante(self, id_estudiante: str) -> None:
        if self.get_estudiante(id_estudiante) is None:
            raise ValueError("El estudiante no existe")
        if self.estudiante_tiene_inscripciones(id_estudiante):
            raise ValueError("No se puede borrar: el estudiante tiene inscripciones")

        for idx, e in enumerate(self.estudiantes):
            if e.id_persona == id_estudiante:
                self.estudiantes.pop(idx)
                return

    def eliminar_curso(self, id_curso: str) -> None:
        if self.get_curso(id_curso) is None:
            raise ValueError("El curso no existe")
        if self.curso_tiene_inscripciones(id_curso):
            raise ValueError("No se puede borrar: el curso tiene inscripciones")

        for idx, c in enumerate(self.cursos):
            if c.id_curso == id_curso:
                self.cursos.pop(idx)
                return

    def eliminar_docente(self, id_docente: str) -> None:
        if self.get_docente(id_docente) is None:
            raise ValueError("El docente no existe")
        if self.docente_tiene_cursos(id_docente):
            raise ValueError("No se puede borrar: el docente tiene cursos")

        for idx, d in enumerate(self.docentes):
            if d.id_persona == id_docente:
                self.docentes.pop(idx)
                return

    def get_estudiante(self, id_estudiante: str) -> Estudiante | None:
        for e in self.estudiantes:
            if e.id_persona == id_estudiante:
                return e
        return None

    def get_docente(self, id_docente: str) -> Docente | None:
        for d in self.docentes:
            if d.id_persona == id_docente:
                return d
        return None

    def get_curso(self, id_curso: str) -> Curso | None:
        for c in self.cursos:
            if c.id_curso == id_curso:
                return c
        return None

    def cursos_de_estudiante(self, id_estudiante: str) -> list[Curso]:
        cursos: list[Curso] = []
        ids: set[str] = set()
        for insc in self.inscripciones:
            if insc.id_estudiante == id_estudiante:
                ids.add(insc.id_curso)

        for id_curso in ids:
            curso = self.get_curso(id_curso)
            if curso is not None:
                cursos.append(curso)

        cursos.sort(key=lambda c: int(c.id_curso))
        return cursos

    def cursos_de_docente(self, id_docente: str) -> list[Curso]:
        cursos = [c for c in self.cursos if c.id_docente == id_docente]
        cursos.sort(key=lambda c: int(c.id_curso))
        return cursos

    def curso_cantidad_inscriptos(self, id_curso: str) -> int:
        count = 0
        for i in self.inscripciones:
            if i.id_curso == id_curso:
                count += 1
        return count

    def estudiante_ya_inscripto(self, id_estudiante: str, id_curso: str) -> bool:
        for i in self.inscripciones:
            if i.id_estudiante == id_estudiante and i.id_curso == id_curso:
                return True
        return False

    def add_estudiante(self, estudiante: Estudiante) -> None:
        self._validar_id_numerico(estudiante.id_persona, "ID estudiante")
        self._validar_id_numerico(estudiante.legajo, "Legajo")
        if self.get_estudiante(estudiante.id_persona) is not None:
            raise ValueError("Ya existe un estudiante con ese ID")
        self.estudiantes.append(estudiante)

    def add_docente(self, docente: Docente) -> None:
        self._validar_id_numerico(docente.id_persona, "ID docente")
        if self.get_docente(docente.id_persona) is not None:
            raise ValueError("Ya existe un docente con ese ID")
        self.docentes.append(docente)

    def add_curso(self, curso: Curso) -> None:
        self._validar_id_numerico(curso.id_curso, "ID curso")
        self._validar_id_numerico(curso.id_docente, "ID docente")
        if self.get_curso(curso.id_curso) is not None:
            raise ValueError("Ya existe un curso con ese ID")
        if self.get_docente(curso.id_docente) is None:
            raise ValueError("El docente no existe")
        if curso.cupo <= 0:
            raise ValueError("El cupo debe ser mayor a 0")
        self.cursos.append(curso)

    def inscribir(self, inscripcion: Inscripcion) -> None:
        self._validar_id_numerico(inscripcion.id_inscripcion, "ID inscripción")
        self._validar_id_numerico(inscripcion.id_estudiante, "ID estudiante")
        self._validar_id_numerico(inscripcion.id_curso, "ID curso")

        if self.get_estudiante(inscripcion.id_estudiante) is None:
            raise ValueError("El estudiante no existe")
        curso = self.get_curso(inscripcion.id_curso)
        if curso is None:
            raise ValueError("El curso no existe")
        if self.estudiante_ya_inscripto(inscripcion.id_estudiante, inscripcion.id_curso):
            raise ValueError("El estudiante ya está inscripto en ese curso")

        inscriptos = self.curso_cantidad_inscriptos(inscripcion.id_curso)
        if inscriptos >= curso.cupo:
            raise ValueError("No hay cupo disponible")

        for i in self.inscripciones:
            if i.id_inscripcion == inscripcion.id_inscripcion:
                raise ValueError("Ya existe una inscripción con ese ID")

        self.inscripciones.append(inscripcion)


class AlmacenamientoJson:
    def __init__(self, path: str) -> None:
        self._path = Path(path)

    def cargar(self) -> RepositorioAcademico:
        repo = RepositorioAcademico()
        if not self._path.exists():
            return repo

        raw = self._path.read_text(encoding="utf-8").strip()
        if not raw:
            return repo

        data = json.loads(raw)

        for e in data.get("estudiantes", []):
            repo.estudiantes.append(Estudiante(**e))
        for d in data.get("docentes", []):
            repo.docentes.append(Docente(**d))
        for c in data.get("cursos", []):
            repo.cursos.append(Curso(**c))
        for i in data.get("inscripciones", []):
            repo.inscripciones.append(Inscripcion(**i))

        return repo

    def guardar(self, repo: RepositorioAcademico) -> None:
        data = {
            "estudiantes": [asdict(x) for x in repo.estudiantes],
            "docentes": [asdict(x) for x in repo.docentes],
            "cursos": [asdict(x) for x in repo.cursos],
            "inscripciones": [asdict(x) for x in repo.inscripciones],
        }
        self._path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
