% include('header.tpl', title='Plantas Medicinales')
    <div class="w3-container w3-padding-32 w3-padding-large w3-border w3-margin">
        <h3 class="w3-border-bottom w3-border-light-grey w3-padding-16">Tipo de busqueda</h3>
        <p>Elige entre una busqueda de tipo AND o de tipo OR, es decir si busca plantas donde aparece todas las palabras introducidas o si busca plantas donde aparecen alguna de las palabras introducidas.</p>
        <form action="/tipoBusqueda" method="post" class="w3-xxlarge w3-block">
            <textarea class="w3-hide" rows = "50" cols = "50" name = "texto" readonly="readonly">
                {{texto}}
            </textarea>
            <div class="w3-auto">
                <div class="w3-col l3 m6 w3-margin-bottom">
                    <input class="w3-radio" type="radio" name="opcion" value="and" checked>
                    <label>AND</label>
                </div>
                <div class="w3-col l3 m6 w3-margin-bottom">
                    <input class="w3-radio" type="radio" name="opcion" value="or">
                    <label>OR</label>
                </div>
            </div>
            <input class="w3-button w3-section w3-black w3-block" value="Siguiente" type="submit" />
        </form>
    </div>
</body>
</html>