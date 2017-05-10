# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
def start(request):
	nombre = "Andriy",
	tupla = (1,2,3)
	context = {
    	'saludo': 'hola mundo', 
    	'tupla':tupla,
    	'nombre': nombre,
    }
    # devolvemos los datos a la vista saludo.html para printarlos
	return render(request, 'inicio.html', context)
