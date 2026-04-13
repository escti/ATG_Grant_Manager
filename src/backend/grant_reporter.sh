#!/bin/bash

# ==============================================================================
# Script: grant_reporter.sh
# Descrição: Gera linhas HTML de auditoria a partir da tabela GRANT_CONTROL
# ==============================================================================

# 1. Configuração do Ambiente (Idêntico ao manager)
export ORACLE_HOME="/u01/app/oracle/product/19.0.0/dbhome_1"
export LD_LIBRARY_PATH=$ORACLE_HOME/lib:/lib:/usr/lib
export PATH=$ORACLE_HOME/bin:$PATH
export TNS_ADMIN=$ORACLE_HOME/network/admin

# 2. Credenciais
DB_USER="SVC_DBA"
DB_PASS="svcpasswd"
DB_TNS="DELTA1"

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
    '<td>' || TO_CHAR(DATA_SOLICITACAO, 'DD/MM/YYYY HH24:MI') || '</td>' ||
    '<td>' || TO_CHAR(DATA_EXPIRACAO, 'DD/MM/YYYY') || '</td>' ||
    '<td><span class="badge ' || 
        CASE STATUS 
            WHEN 'SUCESSO' THEN 'bg-success'
            WHEN 'REVOGADO' THEN 'bg-secondary'
            WHEN 'ERRO' THEN 'bg-danger'
            ELSE 'bg-warning'
        END || '">' || STATUS || '</span></td>' ||
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
echo "$SQL_QUERY" | sqlplus -S ${DB_USER}/${DB_PASS}@${DB_TNS}