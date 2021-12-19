import json
import os


def cargar_medicamentos():
    recetas_json = []
    path = os.path.dirname(__file__) + '\\Medicamentos'
    medicamentos_sist = os.listdir(path)
    for medicamento in medicamentos_sist:
        file = open(path + '\\' + medicamento, encoding="utf8")
        receta = json.load(file, strict=False)
        recetas_json.append(receta)

    return recetas_json


def preprocesar_consulta(consulta):
    # 1-Pasamos a minusculas la consulta
    consulta = consulta.lower()

    # 2-Eliminamos acentos
    replacements = (
        ("?", ""),
        ("!", ""),
        ("¿", ""),
        ("¡", ""),
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        consulta = consulta.replace(a, b)
    # 3-Devolvemos la consulta preprocesada
    return consulta


def print_msg_box(msg, indent=1, width=None, title=None):
    """Print message-box with optional title."""
    lines = msg.split('\n')
    space = " " * indent
    if not width:
        width = max(map(len, lines))
    box = f'╔{"═" * (width + indent * 2)}╗\n'  # upper_border
    if title:
        box += f'║{space}{title:<{width}}{space}║\n'  # title
        box += f'║{space}{"-" * len(title):<{width}}{space}║\n'  # underscore
    box += ''.join([f'║{space}{line:<{width}}{space}║\n' for line in lines])
    box += f'╚{"═" * (width + indent * 2)}╝'  # lower_border
    return box


# ===========================BASE DE CONOCIMIENTO===========================


casos_de_uso = ['cuando', 'como', 'circunstancias', 'debo',
                'dolor', 'tomar', 'administrar', 'para', 'sirve', 'tipo']
no_tomar = ['contraindicaciones', 'contraindicacion', 'no tomar', 'dar', 'no toma', 'alergicos',
            'si soy', 'estomago', 'sufro', 'sufre', 'ingerir', 'alergias', 'secundarios', 'secundario',
            'vacunar', 'vacuna']
precauciones = ['contraindicacion', 'contraindicaciones', 'precaucion', 'precauciones', 'advertencias',
                'seguro', 'alergico', 'informacion', 'secundario', 'secundarios']
deportistas = ['contraindicacion', 'contraindicaciones', 'deportista', 'atleta', 'elite',
               'deporte', 'dopaje', 'dopar', 'ejercicio', 'actividad', 'positivo', 'negativo',
               'prueba', 'antidoping']
medicamentos = ['contraindicacion', 'contraindicaciones', 'tomado', 'otro', 'medicamento', 'ibuprofeno', 'enantyum',
                'enantium', 'paracetamol', 'omeprazol', 'alcohol', 'cerveza', 'copa', 'vino', 'vacunar', 'vacuna',
                'mezclo', 'mezclar', 'mezcla', 'diabetico', 'anticonceptivos', 'medicamentos']
embarazo = ['contraindicacion', 'contraindicaciones', 'embarazadas', 'embarazada', 'embarazos', 'lactantes',
            'bebes', 'nacidos', 'crios', 'criaturas', 'lactancia', 'fertilidad', 'fertil', 'pecho']
conducir = ['contraindicacion', 'contraindicaciones', 'conducir', 'conduzco', 'conducido', 'transportar',
            'trasladar', 'traslado', 'pilotar', 'piloto', 'carretillero', 'carretillera', 'carretilla',
            'grua', 'coche', 'volante', 'maquina', 'maquinaria', 'secundarios', 'secundario']
dosis = ['via', 'administrar', 'frecuencia', 'cantidades', 'cada cuanto', 'tiempo', 'comprimidos',
         'tratamiento', 'gramos', 'dosis', 'cantidad', 'veces']
sobredosis = ['sin querer', 'doble', 'triple', 'debo', 'acudir', 'mas',
              'llamar', 'pasa algo', 'repetir', 'cantidad', 'máxima', 'sobredosis']
olvido = ['olvidado', 'olvido', 'olvide', 'recorde', 'recuerdo', 'memoria']
interrupcion = ['interrumpir', 'mejor', 'parar', 'dejar']
efect_adversos = ['secundarios', 'efectos', 'nocivo', 'tripa', 'dolores',
                  'piel', 'diabetico', 'adversa', 'adversos', 'adversas', 'adverso']
conservacion = ['conservar', 'conservacion', 'conserva', 'temperatura', 'estropear',
                'sol', 'luz', 'fresco', 'calor']

contraindicaciones = [no_tomar, precauciones, deportistas, medicamentos, embarazo, conducir]
posologia = [dosis, sobredosis, olvido, interrupcion]

base_conocimiento = [casos_de_uso, contraindicaciones, posologia, efect_adversos, conservacion]

nombre_contraindicaciones = ['no_tomar_si', 'advertencias_precauciones', 'deportistas', 'mezcla_otros_medicamentos',
                             'embarazo_lactancia_fertilidad', 'conduccion']
nombre_posologias = ['dosis', 'sobredosis', 'olvido', 'interrupcion']
posologias = ['dosis', 'sobredosis', 'olvido', 'interrupcion']
dimensiones_json = ['casos_de_uso', nombre_contraindicaciones, nombre_posologias, 'efectos_adversos', 'conservacion']
nombre_dimensiones = ['casos_de_uso', 'contraindicaciones', 'posologia', 'efectos_adversos', 'conservacion']


# ===========================FIN BASE DE CONOCIMIENTO===========================

def detectar_medicamentos_consulta(medicamentos_sistema, consulta):
    medicamentos_detectados = []
    palabras = consulta.split(' ')
    for palabra in palabras:
        if palabra in medicamentos_sistema and palabra not in medicamentos_detectados:
            medicamentos_detectados.append(palabra)
    return medicamentos_detectados


def interpretar_consulta(consulta):
    consulta_procesada = preprocesar_consulta(consulta)
    respuestas = ''
    nombre_dim_encontradas = []
    existe_medicamento = 0
    nombre_medicamentos = obtener_nombre_medicamentos_sist()
    medicamentos_json = cargar_medicamentos()
    medicamentos_detectados = detectar_medicamentos_consulta(nombre_medicamentos, consulta_procesada)

    if len(medicamentos_detectados) > 0:
        existe_medicamento = 1
        for palabra in consulta_procesada.split():
            for dimension in range(len(base_conocimiento)):
                dimension_actual = base_conocimiento[dimension]
                nombre_dimension = nombre_dimensiones[dimension]
                if type(dimension_actual[0]) == list:
                    # 2A-Si estamos en una dimension con parametros
                    for parametro in range(len(dimension_actual)):
                        nombre_parametro = dimensiones_json[dimension][parametro]
                        palabras_parametro = dimension_actual[parametro]
                        for medicamento in medicamentos_detectados:
                            if palabra in palabras_parametro and medicamento + ':' + nombre_parametro not in nombre_dim_encontradas:
                                medicamento_json = medicamentos_json[nombre_medicamentos.index(medicamento)]
                                nombre_dim_encontradas.append(medicamento + ':' + nombre_parametro)
                                ancho_caja = max(len(nombre_dimension + '\n|--{' + nombre_parametro + '}'),
                                                 len(medicamento + ':' + palabra))
                                respuestas = respuestas + '\n' + \
                                             print_msg_box(nombre_dimensiones[dimension] + '\n|--{' +
                                                           nombre_parametro + '}', title=medicamento + ':' + palabra,
                                                           width=ancho_caja) \
                                             + '\n' + medicamento_json[nombre_dimension][nombre_parametro]

                # 2B-Si no estamos en una dimension con parametros
                for medicamento in medicamentos_detectados:
                    if palabra in dimension_actual and medicamento + ':' + nombre_dimension not in nombre_dim_encontradas:
                        medicamento_json = medicamentos_json[nombre_medicamentos.index(medicamento)]
                        nombre_dim_encontradas.append(medicamento + ':' + nombre_dimension)
                        ancho_caja = max(len(medicamento + ':' + palabra), len(nombre_dimension))
                        respuestas = respuestas + '\n' + \
                                     print_msg_box(nombre_dimension, title=medicamento + ':' + palabra,
                                                   width = ancho_caja) + \
                                     '\n' + medicamento_json[nombre_dimension]

    if existe_medicamento == 0:
        respuestas = respuestas + print_msg_box(
            "Por favor introduzca en su consulta el nombre del medicamento del que desea obtener informacion, " +
            "actualmente solo disponemos de los siguientes medicamentos: \n" + print_msg_box(
                ",".join(nombre_medicamentos)))
    
    if respuestas == '':
        respuestas = print_msg_box('Lo sentimos, el sistema no ha conseguido encontrar respuesta a su consulta, pruebe a enunciarla de otra forma', title='INFORMACIÓN NO ENCONTRADA')
    
    return print_msg_box("CONSULTA --> " + consulta) + '\n' + print_msg_box(respuestas, title='RESPUESTAS')


def obtener_nombre_medicamentos_sist():
    recetas_json = []
    path = os.path.dirname(__file__) + '\\Medicamentos'
    medicamentos_sist = os.listdir(path)
    nombre_medicamentos = []
    for nombre_medicamento in range(len(medicamentos_sist)):
        nombre_medicamentos.append(medicamentos_sist[nombre_medicamento].replace('.json', ''))

    return nombre_medicamentos


def volcar_en_fichero_prueba_general():
    respuesta_usuario = 0
    medicamentos = obtener_nombre_medicamentos_sist()
    if os.path.isfile('prueba_general.txt'):
        respuesta_valida = 0
        while not respuesta_valida:
            try:
                respuesta_usuario = int(input(
                    "Ya existe el fichero que contiene el resumen de la prueba general, ¿seguro que quiere volver a hacerlo? "
                    "1/0: "))
                respuesta_valida = 1
            except ValueError:
                respuesta_usuario = input('Introduzca 0 para no ó 1 para si: ')

        if respuesta_usuario != 0:
            with open('prueba_general.txt', "w", encoding="utf-8") as f:
                for medicamento in medicamentos:
                    f.write(
                        "\n==============================================================MEDICAMENTO"
                        "==============================================================" + medicamento)
                    consultas = obtener_consultas_medicamento(medicamento)
                    for tipo_consulta in consultas:
                        for consulta in tipo_consulta:
                            f.write('\n')
                            f.write(interpretar_consulta(consulta))
            path = os.path.dirname(__file__) + '\\prueba_general.txt'
            print('Informe general volcado en ' + path + ' de forma exitosa.')

    else:
        with open('prueba_general.txt', "w", encoding="utf-8") as f:
            for medicamento in medicamentos:
                f.write(
                    "\n==============================================================MEDICAMENTO"
                    "==============================================================" + medicamento)
                consultas = obtener_consultas_medicamento(medicamento)
                for tipo_consulta in consultas:
                    for consulta in tipo_consulta:
                        f.write('\n')
                        f.write(interpretar_consulta(consulta))
        path = os.path.dirname(__file__) + '\\prueba_general.txt'
        print('Informe general volcado en ' + path + ' de forma exitosa.')


def imprimir_prueba_general():
    medicamentos = obtener_nombre_medicamentos_sist()
    for medicamento in medicamentos:
        print(
            "\n==============================================================MEDICAMENTO: |{0}| "
            "==============================================================".format(medicamento))
        consultas = obtener_consultas_medicamento(medicamento)
        for tipo_consulta in consultas:
            for consulta in tipo_consulta:
                print(interpretar_consulta(consulta))




def mostrar_menu_2():
    medicamentos_sistema = (', ').join(obtener_nombre_medicamentos_sist())
    mensaje = 'Actualmente los medicamentos del sistema son: '
    print(print_msg_box(medicamentos_sistema, title=mensaje, width=len(mensaje)))
    medicamento_seleccionado = input("Elija uno de los medicamentos mostrados: ")
    while medicamento_seleccionado not in medicamentos_sistema:
        medicamento_seleccionado = input(
            str(medicamento_seleccionado) + " No es una opción válida, actualmente los medicamentos del sistema son: "
            + medicamentos_sistema + "\nElija uno de los medicamentos mostrados: ")

    print("\n==============================================================MEDICAMENTO: |{0}| "
          "==============================================================".format(medicamento_seleccionado))
    consultas = obtener_consultas_medicamento(medicamento_seleccionado)
    for tipo_consulta in consultas:
        for consulta in tipo_consulta:
            print(interpretar_consulta(consulta))


def obtener_consultas_medicamento(medicamento):
    lista_consultas_casos_de_uso = \
        [
            '¿Para qué sirve ' + medicamento + '?',
            '¿Para qué tipo de patologías está indicado' + medicamento + '?',
            '¿Se puede tomar ' + medicamento + ' para cualquier síntoma alérgico?',
            '¿Cuál es la sintomatología para poder tomar ' + medicamento + '?',
        ]

    lista_consultas_posologia = \
        [
            '¿Cuál es la dosis recomendada de ' + medicamento + ' en adultos?',
            '¿Cuál es la dosis recomendada de ' + medicamento + ' en niños?',
            '¿Se pueden repetir la toma de ' + medicamento + ' en casos graves?',
            '¿Cuál es la cantidad de ' + medicamento + ' máxima que se pude administrar?',
            '¿Cuántas veces al día se deben administrar las tomas de ' + medicamento + '?',
            '¿Se puede tomar una dosis de ' + medicamento + ' mayor en caso de olvido?',
            '¿Qué debo hacer en caso de sobredosis de ' + medicamento + '?',
            '¿Qué síntomas tiene una persona en caso de sobredosis de ' + medicamento + '?',
            '¿Se puede interrumpir el tratamiento de ' + medicamento + ' sin supervisión médica?'

        ]

    lista_consultas_contraindicaciones = \
        [
            '¿Qué efectos secundarios tiene ' + medicamento + '?',
            '¿Tiene el medicamento ' + medicamento + ' contraindicaciones no conocidas?',
            '¿Cuáles son las contraindicaciones de ' + medicamento + ' más conocidas?',
            '¿Puedo tomar ' + medicamento + ' si me acabo de vacunar?',
            '¿Tiene ' + medicamento + ' efectos adversos en el crecimiento de niños?',
            '¿Puedo tomar ' + medicamento + ' si estoy embarazada?',
            '¿Puedo tomar ' + medicamento + ' si estoy dándole el pecho a mi hijo?',
            '¿Si tomo ' + medicamento + ' daría positivo en controles antidoping?',
            '¿Qué efectos secundarios tiene ' + medicamento + ' a largo plazo?',
            '¿Tiene ' + medicamento + ' efectos secundarios si los mezclo con otros medicamentos?',
            '¿Puedo tomar ' + medicamento + ' si soy diabético?',
            '¿Si tomo ' + medicamento + ' disminuye la eficacia de los anticonceptivos?',
            '¿Puede interferir ' + medicamento + ' con otros medicamentos?',
            '¿Puedo conducir si tomo ' + medicamento + '?',
            '¿Puedo manejar maquinaria en mi puesto de trabajo si tomo ' + medicamento + '?',
            '¿Puedo consumir alcohol si tomo ' + medicamento + '?',
            '¿Existe alguna contraindicación alimentaria si tomo ' + medicamento + '?',
            '¿Con qué medicamentos no puedo tomar ' + medicamento + '?'

        ]

    lista_consultas_efectos_adversos = \
        [
            '¿Qué efectos adversos puede tener ' + medicamento + '?',
            '¿Tiene ' + medicamento + ' frecuencia de efectos adversos no conocidas?',
            '¿Es el constipado una reacción adversa a ' + medicamento + '?'
        ]

    lista_consultas_conservacion = \
        [
            '¿Cómo se conserva ' + medicamento + '?',
            '¿Se puede conservar ' + medicamento + ' en un armario?',
            '¿Se puede conservar ' + medicamento + ' en un frigorífico?',
            '¿Se puede conservar ' + medicamento + ' en casa una vez abierto el envase?'

        ]
    consultas = [lista_consultas_casos_de_uso, lista_consultas_contraindicaciones,
                 lista_consultas_posologia, lista_consultas_efectos_adversos,
                 lista_consultas_conservacion]
    return consultas


def mostrar_menu():
    print(print_msg_box(
        'BIENVENIDO AL SISTEMA PREGUNTA-RESPUESTA'.center(150, '*') + '\nAutor: Carlos Yanguas'
                                                                      '\nGithub user:'
                                                                      ' c-yanguas'))
    salir = 0
    while not salir:
        print('\n\n\n')
        print(print_msg_box('OPCIONES DEL SISTEMA PREGUNTA-RESPUESTA'.center(100, '*') +
                            '\n1-Imprimir por pantalla una prueba general de las preguntas sobre todos los medicamentos'
                            '\n2-Ejecutar una prueba general sobre un único medicamento'
                            '\n3-Ejecutar una prueba general sobre todos los medicamentos y volcarlo en un txt'
                            '\n4-Ver las preguntas generales para cada dimension'
                            '\n5-Realizar una consulta'
                            '\n6-Finalizar el programa'))
        opcion = input('\nESCRIBA SU OPCIÓN: ')
        es_int = 0
        while not es_int:
            try:
                opcion = int(opcion)
                if 0 < opcion < 7:
                    es_int = True
                else:
                    opcion = input(
                        'Por favor, elija una de las posibles opciones \'' + str(opcion) + '\' no es una de ellas: ')
            except ValueError:
                opcion = input(
                    'Por favor, elija una de las posibles opciones \'' + str(opcion) + '\' no es una de ellas: ')

        if opcion == 1:
            imprimir_prueba_general()
        elif opcion == 2:
            mostrar_menu_2()
        elif opcion == 3:
            volcar_en_fichero_prueba_general()
        elif opcion == 4:
            consultas = obtener_consultas_medicamento('NOMBRE_MEDICAMENTO')
            for tipo_consulta in range(len(consultas)):
                print(print_msg_box('\n'.join(consultas[tipo_consulta]), title=nombre_dimensiones[tipo_consulta]))
        elif opcion == 5:
            consulta = input('Introduce la consulta que deseas realizar al sistema: ')
            print(interpretar_consulta(consulta))
        else:
            salir = 1


mostrar_menu()
