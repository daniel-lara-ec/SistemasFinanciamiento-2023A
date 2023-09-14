from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import pandas as pd
import json
from .forms import FormularioSeguro
from pathlib import Path
from pyliferisk import MortalityTable, Actuarial, Ax, Axn, nEx
import numpy as np
import plotly.graph_objects as go
import os
from django.shortcuts import get_object_or_404

archivo = "/home/azureuser/myprojectdir/static/files/Mortalidad_Amazonia.xlsx"
BASE_DIR = Path(__file__).resolve().parent.parent

FILES = os.path.join(BASE_DIR, "static/files")


def Procesodf(df):
    json_df = df.reset_index().to_json(orient="records")
    df_json_export = json.loads(json_df)
    return df_json_export


def Home(request):
    return render(request, "index.html")


def Hipotesis(request):
    df_rs_pensionistas = pd.read_excel(
        FILES + "/RepartoSimple.xlsx", sheet_name="Pensionistas"
    )

    # fill empty values with 0
    df_rs_pensionistas = df_rs_pensionistas.fillna(0)
    # round to int values
    df_rs_pensionistas = df_rs_pensionistas.astype(int)

    json_pensionistas = Procesodf(df_rs_pensionistas)

    return render(request, "Hipotesis.html", {"json_pensionistas": json_pensionistas})


def RepartoSimple(request):
    df_rs_resumen = pd.read_excel(FILES + "/RepartoSimple.xlsx", sheet_name="Resumen")
    df_rs_gasto = pd.read_excel(FILES + "/RepartoSimple.xlsx", sheet_name="Gasto")
    df_rs_tasas = pd.read_excel(FILES + "/RepartoSimple.xlsx", sheet_name="Tasas")

    # round to 2 decimals
    df_rs_resumen = df_rs_resumen.round(2)
    df_rs_gasto = df_rs_gasto.round(2)
    df_rs_tasas = df_rs_tasas.round(2)

    #############################################

    json_resumen = Procesodf(df_rs_resumen)
    json_gasto = Procesodf(df_rs_gasto)
    json_tasas = Procesodf(df_rs_tasas)

    #############################################
    #############################################
    df_rs_tasas = pd.read_excel(FILES + "/RepartoSimple.xlsx", sheet_name="Tasas")
    df_rs_tasas = df_rs_tasas.round(2)

    # get columns of df_rs_tasas

    df_rs_tasas = df_rs_tasas.set_index("Descripcion")
    listado_leyenda = list(df_rs_tasas.index)
    edades = list(df_rs_tasas.columns)

    datos = []

    for i in range(len(listado_leyenda)):
        datos.append(
            {
                "name": listado_leyenda[i],
                "type": "line",
                "data": list(df_rs_tasas.iloc[i].values),
            }
        )

    chart = {
        "tooltip": {
            "show": True,
            "trigger": "axis",
            "triggerOn": "mousemove|click",
        },
        "toolbox": {
            "show": True,
            "feature": {
                "dataZoom": {"yAxisIndex": "none"},
                "magicType": {"type": ["line", "bar"]},
                "restore": {},
                "saveAsImage": {},
            },
        },
        "legend": {
            "data": listado_leyenda,
            "x": "center",
            "bottom": 0,
        },
        "title": {"text": "Tasas de cotización (Reparto simple)"},
        "xAxis": {"type": "category", "data": edades},
        "yAxis": {"type": "value"},
        "series": datos,
    }

    return render(
        request,
        "RepartoSimple.html",
        {
            "json_resumen": json_resumen,
            "json_gasto": json_gasto,
            "json_tasas": json_tasas,
            "chartjson": chart,
        },
    )

def DescargarRepartoSimple(request):
    with open(FILES + "/RepartoSimle_Completo.xlsx", "rb") as file:
        response = HttpResponse(file.read(), content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = "attachment; filename=RepartoSimple.xlsx"

        return response


#############################################
#############################################
# Reparto Simple Revalorizado
#############################################
#############################################


def SimpleRevalorizado(request):
    df_rs_resumen = pd.read_excel(
        FILES + "/SimpleRevalorizado.xlsx", sheet_name="Resumen"
    )
    df_rs_gasto = pd.read_excel(FILES + "/SimpleRevalorizado.xlsx", sheet_name="Gasto")
    df_rs_tasas = pd.read_excel(FILES + "/SimpleRevalorizado.xlsx", sheet_name="Tasas")

    # round to 2 decimals
    df_rs_resumen = df_rs_resumen.round(2)
    df_rs_gasto = df_rs_gasto.round(2)
    df_rs_tasas = df_rs_tasas.round(2)

    #############################################

    json_resumen = Procesodf(df_rs_resumen)
    json_gasto = Procesodf(df_rs_gasto)
    json_tasas = Procesodf(df_rs_tasas)

    return render(
        request,
        "SimpleRevalorizado.html",
        {
            "json_resumen": json_resumen,
            "json_gasto": json_gasto,
            "json_tasas": json_tasas,
        },
    )


def DescargarSimpleRevalorizado(request):
    with open(FILES + "/SimpleRevalorizado_Completo.xlsx", "rb") as file:
        response = HttpResponse(file.read(), content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = "attachment; filename=RepartoSimpleRevalorizado.xlsx"

        return response


#############################################
#############################################
# Escalonado
#############################################
#############################################


def Escalonado(request):
    df_resumen = pd.read_excel(FILES + "/Escalonado.xlsx", sheet_name="Resumen")
    df_gasto = pd.read_excel(FILES + "/Escalonado.xlsx", sheet_name="Gasto")
    df_salarios = pd.read_excel(FILES + "/Escalonado.xlsx", sheet_name="Salarios")
    df_pensiones = pd.read_excel(FILES + "/Escalonado.xlsx", sheet_name="Pensiones")
    df_tasas = pd.read_excel(FILES + "/Escalonado.xlsx", sheet_name="Tasas")
    df_reservas = pd.read_excel(FILES + "/Escalonado.xlsx", sheet_name="Reservas")

    # round to 2 decimals
    df_resumen = df_resumen.round(2)
    df_gasto = df_gasto.round(2)
    df_tasas = df_tasas.round(2)
    df_salarios = df_salarios.round(2)
    df_pensiones = df_pensiones.round(2)
    df_reservas = df_reservas.round(2)

    #############################################

    json_resumen = Procesodf(df_resumen)
    json_gasto = Procesodf(df_gasto)
    json_tasas = Procesodf(df_tasas)
    json_salarios = Procesodf(df_salarios)
    json_pensiones = Procesodf(df_pensiones)
    json_reservas = Procesodf(df_reservas)

    return render(
        request,
        "Escalonado.html",
        {
            "json_resumen": json_resumen,
            "json_gasto": json_gasto,
            "json_tasas": json_tasas,
            "json_salarios": json_salarios,
            "json_pensiones": json_pensiones,
            "json_reservas": json_reservas,
        },
    )


def DescargarEscalonado(request):
    with open(FILES + "/Escalonado_Completo.xlsx", "rb") as file:
        response = HttpResponse(file.read(), content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = "attachment; filename=RepartoEscalonado.xlsx"

        return response


def EscalonadoGrafico(request):
    df_rs_tasas = pd.read_excel(FILES + "/Escalonado.xlsx", sheet_name="Tasas")
    df_rs_tasas = df_rs_tasas.round(2)

    # get columns of df_rs_tasas
    # fil nan values with 0
    df_rs_tasas = df_rs_tasas.fillna(0)

    df_rs_tasas = df_rs_tasas.set_index("Descripcion")
    listado_leyenda = list(df_rs_tasas.index)
    edades = list(df_rs_tasas.columns)

    datos = []

    for i in range(len(listado_leyenda)):
        datos.append(
            {
                "name": listado_leyenda[i],
                "type": "line",
                "data": list(df_rs_tasas.iloc[i].values),
            }
        )

    chart = {
        "tooltip": {
            "show": True,
            "trigger": "axis",
            "triggerOn": "mousemove|click",
        },
        "toolbox": {
            "show": True,
            "feature": {
                "dataZoom": {"yAxisIndex": "none"},
                "magicType": {"type": ["line", "bar"]},
                "restore": {},
                "saveAsImage": {},
            },
        },
        "legend": {
            "data": listado_leyenda,
            "x": "center",
            "bottom": 0,
        },
        "title": {"text": "Tasas de cotización (Reparto escalonado))"},
        "xAxis": {"type": "category", "data": edades},
        "yAxis": {"type": "value"},
        "series": datos,
    }

    return JsonResponse(chart, safe=False)


#############################################
#############################################
# Reparto de capitales
#############################################
#############################################


def RepartoCapitales(request):
    df__rc_resumen = pd.read_excel(
        FILES + "/RepartoCapitales.xlsx", sheet_name="Resumen"
    )
    df__rc_rentas = pd.read_excel(FILES + "/RepartoCapitales.xlsx", sheet_name="Rentas")
    df__rc_gastos = pd.read_excel(FILES + "/RepartoCapitales.xlsx", sheet_name="Gasto")
    df__rc_flujos = pd.read_excel(
        FILES + "/RepartoCapitales.xlsx", sheet_name="FlujosReserva"
    )

    # round to 2 decimals
    df__rc_resumen = df__rc_resumen.round(2)
    df__rc_rentas = df__rc_rentas.round(2)
    df__rc_gastos = df__rc_gastos.round(2)
    # df__rc_flujos = df__rc_flujos.round(2)

    #############################################

    json_resumen = Procesodf(df__rc_resumen)
    json_rentas = Procesodf(df__rc_rentas)
    json_flujos = Procesodf(df__rc_flujos)
    json_gastos = Procesodf(df__rc_gastos)

    return render(
        request,
        "RepartoCapitales.html",
        {
            "json_resumen": json_resumen,
            "json_rentas": json_rentas,
            "json_flujos": json_flujos,
            "json_gastos": json_gastos,
        },
    )


def DescargarRepartoCapitales(request):
    with open(FILES + "/RepartoCapitales_Completo.xlsx", "rb") as file:
        response = HttpResponse(file.read(), content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = "attachment; filename=RepartoCapitales.xlsx"

        return response


def RepartoCapitalesGrafico(request):
    df_rc_flujos = pd.read_excel(
        FILES + "/RepartoCapitales.xlsx", sheet_name="FlujosReserva"
    )

    df_rc_flujos = df_rc_flujos[df_rc_flujos['Flujo']=='Reserva']
    df_rc_flujos = df_rc_flujos.drop(columns=['Flujo'])
    df_rc_flujos = df_rc_flujos.set_index("Descripcion")
    # drop column Flujo
    df_rc_flujos = df_rc_flujos.round(2)
    listado_leyenda = list(df_rc_flujos.index)
    edades = list(df_rc_flujos.columns)

    datos = []

    for i in range(len(listado_leyenda)):
        datos.append(
            {
                "name": listado_leyenda[i],
                "type": "line",
                "data": list(df_rc_flujos.iloc[i].values),
            }
        )

    chart = {
        "tooltip": {
            "show": True,
            "trigger": "axis",
            "triggerOn": "mousemove|click",
        },
        "toolbox": {
            "show": True,
            "feature": {
                "dataZoom": {"yAxisIndex": "none"},
                "magicType": {"type": ["line", "bar"]},
                "restore": {},
                "saveAsImage": {},
            },
        },
        "legend": {
            "data": listado_leyenda,
            "x": "center",
            "bottom": 0,
        },
        "title": {"text": "Reserva matemática (Reparto de capitales)"},
        "xAxis": {"type": "category", "data": edades},
        "yAxis": {"type": "value"},
        "series": datos,
    }

    return JsonResponse(chart, safe=False)


#############################################
#############################################
# Capitalizacion
#############################################
#############################################

def Capitalizacion(request):
    df_s_4h = pd.read_excel(FILES + "/Simulaciones.xlsx", sheet_name="Simu_4_H")
    df_s_4m = pd.read_excel(FILES + "/Simulaciones.xlsx", sheet_name="Simu_4_M")
    df_s_5h = pd.read_excel(FILES + "/Simulaciones.xlsx", sheet_name="Simu_5_H")
    df_s_5m = pd.read_excel(FILES + "/Simulaciones.xlsx", sheet_name="Simu_5_M")
    df_s_6h = pd.read_excel(FILES + "/Simulaciones.xlsx", sheet_name="Simu_6_H")
    df_s_6m = pd.read_excel(FILES + "/Simulaciones.xlsx", sheet_name="Simu_6_M")
    df_s_7h = pd.read_excel(FILES + "/Simulaciones.xlsx", sheet_name="Simu_7_H")
    df_s_7m = pd.read_excel(FILES + "/Simulaciones.xlsx", sheet_name="Simu_7_M")
    df_s_8h = pd.read_excel(FILES + "/Simulaciones.xlsx", sheet_name="Simu_8_H")
    df_s_8m = pd.read_excel(FILES + "/Simulaciones.xlsx", sheet_name="Simu_8_M")

    # round to 2 decimals
    df_s_4h = df_s_4h.round(2)
    df_s_4m = df_s_4m.round(2)
    df_s_5h = df_s_5h.round(2)
    df_s_5m = df_s_5m.round(2)
    df_s_6h = df_s_6h.round(2)
    df_s_6m = df_s_6m.round(2)
    df_s_7h = df_s_7h.round(2)
    df_s_7m = df_s_7m.round(2)
    df_s_8h = df_s_8h.round(2)
    df_s_8m = df_s_8m.round(2)

    json_s_4h = Procesodf(df_s_4h)
    json_s_4m = Procesodf(df_s_4m)
    json_s_5h = Procesodf(df_s_5h)
    json_s_5m = Procesodf(df_s_5m)
    json_s_6h = Procesodf(df_s_6h)
    json_s_6m = Procesodf(df_s_6m)
    json_s_7h = Procesodf(df_s_7h)
    json_s_7m = Procesodf(df_s_7m)
    json_s_8h = Procesodf(df_s_8h)
    json_s_8m = Procesodf(df_s_8m)

    return render(
        request,
        "Capitalizacion.html",
        {
            "json_s_4h": json_s_4h,
            "json_s_4m": json_s_4m,
            "json_s_5h": json_s_5h,
            "json_s_5m": json_s_5m,
            "json_s_6h": json_s_6h,
            "json_s_6m": json_s_6m,
            "json_s_7h": json_s_7h,
            "json_s_7m": json_s_7m,
            "json_s_8h": json_s_8h,
            "json_s_8m": json_s_8m,
        },
    )

def DescargarCapitalizacion(request):
    with open(FILES + "/Simulaciones.xlsx", "rb") as file:
        response = HttpResponse(file.read(), content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = "attachment; filename=SimulacionesCapitalizacion.xlsx"

        return response


def DescargarCapitalizacionAplicativo(request):
    with open(FILES + "/SimulacionesCodigo.R", "rb") as file:
        response = HttpResponse(file.read(), content_type="text/plain")
        response["Content-Disposition"] = "attachment; filename=SimulacionesCodigo.R"

        return response