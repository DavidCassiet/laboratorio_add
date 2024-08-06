import os
import platform

def limpiar_pantalla():
    ''' Limpiar la pantalla según el sistema operativo'''
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def mostrar_menu():
    print("========== Menú de Gestión de Tareas ==========")
    print('1. Agregar Tarea Simple')
    print('2. Agregar Tarea Recurrente')
    print('3. Buscar Tarea por ID')
    print('4. Actualizar Tarea')
    print('5. Eliminar Tarea por ID')
    print('6. Mostrar Todos los Tareas')
    print('7. Salir')
    print('===============================================')

def agregar_tarea(gestion, tipo_tarea):
    try:
        id_tarea = input('Ingrese ID de la tarea: ')
        descripcion = input('Ingrese descripción de la tarea: ')
        fecha_vencimiento = input('Ingrese fecha de vencimiento (YYYY-MM-DD): ')
        estado = input('Ingrese estado de la tarea (pendiente, en progreso, completada): ')

        if tipo_tarea == '1':
            tarea = TareaSimple(id_tarea, descripcion, fecha_vencimiento, estado)
        elif tipo_tarea == '2':
            frecuencia = input('Ingrese frecuencia de la tarea (diaria, semanal, mensual): ')
            tarea = TareaRecurrente(id_tarea, descripcion, fecha_vencimiento, estado, frecuencia)
        else:
            print('Opción inválida')
            return

        gestion.crear_tarea(tarea)
        input('Presione enter para continuar...')

    except ValueError as e:
        print(f'Error: {e}')
    except Exception as e:
        print(f'Error inesperado: {e}')

def buscar_tarea_por_id(gestion):
    id_tarea = input('Ingrese el ID de la tarea a buscar: ')
    gestion.leer_tarea(id_tarea)
    input('Presione enter para continuar...')

def actualizar_tarea(gestion):
    id_tarea = input('Ingrese el ID de la tarea para actualizar: ')
    descripcion = input('Ingrese nueva descripción (dejar en blanco para no cambiar): ')
    fecha_vencimiento = input('Ingrese nueva fecha de vencimiento (YYYY-MM-DD, dejar en blanco para no cambiar): ')
    estado = input('Ingrese nuevo estado (pendiente, en progreso, completada, dejar en blanco para no cambiar): ')
    gestion.actualizar_tarea(id_tarea, descripcion, fecha_vencimiento if fecha_vencimiento else None, estado if estado else None)
    input('Presione enter para continuar...')

def eliminar_tarea_por_id(gestion):
    id_tarea = input('Ingrese el ID de la tarea a eliminar: ')
    gestion.eliminar_tarea(id_tarea)
    input('Presione enter para continuar...')

def mostrar_todas_las_tareas(gestion):
    print('=============== Listado completo de las Tareas ===============')
    for tarea in gestion.leer_datos().values():
        if 'frecuencia' in tarea:
            print(f"{tarea['descripcion']} (Frecuencia: {tarea['frecuencia']})")
        else:
            print(f"{tarea['descripcion']}")
    print('===========================================================')
    input('Presione enter para continuar...')

if __name__ == "__main__":
    archivo_tareas = 'tareas_db.json'
    gestion = GestionTareas(archivo_tareas)

    while True:
        limpiar_pantalla()
        mostrar_menu()
        opcion = input('Seleccione una opción: ')

        if opcion == '1' or opcion == '2':
            agregar_tarea(gestion, opcion)
        
        elif opcion == '3':
            buscar_tarea_por_id(gestion)

        elif opcion == '4':
            actualizar_tarea(gestion)

        elif opcion == '5':
            eliminar_tarea_por_id(gestion)

        elif opcion == '6':
            mostrar_todas_las_tareas(gestion)

        elif opcion == '7':
            print('Saliendo...')
            break

        else:
            print('Opción no válida. Inténtelo de nuevo.')
