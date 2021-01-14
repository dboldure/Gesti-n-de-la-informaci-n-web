% include('header.tpl', title='Plantas Medicinales')
    <div class="w3-container w3-padding-32 w3-padding-large w3-border w3-margin">
        <h3 class="w3-border-bottom w3-border-light-grey w3-padding-16">Grupo</h3>
        <p>Elige el grupo que desea buscar.</p>
        <form action="/indice" method="post" class="w3-xlarge">
            <select name="grupo" class="w3-select w3-border w3-light-grey w3-block">
                <option value="grupoAB">Plantas medicinales(A-B)</option>
                <option value="grupoC">Plantas medicinales(C)</option>
                <option value="grupoDG">Plantas medicinales(D-G)</option>
                <option value="grupoHM">Plantas medicinales(H-M)</option>
                <option value="grupoNZ">Plantas medicinales(N-Z)</option>
            </select>
            <input class="w3-button w3-section w3-black w3-block" value="Siguiente" type="submit" />
        </form>
    </div>
</body>
</html>