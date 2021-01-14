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

from bottle import route, default_app, template, run, static_file, error, Bottle, request, get, post
import pymongo
import re

@get('/find_users')
def find_users():
    # http://localhost:8080/find_users?name=Luz
    # http://localhost:8080/find_users?name=Luz&surname=Romero
    # http://localhost:8080/find_users?name=Luz&surname=Romero&birthdate=2006-08-14
    
    #Obtener todos los parametros de la query
    params = dict(request.query)
    listKeyParams = list(params.keys())
    
    paramsIncorrect=[]
    #Si la consulta contiene algun parametro
    if len(listKeyParams) > 0:
        
        listPssblParams =['name', 'surname', 'birthdate'] 
        errorParams=False
        #Los parametros son unicamente ['name', 'surname', 'birthdate'] 
        for key in listKeyParams:
            if key not in listPssblParams:
                errorParams=True
                paramsIncorrect.append(key)
                
        if not errorParams:
            #Conexión con el cliente
            client = pymongo.MongoClient()
            #base de datos
            db = client.giw
            #obtencion de la colección
            colUsuarios = db.usuarios
            
            #resultado del find (En este caso como los parametros de la query 
            #ya están en el formato de AND de la consulta en mongo se puede utilizar directamente)
            users = list(colUsuarios.find(params))  
        
            return template("result.tpl", users=users, title="/find_users")
        else:
            return template("errorParametros.tpl", error="Se han introducido parametros de busqueda desconocidos, utilice unicamente ['name', 'surname', 'birthdate'].", listParamsIncorrect=paramsIncorrect, title="/find_users")
    else:
        return template("errorParametros.tpl", error="Introduce algun parametro de busqueda.", listParamsIncorrect=paramsIncorrect, title="/find_users")

@get('/find_email_birthdate')
def email_birthdate():
    # http://localhost:8080/find_email_birthdate?from=1973-01-01&to=1990-12-31
    
    #Obtener el nombre de los parametros de la query
    listKeyParams = list(dict(request.query).keys())
    paramsIncorrect=[]
    
    if len(listKeyParams) > 0:
        listPssblParams =['from', 'to'] 
        errorParams=False
        
        #Los parametros son unicamente ['from', 'to']
        for key in listKeyParams:
            if key not in listPssblParams:
                errorParams=True
                paramsIncorrect.append(key)
                
        if not errorParams:
            #Si todo es correcto obtenemos los parametros ['from', 'to'] de la query
            paramFrom = request.query['from']
            paramTo = request.query['to']
            
            #Conectamos con el cliente mongo y obtenemos la colección deseada
            client = pymongo.MongoClient()
            db = client.giw
            colUsuarios = db.usuarios
            
            #Consulta del tipo SELECT _id, email, birthdate WHERE birthdate >= from AND birthdate <= to
            users = list(colUsuarios.find({'birthdate': {'$gte': paramFrom, '$lte': paramTo}},{"_id": 1, "email": 1, "birthdate": 1 }))
        
            return template("resultDate.tpl", users=users)
        else:
            return template("errorParametros.tpl", error="Se han introducido parametros de busqueda desconocidos, utilice unicamente ['from', 'to'].", listParamsIncorrect=paramsIncorrect, title="/find_email_birthdate")
    else:
        return template("errorParametros.tpl", error="Introduce algun parametro de busqueda.", listParamsIncorrect=paramsIncorrect, title="/find_email_birthdate")


@get('/find_country_likes_limit_sorted')
def find_country_likes_limit_sorted():
    # http://localhost:8080/find_country_likes_limit_sorted?country=Irlanda&likes=movies,animals&limit=4&ord=asc
    
    #Obtener el nombre de los parametros de la query
    listKeyParams = list(dict(request.query).keys())
    paramsIncorrect=[]
    
    if len(listKeyParams) > 0:
        listPssblParams =['country', 'likes', 'limit', 'ord'] 
        errorParams=False
        #Los parametros son unicamente ['country', 'likes', 'limit', 'ord'] 
        for key in listKeyParams:
            if key not in listPssblParams:
                errorParams=True
                paramsIncorrect.append(key)
                
        if not errorParams:
            #Obtenemos todos los parametros
            paramCountry = request.query.country
            paramLikes = request.query.likes.split(',')
            paramLimit = int(request.query.limit)
            paramOrd = request.query.ord
            
            #Transformamos el metodo de ordenación al formato de mongo
            if paramOrd == "asc":
                paramOrd=pymongo.ASCENDING
            elif paramOrd == "desc":
                paramOrd=pymongo.DESCENDING
            else:
                return template("errorParametros.tpl", error="El metodo de ordenación no es correcto.", listParamsIncorrect=paramsIncorrect, title="/find_country_likes_limit_sorted")
            
            #Conectamos con el cliente mongo y obtenemos la colección deseada
            client = pymongo.MongoClient()
            db = client.giw
            colUsuarios = db.usuarios
            
            #Consulta Where que contiene todos($all) los parametros en la lista de likes y el pais es el correcto, ordenado y limitado
            users = list(colUsuarios.find({'likes':{'$all':paramLikes},'address.country':paramCountry}).sort('birthdate',paramOrd).limit(paramLimit))
        
            return template("result.tpl", users=users, title="/find_country_likes_limit_sorted")
        else:
            return template("errorParametros.tpl", error="Se han introducido parametros de busqueda desconocidos, utilice unicamente ['country', 'likes', 'limit', 'ord'].", listParamsIncorrect=paramsIncorrect, title="/find_country_likes_limit_sorted")
    else:
        return template("errorParametros.tpl", error="Introduce algun parametro de busqueda.", listParamsIncorrect=paramsIncorrect, title="/find_country_likes_limit_sorted")


@get('/find_birth_month')
def find_birth_month():
    # http://localhost:8080/find_birth_month?month=abril
    
    #Obtener el nombre de los parametros de la query
    listKeyParams = list(dict(request.query).keys())
    paramsIncorrect=[]
    
    if len(listKeyParams) == 1:
        listPssblParams =['month'] 
        errorParams=False
        
        #El parametro es unicamente ['month']
        for key in listKeyParams:
            if key not in listPssblParams:
                errorParams=True
                paramsIncorrect.append(key)
                
        if not errorParams:
            listPssblValues=['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
            errorValues=False
            #obtenemos el valor del mes
            paramMonth = request.query.month
            
            #El contenido del parametro ['month'] unicamente es un mes de año
            if paramMonth not in listPssblValues:
                errorValues=True
                paramsIncorrect.append(paramMonth)
        
            if not errorValues:
                #obtenemos el numero correspondiente según el mes introducido
                pos = listPssblValues.index(paramMonth)
                
                #Formateo del mes, para poder utilizar una expresión regular con $regex, 
                #en este caso buscamos dentro de una fecha con formato YYYY-MM-dd' solo la parte de -MM-
                #Formateado de esa manera para que no haya confusión con el dia, ya que el dia sería -dd
                month = ''
                if len(str(pos)) == 1:
                    month = '-0'+ str(pos+1)+'-'
                else:
                    month = '-'+str(pos+1)+'-'
                    
                #Conectamos con el cliente mongo y obtenemos la colección deseada
                client = pymongo.MongoClient()
                db = client.giw
                colUsuarios = db.usuarios
                
                #find en el que el 'birthdate' debe coincidir con una expresión regular de tipo '*[-][mes][-]*', ordenadode amnera ascendente por el 'birthdate'
                users = list(colUsuarios.find({'birthdate': {'$regex' : month}}).sort('birthdate', pymongo.ASCENDING))
                
                return template("result.tpl", users=users, title="/find_birth_month")
            else:
                return template("errorParametros.tpl", error="Se ha introducido un valor de month desconocido, utilice unicamente ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']", listParamsIncorrect=paramsIncorrect, title="/find_birth_month")
        else:
            return template("errorParametros.tpl", error="Se ha introducido un parametro de busqueda desconocido, utilice unicamente 'month'", listParamsIncorrect=paramsIncorrect, title="/find_birth_month")
    else:
        return template("errorParametros.tpl", error="Introduce un solo el parametro de busqueda 'month'.", listParamsIncorrect=paramsIncorrect, title="/find_birth_month")

@get('/find_likes_not_ending')
def find_likes_not_ending():
    # http://localhost:8080/find_likes_not_ending?ending=s
    
    #Obtener el nombre de los parametros de la query
    listKeyParams = list(dict(request.query).keys())
    paramsIncorrect=[]
    
    if len(listKeyParams) == 1:
        listPssblParams =['ending'] 
        errorParams=False
        
        #el unico parametro es ['ending']
        for key in listKeyParams:
            if key not in listPssblParams:
                errorParams=True
                paramsIncorrect.append(key)
                
        if not errorParams:
            #Obtenemos el parametro de la query
            paramEnding = request.query.ending
            
            #Conectamos con el cliente mongo y obtenemos la colección deseada
            client = pymongo.MongoClient()
            db = client.giw
            colUsuarios = db.usuarios
                
            #Utilizando regex tambien para seleccionar aquellos usuarios en los que sus likes NO coinciden con la expresión regular, ademas ignorando mayuscula y minuscula
            rgx = re.compile(paramEnding + '$', re.IGNORECASE)
            users = list(colUsuarios.find({"likes": {"$not" : rgx}}))
                
            return template("result.tpl", users=users, title="/find_likes_not_ending")
        else:
            return template("errorParametros.tpl", error="Se ha introducido un parametro de busqueda desconocido, utilice unicamente 'ending'", listParamsIncorrect=paramsIncorrect, title="/find_likes_not_ending")
    else:
        return template("errorParametros.tpl", error="Introduce un solo el parametro de busqueda 'ending'.", listParamsIncorrect=paramsIncorrect, title="/find_likes_not_ending")
    return template("result.tpl")

@get('/find_leap_year')     
def find_leap_year():
    # http://localhost:8080/find_leap_year?exp=20
    
    #Obtener el nombre de los parametros de la query
    listKeyParams = list(dict(request.query).keys())
    paramsIncorrect=[]
    
    if len(listKeyParams) == 1:
        listPssblParams =['exp'] 
        errorParams=False
        
        #el unico parametro de la query es ['exp']
        for key in listKeyParams:
            if key not in listPssblParams:
                errorParams=True
                paramsIncorrect.append(key)
                
        if not errorParams:
            #obtenemos el contenido del parametro ['exp'] de la query
            paramExp = request.query.exp
            
            #Conectamos con el cliente mongo y obtenemos la colección deseada
            client = pymongo.MongoClient()
            db = client.giw
            colUsuarios = db.usuarios
            
            #nos aseguramos que la fecha introducida son unicamente 2 cifras
            if len(paramExp) != 2:
                return template("errorParametros.tpl", error="La fecha de caducidad sera unicamente de 2 digitos.", listParamsIncorrect=paramsIncorrect, title="/find_leap_year")
           
            #Para calcular el año bisiesto se utiliza:
            #p: Es divisible entre 4
            #q: Es divisible entre 100
            #r: Es divisible entre 400
            
            #Entonces se utiliza la fórmula lógica 
            #p∧(¬q∨r) 
            
            #Es bisiesto si es divisible entre cuatro y (no es divisible entre 100 o es divisible entre 400) 
            #(2000 y 2400 sí son bisiestos. 2100, 2200 y 2300 no lo son).
            
            #Un find con una funcion javascript para utilizar en el where
            users = list(colUsuarios.find({'credit_card.expire.year':paramExp, '$where' : """function() { 
                                                                                    if( obj.birthdate.substring(0,4) % 4 == 0 && (obj.birthdate.substring(0,4) % 100 != 0 || obj.birthdate.substring(0,4) % 400 == 0 ))
                                                                                        return true; 
                                                                                    else 
                                                                                        return false;}"""})) 
                
            return template("result.tpl", users=users, title="/find_leap_year")
        else:
            return template("errorParametros.tpl", error="Se ha introducido un parametro de busqueda desconocido, utilice unicamente 'ending'", listParamsIncorrect=paramsIncorrect, title="/find_leap_year")
    else:
        return template("errorParametros.tpl", error="Introduce un solo el parametro de busqueda 'ending'.", listParamsIncorrect=paramsIncorrect, title="/find_leap_year")
    return template("result.tpl")


###################################
# NO MODIFICAR LA LLAMADA INICIAL #
###################################
if __name__ == "__main__":
    run(host='localhost',port=8080,debug=True)
