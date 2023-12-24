import os
import random

from django.shortcuts import render
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus.flowables import Flowable


from .forms import EcuacionesForm
from .utils import generar_ecuaciones
from django.http import HttpResponse

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import io
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph

def dividir_en_filas(lista, elementos_por_fila):
    return [lista[i:i + elementos_por_fila] for i in range(0, len(lista), elementos_por_fila)]

def print_Ast():
    print('********************************************************')

class VerticalCenteredParagraph(Flowable):
    def __init__(self, paragraph):
        self.paragraph = paragraph
        Flowable.__init__(self)

    def wrap(self, availWidth, availHeight):
        self.width, self.height = self.paragraph.wrap(availWidth, availHeight)
        return self.width, self.height

    def draw(self):
        self.canv.saveState()
        self.canv.translate(0, (self.height - self.paragraph.height) / 2)
        self.paragraph.drawOn(self.canv, 0, 0)
        self.canv.restoreState()


def index(request):
    carpetas = os.listdir(os.path.join("static", "img", "listado"))
    count = request.session.get('count', 0)
    request.session['count'] = count + 1

    if request.method == 'POST':
        form = EcuacionesForm(request.POST)
        if form.is_valid():
            num_variables = int(form.cleaned_data['num_variables'])
            suma_maxima = int(form.cleaned_data['suma_maxima'])
            num_ejercicios = int(form.cleaned_data['num_ejercicios'])
            carpeta_seleccionada = request.POST.get('carpeta')
            request.session['carpeta_seleccionada'] = carpeta_seleccionada

            # Generar las ecuaciones en el archivo views.py
            ecuaciones, var_img = generar_ecuaciones(num_variables, suma_maxima, num_ejercicios, carpeta_seleccionada)

            request.session['ecuaciones'] = ecuaciones
            request.session['var_img'] = var_img

            creadas = request.session.get('creadas', 0)
            request.session['creadas'] = creadas + 1




            return render(request, 'index.html', {'form': form, 'ecuaciones': ecuaciones
                , 'carpetas': carpetas, 'var_img':var_img, 'carpeta_seleccionada': carpeta_seleccionada
                                                  , 'creadas': creadas})
    else:
        form = EcuacionesForm()

    return render(request, 'index.html', {'form': form, 'carpetas': carpetas, 'count': count})

def crear_pdf(request):
    if request.method == 'POST':

        ecuaciones = request.session.get('ecuaciones')
        var_img = request.session.get('var_img')
        num_incognitas = len(ecuaciones[0])
        carpeta_seleccionada = request.session.get('carpeta_seleccionada')
        NUM_COLUMNAS = 3

        # Crear el documento PDF con ReportLab
        buffer = io.BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=25,
            rightMargin=25,
            title="Generador de Sumas",
            author="David",
            subject="Página de Sumas",
        )

        formatted_rows = []
        style = getSampleStyleSheet()

        # Obtener el número de filas y columnas
        num_ejercicios = len(ecuaciones[0])  # Número total de ejercicios en una columna
        actividades_por_fila = num_incognitas  # Número de actividades en una fila



        # Agregar las filas de ecuaciones
        for i in range(0, num_ejercicios, actividades_por_fila):  # Incrementar i según actividades_por_fila
            row = []
            for j in range(len(ecuaciones)):  # Iterar sobre las columnas
                column_content = []
                for k in range(actividades_por_fila):  # Iterar sobre las filas
                    ejercicio_index = i + k
                    if ejercicio_index < num_ejercicios:
                        equation = ecuaciones[j][ejercicio_index]

                        result = equation[len(equation) - 1]
                        image_paths = equation[:-1]
                        images_str = " + ".join([f'<img src="{path}" width="22" height="22"/>' for path in image_paths])
                        column_content.append(f'{images_str} = {result}')

                        salto = '<br/><br/>'
                        ejercicio_actual = salto.join(column_content)

                        key = str(j)
                        if key in var_img:
                            img_vars = var_img[key]
                        else:
                            img_vars = []  # Si no existe la clave, utilice una lista vacía

                        # Divide las imágenes en filas con 2 imágenes por fila
                        img_vars_filas = dividir_en_filas(img_vars, 2)

                        # Crea una cadena con las imágenes y los cuadrados en la forma deseada
                        img_str = ""
                        for fila in img_vars_filas:
                            img_linea = "       ".join(
                                [f'<img src="{path}" width="16" height="16"/> = [<u>&nbsp;&nbsp;&nbsp;&nbsp;</u>]' for
                                 path in fila])
                            img_str += img_linea + "<br/><br/>"



                        # Reemplaza las variables en ejercicio_actual con las imágenes
                        ejercicio_actual = ejercicio_actual + salto + img_str + salto

                # Unir las ecuaciones con un salto de línea
                style['BodyText'].alignment = TA_CENTER
                column_paragraph = Paragraph(ejercicio_actual, style['BodyText'])

                # row.append(column_paragraph)
                row.append(VerticalCenteredParagraph(column_paragraph))

                if (j + 1) % NUM_COLUMNAS == 0:
                    formatted_rows.append(row)
                    row = []

            # Añadir la última fila si no es múltiplo de 3
            if row:
                formatted_rows.append(row)

        table = Table(formatted_rows, colWidths='*', rowHeights=16 * 4 * 3)

        # Establecer el estilo de la tabla
        estilo_tabla = TableStyle([
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ])

        # Si la tabla solo tiene una fila, no se muestran las líneas horizontales
        if len(formatted_rows) == 1:
            print("")
        else:
            estilo_tabla.add('LINEABOVE', (0, -1), (-1, -1), 0.0, colors.black),
            estilo_tabla.add('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.black)

        table.setStyle(estilo_tabla)

        # Agregar la tabla al documento y cerrarlo
        doc.build([table])

        # Devolver el archivo PDF generado como una respuesta HTTP
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=sumas.pdf'


        return response

    return render(request, 'pdf_template.html')

def visitas(request):
    # Obtener el contador de visitas de la sesión
    count = request.session.get('count', 0)
    creadas = request.session.get('creadas', 0)

    # Resto del código de la vista...

    return render(request, 'visitas.html', {'count': count, 'creadas':creadas})

