'''
Desafío 3: Sistema de Gestión de Tareas
Objetivo: Desarrollar un sistema para organizar y administrar tareas personales o de equipo.

Requisitos:

Crear una clase base Tarea con atributos como descripción, fecha de vencimiento, estado (pendiente, en progreso, completada), etc.
Definir al menos 2 clases derivadas para diferentes tipos de tareas (por ejemplo, TareaSimple, TareaRecurrente) con atributos y métodos específicos.
Implementar operaciones CRUD para gestionar las tareas.
Manejar errores con bloques try-except para validar entradas y gestionar excepciones.
Persistir los datos en archivo JSON.

'''
import json
from datetime import datetime

class Tarea:
    ESTADOS = ['pendiente', 'en progreso', 'completada']

    def __init__(self, id_tarea, descripcion, fecha_vencimiento, estado='pendiente'):
        self.id_tarea = id_tarea
        self.descripcion = descripcion
        self.fecha_vencimiento = self.validar_fecha(fecha_vencimiento)
        self.estado = self.validar_estado(estado)

    def validar_fecha(self, fecha):
        try:
            return datetime.strptime(fecha, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError("La fecha debe estar en formato YYYY-MM-DD.")

    def validar_estado(self, estado):
        if estado not in self.ESTADOS:
            raise ValueError(f"Estado inválido. Debe ser uno de {self.ESTADOS}.")
        return estado

    def to_dict(self):
        return {
            "id_tarea": self.id_tarea,
            "descripcion": self.descripcion,
            "fecha_vencimiento": str(self.fecha_vencimiento),
            "estado": self.estado
        }

    def __str__(self):
        return f"{self.descripcion} (Estado: {self.estado})"

class TareaSimple(Tarea):
    def __init__(self, id_tarea, descripcion, fecha_vencimiento, estado='pendiente'):
        super().__init__(id_tarea, descripcion, fecha_vencimiento, estado)

class TareaRecurrente(Tarea):
    def __init__(self, id_tarea, descripcion, fecha_vencimiento, estado='pendiente', frecuencia='semanal'):
        super().__init__(id_tarea, descripcion, fecha_vencimiento, estado)
        self.frecuencia = frecuencia

    def to_dict(self):
        data = super().to_dict()
        data["frecuencia"] = self.frecuencia
        return data

    def __str__(self):
        return f"{super().__str__()} (Frecuencia: {self.frecuencia})"

class GestionTareas:
    def __init__(self, archivo):
        self.archivo = archivo

    def leer_datos(self):
        try:
            with open(self.archivo, 'r') as file:
                datos = json.load(file)
        except FileNotFoundError:
            return {}
        except Exception as error:
            raise Exception(f'Error al leer datos del archivo: {error}')
        else:
            return datos

    def guardar_datos(self, datos):
        try:
            with open(self.archivo, 'w') as file:
                json.dump(datos, file, indent=4)
        except IOError as error:
            print(f'Error al intentar guardar los datos en {self.archivo}: {error}')
        except Exception as error:
            print(f'Error inesperado: {error}')

    def crear_tarea(self, tarea):
        try:
            datos = self.leer_datos()
            id_tarea = tarea.id_tarea
            if id_tarea not in datos:
                datos[id_tarea] = tarea.to_dict()
                self.guardar_datos(datos)
                print(f"Tarea '{tarea.descripcion}' creada correctamente.")
            else:
                print(f"Ya existe tarea con ID '{id_tarea}'.")
        except Exception as error:
            print(f'Error inesperado al crear tarea: {error}')

    def leer_tarea(self, id_tarea):
        try:
            datos = self.leer_datos()
            if id_tarea in datos:
                tarea_data = datos[id_tarea]
                if 'frecuencia' in tarea_data:
                    tarea = TareaRecurrente(**tarea_data)
                else:
                    tarea = TareaSimple(**tarea_data)
                print(f'Tarea encontrada con ID {id_tarea}: {tarea}')
            else:
                print(f'No se encontró tarea con ID {id_tarea}')
        except Exception as e:
            print(f'Error al leer tarea: {e}')

    def actualizar_tarea(self, id_tarea, descripcion=None, fecha_vencimiento=None, estado=None):
        try:
            datos = self.leer_datos()
            if id_tarea in datos:
                if descripcion:
                    datos[id_tarea]['descripcion'] = descripcion
                if fecha_vencimiento:
                    datos[id_tarea]['fecha_vencimiento'] = str(self.validar_fecha(fecha_vencimiento))
                if estado:
                    datos[id_tarea]['estado'] = self.validar_estado(estado)
                self.guardar_datos(datos)
                print(f'Tarea con ID {id_tarea} actualizada correctamente.')
            else:
                print(f'No se encontró tarea con ID {id_tarea}')
        except Exception as e:
            print(f'Error al actualizar la tarea: {e}')

    def eliminar_tarea(self, id_tarea):
        try:
            datos = self.leer_datos()
            if id_tarea in datos:
                del datos[id_tarea]
                self.guardar_datos(datos)
                print(f'Tarea con ID {id_tarea} eliminada correctamente.')
            else:
                print(f'No se encontró tarea con ID {id_tarea}')
        except Exception as e:
            print(f'Error al eliminar la tarea: {e}')
