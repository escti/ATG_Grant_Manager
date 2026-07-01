---
name: database
description: Regras de Banco de Dados Oracle, DDL, Segurança e Jobs
---

# 🗄️ Skill: Database (Oracle)

## Padrões DDL

### Nomenclatura
- Schemas: `SVC_DBA` para objetos de serviço (não usar `SYS`, `SYSTEM` ou `ADMIN`)
- Tabelas: `UPPER_SNAKE_CASE` com prefixo descritivo (ex: `GRANT_CONTROL`)
- Jobs: `SVC_DBA.JOB_AUTO_REVOKE_GRANTS`
- Sequences: `SEQ_<TABLE_NAME>` se necessário

### Comentários
- Toda DDL DEVE ter `COMMENT ON TABLE` e `COMMENT ON COLUMN` para cada coluna
- Comentários em português (BR)

### Grants Mínimos
- `SVC_DBA` deve ter apenas:
  - `GRANT ANY OBJECT PRIVILEGES` (ou grants individuais por schema)
  - Acesso às tabelas de auditoria (`SVC_DBA.GRANT_CONTROL`)
  - `CREATE JOB` (para o scheduler)
- **Nunca** conceder `DBA` role ao `SVC_DBA`

## DBMS_ASSERT (Contra SQL Injection)
- **Sempre** usar `DBMS_ASSERT.SQL_OBJECT_NAME` para validar nomes de objetos (tabelas, schemas)
- **Sempre** usar `DBMS_ASSERT.ENQUOTE_NAME` para envelopar nomes de objetos dinâmicos
- Exemplo:
  ```sql
  EXECUTE IMMEDIATE 'GRANT ' || v_privilege || ' ON ' ||
    DBMS_ASSERT.ENQUOTE_NAME(DBMS_ASSERT.SQL_OBJECT_NAME(v_owner)) || '.' ||
    DBMS_ASSERT.ENQUOTE_NAME(DBMS_ASSERT.SQL_OBJECT_NAME(v_object)) ||
    ' TO ' || DBMS_ASSERT.ENQUOTE_NAME(DBMS_ASSERT.SQL_OBJECT_NAME(v_user));
  ```

## Tabela de Auditoria (`GRANT_CONTROL`)
- Colunas obrigatórias (DDL real em `src/db/CREATE_TABLE_SVC_DBA.GRANT_CONTROL.sql`):
  - `ID` (NUMBER PK, auto por sequence)
  - `USUARIO_GRANTED` (VARCHAR2(128), NOT NULL)
  - `PRIVILEGIO` (VARCHAR2(30), NOT NULL)
  - `OBJETO` (VARCHAR2(128), NOT NULL)
  - `GRANTOR` (VARCHAR2(128), NOT NULL)
  - `DATA_SOLICITACAO` (DATE, default SYSDATE, NOT NULL)
  - `DATA_EXPIRACAO` (DATE, default SYSDATE + 15, NOT NULL)
  - `STATUS` (VARCHAR2(20), CHECK IN ('SUCESSO', 'ERRO', 'REVOGADO'))
  - `OBSERVACOES` (VARCHAR2(4000))
  - `CLIENTE_IP` (VARCHAR2(45)) — IP do cliente (REMOTE_ADDR)
  - `MAQUINA` (VARCHAR2(128)) — Nome da máquina (reverse DNS)
  - `USER_AGENT` (VARCHAR2(512)) — User-Agent do navegador

## Job de Revogação Automática
- Usar `DBMS_SCHEDULER` (não `DBMS_JOB` — obsoleto)
- Frequência: diária (ex: `FREQ=DAILY; BYHOUR=2; BYMINUTE=0`)
- Lógica:
  1. Selecionar registros em `GRANT_CONTROL` com `STATUS = 'SUCESSO'` e `DATA_EXPIRACAO < SYSDATE`
  2. Para cada um: `REVOKE` o privilégio e atualizar `STATUS` para `'REVOGADO'` e `OBSERVACOES` concatenando motivo da revogação
- Log de execução via `DBMS_OUTPUT` (para debug) e atualização direta na tabela

## Segurança
- As DDLs são versionadas no Git e aplicadas manualmente pelo DBA (não há migration automática)
- Toda alteração em objeto de banco DEVE ter DDL correspondente em `src/db/`
- Nunca hardcodar senhas nas DDLs
- Usar tablespace `USERS` (padrão) a menos que especificado
