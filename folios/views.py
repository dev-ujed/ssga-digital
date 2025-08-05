from django.shortcuts import redirect, render, get_object_or_404
from folios.forms import *
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from .models import *
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q  # Para búsquedas más complejas
from django.contrib.auth.decorators import login_required

@login_required
def subirExcel(request):
    if request.method == 'POST':
        form = SubirExcelForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Guardar archivo con nombre original
                excel_file = form.save(commit=False)
                excel_file.nombre_original = request.FILES['archivo'].name
                excel_file.save()  # Esto disparará la señal post_save

                messages.success(request, "Archivo subido y procesado correctamente.")
                return redirect('subir')

            except ValueError as e:  # Captura el error de columnas faltantes
                messages.error(request, str(e))
                if excel_file.pk:  # Elimina el archivo si se guardó
                    excel_file.delete()
                return render(request, 'subir_excel.html', {'form': form})

            except Exception as e:  # Otros errores inesperados
                messages.error(request, f"Error inesperado: {str(e)}")
                if excel_file.pk:
                    excel_file.delete()
                return render(request, 'subir_excel.html', {'form': form})
    else:
        form = SubirExcelForm()
    
    return render(request, 'subir_excel.html', {'form': form})


class ParticipantesListView(ListView):
    model = Producto 
    context_object_name = 'participantes'
    template_name = 'participantes.html'

    def get_queryset(self):
        query = self.request.GET.get('q')  # 'q' es el nombre del parámetro de búsqueda
        if query:
            # Filtra los resultados (ajusta los campos según tu modelo)
            return Producto.objects.filter(
                Q(actividad__icontains=query) | 
                Q(folio__icontains=query) |  
                Q(nombre__icontains=query) 
            )
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_term'] = self.request.GET.get('q', '')
        return context


def buscar_folio(request):
    if request.method == 'POST':
        form = BuscarFolioForm(request.POST)
        if form.is_valid():
            folio = form.cleaned_data['folio'].strip()  # Eliminar espacios
            productos = Producto.objects.filter(folio__iexact=folio)  # Buscar como texto
            return render(request, 'resultado_folio.html', {
                'productos': productos,
                'folio_buscado': folio,
            })
    else:
        form = BuscarFolioForm()
    
    return render(request, 'validacion_folio.html', {'form': form})

class AddParticipante(CreateView):
    model = Producto
    form_class = AddProductoForm
    template_name = 'create.html'
    success_url = reverse_lazy('participantes')


class DelParticipante(DeleteView):
    model = Producto
    template_name = 'del_participante.html'
    success_url = reverse_lazy('participantes')


class UpdateParseView(UpdateView):
    model = Producto
    template_name = 'edit_participante.html'
    form_class = AddProductoForm
    success_url = reverse_lazy('participantes') 