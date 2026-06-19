from __future__ import annotations

from datetime import date

from modelos import Curso, Docente, Estudiante, Inscripcion
from repositorio import AlmacenamientoJson, RepositorioAcademico
from busqueda import (Buscador, BuscarPorEmail, BuscarPorId, BuscarPorNombre, BuscarPorLegajo)


DATA_PATH = "data.json"


class Cancelado(Exception):
    pass


def input_non_empty(label: str) -> str:
    while True:
        value = input(label).strip()
        if value.lower() == "x":
            raise Cancelado
        if value:
            return value
        print("No puede estar vacío")


def input_int(label: str) -> int:
    while True:
        raw = input(label).strip()
        if raw.lower() == "x":
            raise Cancelado
        try:
            return int(raw)
        except ValueError:
            print("Debe ser un número entero")


def input_id_numerico(label: str) -> str:
    while True:
        value = input(label).strip()
        if value.lower() == "x":
            raise Cancelado
        if not value:
            print("No puede estar vacío")
            continue
        if not value.isdigit():
            print("Debe ser numérico (solo dígitos)")
            continue
        return value


def input_id_o_auto(label: str, sugerido: str) -> str:
    while True:
        value = input(f"{label} (Enter = {sugerido}): ").strip()
        if value.lower() == "x":
            raise Cancelado
        if value == "":
            return sugerido
        if not value.isdigit():
            print("Debe ser numérico (solo dígitos)")
            continue
        return value


def ejecutar_con_reintento(accion, titulo: str) -> None:
    while True:
        try:
            accion()
            return
        except Cancelado:
            print("Cancelado. Volviendo al menú...")
            return
        except ValueError as ex:
            # Reintento automático
            print(f"Error: {ex}")


def menu() -> None:
    almacenamiento = AlmacenamientoJson(DATA_PATH)
    repo = almacenamiento.cargar()

    buscador = Buscador(BuscarPorId())

    while True:
        print("\n=== Gestión académica ===")
        print("1) Alta estudiante")
        print("2) Alta docente")
        print("3) Alta curso")
        print("4) Inscribir estudiante")
        print("5) Listar cursos")
        print("6) Buscar estudiante")
        print("7) Listar estudiantes")
        print("8) Listar docentes")
        print("9) Listar inscripciones")
        print("X) Eliminar...")
        print("0) Guardar y salir")

        try:
            op = input("Opción: ").strip()
            if op.lower() == "e":
                print("Cancelado. Volviendo al menú...")
                continue
        except EOFError:
            almacenamiento.guardar(repo)
            print(f"\nEOF detectado. Guardado en {DATA_PATH}.")
            return

        if op == "1":
            ejecutar_con_reintento(lambda: alta_estudiante(repo), "Alta estudiante")
        elif op == "2":
            ejecutar_con_reintento(lambda: alta_docente(repo), "Alta docente")
        elif op == "3":
            ejecutar_con_reintento(lambda: alta_curso(repo), "Alta curso")
        elif op == "4":
            ejecutar_con_reintento(lambda: inscribir_estudiante(repo), "Inscribir estudiante")
        elif op == "5":
            listar_cursos(repo)
        elif op == "6":
            ejecutar_con_reintento(lambda: buscar_estudiante(repo, buscador), "Buscar estudiante")
        elif op == "7":
            listar_estudiantes(repo)
        elif op == "8":
            listar_docentes(repo)
        elif op == "9":
            listar_inscripciones(repo)
        elif op.lower() == "x":
            ejecutar_con_reintento(lambda: menu_eliminar(repo), "Eliminar")
        elif op == "0":
            almacenamiento.guardar(repo)
            print(f"Guardado en {DATA_PATH}. Chau!")
            return
        else:
            print("Opción inválida")


def alta_estudiante(repo: RepositorioAcademico) -> None:
    print("\n-- Alta estudiante --")
    print("ID estudiante: número único. Ej: 1, 2, 3...")
    id_persona = input_id_o_auto("ID estudiante", repo.next_id_estudiante())
    print("Nombre: texto. Ej: Juan Perez")
    nombre = input_non_empty("Nombre: ")
    print("Email: texto con @. Ej: juan@gmail.com")
    email = input_non_empty("Email: ")
    print("Legajo: número. Ej: 1001")
    legajo = input_id_o_auto("Legajo", repo.next_legajo_estudiante())

    repo.add_estudiante(Estudiante(id_persona=id_persona, nombre=nombre, email=email, legajo=legajo))
    print("Estudiante creado")


def alta_docente(repo: RepositorioAcademico) -> None:
    print("\n-- Alta docente --")
    print("ID docente: número único. Ej: 1, 2, 3...")
    id_persona = input_id_o_auto("ID docente", repo.next_id_docente())
    print("Nombre: texto. Ej: Maria Lopez")
    nombre = input_non_empty("Nombre: ")
    print("Email: texto con @. Ej: maria@uni.edu")
    email = input_non_empty("Email: ")
    print("Departamento: texto. Ej: Sistemas")
    depto = input_non_empty("Departamento: ")

    repo.add_docente(Docente(id_persona=id_persona, nombre=nombre, email=email, departamento=depto))
    print("Docente creado")


def alta_curso(repo: RepositorioAcademico) -> None:
    print("\n-- Alta curso --")
    print("ID curso: número único. Ej: 1, 2, 3...")
    id_curso = input_id_o_auto("ID curso", repo.next_id_curso())
    print("Nombre curso: texto. Ej: Programación 1")
    nombre = input_non_empty("Nombre curso: ")

    while True:
        print("ID docente: número de un docente existente. Ej: 1")
        id_docente = input_id_numerico("ID docente (debe existir): ")
        if repo.get_docente(id_docente) is None:
            print("Error: El docente no existe")
            continue
        break

    print("Cupo: número entero > 0. Ej: 30")
    cupo = input_int("Cupo: ")

    repo.add_curso(Curso(id_curso=id_curso, nombre=nombre, id_docente=id_docente, cupo=cupo))
    print("Curso creado")


def inscribir_estudiante(repo: RepositorioAcademico) -> None:
    print("\n-- Inscribir estudiante --")
    print("ID inscripción: número único. Ej: 1, 2, 3...")
    id_insc = input_id_o_auto("ID inscripción", repo.next_id_inscripcion())

    while True:
        print("ID estudiante: número de un estudiante existente. Ej: 1")
        id_est = input_id_numerico("ID estudiante: ")
        if repo.get_estudiante(id_est) is None:
            print("Error: El estudiante no existe")
            continue
        break

    while True:
        print("ID curso: número de un curso existente. Ej: 1")
        id_curso = input_id_numerico("ID curso: ")
        if repo.get_curso(id_curso) is None:
            print("Error: El curso no existe")
            continue
        break

    fecha = str(date.today())

    repo.inscribir(Inscripcion(id_inscripcion=id_insc, id_estudiante=id_est, id_curso=id_curso, fecha=fecha))
    print("Inscripción realizada")


def listar_cursos(repo: RepositorioAcademico) -> None:
    print("\n-- Cursos (ordenados por ID) --")
    if not repo.cursos:
        print("(no hay cursos)")
        return

    ordenados = sorted(repo.cursos, key=lambda c: int(c.id_curso))
    for c in ordenados:
        docente = repo.get_docente(c.id_docente)
        docente_nombre = docente.nombre if docente is not None else "(docente no encontrado)"
        inscriptos = repo.curso_cantidad_inscriptos(c.id_curso)
        print(f"{c.id_curso} - {c.nombre} | docente: {docente_nombre} | {inscriptos}/{c.cupo}")


def buscar_estudiante(repo: RepositorioAcademico, buscador: Buscador) -> None:
    print("\n-- Buscar estudiante --")

    while True:
        print("Estrategia: 1) ID  2) Nombre  3) Email 4)Legajo")
        e = input("Elegí (o X para cancelar): ").strip()
        if e.lower() == "x":
            raise Cancelado
        if e == "1":
            buscador.set_estrategia(BuscarPorId())
            break
        if e == "2":
            buscador.set_estrategia(BuscarPorNombre())
            break
        if e == "3":
            buscador.set_estrategia(BuscarPorEmail())
            break
        if e == "4":
            buscador.set_estrategia(BuscarPorLegajo())
            break
        print("Error: Estrategia inválida")

    query = input_non_empty("Buscar: ")
    results = buscador.buscar(repo.estudiantes, query)

    if not results:
        print("Sin resultados")
        return

    for r in results:
        cursos = repo.cursos_de_estudiante(r.id_persona)
        if cursos:
            cursos_txt = ", ".join([f"{c.id_curso}-{c.nombre}" for c in cursos])
        else:
            cursos_txt = "Libre"
        print(f"{r.descripcion()} | cursos: {cursos_txt}")


def listar_estudiantes(repo: RepositorioAcademico) -> None:
    print("\n-- Estudiantes (ordenados por ID) --")
    if not repo.estudiantes:
        print("(no hay estudiantes)")
        return

    ordenados = sorted(repo.estudiantes, key=lambda e: int(e.id_persona))
    for e in ordenados:
        cursos = repo.cursos_de_estudiante(e.id_persona)
        if cursos:
            cursos_txt = ", ".join([f"{c.id_curso}-{c.nombre}" for c in cursos])
        else:
            cursos_txt = "Libre"
        print(f"{e.descripcion()} | cursos: {cursos_txt}")


def listar_docentes(repo: RepositorioAcademico) -> None:
    print("\n-- Docentes (ordenados por ID) --")
    if not repo.docentes:
        print("(no hay docentes)")
        return

    ordenados = sorted(repo.docentes, key=lambda d: int(d.id_persona))
    for d in ordenados:
        cursos = repo.cursos_de_docente(d.id_persona)
        if cursos:
            cursos_txt = ", ".join([f"{c.id_curso}-{c.nombre}" for c in cursos])
        else:
            cursos_txt = "Sin cursos"
        print(f"{d.descripcion()} | cursos: {cursos_txt}")


def listar_inscripciones(repo: RepositorioAcademico) -> None:
    print("\n-- Inscripciones (ordenadas por ID) --")
    if not repo.inscripciones:
        print("(no hay inscripciones)")
        return

    ordenadas = sorted(repo.inscripciones, key=lambda i: int(i.id_inscripcion))
    for i in ordenadas:
        est = repo.get_estudiante(i.id_estudiante)
        curso = repo.get_curso(i.id_curso)
        est_nombre = est.nombre if est is not None else "(estudiante no encontrado)"
        curso_nombre = curso.nombre if curso is not None else "(curso no encontrado)"
        print(f"{i.id_inscripcion} | {i.fecha} | {i.id_estudiante} - {est_nombre} -> {i.id_curso} - {curso_nombre}")


def menu_eliminar(repo: RepositorioAcademico) -> None:
    while True:
        print("\n=== Eliminar ===")
        print("1) Eliminar estudiante")
        print("2) Eliminar docente")
        print("3) Eliminar curso")
        print("4) Eliminar inscripción")
        print("0) Volver")
        print("(X en cualquier momento para cancelar)")

        op = input("Opción: ").strip().lower()
        if op == "x":
            raise Cancelado
        if op == "0":
            return

        if op == "1":
            id_est = input_id_numerico("ID estudiante a eliminar: ")
            repo.eliminar_estudiante(id_est)
            print("Estudiante eliminado")
        elif op == "2":
            id_doc = input_id_numerico("ID docente a eliminar: ")
            repo.eliminar_docente(id_doc)
            print("Docente eliminado")
        elif op == "3":
            id_curso = input_id_numerico("ID curso a eliminar: ")
            repo.eliminar_curso(id_curso)
            print("Curso eliminado")
        elif op == "4":
            id_insc = input_id_numerico("ID inscripción a eliminar: ")
            repo.eliminar_inscripcion(id_insc)
            print("Inscripción eliminada")
        else:
            print("Opción inválida")


if __name__ == "__main__":
    menu()
