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
    while IFS='|' read -r dbid dbname dbstring dbtype dbambiente; do
        [[ "$dbid" =~ ^#.* ]] && continue
        [ -z "$dbid" ] && continue
        [ -z "$dbtype" ] && dbtype="oracle"
        [ -z "$dbambiente" ] && dbambiente="DEV"
        DB_OPTIONS+="<option value=\"$dbid\" data-sgbd=\"$dbtype\" data-ambiente=\"$dbambiente\">$dbname</option>"
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
    DB_ID_VAL=$(urldecode "$db_id")
    SGBD_VAL=$(urldecode "$db_sgbd")
    AMBIENTE_VAL=$(urldecode "$db_ambiente")

    # Sanitização Shell
    USUARIO_CLEAN=$(echo "$USUARIO_VAL" | tr -cd '[:alnum:]_')
    OBJETO_CLEAN=$(echo "$OBJETO_VAL" | tr -cd '[:alnum:]_$.')
    GRANTOR_CLEAN=$(echo "$GRANTOR_VAL" | tr -cd '[:alnum:]_')
    PRIVILEGIO_CLEAN=$(echo "$PRIVILEGIO_VAL" | tr -cd '[:alpha:]')
    DB_ID_CLEAN=$(echo "$DB_ID_VAL" | tr -cd '[:alnum:]_')
    SGBD_CLEAN=$(echo "$SGBD_VAL" | tr -cd '[:alpha:]')
    AMBIENTE_CLEAN=$(echo "$AMBIENTE_VAL" | tr -cd '[:alnum:]')

    OUTPUT=$(/usr/local/bin/grant_manager.sh "$USUARIO_CLEAN" "$PRIVILEGIO_CLEAN" "$OBJETO_CLEAN" "$GRANTOR_CLEAN" "$DB_ID_CLEAN" "$SGBD_CLEAN" "$AMBIENTE_CLEAN")
    RET_CODE=$?

    if [ $RET_CODE -eq 0 ]; then
        ALERT_HTML="<div class='alert alert-success d-flex align-items-center gap-3' role='alert'><i class='bi bi-check-circle-fill fs-4'></i><div><strong>Sucesso!</strong> $OUTPUT</div></div>"
    else
        ALERT_HTML="<div class='alert alert-danger d-flex align-items-center gap-3' role='alert'><i class='bi bi-x-circle-fill fs-4'></i><div><strong>Erro:</strong> $OUTPUT</div></div>"
    fi
fi

# HTML Template - Tabler Dark Mode
cat <<EOF
<!DOCTYPE html>
<html lang="pt-BR" data-bs-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Autoglass GRANT MANAGER | ATGGM</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/core@1.4.0/dist/css/tabler.min.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.13.1/font/bootstrap-icons.min.css">
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
    .btn-primary { background: linear-gradient(135deg, #1a5fb4 0%, #3584e4 100%); border: none; border-radius: 8px; padding: 0.7rem 1.5rem; font-weight: 600; transition: all 0.2s ease; }
    .btn-primary:hover { transform: translateY(-1px); box-shadow: 0 6px 20px rgba(53, 132, 228, 0.35); }
    .btn-outline-primary { border-color: #3584e4; color: #3584e4; border-radius: 8px; }
    .btn-outline-primary:hover { background: #3584e4; border-color: #3584e4; }
    .page-title { font-size: 1.3rem; font-weight: 700; color: #e6e7ed; }
    .page-title small { font-size: 0.8rem; font-weight: 400; color: #8b8fa3; display: block; margin-top: 4px; }
    .alert { border-radius: 10px; border: none; }
    .alert-success { background: rgba(46, 213, 115, 0.1); border-left: 4px solid #2ed573; color: #2ed573; }
    .alert-danger { background: rgba(255, 71, 87, 0.1); border-left: 4px solid #ff4757; color: #ff4757; }
    .alert-info { background: rgba(53, 132, 228, 0.1); border-left: 4px solid #3584e4; color: #62a0ea; }
    .footer { border-top: 1px solid #2a2d3a; padding: 1rem 1.5rem; }
    .badge-soft-info { background: rgba(53, 132, 228, 0.12); color: #62a0ea; border-radius: 6px; padding: 0.3rem 0.7rem; }
    .divider { border-color: #2a2d3a; opacity: 0.6; }
    hr { border-color: #2a2d3a; }
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
              <a class="nav-link active" href="index.cgi">
                <i class="bi bi-shield-check me-2"></i> Solicitar Grant
              </a>
            </li>
            <li class="nav-item mb-1">
              <a class="nav-link" href="audit.cgi">
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
                Solicitar Grant
                <small>Preencha o formulario para conceder acesso temporario a um banco de dados</small>
              </h2>
            </div>
            <div class="col-auto">
              <a href="audit.cgi" class="btn btn-outline-primary">
                <i class="bi bi-clock-history me-1"></i> Auditoria
              </a>
            </div>
          </div>
        </div>
      </div>

      <!-- Body -->
      <div class="page-body">
        <div class="container-xl">

          $ALERT_HTML

          <!-- Formulario -->
          <div class="card">
            <div class="card-header d-flex align-items-center gap-3">
              <i class="bi bi-pencil-square fs-4 text-primary"></i>
              <div>
                <h3 class="card-title mb-0">Nova Solicitacao de Acesso</h3>
                <p class="text-muted small mb-0">Preencha todos os campos obrigatorios</p>
              </div>
            </div>
            <div class="card-body">
              <form method="POST" action="index.cgi">

                <div class="row g-3 mb-3">
                  <div class="col-md-6">
                    <label class="form-label" for="db_sgbd">SGBD</label>
                    <select class="form-select" id="db_sgbd" name="db_sgbd" onchange="filtrarBancos()">
                      <option value="oracle" selected>Oracle</option>
                      <option value="mysql">MySQL</option>
                    </select>
                  </div>
                  <div class="col-md-6">
                    <label class="form-label" for="db_ambiente">Ambiente</label>
                    <select class="form-select" id="db_ambiente" name="db_ambiente" onchange="filtrarBancos()">
                      <option value="HML">HML</option>
                      <option value="DEV" selected>DEV</option>
                    </select>
                  </div>
                </div>

                <div class="mb-3">
                  <label class="form-label" for="db_id">Banco Alvo</label>
                  <select class="form-select" id="db_id" name="db_id" required>
                    <option value="" disabled selected>Selecione o banco...</option>
                    $DB_OPTIONS
                  </select>
                </div>

                <div class="mb-3">
                  <label class="form-label" for="grantor">Solicitante (DBA / Responsavel)</label>
                  <div class="input-group">
                    <span class="input-group-text bg-dark border-secondary"><i class="bi bi-person-badge"></i></span>
                    <input type="text" class="form-control" id="grantor" name="grantor" required placeholder="Ex: JOAO.SILVA" autocomplete="off">
                  </div>
                </div>

                <hr class="divider my-4">

                <div class="row g-3 mb-3">
                  <div class="col-md-6">
                    <label class="form-label" for="usuario">Usuario / Role Destino</label>
                    <div class="input-group">
                      <span class="input-group-text bg-dark border-secondary"><i class="bi bi-person"></i></span>
                      <input type="text" class="form-control" id="usuario" name="usuario" required placeholder="Ex: MARIA.SOUZA">
                    </div>
                  </div>
                  <div class="col-md-6">
                    <label class="form-label" for="privilegio">Privilegio</label>
                    <select class="form-select" id="privilegio" name="privilegio">
                      <option value="CONSULTA" selected>CONSULTA (SELECT)</option>
                      <option value="EDICAO">EDICAO (INSERT, UPDATE, DELETE)</option>
                      <option value="AMBAS">AMBAS (SELECT, INSERT, UPDATE, DELETE)</option>
                    </select>
                  </div>
                </div>

                <div class="mb-4">
                  <label class="form-label" for="objeto">Objeto Alvo (Schema.Tabela)</label>
                  <div class="input-group">
                    <span class="input-group-text bg-dark border-secondary"><i class="bi bi-table"></i></span>
                    <input type="text" class="form-control" id="objeto" name="objeto" required placeholder="Ex: HR.EMPLOYEES">
                  </div>
                  <div class="mt-1">
                    <small class="text-muted"><i class="bi bi-info-circle me-1"></i>Certifique-se que o Schema esta correto.</small>
                  </div>
                </div>

                <button type="submit" class="btn btn-primary w-100 py-2">
                  <i class="bi bi-shield-lock-fill me-2"></i>
                  Conceder Acesso
                </button>
              </form>
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
              <span class="badge-soft-info px-2">v2.4.0</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/@tabler/core@1.4.0/dist/js/tabler.min.js"></script>
  <script>
    function filtrarBancos() {
      var sgbd = document.getElementById('db_sgbd').value;
      var ambiente = document.getElementById('db_ambiente').value;
      var selectBanco = document.getElementById('db_id');
      var options = selectBanco.querySelectorAll('option[data-sgbd]');
      var temVisivel = false;
      options.forEach(function(opt) {
        if (opt.getAttribute('data-sgbd') === sgbd && opt.getAttribute('data-ambiente') === ambiente) {
          opt.style.display = '';
          temVisivel = true;
        } else {
          opt.style.display = 'none';
        }
      });
      selectBanco.value = '';
      var placeholder = selectBanco.querySelector('option[disabled]');
      if (placeholder) {
        placeholder.textContent = temVisivel ? 'Selecione o banco...' : 'Nenhum banco disponivel para este SGBD/Ambiente';
      }
    }
    document.addEventListener('DOMContentLoaded', filtrarBancos);
  </script>
</body>
</html>
EOF