% include('header.tpl', title='Plantas Medicinales')
    <div class="w3-container w3-padding-32 w3-padding-large w3-border w3-margin">
        <h3 class="w3-border-bottom w3-border-light-grey w3-padding-16">Busqueda por enfermedad</h3>
        <p>Marca las enfermedades que desea buscar.</p>
        <form action="/enfermedades" method="post" class="w3-large">
            <div class="w3-margin">
                %for enfermedad in enfermedades:
                    <input type="checkbox" class="w3-check" name="enfermedad" value="{{enfermedad}}">
                    <label>{{enfermedad}}</label>
                    <br>
                %end
            </div>
            <input class="w3-button w3-section w3-black w3-block" value="Buscar" type="submit" />
        </form>
    </div>
</body>
</html>