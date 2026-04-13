CREATE BIGFILE TABLESPACE "USERS" DATAFILE SIZE 10m AUTOEXTEND ON NEXT 50m MAXSIZE 10g;
-- CREATE BIGFILE TEMPORARY TABLESPACE "TEMP" TEMPFILE SIZE 10m AUTOEXTEND ON NEXT 50m MAXSIZE 10g;

-- 1. Criar o Usuário Administrador da Ferramenta
CREATE USER "SVC_DBA" IDENTIFIED BY "SVC_DBA_01" DEFAULT TABLESPACE "USERS" TEMPORARY TABLESPACE "TEMP";
	  
GRANT CONNECT, RESOURCE TO SVC_DBA;
GRANT CREATE JOB TO SVC_DBA;
GRANT UNLIMITED TABLESPACE TO SVC_DBA;
-- Permissões perigosas necessárias para o funcionamento (Ajuste conforme politica de segurança)
GRANT GRANT ANY OBJECT PRIVILEGE TO SVC_DBA with admin OPTION;
-- GRANT REVOKE ANY OBJECT PRIVILEGE TO SVC_DBA;

-- 2. Criar a Tabela de Controle e Sequencia
CREATE SEQUENCE SVC_DBA.SEQ_TB_GRANT_CONTROL START WITH 1 INCREMENT BY 1;

CREATE TABLE SVC_DBA.TB_GRANT_CONTROL (
    ID              NUMBER DEFAULT SVC_DBA.SEQ_TB_GRANT_CONTROL.NEXTVAL PRIMARY KEY,
    USUARIO_GRANTED VARCHAR2(128) NOT NULL,
    PRIVILEGIO      VARCHAR2(30)  NOT NULL,
    OBJETO          VARCHAR2(128) NOT NULL,
    GRANTOR         VARCHAR2(128) NOT NULL,
    DATA_SOLICITACAO DATE DEFAULT SYSDATE NOT NULL,
    DATA_EXPIRACAO   DATE DEFAULT SYSDATE + 15 NOT NULL,
    STATUS           VARCHAR2(20) CHECK (STATUS IN ('SUCESSO', 'ERRO', 'REVOGADO')),
    OBSERVACOES      VARCHAR2(4000)
);

-- 3. Criar o Job de Revoke Automático (Roda todo dia à 01:00 AM)
BEGIN
    DBMS_SCHEDULER.create_job (
        job_name        => 'SVC_DBA.JOB_AUTO_REVOKE_GRANTS',
        job_type        => 'PLSQL_BLOCK',
        job_action      => '
            DECLARE
                CURSOR c_expired IS
                    SELECT ID, USUARIO_GRANTED, PRIVILEGIO, OBJETO
                    FROM SVC_DBA.TB_GRANT_CONTROL
                    WHERE STATUS = ''SUCESSO''
                    AND DATA_EXPIRACAO < SYSDATE;
            BEGIN
                FOR r IN c_expired LOOP
                    BEGIN
                        EXECUTE IMMEDIATE ''REVOKE '' || r.PRIVILEGIO || '' ON '' || r.OBJETO || '' FROM '' || r.USUARIO_GRANTED;
                        UPDATE SVC_DBA.TB_GRANT_CONTROL
                        SET STATUS = ''REVOGADO'', OBSERVACOES = OBSERVACOES || '' | Revogado via Job.''
                        WHERE ID = r.ID;
                    EXCEPTION WHEN OTHERS THEN
                        UPDATE SVC_DBA.TB_GRANT_CONTROL
                        SET OBSERVACOES = OBSERVACOES || '' | Erro Revoke: '' || SQLERRM
                        WHERE ID = r.ID;
                    END;
                END LOOP;
                COMMIT;
            END;',
        start_date      => SYSTIMESTAMP,
        repeat_interval => 'FREQ=DAILY; BYHOUR=01; BYMINUTE=00',
        enabled         => TRUE
    );
END;
/

-- 4. criação de trigger para alimentar a tabela que será a base para gerar o revoke Automático
CREATE OR REPLACE TRIGGER SVC_DBA.TRG_AUDIT_DBA_GRANTS
AFTER GRANT ON DATABASE
DECLARE
    -- Coleções para armazenar listas de grantees e privilégios
    v_grantees      ora_name_list_t;
    v_privs         ora_name_list_t;
    v_num_grantees  BINARY_INTEGER;
    v_num_privs     BINARY_INTEGER;
    
    -- Variáveis auxiliares
    v_current_user  VARCHAR2(128);
    v_obj_owner     VARCHAR2(128);
    v_obj_name      VARCHAR2(128);
BEGIN
    -- 1. Identificar quem está executando o comando
    v_current_user := SYS_CONTEXT('USERENV', 'SESSION_USER');

    -- 2. Filtro de Segurança e Escopo: Apenas usuários 'DBA_%'
    IF v_current_user LIKE 'DBA_%' THEN
        
        -- Carrega as listas de quem recebeu e o que recebeu
        v_num_grantees := ora_grantee(v_grantees);
        v_num_privs    := ora_privilege_list(v_privs);
        
        -- Captura objeto alvo (Owner e Nome)
        v_obj_owner := ora_dict_obj_owner;
        v_obj_name  := ora_dict_obj_name;

        -- 3. Loop Aninhado: Processar cada combinação de Usuário x Privilégio
        -- Necessário pois um "GRANT SELECT, INSERT TO USR1, USR2" gera múltiplas entradas
        FOR i IN 1 .. v_num_grantees LOOP
            FOR j IN 1 .. v_num_privs LOOP
                
                -- 4. Filtrar apenas os privilégios de interesse
                IF v_privs(j) IN ('SELECT', 'INSERT', 'UPDATE', 'DELETE') THEN
                    
                    INSERT INTO SVC_DBA.TB_GRANT_CONTROL (
                        USUARIO_GRANTED,
                        PRIVILEGIO,
                        OBJETO,
                        GRANTOR,
                        STATUS,
                        OBSERVACOES
                    ) VALUES (
                        v_grantees(i),                -- Quem recebeu
                        v_privs(j),                   -- O privilégio (ex: SELECT)
                        v_obj_owner || '.' || v_obj_name, -- Objeto (SCHEMA.TABELA)
                        v_current_user,               -- Quem concedeu (DBA_...)
                        'SUCESSO',                    -- Se a trigger disparou (AFTER), o grant ocorreu
                        'Capturado via System Trigger em instância RAC: ' || 
                        SYS_CONTEXT('USERENV', 'INSTANCE_NAME')
                    );
                    
                END IF;
            END LOOP;
        END LOOP;
    END IF;
EXCEPTION
    WHEN OTHERS THEN
        -- Boas Práticas: Em triggers de sistema, evite travar o banco se o log falhar.
        -- Opcional: Gravar no alert log ou ignorar falha de insert.
        -- Aqui, optamos por não interromper a operação de GRANT original.
        NULL;
END;
/