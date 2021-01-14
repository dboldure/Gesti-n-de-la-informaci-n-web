 # -*- coding: utf-8 -*-
 
## Asignatura: Gestión de la información en la Web
## Practica Aggregation Pipeline
## Grupo: 7
## Autores: MIGUEL ÁNGEL ARROYO CLEMENTE, DANIELA-NICOLETA BOLDUREANU, DAVID PRATS ULLOA, IVÁN RUIZ QUINTANA
## MIGUEL ÁNGEL ARROYO CLEMENTE, DANIELA-NICOLETA BOLDUREANU, DAVID PRATS ULLOA, IVÁN RUIZ QUINTANA declaramos 
## que esta solución es fruto exclusivamente de nuestro trabajo personal. 
## No hemos sido ayudados por ninguna otra persona ni hemos obtenido la solución de fuentes externas, 
## y tampoco hemos compartido nuestra solución con nadie. 
## Declaramos además que no hemos realizado de manera deshonesta ninguna otra 
## actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás. 

from bottle import *
import pymongo

#Terminado, verificado, correcto
@get('/top_countries')
# http://localhost:8080/top_countries?n=3
def agg1():
    #Obtener todos los parametros de la query
    params = dict(request.query)
    listKeyParams = list(params.keys())
    
    paramsIncorrect=[]
    #Si la consulta contiene algun parametro
    if len(listKeyParams) > 0:
        
        listPssblParams =['n'] 
        errorParams=False
   
        #Verificar que los parametros son correctos
        for key in listKeyParams:
            if key not in listPssblParams:
                errorParams=True
                paramsIncorrect.append(key)
                
        #Si no hay error en los parametros
        if not errorParams:
            #Obtencion del valor del parametro de la consulta
            paramN = request.query.n
            limite=int(paramN)
            #Conexión con el cliente
            client = pymongo.MongoClient()
            #base de datos
            db = client.giw
            #obtencion de la colección
            colUsuarios = db.usuarios
            
            #Selecciona los paises y el total de usuarios del pais,
            #agrupando por pais,
            #ordenando por el total de usuarios y el pais por orden alfabetico
            #limitando los resultados a tantas filas como infica el parametro de la query
            result=list(colUsuarios.aggregate([
                {'$group': {'_id': "$pais", 'totalUsuarios': {"$sum":1}}},
                {'$sort' : {'totalUsuarios' : -1, 'pais': 1}},
                {'$limit' : limite}
            ]))

            return template("result.tpl", result=result, title="/top_countries", columnasResul=["Pais", "Numero de personas"])
        else:
            return template("errorParametros.tpl", error="Se han introducido parametros de busqueda desconocidos, utilice unicamente ['n'].", listParamsIncorrect=paramsIncorrect, title="/top_countries ERROR")
    else:
        return template("errorParametros.tpl", error="Introduce el parametro ['n'].", listParamsIncorrect=paramsIncorrect, title="/top_countries ERROR")

#Terminado, verificado, correcto
@get('/products')
# http://localhost:8080/products?min=2.34
def agg2():
    #Obtener todos los parametros de la query
    params = dict(request.query)
    listKeyParams = list(params.keys())
    
    paramsIncorrect=[]
    #Si la consulta contiene algun parametro
    if len(listKeyParams) > 0:
        
        listPssblParams =['min'] 
        errorParams=False
   
        #Verificar que los parametros son correctos
        for key in listKeyParams:
            if key not in listPssblParams:
                errorParams=True
                paramsIncorrect.append(key)
                
        #Si no hay error en los parametros
        if not errorParams:
            #Obtencion del valor del parametro de la consulta
            paramN = request.query.min
            precioMin=float(paramN)
            #Conexión con el cliente
            client = pymongo.MongoClient()
            #base de datos
            db = client.giw
            #obtencion de la colección
            colPedidos = db.pedidos
            
            #Selecciona el producto, la cantidad total de productos entre todos los pedidos 
            #y el precio unitario del producto
            #solo los productos cuyo precio sea mayor oigual al parametro de la query
            result=list(colPedidos.aggregate([
                {'$unwind': "$lineas"},
                {'$project' : {
                        'lineas':1, 
                        'producto':'$lineas'}},
                {'$match': {'producto.precio':{'$gte':precioMin}}},
                {'$group': {
                        '_id': "$producto.nombre", 
                        'totalUnidades': { "$sum" : '$producto.cantidad'}, 
                        'pecioUnitario': { '$first' : '$producto.precio'}}}
            ]))

            return template("result.tpl", result=result, title="/products", columnasResul=["Producto", "Unidades vendidas", "Precio unitario"])
        else:
            return template("errorParametros.tpl", error="Se han introducido parametros de busqueda desconocidos, utilice unicamente ['min'].", listParamsIncorrect=paramsIncorrect, title="/products ERROR")
    else:
        return template("errorParametros.tpl", error="Introduce el parametro ['min'].", listParamsIncorrect=paramsIncorrect, title="/products ERROR")
    
#Terminado, verificado, correcto
@get('/age_range')
# http://localhost:8080/age_range?min=80
def agg3():
  #Obtener todos los parametros de la query
    params = dict(request.query)
    listKeyParams = list(params.keys())
    
    paramsIncorrect=[]
    #Si la consulta contiene algun parametro
    if len(listKeyParams) > 0:
        
        listPssblParams =['min'] 
        errorParams=False
   
        #Verificar que los parametros son correctos
        for key in listKeyParams:
            if key not in listPssblParams:
                errorParams=True
                paramsIncorrect.append(key)
                
        #Si no hay error en los parametros
        if not errorParams:
            #Obtencion del valor del parametro de la consulta
            paramN = request.query.min
            minimo=int(paramN)
            #Conexión con el cliente
            client = pymongo.MongoClient()
            #base de datos
            db = client.giw
            #obtencion de la colección
            colUsuarios = db.usuarios
            
            #Seleciona el pais y el rango de edades de ese pais, 
            #siendo el rango la diferencia de la edad maxima y la edad minima de las pesonas
            #agrupando por pais
            #where count usuarios del pais es mayor al minimo que indica el parametro de la query
            #ordenado por rango de edades y por nombre del pais
            result=list(colUsuarios.aggregate([
                {'$group': {
                        '_id': "$pais", 
                        'count': {"$sum":1}, 'edadMax': {'$max': '$edad'}, 
                        'edadMin': {'$min': '$edad'}}},
                {'$match': {'count':{'$gt':minimo}}},
                {'$project' : {'rango':{'$subtract': ['$edadMax', '$edadMin']}}},
                {'$sort' : {'rango' : -1, '_id': 1}}
            ]))

            return template("result.tpl", result=result, title="/age_range", columnasResul=["Pais", "Rango de edad"])
        else:
            return template("errorParametros.tpl", error="Se han introducido parametros de busqueda desconocidos, utilice unicamente ['min'].", listParamsIncorrect=paramsIncorrect, title="/age_range ERROR")
    else:
        return template("errorParametros.tpl", error="Introduce el parametro ['min'].", listParamsIncorrect=paramsIncorrect, title="/age_range ERROR")
    
@get('/avg_lines')
# http://localhost:8080/avg_lines
def agg4():
    #Conexión con el cliente
    client = pymongo.MongoClient()
    #base de datos
    db = client.giw
    #obtencion de la colección
    colUsuarios = db.usuarios
    
    #Une cada usuario con todos sus pedidos, despues desglosa por linea de pedido, 
    #por tanto habra una fila por cada linea de cada pedido de cada usuario.
    #despues agrupa por pais y por pedido, sumando la cantidad de lineas por pedido
    #y vuelve a agrupar para aplicar la funcion de agregación de la media para cada pais.
    result=list(colUsuarios.aggregate([
        {'$lookup': {'from':'pedidos',
                     'localField':'_id',
                     'foreignField':'cliente',
                     'as':'usuariosPedido'}},
        {'$unwind': '$usuariosPedido'},
        {'$unwind': '$usuariosPedido.lineas'},
        {'$group': {
                '_id': {'pais':"$pais", 
                        'pedido': '$usuariosPedido._id' }, 
                'count': {'$sum':1} }},
        {'$group': {
                '_id': "$_id.pais", 
                'mediaLineasPorPedido': {'$avg': '$count'}}}
    ]))
    return template("result.tpl", result=result, title="/avg_lines", columnasResul=["Pais", "Promedio de numero de lineas"])

            
    
@get('/total_country')
# http://localhost:8080/total_country?c=Alemania
def agg5():
   #Obtener todos los parametros de la query
    params = dict(request.query)
    listKeyParams = list(params.keys())
    
    paramsIncorrect=[]
    #Si la consulta contiene algun parametro
    if len(listKeyParams) > 0:
        
        listPssblParams =['c'] 
        errorParams=False
   
        #Verificar que los parametros son correctos
        for key in listKeyParams:
            if key not in listPssblParams:
                errorParams=True
                paramsIncorrect.append(key)
                
        #Si no hay error en los parametros
        if not errorParams:
            #Obtencion del valor del parametro de la consulta
            paisC = request.query.c
            #Conexión con el cliente
            client = pymongo.MongoClient()
            #base de datos
            db = client.giw
            #obtencion de la colección
            colUsuarios = db.usuarios
          
            #elimina todos los usurios que no pertenezcan a un pais especificado,
            #de los usuarios restantes coge sus pedidos y desglosa una fila por cada linea de cada pedidio de cada usuario
            #agrupa por pais para carcular la función de agregación de suma para el total de cada linea
            result=list(colUsuarios.aggregate([
                {'$match': {'pais':paisC}},
                {'$lookup': {"from" :"pedidos",
                             "localField" : "_id",
                             "foreignField" : "cliente",
                             "as" : "pedidosLinea"}},
                {'$unwind':'$pedidosLinea'},
                {'$unwind':'$pedidosLinea.lineas'},
                {'$group': {
                        '_id': "$pais", 
                        'gastosTotalPedidos': {"$sum" :"$pedidosLinea.lineas.total"}
                       }}
                
            ]))


            return template("result.tpl", result=result, title="/total_country", columnasResul=["Pais", "Total de euros gastados"])
        else:
            return template("errorParametros.tpl", error="Se han introducido parametros de busqueda desconocidos, utilice unicamente ['c'].", listParamsIncorrect=paramsIncorrect, title="/total_country ERROR")
    else:
        return template("errorParametros.tpl", error="Introduce el parametro ['c'].", listParamsIncorrect=paramsIncorrect, title="/total_country ERROR")
    
        
if __name__ == "__main__":
    # No cambiar host ni port ni debug
    run(host='localhost',port=8080,debug=True)
