#!/bin/bash

# ==============================================================================
# Script: grant_reporter.sh
# Descrição: Gera linhas HTML de auditoria a partir da tabela GRANT_CONTROL
# ==============================================================================

# 1. Configuração do Ambiente (Idêntico ao manager)
if ! command -v sqlplus >/dev/null 2>&1; then
    export ORACLE_HOME="${ORACLE_HOME:-/u01/app/oracle/product/19.0.0/dbhome_1}"
    export LD_LIBRARY_PATH="${LD_LIBRARY_PATH:-$ORACLE_HOME/lib:/lib:/usr/lib}"
    export PATH="$ORACLE_HOME/bin:$PATH"
    export TNS_ADMIN="${TNS_ADMIN:-$ORACLE_HOME/network/admin}"
fi

# 2. Setup Base
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
ENV_FILE="$SCRIPT_DIR/.env"
CATALOG_FILE="$SCRIPT_DIR/tns_catalog.conf"

if [ -f "$ENV_FILE" ]; then
    source "$ENV_FILE"
else
    echo "ERRO: Arquivo de ambiente (.env) não encontrado."
    exit 1
fi

DB_ID=$1
if [ -z "$DB_ID" ]; then
    echo "ERRO: Banco de dados não informado."
    exit 1
fi

DB_TNS=$(awk -F'|' -v id="$DB_ID" '$1==id {print $3}' "$CATALOG_FILE")
DB_TYPE=$(awk -F'|' -v id="$DB_ID" '$1==id {print $4}' "$CATALOG_FILE")
[ -z "$DB_TYPE" ] && DB_TYPE="oracle"
if [ -z "$DB_TNS" ]; then
    echo "ERRO: Banco de dados '$DB_ID' não cadastrado."
    exit 1
fi

# Roteamento para MySQL
if [ "$DB_TYPE" = "mysql" ]; then
    MYSQL_SCRIPT="$SCRIPT_DIR/mysql_grant_reporter.py"
    if [ ! -f "$MYSQL_SCRIPT" ]; then
        echo "<tr><td colspan='12' class='text-center py-4 text-muted'>Script MySQL ($MYSQL_SCRIPT) não encontrado. Aguardando implementação do colega.</td></tr>"
        exit 0
    fi
    python3 "$MYSQL_SCRIPT" "$DB_TNS"
    exit $?
fi

# 3. Query SQL Geradora de HTML
# Usamos concatenação para criar as tags <tr> e <td> diretamente.
# A lógica CASE define a cor do badge (Verde para sucesso, Vermelho erro, Cinza revogado)

SQL_QUERY=$(cat <<EOF
SET PAGESIZE 0
SET FEEDBACK OFF
SET VERIFY OFF
SET HEADING OFF
SET LINESIZE 1000
SET TRIMSPOOL ON

SELECT 
    '<tr>' ||
    '<td>' || ID || '</td>' ||
    '<td><strong>' || USUARIO_GRANTED || '</strong></td>' ||
    '<td>' || PRIVILEGIO || '</td>' ||
    '<td>' || OBJETO || '</td>' ||
    '<td>' || GRANTOR || '</td>' ||
    '<td><code class="small">' || NVL(CLIENTE_IP, '-') || '</code></td>' ||
    '<td><code class="small">' || NVL(MAQUINA, '-') || '</code></td>' ||
    '<td class="text-muted small text-truncate" style="max-width:150px;" title="' || NVL(USER_AGENT, '-') || '">' || NVL(USER_AGENT, '-') || '</td>' ||
    '<td>' || TO_CHAR(DATA_SOLICITACAO, 'DD/MM/YYYY HH24:MI') || '</td>' ||
    '<td>' || TO_CHAR(DATA_EXPIRACAO, 'DD/MM/YYYY') || '</td>' ||
    '<td><span class="badge-soft-' || 
        CASE STATUS 
            WHEN 'SUCESSO' THEN 'success'
            WHEN 'REVOGADO' THEN 'secondary'
            WHEN 'ERRO' THEN 'danger'
            ELSE 'warning'
        END || ' px-2 py-1">' || STATUS || '</span></td>' ||
    '<td class="text-muted small text-truncate" style="max-width: 200px;" title="' || OBSERVACOES || '">' || 
        OBSERVACOES || 
    '</td>' ||
    '</tr>'
FROM SVC_DBA.GRANT_CONTROL
ORDER BY ID DESC;

EXIT;
EOF
)

# 4. Execução
echo "$SQL_QUERY" | sqlplus -S "${DB_USER}/${DB_PASS}@${DB_TNS}"