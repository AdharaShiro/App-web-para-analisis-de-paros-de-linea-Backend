import io
from django.core.management.base import BaseCommand
from django.http import HttpResponse
from ...reports.utils import generar_reporte_por_turno, generar_reporte_excel

class Command(BaseCommand):
    help = 'Generar reporte de bitácoras en PDF y Excel'

    def handle(self, *args, **kwargs):
        response_pdf = HttpResponse(content_type='application/pdf')
        response_pdf['Content-Disposition'] = 'attachment; filename="reporte_bitacoras.pdf"'

        turnos = ['Matutino', 'Vespertino', 'Nocturno']
        generar_reporte_por_turno(response_pdf, turnos)

        # Guardar el archivo PDF
        with open('reporte_bitacoras.pdf', 'wb') as f:
            f.write(response_pdf.content)
        self.stdout.write(self.style.SUCCESS('Reporte PDF generado exitosamente'))

        # Generar y guardar el archivo Excel
        generar_reporte_excel(turnos)
        self.stdout.write(self.style.SUCCESS('Reporte Excel generado exitosamente'))
