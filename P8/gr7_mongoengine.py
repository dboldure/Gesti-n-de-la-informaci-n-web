# -*- coding: utf-8 -*-
 
## Asignatura: Gestión de la información en la Web
## Practica: MongoEngine
## Grupo: 7
## Autores: MIGUEL ÁNGEL ARROYO CLEMENTE, DANIELA-NICOLETA BOLDUREANU, DAVID PRATS ULLOA, IVÁN RUIZ QUINTANA
## MIGUEL ÁNGEL ARROYO CLEMENTE, DANIELA-NICOLETA BOLDUREANU, DAVID PRATS ULLOA, IVÁN RUIZ QUINTANA declaramos 
## que esta solución es fruto exclusivamente de nuestro trabajo personal. 
## No hemos sido ayudados por ninguna otra persona ni hemos obtenido la solución de fuentes externas, 
## y tampoco hemos compartido nuestra solución con nadie. 
## Declaramos además que no hemos realizado de manera deshonesta ninguna otra 
## actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.

from mongoengine import *

#client = pymongo.MongoClient()
#db = client.giw_mongoengine

connect('giw_mongoengine')

#Completo (Correcto)
class Producto(Document):
    codigoBarrasEAN=StringField(required=True,unique=True, max_length=13,regex="[0-9]{13}")
    nombre=StringField(required=True)
    catPrincipal=IntField(required=True,min_value=0)
    ListaCatSec=ListField(IntField(min_value=0))
    
    def calcularCodigo(self):
        code = self.codigoBarrasEAN[0:12]
        digits = list(reversed(code))
        even = [int(i) for i in digits[0::2]]
        odd = [int(i) for i in digits[1::2]]
        number = sum(odd) + sum(even) * 3
        checksum = (10 - (number % 10)) % 10
        result = checksum == int(self.codigoBarrasEAN[12])
        return result
    
    def comprobarCategoriaPrincipal(self):
        categoria = self.catPrincipal
        if (len(self.ListaCatSec > 0)):
            return self.ListaCatSec[0] == categoria
        return True
        
    def clean(self):
        if self.calcularCodigo()==False:
            raise ValidationError("La cifra de control del codigo EAN-13 no es correcta")
        if self.comprobarCategoriaPrincipal()==False:
            raise ValidationError("La categoria principal del producto no se encuentra en las categorias secundarias")

#Completo (Correcto)
class Linea_de_pedido(EmbeddedDocument):
    cantProdCompr=IntField(required=True)
    precioProd=FloatField(required=True)
    nombreProd=StringField(required=True)
    precioTotalLinea=FloatField(required=True)
    refProd=ReferenceField(Producto,required=True)

    #4El nombre del producto de una l´ınea de pedido es el mismo que el del producto al que apunta la referencia
    def errorNombre(self):
        return self.nombreProd != self.refProd.nombre
        
    def clean(self):
        totalCalculado = self.precioProd*self.cantProdCompr
        if self.precioTotalLinea != totalCalculado:
            self.precioTotalLinea = totalCalculado
        if self.errorNombre():
            raise ValidationError("El nombre del producto de esta linea no es el mismo que el del producto al que apunta la referencia")

class Tarjeta(EmbeddedDocument):
     nombrePropietario=StringField(required=True)
     numeroTarjeta=StringField(required=True, max_length=16,regex="[0-9]{16}")
     mesCaducidad=StringField(required=True, max_length=2,regex ="(0[1-9]|1[0-2])")
     anioCaducidad=StringField(required=True, max_length=2 ,regex ="[0-9][0-9]")
     cvv=StringField(required=True, max_length=3, regex="[0-9]{3}")

#Completo (Correcto)
class Pedido(Document):
    precioTotal=FloatField(required=True)
    fechaPedidio=ComplexDateTimeField(required=True)
    listLineaPedido=ListField(EmbeddedDocumentField(Linea_de_pedido),required=True)

    #2El precio total de un pedido es exactamente la suma de los precios de todas sus lineas.
    def sumaLineas(self):
        total=0
        for linea in self.listLineaPedido:
            total=total+(linea.precioProd*linea.cantProdCompr)
        return total
        
    def clean(self):
        precioTotalCalculado = self.sumaLineas()
        if self.precioTotal != precioTotalCalculado:
            self.precioTotal = precioTotalCalculado

#Completo (Correcto)
class Usuario(Document):
    dni=StringField(required=True, unique=True, max_length=9, regex="\d{8}[A-Z]")
    nombre=StringField(required=True)
    primerApellido=StringField(required=True)
    segundoApellido=StringField()
    fechaNacimiento=StringField(required=True, max_length=10, regex="(\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))")
    lastAccess=ComplexDateTimeField()
    listTarjetas=ListField(EmbeddedDocumentField(Tarjeta))
    
    #reverse_delete_rule=PULL, Elimina dicha referencia de la lista.
    listPedidos=ListField(ReferenceField(Pedido, reverse_delete_rule=PULL))
    
    def clean(self):
        numero = int(self.dni[0:8])
        diccionario = {0:"T",1:"R",2:"W",3:"A",4:"G",5:"M",6:"Y",7:"F",8:"P",9:"D",10:"X",
               11:"B",12:"N",13:"J",14:"Z",15:"S",16:"Q",17:"V",18:"H",19:"L",
               20:"C",21:"K",22:"E"}
        resto = numero%23
        letra = diccionario[resto]
        if letra != self.dni[8]:
            raise ValidationError("El digito de control del DNI no es correcto")
     
def insertar():
    naranja = Producto("1234567890418", "Naranja", 5, [5,4])
    naranja.save()
    
    pera = Producto("9780201379624", "Pera", 1, [1,0])
    pera.save()
    
    manzana = Producto("2894563781128", "Manzana", 2, [2,3,4])
    manzana.save()
    
    platano = Producto("2543675432564", "Platano", 8, [8,7,9,6])
    platano.save()
    
    cereza = Producto("7893452341127", "Cereza", 3, [3,1])
    cereza.save()
    
    kiwi = Producto("1324564345766", "Kiwi", 4, [4,5,1])
    kiwi.save()
    
    fresa = Producto("5435678345620", "Fresa", 5, [5,1,9])
    fresa.save()
    
    melocoton = Producto("1247568754658", "Melocoton", 6, [6,5])
    melocoton.save()
    
    mandarina = Producto("9825467435643", "Mandarina", 7, [7,8,3,5])
    mandarina.save()
    
    sandia = Producto("1785643543259", "Sandia", 9, [9,8,5])
    sandia.save()
    
    #Hacer en total 10 - 15 productos
    
    linea1 = Linea_de_pedido(10, 5.5, "Naranja", 55, naranja)
    linea1.save()
    
    linea2 = Linea_de_pedido(2, 2, "Naranja", 4, naranja)
    linea2.save()
    
    linea3 = Linea_de_pedido(3, 4, "Naranja", 12, naranja)
    linea3.save()
    
    linea4 = Linea_de_pedido(4, 2.3, "Pera", 9.2, pera)
    linea4.save()
    
    linea5 = Linea_de_pedido(1, 6, "Pera", 6, pera)
    linea5.save()
    
    linea6 = Linea_de_pedido(2, 2.5, "Manzana", 5, manzana)
    linea6.save()
    
    linea7 = Linea_de_pedido(6, 6.3, "Manzana", 37.8, manzana)
    linea7.save()
    
    linea8 = Linea_de_pedido(2, 3, "Platano", 6, platano)
    linea8.save()
    
    linea9 = Linea_de_pedido(1, 6, "Platano", 6, platano)
    linea9.save()
    
    linea10 = Linea_de_pedido(5, 7, "Platano", 35, platano)
    linea10.save()
    
    linea11 = Linea_de_pedido(7, 8, "Cereza", 56, cereza)
    linea11.save()
    
    linea12 = Linea_de_pedido(3, 9.5, "Cereza", 28.5, cereza)
    linea12.save()
    
    linea13 = Linea_de_pedido(6, 4, "Cereza", 12, cereza)
    linea13.save()
    
    linea14 = Linea_de_pedido(23, 3, "Kiwi", 69, kiwi)
    linea14.save()
    
    linea15 = Linea_de_pedido(2, 6, "Kiwi", 12, kiwi)
    linea15.save()
    
    linea16 = Linea_de_pedido(8, 3, "Kiwi", 24, kiwi)
    linea16.save()
    
    linea17 = Linea_de_pedido(8, 6.7, "Fresa", 53.6, fresa)
    linea17.save()
    
    linea18 = Linea_de_pedido(9, 1, "Fresa", 9, fresa)
    linea18.save()
    
    linea19 = Linea_de_pedido(10, 2, "Melocoton", 20, melocoton)
    linea19.save()
    
    linea20 = Linea_de_pedido(56, 4, "Melocoton", 224, melocoton)
    linea20.save()
    
    linea21 = Linea_de_pedido(3, 3, "Mandarina", 9, mandarina)
    linea21.save()
    
    linea22 = Linea_de_pedido(5, 4, "Mandarina", 20, mandarina)
    linea22.save()
    
    linea23 = Linea_de_pedido(34, 9, "Sandia", 306, sandia)
    linea23.save()
    
    linea24 = Linea_de_pedido(2, 1.5, "Sandia", 3, sandia)
    linea24.save()
    
    linea25 = Linea_de_pedido(4, 3, "Sandia", 12, sandia)
    linea25.save()
   
    
    #Hacer 25 lineas (y repartirlas entre los pedidos pero que todos los pedidos tengan mas de 2 lineas)
    
    pedido1 = Pedido(86.2, "2019,11,20,12,15,10,123456", [linea1, linea2, linea3, linea4, linea5])
    pedido1.save() 
    
    pedido2 = Pedido(54.8, "2019,11,20,09,24,40,456234", [linea6, linea7, linea8, linea9])
    pedido2.save()
    
    pedido3 = Pedido(131,5, "2019,11,09,12,32,10,698432", [linea10, linea11, linea12, linea13])
    pedido3.save()
    
    pedido4 = Pedido(81, "2019,11,03,12,17,35,235189", [linea14, linea15])
    pedido4.save()
    
    pedido5 = Pedido(86.6, "2019,11,01,18,15,10,451224", [linea16, linea17, linea18])
    pedido5.save()
    
    pedido6 = Pedido(253, "2019,10,27,11,24,43,887564", [linea19, linea20, linea21])
    pedido6.save()
    
    pedido7 = Pedido(341, "2019,10,24,12,02,05,322168", [linea22, linea23, linea24, linea25])
    pedido7.save()
    
    #hacer 7 pedidos (3 para un usuario y 2 para cada uno de los restantes)
    
    tarjeta1 = Tarjeta("Miguel", "1234432112344322", "12", "20", "123")
    tarjeta1.save()
    
    tarjeta2 = Tarjeta("Miguel", "2957483964376328", "11", "23", "432")
    tarjeta2.save()
    
    tarjeta3 = Tarjeta("Miguel", "9472684627586745", "05", "21", "378")
    tarjeta3.save()
    
    tarjeta4 = Tarjeta("Ivan", "1276954378947264", "03", "28", "657")
    tarjeta4.save()
    
    tarjeta5 = Tarjeta("Ivan", "7493526584637234", "01", "27", "423")
    tarjeta5.save()
    
    #hacer 5 tarjetas (un usuario con 3, otro con 2, y otro con 0)
    
    paco= Usuario(dni="58056402D", nombre="Paco", primerApellido="perez",fechaNacimiento="1993-12-02", listPedidos=[pedido1, pedido2, pedido3])
    paco.save()
    
    miguel= Usuario("11842691Z", "Miguel", "perez", "hola", "1993-12-02", "2019,11,20,12,15,10,123456", [tarjeta1, tarjeta2, tarjeta3], [pedido4, pedido5])
    miguel.save()
    
    ivan= Usuario("05441027D", "Ivan", "Ruiz", "Quintana", "1998-06-29", "2019,11,18,11,20,01,846371", [tarjeta4, tarjeta5], [pedido6, pedido7])
    ivan.save()
    
    #hacer 3 usuarios
    
insertar()
