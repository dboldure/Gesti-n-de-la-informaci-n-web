<!DOCTYPE html>
<html>
    <head>
        <title>Consultas</title>
        <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
        <link rel="stylesheet" type="text/css" href="w3.css" />
    </head>
    <body>
        <!-- Navbar (sit on top)
        <div>
            <div class="w3-bar w3-white w3-wide w3-padding w3-card">
                <a href="/" class="w3-bar-item w3-button"><b>Início</b></a>
            </div>
        </div>
        -->
        <div class="w3-container w3-padding-32 w3-padding-large w3-border w3-margin">
            <h2 class="w3-border-bottom w3-border-light-grey w3-padding-16">/find email birthdate</h2>
            <p>Numero de usuarios encontrados: <b>{{len(users)}}</b></p>
            % if len(users) > 0:
                <table style="border-collapse: collapse;" border = "1" cellpadding = "2">
                    <tr>
                        <th>_id</th>
                        <th>E-Mail</th>
                        <th>Fecha de nacimiento</th>
                    </tr>
                    % for user in users:
                        <tr>
                            <th>{{user["_id"]}}</th>
                            <td>{{user["email"]}}</td>
                            <td>{{user["birthdate"]}}</td>
                        </tr>
                    % end
                </table>
            % else:
                <p>No se ha encontrado ningún usuario que coincida con los parametros de busqueda.<br>
            % end
        </div>
    </body>
</html>
