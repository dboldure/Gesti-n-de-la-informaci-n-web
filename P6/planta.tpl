% include('header.tpl', title='Plantas Medicinales')
    <div class="w3-container w3-padding-32 w3-padding-large w3-border w3-margin">
        <h3 class="w3-border-bottom w3-border-light-grey w3-padding-16">Planta</h3>
        <p>Elige la planta que desea buscar.</p>
        <form action="/planta" method="post" class="w3-xlarge">
            <input class="w3-input w3-hide" type="text" name="grupo" value={{grupo}} readonly="readonly">
            <select name="plantas" class="w3-select w3-border w3-light-grey w3-block">
                % for planta in plantas:
                <option value="{{planta}}">{{planta}}</option>
                %end
            </select>
            <input class="w3-button w3-section w3-black w3-block" value="Buscar" type="submit" />
        </form>
    </div>
</body>
</html>