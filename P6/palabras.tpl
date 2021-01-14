% include('header.tpl', title='Plantas Medicinales')
    <div class="w3-container w3-padding-32 w3-padding-large w3-border w3-margin">
        <h3 class="w3-border-bottom w3-border-light-grey w3-padding-16">Palabras de busqueda</h3>
        <p>Introduce las palabras que desea buscar.</p>
        <form action="/palabras" method="post" class="w3-large">
            <input class="w3-input w3-border" type="text" placeholder="Texto de busqueda" required="" name="texto">
            <input class="w3-button w3-section w3-black w3-block" value="Siguiente" type="submit" />
        </form>
    </div>
</body>
</html>