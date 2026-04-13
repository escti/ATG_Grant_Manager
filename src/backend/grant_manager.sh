# colocar esse script no caminho: /usr/local/bin/grant_manager.sh

#!/bin/bash

# ==============================================================================
# Script: grant_manager.sh (Versão Hardened)
# Descrição: Backend para concessão de grants com validação DBMS_ASSERT e Env Setup.
# ==============================================================================

# 1. Configuração do Ambiente Oracle (CRÍTICO PARA RODAR VIA APACHE)
# Ajuste estes caminhos exatamente conforme sua instalação no servidor
export ORACLE_HOME="/u01/app/oracle/product/19.0.0/dbhome_1"
export LD_LIBRARY_PATH=$ORACLE_HOME/lib:/lib:/usr/lib
export PATH=$ORACLE_HOME/bin:$PATH
# Define onde o sqlplus buscará o tnsnames.ora (normalmente $ORACLE_HOME/network/admin)
export TNS_ADMIN=$ORACLE_HOME/network/admin

# 2. Setup Base
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
ENV_FILE="$SCRIPT_DIR/.env"
CATALOG_FILE="$SCRIPT_DIR/tns_catalog.conf"
JIRA_SCRIPT="$SCRIPT_DIR/jira_validator.py"

if [ -f "$ENV_FILE" ]; then
    source "$ENV_FILE"
else
    echo "ERRO: Arquivo de ambiente (.env) não encontrado em $SCRIPT_DIR."
    exit 1
fi

# 3. Recebimento de Variáveis
USUARIO_GRANTED="$1"
PRIVILEGIO="$2"
OBJETO="$3"
GRANTOR="$4"
JIRA_TICKET="$5"
DB_ID="$6"

# 4. Validações Preliminares (Shell Level)
if [[ -z "$USUARIO_GRANTED" || -z "$PRIVILEGIO" || -z "$OBJETO" || -z "$GRANTOR" || -z "$JIRA_TICKET" || -z "$DB_ID" ]]; then
    echo "ERRO: Parâmetros insuficientes. Chamado Jira e Banco são obrigatórios."
    exit 1
fi

# 4.1 Validação do Jira Ticket
JIRA_OUTPUT=$(python3 "$JIRA_SCRIPT" "$JIRA_TICKET" 2>&1)
if [ $? -ne 0 ]; then
    echo "$JIRA_OUTPUT"
    exit 1
fi

# 4.2 Carregar TNS String do Banco Alvo
DB_TNS=$(awk -F'|' -v id="$DB_ID" '$1==id {print $3}' "$CATALOG_FILE")
if [ -z "$DB_TNS" ]; then
    echo "ERRO: Banco de dados '$DB_ID' não encontrado no tns_catalog.conf."
    exit 1
fi

# Whitelist de privilégios
if [[ ! "$PRIVILEGIO" =~ ^(SELECT|INSERT|UPDATE|DELETE)$ ]]; then
    echo "ERRO: Privilégio inválido."
    exit 1
fi

# 5. Construção do Script SQL com Segurança (DBMS_ASSERT)
SQL_SCRIPT=$(cat <<EOF
SET SERVEROUTPUT ON
SET FEEDBACK OFF
WHENEVER SQLERROR EXIT SQL.SQLCODE ROLLBACK;

DECLARE
    v_usuario_raw  VARCHAR2(128) := '$USUARIO_GRANTED';
    v_objeto_raw   VARCHAR2(128) := '$OBJETO';
    v_privilegio   VARCHAR2(30)  := '$PRIVILEGIO'; -- Validado via Shell regex
    v_grantor      VARCHAR2(128) := '$GRANTOR';
    
    v_usuario_safe VARCHAR2(128);
    v_objeto_safe  VARCHAR2(128);
    v_sql_stmt     VARCHAR2(1000);
    v_err_msg      VARCHAR2(4000);
BEGIN
    -- CAMADA DE SEGURANÇA DB: Validação contra SQL Injection e Existência
    BEGIN
        -- Enquote name garante que a string é um identificador válido. 
        -- O segundo parametro FALSE evita forçar aspas duplas se não necessário (case insensitive).
        v_usuario_safe := DBMS_ASSERT.ENQUOTE_NAME(v_usuario_raw, FALSE);
        
        -- Verifica se o objeto existe e é válido para SQL. Se não existir, lança exceção aqui.
        v_objeto_safe  := DBMS_ASSERT.SQL_OBJECT_NAME(v_objeto_raw);
        
    EXCEPTION WHEN OTHERS THEN
        RAISE_APPLICATION_ERROR(-20001, 'Falha de validação de segurança (DBMS_ASSERT): Objeto ou Usuário inválido/inexistente.');
    END;

    -- Execução do GRANT
    BEGIN
        v_sql_stmt := 'GRANT ' || v_privilegio || ' ON ' || v_objeto_safe || ' TO ' || v_usuario_safe;
        EXECUTE IMMEDIATE v_sql_stmt;
        
        -- Auditoria
        INSERT INTO SVC_DBA.GRANT_CONTROL 
        (USUARIO_GRANTED, PRIVILEGIO, OBJETO, GRANTOR, STATUS, OBSERVACOES)
        VALUES 
        (v_usuario_safe, v_privilegio, v_objeto_safe, v_grantor, 'SUCESSO', 'Grant aplicado via Web (Secure)');
        
        COMMIT;
        DBMS_OUTPUT.PUT_LINE('STATUS:SUCESSO');
        
    EXCEPTION WHEN OTHERS THEN
        v_err_msg := SQLERRM;
        ROLLBACK; -- Rollback do Grant se falhou, mas vamos inserir o log
        
        -- Log de Erro (Transação Autônoma para garantir insert mesmo após erro)
        DECLARE
            PRAGMA AUTONOMOUS_TRANSACTION;
        BEGIN
            INSERT INTO SVC_DBA.GRANT_CONTROL 
            (USUARIO_GRANTED, PRIVILEGIO, OBJETO, GRANTOR, STATUS, OBSERVACOES)
            VALUES 
            (v_usuario_raw, v_privilegio, v_objeto_raw, v_grantor, 'ERRO', v_err_msg);
            COMMIT;
        END;
        
        DBMS_OUTPUT.PUT_LINE('STATUS:ERRO|MSG:' || v_err_msg);
    END;
END;
/
EXIT;
EOF
)

# 6. Execução
# Usamos aspas no env DB_TNS no sqlplus para suportar ezconnect completo
RESULTADO=$(echo "$SQL_SCRIPT" | sqlplus -S "${DB_USER}/${DB_PASS}@${DB_TNS}")

# 7. Tratamento de Retorno
if echo "$RESULTADO" | grep -q "STATUS:SUCESSO"; then
    echo "Grant aplicado com sucesso em $OBJETO para $USUARIO_GRANTED."
    exit 0
elif echo "$RESULTADO" | grep -q "STATUS:ERRO"; then
    MSG_ERRO=$(echo "$RESULTADO" | grep "MSG:" | cut -d':' -f2-)
    echo "Falha Oracle: $MSG_ERRO"
    exit 1
else
    # Captura erros de conexão (ORA-12154, etc) que não foram tratados no PL/SQL
    echo "Erro Crítico de Conexão/Ambiente: $(echo $RESULTADO | head -n 1)"
    exit 2
fi