library(lifecontingencies)

library(readxl)
install.packages("xlsx")
library(xlsx)

#Lectura de datos
prob_H<-read_excel("C:/Users/usuario/Downloads/Modelos de Financiamiento.xlsx",sheet = 1)[[4]]
prob_M<-read_excel("C:/Users/usuario/Downloads/Modelos de Financiamiento.xlsx",sheet = 2)[[4]]
TH<-probs2lifetable(probs=prob_H, radix=100000, type="qx", name = "Mortalidad Hombres")
TM<-probs2lifetable(probs=prob_M, radix=100000, type="qx", name = "Mortalidad Mujeres")

#Cálculo del ahorro de una persona que comienza a realizar aportaciones a la edad x=25
#Se jubila a la edad y, con salario dado según la tabla de salarios
#de la policia según edad y rango, que se va a revalorizar a través de los años
#con una tasa q1. Además se considera una tasa de cotización tc=0.1

#Sexo
TS<-TH
#Edad
x<-25
#Edad de jubilación
y<-65
#Salario Básico Unificado
SBU<-450
#Salario
Salary<-numeric(45)
#Tasa de revalorización salarial
q1<-1+0.03
#Tasa de cotización
tc<-0.10
#Tasa de interés
i<-0.04
#Gastos administrativos
ga<-0.001
#Tasa de interés efectiva
ie<-i-ga



#Ahora calcularemos el ahorro de todos los años. Este cálculo es financiero, no actuarial
#Se consideran 12 aportaciones anuales de cuantía dada por la tabla de salarios
#que se revaloriza según la revalorización del salario.

Salary<-c(960,1061,1184,1331,1505,1553,1770,2436,2643)
Salary<-rep(Salary,each=5)
Salary



Ahorro<-function(x,y,Salary,q1,tc,ie){
  ie12<-((1+ie)^(1/12))-1
  s<-(((1+ie12)^12)-1)/ie12
  a<-0
  for (j in 1:(y-x-1)) {
    a<-a+(Salary[j]*tc*(q1^(j-1)))*s*(1+ie)^(y-j)
  }
  return(a)
}
ahorro<-Ahorro(x,y,Salary,q1,tc,ie)
ahorro

#Cálculo de la pensión. Se considera que con el ahorro obtenido se compra una renta vitalicia.
#Para esto apartir del ahorro encontrado, se calculara una pensión P
#constante que se revalorizará con una tasa q2.
#La pensión considera 13 pagos y un SBU adicional.
#La pensión calculada será solamente un porcentaje de la pension completa PC, pues se considera
#un aporte del estado default AE del 40%

#Este cálculo es actuarial.
#Tasa de revalorización de pension
q2<-1+0.02
AE<-0.4

pension<-function(ahorro,TS,y,q2,ie){
  P1<-0
  S1<-0
  for (j in 0:(99-y)) {
    S1<-12*((q2)^j)*axn(TS,x=y,n=1,k=12,i=ie,m=j,payment = "immediate")
    P1<-P1+S1
  }
  P2<-0
  S2<-0
  for (j in 0:(99-y)) {
    S2<-((q2)^j)*axn(TS,x=y,n=1,i=ie,m=j,payment = "immediate")
    P2<-P2+S2
  }
  P3<-0
  S3<-0
  for (j in 0:(99-y)) {
    S3<-((q1)^j)*axn(TS,x=y,n=1,i=ie,m=j,payment = "immediate")
    P3<-P3+S3
  }
  return((ahorro-((SBU*q1^(y-25))*P3))/(P1+P2)) 
}
P<-pension(ahorro,TS,y,q2,ie)
PC<-P/(1-AE)
PC
#Para obtener la tasa de remplazo se descuenta el valor de la PC hasta la edad de inicio de aportaciones
#Ejemplo
PC_des<-PC/((1+ie)^(y-x))
PC_des
TR<-PC_des/Salary
TR

#Ahora se generan los datos para las tablas. Siempre se considera la edad de ingreso a como x=25
#Interes de 4 a 8, Salario dado por los salarios de policias y rangos y 0 de gastos administrativos
#Para la generación de todas las tablas se considero una tasa de revalorización salarial del
#q1 del 0.03 y de revalorización de pensiones q2 del 0.02

#Función generadora de tablas
tablas<-function(Salario, Edad_ingreso, interes, TS, RevPen, RevSal,TasaCot,AE){
  Edad<-numeric(70-50)
  for (j in 50:70) {
    Edad[j-50+1]<-j
  }
  Edad
  Pen_Table<-numeric(70-50)
  for (j in 50:70) {
    Pen_Table[j-50+1]<-(pension(Ahorro(Edad_ingreso,j,Salario,RevSal,TasaCot,interes),TS,j,RevPen,interes)/(1-AE))
  }
  Pen_Table
  Tasa_Rem<-numeric(70-50)
  for (j in 50:70) {
    Tasa_Rem[j-50+1]<-(Pen_Table[j-50+1]/((1+interes)^(j-25)))/(Salario[j-25-1])
  }
  Tasa_Rem
  
  #Esperanza residual de vida
  Erv<-numeric(70-50)
  for (j in 50:70) {
    Erv[j-50+1]<-exn(TS,x=j)
  }
  Erv
  
  Pen_Rev<-numeric(70-50)
  for (j in 50:70) {
    Pen_Rev[j-50+1]<-Pen_Table[j-50+1]*(1+interes)^(-(j-25))
    }
  Pen_Rev
  
  return(data.frame(Edad=Edad,Pension=Pen_Table,Pension_VA=Pen_Rev,Tasa_Reemplazo=Tasa_Rem, Esperanza_vida=Erv))

  
  
  }

#Aquí se generan las tablas

for (a in 1:5) {
  nombre<-paste0("Simu_",a+3,"_M.xlsx")
  nombre1<-paste0("Simu_",a+3,"_M")
  write.xlsx(tablas(Salary, 25, ((3+a)/100), TM, q2, q1,0.1,0.4),nombre,sheetName = nombre1)
} 



