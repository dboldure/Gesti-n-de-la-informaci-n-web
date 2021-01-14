% include('header.tpl', title='Plantas Medicinales')
    %if len(plantas) > 0:    
        % for nombrePlanta, infoPlanta in plantas.items():
            <div class="w3-card-4 w3-margin w3-white">
                <img src="/static/img/planta.jpg" alt="planta" style="width:100%">
                <div class="w3-container">
                  <h3 class="w3-border-bottom w3-border-light-grey w3-padding-16">{{nombrePlanta}}</h3>
                  <p class="w3-opacity">{{infoPlanta[0]}}</p>
                </div>
                <div class="w3-container">
                  <p>{{infoPlanta[1]}}</p>
                </div>
             </div>
        % end
    %else:
        <div class="w3-card-4 w3-margin w3-white">
            <div class="w3-container">
              <h3 class="w3-border-bottom w3-border-light-grey w3-padding-16">Sin resultados</h3>
            </div>
            <div class="w3-container">
              <p>Repite la busqueda con otras palabras o otro método, no existe ningun resultado con las palabras introducidas</p>
            </div>
         </div>
    %end
</body>
</html>