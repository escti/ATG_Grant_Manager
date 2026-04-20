#!/bin/bash
# colocar este script em /var/www/cgi-bin/index.cgi

echo "Content-type: text/html"
echo ""

urldecode() { : "${*//+/ }"; echo -e "${_//%/\\x}"; }

# Carrega as opções de Banco de Dados do Catálogo
CATALOG_FILE="/usr/local/bin/tns_catalog.conf"
if [ ! -f "$CATALOG_FILE" ]; then
    CATALOG_FILE="$(dirname "$0")/../backend/tns_catalog.conf"
fi

DB_OPTIONS=""
if [ -f "$CATALOG_FILE" ]; then
    while IFS='|' read -r dbid dbname dbstring; do
        [[ "$dbid" =~ ^#.* ]] && continue
        [ -z "$dbid" ] && continue
        DB_OPTIONS+="<option value=\"$dbid\">$dbname</option>"
    done < "$CATALOG_FILE"
else
    DB_OPTIONS="<option value=\"\" disabled>Catálogo não encontrado</option>"
fi

if [ "$REQUEST_METHOD" = "POST" ]; then
    read -n $CONTENT_LENGTH POST_DATA
    eval $(echo "$POST_DATA" | awk -F'&' '{for(i=1;i<=NF;i++){print $i}}')
    
    USUARIO_VAL=$(urldecode "$usuario")
    PRIVILEGIO_VAL=$(urldecode "$privilegio")
    OBJETO_VAL=$(urldecode "$objeto")
    GRANTOR_VAL=$(urldecode "$grantor")
    JIRA_TICKET_VAL=$(urldecode "$jira_ticket")
    DB_ID_VAL=$(urldecode "$db_id")
    
    # Sanitização Shell
    USUARIO_CLEAN=$(echo "$USUARIO_VAL" | tr -cd '[:alnum:]_')
    OBJETO_CLEAN=$(echo "$OBJETO_VAL" | tr -cd '[:alnum:]_$.')
    GRANTOR_CLEAN=$(echo "$GRANTOR_VAL" | tr -cd '[:alnum:]_')
    PRIVILEGIO_CLEAN=$(echo "$PRIVILEGIO_VAL" | tr -cd '[:alpha:]')
    JIRA_TICKET_CLEAN=$(echo "$JIRA_TICKET_VAL" | tr -cd '[:alnum:]_-')
    DB_ID_CLEAN=$(echo "$DB_ID_VAL" | tr -cd '[:alnum:]_')

    OUTPUT=$(/usr/local/bin/grant_manager.sh "$USUARIO_CLEAN" "$PRIVILEGIO_CLEAN" "$OBJETO_CLEAN" "$GRANTOR_CLEAN" "$JIRA_TICKET_CLEAN" "$DB_ID_CLEAN")
    RET_CODE=$?

    if [ $RET_CODE -eq 0 ]; then
        ALERT_HTML="<div class='alert alert-success border-success shadow-lg'>✅ <b>Sucesso!</b> $OUTPUT</div>"
    else
        ALERT_HTML="<div class='alert alert-danger border-danger shadow-lg'>❌ <b>Erro:</b> $OUTPUT</div>"
    fi
fi

# HTML Template - Dark Mode
cat <<EOF
<!DOCTYPE html>
<html lang="pt-BR" data-bs-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Oracle Grant Manager</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { 
            background-color: #121212; 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .main-card { 
            background-color: #1e1e1e; 
            border: 1px solid #333; 
            border-radius: 12px; 
            padding: 40px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }
        .form-control, .form-select {
            background-color: #2d2d2d;
            border-color: #444;
            color: #e0e0e0;
        }
        .form-control:focus, .form-select:focus {
            background-color: #333;
            border-color: #0d6efd;
            color: #fff;
            box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
        }
        .header-title {
            color: #0d6efd; /* Azul Oracle */
            font-weight: 700;
            letter-spacing: 1px;
        }
        .btn-primary {
            background-color: #0d6efd;
            border: none;
            padding: 12px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        .btn-primary:hover {
            background-color: #0b5ed7;
            transform: translateY(-2px);
        }
        label { color: #adb5bd; margin-bottom: 5px; }
        .text-xs { font-size: 0.85rem; color: #6c757d; }
    </style>
</head>
<body>

<div class="container d-flex justify-content-center align-items-center min-vh-100">
    <div class="col-md-8 col-lg-6">
        
        <div class="main-card">
            <div class="text-center mb-4">
                <h2 class="header-title">Autoglass OGM: ORACLE GRANT MANAGER</h2>
                <p class="text-muted">Gestão de Acesso Temporário | Auditoria Ativa</p>
            </div>

            $ALERT_HTML

            <!-- Banner Jira Instrução -->
            <div class="alert alert-info border-info mb-4" role="alert">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-info-circle-fill me-2" viewBox="0 0 16 16">
                  <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"/>
                </svg>
                Atenção: É necessário ter um chamado aprovado pelo Gestor para prosseguir. 
                <a href="https://jira.autoglass.com.br/servicedesk/customer/portal/exemplo" target="_blank" class="alert-link">Clique aqui para abrir seu chamado de acesso ao banco.</a>
            </div>

            <form method="POST" action="index.cgi">
                <div class="row">
                    <div class="col-md-6 mb-3">
                        <label for="db_id">Banco Alvo</label>
                        <select class="form-select" id="db_id" name="db_id" required>
                            <option value="" disabled selected>Selecione...</option>
                            $DB_OPTIONS
                        </select>
                    </div>
                    <div class="col-md-6 mb-3">
                        <label for="jira_ticket">Chamado Jira (Aprovado)</label>
                        <input type="text" class="form-control" id="jira_ticket" name="jira_ticket" required placeholder="Ex: ATG-1234">
                    </div>
                </div>

                <div class="mb-4">
                    <label for="grantor">Solicitante (DBA/Responsável logado)</label>
                    <input type="text" class="form-control" id="grantor" name="grantor" required placeholder="Ex: JOAO.SILVA" autocomplete="off">
                </div>

                <hr class="border-secondary my-4">

                <div class="row">
                    <div class="col-md-6 mb-3">
                        <label for="usuario">Usuário/Role Destino</label>
                        <input type="text" class="form-control" id="usuario" name="usuario" required placeholder="Ex: MARIA.SOUZA">
                    </div>
                    <div class="col-md-6 mb-3">
                        <label for="privilegio">Privilégio</label>
                        <select class="form-select" id="privilegio" name="privilegio">
                            <option value="SELECT" selected>SELECT</option>
                            <option value="INSERT">INSERT</option>
                            <option value="UPDATE">UPDATE</option>
                            <option value="DELETE">DELETE</option>
                        </select>
                    </div>
                </div>

                <div class="mb-4">
                    <label for="objeto">Objeto Alvo (Schema.Tabela)</label>
                    <input type="text" class="form-control" id="objeto" name="objeto" required placeholder="Ex: HR.EMPLOYEES">
                    <div class="text-xs mt-1">Certifique-se que o Schema está correto.</div>
                </div>

                <button type="submit" class="btn btn-primary w-100">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-shield-lock-fill me-2" viewBox="0 0 16 16">
                        <path fill-rule="evenodd" d="M8 0c-.69 0-1.843.265-2.928.56-1.11.3-2.229.655-2.887.87a1.54 1.54 0 0 0-1.044 1.262c-.596 4.477.787 7.795 2.465 9.99a11.777 11.777 0 0 0 2.517 2.453c.386.273.744.482 1.048.625.28.132.581.24.829.24s.548-.108.829-.24a7.159 7.159 0 0 0 1.048-.625 11.775 11.775 0 0 0 2.517-2.453c1.678-2.195 3.061-5.513 2.465-9.99a1.541 1.541 0 0 0-1.044-1.263 62.467 62.467 0 0 0-2.887-.87C9.843.266 8.69 0 8 0zm0 5a1.5 1.5 0 0 1 .5 2.915l.385 1.99a.5.5 0 0 1-.491.595h-.788a.5.5 0 0 1-.49-.595l.384-1.99A1.5 1.5 0 0 1 8 5z"/>
                    </svg>
                    Conceder Acesso
                </button>
            </form>
            
            <div class="text-center mt-4 text-xs">
                &copy; 2026 DBA Team - Segurança & Auditoria | Versão: v2.0.2
            </div>
        </div>
    </div>
</div>

</body>
</html>
EOF