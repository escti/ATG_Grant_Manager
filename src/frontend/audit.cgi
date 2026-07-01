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
    while IFS='|' read -r dbid dbname dbstring dbtype dbambiente; do
        [[ "$dbid" =~ ^#.* ]] && continue
        [ -z "$dbid" ] && continue
        [ -z "$dbtype" ] && dbtype="oracle"
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
    TABLE_ROWS="<tr><td colspan='12' class='text-center py-4 text-muted'>Selecione um banco de dados para carregar os relatórios de concessão e auditoria.</td></tr>"
fi

# Renderiza o HTML
DATA_ATUAL=$(date "+%d/%m/%Y %H:%M:%S")

cat <<EOF
<!DOCTYPE html>
<html lang="pt-BR" data-bs-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Autoglass GRANT MANAGER | ATGGM — Auditoria</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/core@1.4.0/dist/css/tabler.min.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.13.1/font/bootstrap-icons.min.css">
  <link rel="stylesheet" href="https://cdn.datatables.net/1.13.4/css/dataTables.bootstrap5.min.css">
  <style>
    body { background-color: #0f1117; font-family: 'Segoe UI', Tahoma, sans-serif; }
    .page { background-color: #0f1117; }
    .navbar-vertical { background-color: #15171e !important; border-right: 1px solid #1e2130; }
    .navbar-vertical .nav-link { color: #8b8fa3; border-radius: 8px; margin: 2px 8px; }
    .navbar-vertical .nav-link:hover { color: #e6e7ed; background: #1e2130; }
    .navbar-vertical .nav-link.active { color: #fff; background: linear-gradient(135deg, #1a5fb4 0%, #3584e4 100%); box-shadow: 0 4px 12px rgba(26, 95, 180, 0.3); }
    .navbar-vertical .navbar-brand { padding: 1rem 1.25rem; }
    .navbar-vertical .navbar-brand .logo-text { font-weight: 700; font-size: 1.4rem; background: linear-gradient(135deg, #3584e4, #62a0ea); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .navbar-vertical .navbar-brand .logo-sub { font-size: 0.65rem; color: #8b8fa3; letter-spacing: 2px; text-transform: uppercase; -webkit-text-fill-color: #8b8fa3; }
    .page-header { background: transparent; padding-top: .5rem; }
    .card { background-color: #1c1e2a; border: 1px solid #2a2d3a; border-radius: 12px; }
    .card-header { background: transparent; border-bottom: 1px solid #2a2d3a; padding: 1.25rem 1.5rem; }
    .card-body { padding: 1.5rem; }
    .form-label { color: #a0a4b8; font-weight: 500; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.5px; }
    .form-control, .form-select { background-color: #252836; border: 1px solid #33364a; color: #e6e7ed; border-radius: 8px; font-size: 0.9rem; padding: 0.6rem 1rem; }
    .form-control:focus, .form-select:focus { background-color: #2a2d3e; border-color: #3584e4; box-shadow: 0 0 0 3px rgba(53, 132, 228, 0.15); }
    .btn-outline-primary { border-color: #3584e4; color: #3584e4; border-radius: 8px; }
    .btn-outline-primary:hover { background: #3584e4; border-color: #3584e4; }
    .page-title { font-size: 1.3rem; font-weight: 700; color: #e6e7ed; }
    .page-title small { font-size: 0.8rem; font-weight: 400; color: #8b8fa3; display: block; }
    .stat-card { border-radius: 12px; padding: 1.25rem; background: linear-gradient(135deg, #1c1e2a 0%, #222538 100%); border: 1px solid #2a2d3a; }
    .stat-card .stat-icon { width: 44px; height: 44px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; }
    .stat-card .stat-value { font-size: 1.5rem; font-weight: 700; color: #fff; line-height: 1; }
    .stat-card .stat-label { font-size: 0.75rem; color: #8b8fa3; text-transform: uppercase; letter-spacing: 0.5px; }
    .badge-soft-success { background: rgba(46, 213, 115, 0.12); color: #2ed573; border-radius: 6px; padding: 0.3rem 0.7rem; }
    .badge-soft-warning { background: rgba(255, 183, 77, 0.12); color: #ffb74d; border-radius: 6px; padding: 0.3rem 0.7rem; }
    .badge-soft-danger { background: rgba(255, 71, 87, 0.12); color: #ff4757; border-radius: 6px; padding: 0.3rem 0.7rem; }
    .badge-soft-secondary { background: rgba(139, 143, 163, 0.12); color: #8b8fa3; border-radius: 6px; padding: 0.3rem 0.7rem; }
    .badge-soft-info { background: rgba(53, 132, 228, 0.12); color: #62a0ea; border-radius: 6px; padding: 0.3rem 0.7rem; }
    .table { color: #e6e7ed; font-size: 0.85rem; margin-bottom: 0; }
    .table thead th { border-bottom: 2px solid #2a2d3a; color: #8b8fa3; font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px; }
    .table tbody td { border-color: #2a2d3a; vertical-align: middle; }
    .table tbody tr:hover { background: rgba(53, 132, 228, 0.04); }
    .dataTables_wrapper .dataTables_length,
    .dataTables_wrapper .dataTables_filter,
    .dataTables_wrapper .dataTables_info,
    .dataTables_wrapper .dataTables_paginate { color: #8b8fa3 !important; }
    .dataTables_wrapper .dataTables_filter input { background: #252836; border: 1px solid #33364a; color: #e6e7ed; border-radius: 8px; }
    .page-link { background: #252836; border-color: #33364a; color: #e6e7ed; }
    .page-item.active .page-link { background: #3584e4; border-color: #3584e4; }
    .page-item.disabled .page-link { background: #1c1e2a; border-color: #2a2d3a; color: #555; }
    .footer { border-top: 1px solid #2a2d3a; padding: 1rem 1.5rem; background: transparent; }
  </style>
</head>
<body>
  <div class="page">

    <!-- SIDEBAR -->
    <aside class="navbar navbar-vertical navbar-expand-lg" data-bs-theme="dark">
      <div class="container-fluid">
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#sidebar-menu">
          <span class="navbar-toggler-icon"></span>
        </button>
        <a href="index.cgi" class="navbar-brand navbar-brand-autodark">
          <span>
            <span class="logo-text">ATGGM</span>
            <br><span class="logo-sub">Autoglass Grant Manager</span>
          </span>
        </a>
        <div class="collapse navbar-collapse" id="sidebar-menu">
          <ul class="navbar-nav pt-4">
            <li class="nav-item mb-1">
              <a class="nav-link" href="index.cgi">
                <i class="bi bi-shield-check me-2"></i> Solicitar Grant
              </a>
            </li>
            <li class="nav-item mb-1">
              <a class="nav-link active" href="audit.cgi">
                <i class="bi bi-clock-history me-2"></i> Auditoria
              </a>
            </li>
          </ul>
        </div>
      </div>
    </aside>

    <!-- CONTEUDO -->
    <div class="page-wrapper">

      <!-- Header -->
      <div class="page-header d-print-none">
        <div class="container-xl">
          <div class="row g-3 align-items-center">
            <div class="col">
              <h2 class="page-title">
                Auditoria de Grants
                <small>Historico completo de solicitacoes ativas e revogadas</small>
              </h2>
            </div>
            <div class="col-auto d-flex gap-2">
              <form method="GET" action="audit.cgi" class="d-flex gap-2 m-0">
                <select class="form-select" id="db_id" name="db_id" onchange="this.form.submit()">
                  <option value="" disabled selected>Selecione um Banco...</option>
                  $DB_OPTIONS
                </select>
              </form>
              <a href="index.cgi" class="btn btn-outline-primary">
                <i class="bi bi-plus-lg me-1"></i> Nova Solicitacao
              </a>
            </div>
          </div>
        </div>
      </div>

      <!-- Body -->
      <div class="page-body">
        <div class="container-xl">

          <!-- Stats -->
          <div class="row g-3 mb-4">
            <div class="col-md-3">
              <div class="stat-card d-flex align-items-center gap-3">
                <div class="stat-icon" style="background: rgba(53,132,228,0.12); color: #62a0ea;">
                  <i class="bi bi-list-check"></i>
                </div>
                <div>
                  <div class="stat-value" id="stat-total">--</div>
                  <div class="stat-label">Total de Solicitacoes</div>
                </div>
              </div>
            </div>
            <div class="col-md-3">
              <div class="stat-card d-flex align-items-center gap-3">
                <div class="stat-icon" style="background: rgba(46,213,115,0.12); color: #2ed573;">
                  <i class="bi bi-check-circle"></i>
                </div>
                <div>
                  <div class="stat-value" id="stat-ativos">--</div>
                  <div class="stat-label">Ativos (Sucesso)</div>
                </div>
              </div>
            </div>
            <div class="col-md-3">
              <div class="stat-card d-flex align-items-center gap-3">
                <div class="stat-icon" style="background: rgba(139,143,163,0.12); color: #8b8fa3;">
                  <i class="bi bi-archive"></i>
                </div>
                <div>
                  <div class="stat-value" id="stat-revogados">--</div>
                  <div class="stat-label">Revogados</div>
                </div>
              </div>
            </div>
            <div class="col-md-3">
              <div class="stat-card d-flex align-items-center gap-3">
                <div class="stat-icon" style="background: rgba(255,71,87,0.12); color: #ff4757;">
                  <i class="bi bi-x-circle"></i>
                </div>
                <div>
                  <div class="stat-value" id="stat-erros">--</div>
                  <div class="stat-label">Com Erro</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Tabela -->
          <div class="card">
            <div class="card-body p-0">
              <div class="table-responsive">
                <table id="auditTable" class="table table-striped table-hover mb-0 w-100">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Usuario Destino</th>
                      <th>Privilegio</th>
                      <th>Objeto</th>
                      <th>Solicitante</th>
                      <th>IP Cliente</th>
                      <th>Maquina</th>
                      <th>User-Agent</th>
                      <th>Data Inicio</th>
                      <th>Expira em</th>
                      <th>Status</th>
                      <th>Observacoes</th>
                    </tr>
                  </thead>
                  <tbody>
                    $TABLE_ROWS
                  </tbody>
                </table>
              </div>
            </div>
          </div>

        </div>
      </div>

      <!-- Footer -->
      <footer class="footer">
        <div class="container-fluid">
          <div class="row align-items-center">
            <div class="col text-muted small">
              &copy; 2026 DBA Team &mdash; Seguranca &amp; Auditoria
            </div>
            <div class="col-auto text-muted small">
              Atualizado em: $DATA_ATUAL
              &nbsp;&middot;&nbsp;
              <span class="badge-soft-info px-2">v2.5.0</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/@tabler/core@1.4.0/dist/js/tabler.min.js"></script>
  <script src="https://code.jquery.com/jquery-3.6.4.min.js"></script>
  <script src="https://cdn.datatables.net/1.13.4/js/jquery.dataTables.min.js"></script>
  <script src="https://cdn.datatables.net/1.13.4/js/dataTables.bootstrap5.min.js"></script>

  <script>
    $(document).ready(function () {
      var tabela = $('#auditTable').DataTable({
        order: [[0, 'desc']],
        language: { url: '//cdn.datatables.net/plug-ins/1.13.4/i18n/pt-BR.json' },
        pageLength: 10,
        lengthMenu: [10, 25, 50, 100],
        drawCallback: function () {
          var api = this.api();
          var total = api.rows().count();
          var dados = api.column(10).data();
          var ativos = 0, revogados = 0, erros = 0;
          dados.each(function (val) {
            var s = val.replace(/<[^>]+>/g, '').trim().toUpperCase();
            if (s.indexOf('SUCESSO') !== -1) ativos++;
            else if (s.indexOf('REVOGADO') !== -1) revogados++;
            else if (s.indexOf('ERRO') !== -1) erros++;
          });
          $('#stat-total').text(total);
          $('#stat-ativos').text(ativos);
          $('#stat-revogados').text(revogados);
          $('#stat-erros').text(erros);
        }
      });
    });
  </script>
</body>
</html>
EOF