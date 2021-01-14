# -*- coding: utf-8 -*-

## Asignatura: Gestión de la información en la Web
## Practica Autenticación delegada
## Grupo: 7
## Autores: MIGUEL ÁNGEL ARROYO CLEMENTE, DANIELA-NICOLETA BOLDUREANU, DAVID PRATS ULLOA, IVÁN RUIZ QUINTANA
## MIGUEL ÁNGEL ARROYO CLEMENTE, DANIELA-NICOLETA BOLDUREANU, DAVID PRATS ULLOA, IVÁN RUIZ QUINTANA declaramos 
## que esta solución es fruto exclusivamente de nuestro trabajo personal. 
## No hemos sido ayudados por ninguna otra persona ni hemos obtenido la solución de fuentes externas, 
## y tampoco hemos compartido nuestra solución con nadie. 
## Declaramos además que no hemos realizado de manera deshonesta ninguna otra 
## actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás. 


from bottle import get, template, request, run
# Resto de importaciones
import requests
import hashlib
import os
import json


# Credenciales. 
# https://developers.google.com/identity/protocols/OpenIDConnect#appsetup
# Copiar los valores adecuados.
CLIENT_ID     = "696730492243-n5h66s753lbkgb1r9u325suelln6kbcl.apps.googleusercontent.com"
CLIENT_SECRET = ""
REDIRECT_URI  = "http://localhost:8080/token"


# Fichero de descubrimiento para obtener el 'authorization endpoint' y el 
# 'token endpoint'
# https://developers.google.com/identity/protocols/OpenIDConnect#authenticatingtheuser
DISCOVERY_DOC = "https://accounts.google.com/.well-known/openid-configuration"


# Token validation endpoint para decodificar JWT
# https://developers.google.com/identity/protocols/OpenIDConnect#validatinganidtoken
#https://oauth2.googleapis.com/tokeninfo
TOKENINFO_ENDPOINT = 'https://oauth2.googleapis.com/tokeninfo'

session = {}

@get('/login_google')
def login_google():
    #Obtencion daots del fichero de descubrimiento
    respDescubrimiento = requests.get(DISCOVERY_DOC)
    datosDescubrimiento = json.loads(respDescubrimiento.content)
    
    session['authorization_endpoint'] = datosDescubrimiento['authorization_endpoint']
    session['token_endpoint'] = datosDescubrimiento['token_endpoint']
    
    state = hashlib.sha256(os.urandom(1024)).hexdigest()
    session['state'] = state
    
    url = session['authorization_endpoint']+'?'+'client_id='+ str(CLIENT_ID) +'&'+ 'response_type=code&'+ 'scope=openid%20email&'+ 'redirect_uri='+ str(REDIRECT_URI) +'&'+ 'state='+ str(session['state'])
                    
    return template("login_google.tpl", url=url)
   
@get('/token')
def token():
    if request.query.get('state', '') != session['state']:
        return template("errorParametros.tpl", title="Ataque malicioso", error = "Se ha detectado un token (CSRF) incorrecto, lo que puede indicar que intenten hacer una peticion maliciosa.")
    
    payload = {'code': request.query.get('code', None), 'client_id' : CLIENT_ID, 'client_secret': CLIENT_SECRET, 'redirect_uri': REDIRECT_URI, 'grant_type':'authorization_code'}
    req = requests.post(session['token_endpoint'] , data=payload)
    req.raise_for_status()
    contenido = req.json()
    
    
    payload_2 = {'id_token': contenido['id_token']}
    reqFinal = requests.get(TOKENINFO_ENDPOINT , params=payload_2)
    reqFinal.raise_for_status()
    contenidoFinal = reqFinal.json()
    
    return template("result.tpl", email=contenidoFinal['email'])
   

if __name__ == "__main__":
    # Usar sesiones requiere crear objetos adicionales y modificar los parámetros de run()
    run(host='localhost',port=8080,debug=True)
