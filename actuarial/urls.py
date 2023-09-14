from django.urls import path
from . import views

urlpatterns = [
    path("",views.Home,name="Index"),
    path("Hipotesis",views.Hipotesis,name="Hipotesis"),
    # Reparto simple    
    path("RepartoSimple",views.RepartoSimple,name="RepartoSimple"),
    path("DescargarRepartoSimple",views.DescargarRepartoSimple,name="DescargarRepartoSimple"),
    # Reparto simple revalorizado
    path("DescargarSimpleRevalorizado",views.DescargarSimpleRevalorizado,name="DescargarSimpleRevalorizado"),
    path("SimpleRevalorizado",views.SimpleRevalorizado,name="SimpleRevalorizado"),
    # Escalonado
    path("Escalonado",views.Escalonado,name="Escalonado"),
    path("EscalonadoGrafico",views.EscalonadoGrafico,name="EscalonadoGrafico"),
    path("DescargarEscalonado",views.DescargarEscalonado,name="DescargarEscalonado"),
    # Reparto capitales
    path("RepartoCapitales",views.RepartoCapitales,name="RepartoCapitales"),
    path("RepartoCapitalesGrafico",views.RepartoCapitalesGrafico,name="RepartoCapitalesGrafico"),
    path("DescargarRepartoCapitales",views.DescargarRepartoCapitales,name="DescargarRepartoCapitales"),
    # Capitalizacion
    path("Capitalizacion",views.Capitalizacion,name="Capitalizacion"),
    path("DescargarCapitalizacionAplicativo",views.DescargarCapitalizacionAplicativo,name="DescargarCapitalizacionAplicativo"),
    path("DescargarCapitalizacion",views.DescargarCapitalizacion,name="DescargarCapitalizacion"),
]
