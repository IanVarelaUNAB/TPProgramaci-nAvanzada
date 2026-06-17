from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Persona:
    id_persona: str
    nombre: str
    email: str

    def descripcion(self) -> str:
        return f"{self.id_persona} - {self.nombre} ({self.email})"


@dataclass
class Estudiante(Persona):
    legajo: str

    def descripcion(self) -> str:
        return f"Estudiante | {self.id_persona} - {self.nombre} | legajo={self.legajo} | {self.email}"


@dataclass
class Docente(Persona):
    departamento: str

    def descripcion(self) -> str:
        return f"Docente | {self.id_persona} - {self.nombre} | depto={self.departamento} | {self.email}"


@dataclass
class Curso:
    id_curso: str
    nombre: str
    id_docente: str
    cupo: int

    def descripcion(self) -> str:
        return f"{self.id_curso} - {self.nombre} | docente={self.id_docente} | cupo={self.cupo}"


@dataclass
class Inscripcion:
    id_inscripcion: str
    id_estudiante: str
    id_curso: str
    fecha: str  # "YYYY-MM-DD"

    def descripcion(self) -> str:
        return f"{self.id_inscripcion} | est={self.id_estudiante} -> curso={self.id_curso} | {self.fecha}"
