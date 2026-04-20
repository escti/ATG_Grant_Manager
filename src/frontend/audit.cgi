#!/bin/bash

echo "Content-type: text/html"
echo ""

# Pega parametros via GET
DB_ID_VAL=""
if [ "$REQUEST_METHOD" = "GET" ]; then
    SAVEIFS=$IFS
    IFS='&'
    for param in $QUERY_STRING; do
        if [[ $param == db_id=* ]]; then
            DB_ID_VAL=$(echo $param | cut -d= -f2)
        fi
    done
    IFS=$SAVEIFS
fi

DB_ID_CLEAN=$(echo "$DB_ID_VAL" | tr -cd '[:alnum:]_')

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
        if [ "$dbid" == "$DB_ID_CLEAN" ]; then
            DB_OPTIONS+="<option value=\"$dbid\" selected>$dbname</option>"
        else
            DB_OPTIONS+="<option value=\"$dbid\">$dbname</option>"
        fi
    done < "$CATALOG_FILE"
fi

# Executa o backend para pegar os dados caso banco selecionado
if [ -n "$DB_ID_CLEAN" ]; then
    TABLE_ROWS=$(/usr/local/bin/grant_reporter.sh "$DB_ID_CLEAN")
else
    TABLE_ROWS="<tr><td colspan='9' class='text-center py-4 text-muted'>Selecione um banco de dados para carregar os relatórios de concessão e auditoria.</td></tr>"
fi

# Renderiza o HTML
cat <<EOF
<!DOCTYPE html>
<html lang="pt-BR" data-bs-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Auditoria de Grants Oracle</title>
    
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.datatables.net/1.13.4/css/dataTables.bootstrap5.min.css" rel="stylesheet">
    
    <style>
        body { 
            background-color: #121212; 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            padding-top: 20px;
        }
        .card {
            background-color: #1e1e1e;
            border: 1px solid #333;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }
        .table-dark {
            --bs-table-bg: #1e1e1e;
            --bs-table-striped-bg: #252525;
        }
        /* Ajustes do DataTables no modo escuro */
        .dataTables_wrapper .dataTables_length, 
        .dataTables_wrapper .dataTables_filter, 
        .dataTables_wrapper .dataTables_info, 
        .dataTables_wrapper .dataTables_processing, 
        .dataTables_wrapper .dataTables_paginate {
            color: #aaa !important;
        }
        .page-link {
            background-color: #2d2d2d;
            border-color: #444;
            color: #fff;
        }
        .page-item.active .page-link {
            background-color: #0d6efd;
            border-color: #0d6efd;
        }
    </style>
</head>
<body>

<div class="container-fluid px-4">
    
    <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
            <h2 class="text-primary fw-bold">AUDITORIA DE GRANTS</h2>
            <p class="text-muted mb-0">Histórico de solicitações ativas e revogadas por sistema.</p>
        </div>
        <div class="d-flex gap-3 align-items-center">
            <form method="GET" action="audit.cgi" class="d-flex gap-2 m-0">
                <select class="form-select bg-dark text-white border-secondary" id="db_id" name="db_id" onchange="this.form.submit()" required>
                    <option value="" disabled selected>Selecione um Banco...</option>
                    $DB_OPTIONS
                </select>
            </form>
            <a href="index.cgi" class="btn btn-outline-primary text-nowrap">
                &larr; Conceder Permissões
            </a>
        </div>
    </div>

    <div class="card p-3">
        <div class="table-responsive">
            <table id="auditTable" class="table table-dark table-striped table-hover w-100">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Usuário Destino</th>
                        <th>Privilégio</th>
                        <th>Objeto</th>
                        <th>Solicitante</th>
                        <th>Data Início</th>
                        <th>Expira em</th>
                        <th>Status</th>
                        <th>Observações</th>
                    </tr>
                </thead>
                <tbody>
                    $TABLE_ROWS
                </tbody>
            </table>
        </div>
    </div>
    
    <div class="text-center mt-4 text-muted small">
        Atualizado em: $(date "+%d/%m/%Y %H:%M:%S") <br>
        Versão: v2.0.2
    </div>

</div>

<script src="https://code.jquery.com/jquery-3.6.4.min.js"></script>
<script src="https://cdn.datatables.net/1.13.4/js/jquery.dataTables.min.js"></script>
<script src="https://cdn.datatables.net/1.13.4/js/dataTables.bootstrap5.min.js"></script>

<script>
    $(document).ready(function () {
        $('#auditTable').DataTable({
            "order": [[ 0, "desc" ]], // Ordena por ID decrescente
            "language": {
                "url": "//cdn.datatables.net/plug-ins/1.13.4/i18n/pt-BR.json"
            },
            "pageLength": 10,
            "lengthMenu": [10, 25, 50, 100]
        });
    });
</script>

</body>
</html>
EOF