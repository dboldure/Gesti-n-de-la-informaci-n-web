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
        </div> -->
        <div class="w3-container w3-padding-32 w3-padding-large w3-border w3-margin">
            <h2 class="w3-border-bottom w3-border-light-grey w3-padding-16">{{title}}</h2>
            <p>{{error}} <br>
            % if len(listParamsIncorrect) > 0:
                Error:
                % for param in listParamsIncorrect:
                    <span><b>{{param}} </b></span>
                % end
            % end
            </p>
        </div>
    </body>
</html>
