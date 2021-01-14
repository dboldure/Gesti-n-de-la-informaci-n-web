<!DOCTYPE html>
<html>
    <head>
        <title>Consultas</title>
        <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
        <link rel="stylesheet" type="text/css" href="w3.css" />
    </head>
    <body>
        <div>
            <h2>{{title}}</h2>
            % if len(result) > 0:
                <table style="border-collapse: collapse;" border = "1" cellpadding = "2">
                    <tr>
                    % for tituloColumna in columnasResul:
                        <th>{{tituloColumna}}</th>
                    % end
                    </tr>
                    % for value in result:
                        <tr>
                            % for valorColumna in value.values():
                                    <td>{{valorColumna}}</td>
                            % end
                        </tr>
                    % end
                </table>
            % else:
                <p>No se ha encontrado ningún resultado que coincida con los parametros de busqueda.<br>
            % end
            <p>Numero de resultados devueltos encontrados: <b>{{len(result)}}</b></p>
        </div>
    </body>
</html>
