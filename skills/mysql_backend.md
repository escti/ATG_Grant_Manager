---
name: mysql_backend
description: Implementação dos scripts Python de gerenciamento de grants em MySQL, DDLs, Event Scheduler de revogação automática e integração com o roteamento Oracle existente
---

# 🧠 Skill: Backend MySQL para o Oracle Grant Manager (OGM)

Este documento define tudo que o colega precisa saber para implementar os scripts Python de gerenciamento de grants em **MySQL**, seguindo a mesma arquitetura, padrões de segurança e contrato de interface do backend Oracle existente.

---

## Sumário

1. [Visão Geral](#1-visão-geral)
2. [Contrato de Interface](#2-contrato-de-interface)
3. [Correção Obrigatória no Shell Antes de Começar](#3-correção-obrigatória-no-shell-antes-de-começar)
4. [Estrutura do Banco MySQL](#4-estrutura-do-banco-mysql)
5. [Arquivo 1: `mysql_grant_manager.py`](#5-arquivo-1-mysql_grant_managerpy)
6. [Arquivo 2: `mysql_grant_reporter.py`](#6-arquivo-2-mysql_grant_reporterpy)
7. [Scripts DDL MySQL](#7-scripts-ddl-mysql)
8. [Regras de Segurança Obrigatórias](#8-regras-de-segurança-obrigatórias)
9. [Como Testar a Integração](#9-como-testar-a-integração)

---

## 1. Visão Geral

O OGM já possui roteamento para MySQL implementado nos shells:

- `grant_manager.sh`: detecta `dbtype=mysql` no `tns_catalog.conf` e redireciona para `mysql_grant_manager.py`
- `grant_reporter.sh`: faz o mesmo para `mysql_grant_reporter.py`

O frontend (`index.cgi`) já tem o dropdown com opção "MySQL" e o filtro dinâmico por SGBD+Ambiente.

**Seu trabalho**: implementar os dois scripts Python e os scripts DDL MySQL para que o fluxo completo funcione.

### Fluxo Atual (já funcionando para Oracle, aplicar para MySQL)

```
Usuário → Browser → index.cgi → POST → grant_manager.sh
                                          ↓
                                    lê tns_catalog.conf
                                          ↓
                                    dbtype=mysql? → mysql_grant_manager.py
                                          ↓
                                    Conecta MySQL → GRANT → auditoria
```

---

## 2. Contrato de Interface

### 2.1. `mysql_grant_manager.py`

**Localização**: `src/backend/mysql_grant_manager.py`

**Parâmetros** (recebidos via `sys.argv`, nesta ordem):

| # | Nome | Descrição | Exemplo |
|---|------|-----------|---------|
| 1 | `USUARIO` | Usuário/role que receberá o grant | `MARIA.SOUZA` |
| 2 | `PRIVILEGIO` | Privilégio SQL (já mapeado pelo shell) | `SELECT` ou `INSERT, UPDATE, DELETE` |
| 3 | `OBJETO` | Objeto alvo (`banco.tabela`) | `meu_banco.clientes` |
| 4 | `GRANTOR` | Nome do DBA/responsável que solicitou | `JOAO.SILVA` |
| 5 | `CLIENTE_IP` | IP do cliente (REMOTE_ADDR) | `10.0.0.1` |
| 6 | `MAQUINA` | Nome da máquina (reverse DNS) | `DESKTOP-ABC123` |
| 7 | `USER_AGENT` | User-Agent do navegador | `Mozilla/5.0 ...` |
| 8 | `DB_CONN_STR` | String de conexão do catálogo TNS | `host:porta/banco` |

**Saída esperada (stdout)**:

- **Sucesso**: `Grant aplicado com sucesso em <OBJETO> para <USUARIO>.` + `exit 0`
- **Erro**: `ERRO: <mensagem descritiva>` + `exit 1`

**Exemplo de chamada real**:
```bash
python3 mysql_grant_manager.py \
  "MARIA.SOUZA" \
  "SELECT" \
  "meu_banco.clientes" \
  "JOAO.SILVA" \
  "10.0.0.1" \
  "DESKTOP-ABC" \
  "Mozilla/5.0 ..." \
  "127.0.0.1:3306/meu_banco"
```

### 2.2. `mysql_grant_reporter.py`

**Localização**: `src/backend/mysql_grant_reporter.py`

**Parâmetros**:

| # | Nome | Descrição | Exemplo |
|---|------|-----------|---------|
| 1 | `DB_CONN_STR` | String de conexão do catálogo TNS | `host:porta/banco` |

**Saída esperada (stdout)**: Linhas `<tr>` HTML no mesmo formato do Oracle (`grant_reporter.sh`). Exit code: `0` sempre (mesmo se vazio).

**Formato HTML esperado** (12 colunas — igual ao Oracle):
```html
<tr>
  <td>1</td>
  <td><strong>MARIA.SOUZA</strong></td>
  <td>SELECT</td>
  <td>meu_banco.clientes</td>
  <td>JOAO.SILVA</td>
  <td><code class="small">10.0.0.1</code></td>
  <td><code class="small">DESKTOP-ABC</code></td>
  <td class="text-muted small text-truncate" style="max-width:150px;" title="Mozilla/5.0 ...">Mozilla/5.0 ...</td>
  <td>01/07/2026 14:30</td>
  <td>16/07/2026</td>
  <td><span class="badge-soft-success px-2 py-1">SUCESSO</span></td>
  <td class="text-muted small text-truncate" style="max-width:200px;" title="observacao">observacao</td>
</tr>
```

**Mapeamento de badge por STATUS**:
| STATUS | Classe CSS |
|--------|-----------|
| `SUCESSO` | `badge-soft-success` |
| `REVOGADO` | `badge-soft-secondary` |
| `ERRO` | `badge-soft-danger` |
| outro | `badge-soft-warning` |

Se não houver registros, retornar:
```html
<tr><td colspan='12' class='text-center py-4 text-muted'>Nenhum registro de auditoria encontrado.</td></tr>
```

---

## 3. Correção Obrigatória no Shell Antes de Começar

**Arquivo**: `src/backend/grant_manager.sh` — **linha 72**

**Problema**: A chamada ao MySQL passa `$JIRA_TICKET` como 5º argumento, mas essa variável não existe mais (Jira removido na v2.4.0). Além disso, os parâmetros de rastreamento (`CLIENTE_IP`, `MAQUINA`, `USER_AGENT`) não são repassados ao script MySQL.

**Código atual (quebrado)**:
```bash
RESULTADO_MYSQL=$(python3 "$MYSQL_SCRIPT" "$USUARIO_GRANTED" "$PRIV_SQL" "$OBJETO" "$GRANTOR" "$JIRA_TICKET" "$DB_TNS" 2>&1)
```

**Código corrigido (deve substituir)**:
```bash
RESULTADO_MYSQL=$(python3 "$MYSQL_SCRIPT" "$USUARIO_GRANTED" "$PRIV_SQL" "$OBJETO" "$GRANTOR" "$CLIENTE_IP" "$MAQUINA" "$USER_AGENT" "$DB_TNS" 2>&1)
```

> **Aplicar esta correção antes de testar o fluxo MySQL**, senão os argumentos chegarão errados no script Python.

---

## 4. Estrutura do Banco MySQL

Toda a estrutura MySQL deve ser criada em um banco próprio (definido em `.env` como `MYSQL_DB`). Valor sugerido: `oracle_grant_manager`.

### 4.1. Tabela `grant_control`

Equivalente MySQL da tabela Oracle `SVC_DBA.GRANT_CONTROL`:

```sql
CREATE TABLE grant_control (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    usuario_granted VARCHAR(128) NOT NULL,
    privilegio      VARCHAR(30)  NOT NULL,
    objeto          VARCHAR(128) NOT NULL,
    grantor         VARCHAR(128) NOT NULL,
    data_solicitacao DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    data_expiracao  DATETIME DEFAULT (CURRENT_TIMESTAMP + INTERVAL 15 DAY) NOT NULL,
    status          ENUM('SUCESSO', 'ERRO', 'REVOGADO') NOT NULL DEFAULT 'SUCESSO',
    observacoes     TEXT,
    cliente_ip      VARCHAR(45),
    maquina         VARCHAR(128),
    user_agent      VARCHAR(512),

    INDEX idx_status (status),
    INDEX idx_data_expiracao (data_expiracao),
    INDEX idx_usuario (usuario_granted)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 4.2. Event Scheduler de Revogação Automática (equivalente ao JOB Oracle)

Substitui o `DBMS_SCHEDULER.JOB_AUTO_REVOKE_GRANTS` do Oracle:

```sql
DELIMITER //

CREATE EVENT event_auto_revoke_grants
ON SCHEDULE EVERY 1 DAY
STARTS CURRENT_TIMESTAMP
DO
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE v_id INT;
    DECLARE v_usuario VARCHAR(128);
    DECLARE v_privilegio VARCHAR(30);
    DECLARE v_objeto VARCHAR(128);
    DECLARE v_observacoes TEXT;

    DECLARE cur CURSOR FOR
        SELECT id, usuario_granted, privilegio, objeto
        FROM grant_control
        WHERE status = 'SUCESSO'
          AND data_expiracao < NOW();

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO v_id, v_usuario, v_privilegio, v_objeto;
        IF done THEN
            LEAVE read_loop;
        END IF;

        -- Tenta revogar
        BEGIN
            SET @sql = CONCAT('REVOKE ', v_privilegio, ' ON ', v_objeto, ' FROM ', v_usuario);
            PREPARE stmt FROM @sql;
            EXECUTE stmt;
            DEALLOCATE PREPARE stmt;

            UPDATE grant_control
            SET status = 'REVOGADO',
                observacoes = CONCAT(COALESCE(observacoes, ''), ' | Revogado automaticamente pelo EVENT.')
            WHERE id = v_id;
        END;
    END LOOP;

    CLOSE cur;
    COMMIT;
END //

DELIMITER ;
```

**Pré-requisito**: O Event Scheduler precisa estar ativo no MySQL:
```sql
SET GLOBAL event_scheduler = ON;
```

---

## 5. Arquivo 1: `mysql_grant_manager.py`

### 5.1. Dependências

O script deve usar **`mysql-connector-python`** (já previsto na instalação via pip3). Instalação:
```bash
pip3 install mysql-connector-python python-dotenv
```

### 5.2. Estrutura do Código

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Script: mysql_grant_manager.py
# Descricao: Concede grants em MySQL e registra auditoria.
# Uso: python3 mysql_grant_manager.py <USUARIO> <PRIVILEGIO> <OBJETO>
#                                     <GRANTOR> <CLIENTE_IP> <MAQUINA>
#                                     <USER_AGENT> <DB_CONN_STR>
```

### 5.3. Lógica Principal

1. **Ler argumentos** conforme a ordem do contrato (8 args)
2. **Carregar credenciais** do arquivo `.env` (mesmo diretório do script):
   - Usar `python-dotenv` (`from dotenv import load_dotenv`)
   - Ler: `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASS`, `MYSQL_DB`
3. **Conectar ao MySQL**:
   - String de conexão: `host` = `MYSQL_HOST`, `port` = `MYSQL_PORT`, `database` = `MYSQL_DB`
   - Usar `mysql.connector.connect()`
   - Atenção: a `DB_CONN_STR` do catálogo pode ser ignorada nesse caso (as credenciais vêm do `.env`), mas ela deve ser parseada para extrair `host:port` caso o colega opte por conectar direto no banco alvo do grant. **Decisão arquitetural**: como o usuário `SVC_DBA` do MySQL gerencia grants em outros bancos, a conexão deve ser no banco alvo onde o GRANT será executado. Use `DB_CONN_STR` no formato `host:porta/nome_banco` para conectar.
4. **Validar objetos**:
   - Verificar se o banco e a tabela informados em `OBJETO` existem (opcional, boa prática)
5. **Executar GRANT**:
   ```sql
   GRANT <privilegio> ON <objeto> TO '<usuario>'@'%';
   ```
   (ou o host apropriado conforme política local)
6. **Registrar auditoria**:
   ```sql
   INSERT INTO grant_control
       (usuario_granted, privilegio, objeto, grantor, status, observacoes,
        cliente_ip, maquina, user_agent)
   VALUES
       (%s, %s, %s, %s, 'SUCESSO', 'Grant aplicado via Web (Secure)',
        %s, %s, %s);
   ```
7. **Output padronizado**:
   - Sucesso: `print("Grant aplicado com sucesso em <OBJETO> para <USUARIO>.")`
   - Erro: `print(f"ERRO: {mensagem}")` + `sys.exit(1)`
8. **Tratamento de exceções**:
   - Erro de conexão → log como erro com `sys.exit(1)`
   - Erro de GRANT → registrar na auditoria com status `ERRO`, rollback, retornar erro
   - Sempre usar transações (`commit`/`rollback`)

### 5.4. Exemplo de Tratamento de Erro com Auditoria

```python
try:
    cursor.execute(sql_grant)
    conn.commit()

    cursor.execute(sql_audit_sucesso, params)
    conn.commit()

    print(f"Grant aplicado com sucesso em {objeto} para {usuario}.")
    sys.exit(0)

except mysql.connector.Error as err:
    conn.rollback()

    # Registrar erro na auditoria (transação separada)
    cursor.execute(sql_audit_erro, params_erro)
    conn.commit()

    print(f"ERRO: {err}")
    sys.exit(1)
```

---

## 6. Arquivo 2: `mysql_grant_reporter.py`

### 6.1. Estrutura do Código

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Script: mysql_grant_reporter.py
# Descricao: Gera linhas HTML de auditoria a partir da tabela grant_control (MySQL)
# Uso: python3 mysql_grant_reporter.py <DB_CONN_STR>
```

### 6.2. Lógica Principal

1. **Ler argumentos**: 1 arg (`DB_CONN_STR`)
2. **Carregar credenciais** do `.env` (mesmo esquema do manager)
3. **Conectar ao MySQL**
4. **Query**:
   ```sql
   SELECT id, usuario_granted, privilegio, objeto, grantor,
          cliente_ip, maquina, user_agent,
          DATE_FORMAT(data_solicitacao, '%d/%m/%Y %H:%i') AS data_solicitacao_fmt,
          DATE_FORMAT(data_expiracao, '%d/%m/%Y') AS data_expiracao_fmt,
          status, observacoes
   FROM grant_control
   ORDER BY id DESC;
   ```
5. **Gerar HTML** — para cada linha, concatenar uma string `<tr>...</tr>` exatamente no mesmo formato do Oracle (seção 2.2 acima)
6. **Mapeamento de badge**:
   ```python
   badge_map = {
       'SUCESSO': 'success',
       'REVOGADO': 'secondary',
       'ERRO': 'danger'
   }
   badge_class = badge_map.get(status, 'warning')
   ```
7. **Output**: todas as `<tr>` linhas concatenadas no stdout
8. Caso não haja registros, retornar a mensagem de tabela vazia

---

## 7. Scripts DDL MySQL

Criar dois arquivos em `src/db/`:

### 7.1. `src/db/CREATE_TABLE_MYSQL_GRANT_CONTROL.sql`

```sql
-- Database: orcale_grant_manager (definido no .env como MYSQL_DB)
-- Conectar como SVC_DBA ou root e executar:

CREATE DATABASE IF NOT EXISTS orcale_grant_manager
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE orcale_grant_manager;

CREATE TABLE IF NOT EXISTS grant_control (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    usuario_granted VARCHAR(128) NOT NULL,
    privilegio      VARCHAR(30)  NOT NULL,
    objeto          VARCHAR(128) NOT NULL,
    grantor         VARCHAR(128) NOT NULL,
    data_solicitacao DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    data_expiracao  DATETIME DEFAULT (CURRENT_TIMESTAMP + INTERVAL 15 DAY) NOT NULL,
    status          ENUM('SUCESSO', 'ERRO', 'REVOGADO') NOT NULL DEFAULT 'SUCESSO',
    observacoes     TEXT,
    cliente_ip      VARCHAR(45),
    maquina         VARCHAR(128),
    user_agent      VARCHAR(512),

    INDEX idx_status (status),
    INDEX idx_data_expiracao (data_expiracao),
    INDEX idx_usuario (usuario_granted)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 7.2. `src/db/MYSQL_EVENT_AUTO_REVOKE_GRANTS.sql`

```sql
-- Evento de revogacao automatica (executa todo dia a 01:00)
-- Necessario: SET GLOBAL event_scheduler = ON;

USE orcale_grant_manager;

DELIMITER //

CREATE EVENT IF NOT EXISTS event_auto_revoke_grants
ON SCHEDULE EVERY 1 DAY
STARTS (CURRENT_TIMESTAMP + INTERVAL 1 DAY)
DO
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE v_id INT;
    DECLARE v_usuario VARCHAR(128);
    DECLARE v_privilegio VARCHAR(30);
    DECLARE v_objeto VARCHAR(128);

    DECLARE cur CURSOR FOR
        SELECT id, usuario_granted, privilegio, objeto
        FROM grant_control
        WHERE status = 'SUCESSO'
          AND data_expiracao < NOW();

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO v_id, v_usuario, v_privilegio, v_objeto;
        IF done THEN
            LEAVE read_loop;
        END IF;

        BEGIN
            SET @sql = CONCAT('REVOKE ', v_privilegio, ' ON ', v_objeto, ' FROM ', v_usuario);
            PREPARE stmt FROM @sql;
            EXECUTE stmt;
            DEALLOCATE PREPARE stmt;

            UPDATE grant_control
            SET status = 'REVOGADO',
                observacoes = CONCAT(COALESCE(observacoes, ''),
                                     ' | Revogado automaticamente pelo EVENT.')
            WHERE id = v_id;
        END;
    END LOOP;

    CLOSE cur;
END //

DELIMITER ;
```

---

## 8. Regras de Segurança Obrigatórias

> Todas as regras abaixo são **obrigatórias** e seguem o que já está implementado no backend Oracle.

1. **Sanitização de Input**:
   - Nunca confiar nos dados recebidos. Usar `tr -cd` ou regex para filtrar caracteres perigosos.
   - No Python, usar `mysql.connector` com **placeholders** (`%s`) — **NUNCA** concatenar strings SQL.

2. **Mínimo Privilégio**:
   - O usuário MySQL `SVC_DBA` deve ter apenas:
     ```sql
     GRANT CREATE USER ON *.* TO 'SVC_DBA'@'localhost';
     GRANT GRANT OPTION ON *.* TO 'SVC_DBA'@'localhost';
     GRANT SELECT, INSERT, UPDATE ON orcale_grant_manager.* TO 'SVC_DBA'@'localhost';
     ```
   - **Nunca** usar `root` ou `SYSTEM` para operações de backend.

3. **Proteção de Credenciais**:
   - Senhas lidas exclusivamente do `.env`.
   - O `.env` deve ter permissão `600` no servidor Linux.
   - **Nunca** hardcoded no código.

4. **Auditoria Obrigatória**:
   - Toda operação de GRANT deve gerar um registro em `grant_control`.
   - Mesmo operações com erro devem ser registradas (com status `ERRO`).
   - Colunas de rastreamento (`cliente_ip`, `maquina`, `user_agent`) sempre preenchidas.

5. **Uso de Transações**:
   - `commit` explícito após GRANT bem-sucedido.
   - `rollback` em caso de erro.
   - A auditoria de erro deve usar transação separada (ou ser inserida antes do rollback).

6. **Tratamento de Erro Robusto**:
   - Todo comando deve validar retorno.
   - Mensagens de erro devem ser descritivas para facilitar debug no frontend.

---

## 9. Como Testar a Integração

### 9.1. Preparação

1. Aplicar a correção no `grant_manager.sh` (linha 72)
2. Criar os scripts Python em `src/backend/`
3. Adicionar uma entrada MySQL no `tns_catalog.conf`:
   ```
   MYSQLDEV|MySQL Lab (DEV)|127.0.0.1:3306/mysql|mysql|DEV
   ```
4. Executar os DDLs no MySQL para criar banco, tabela e event
5. Configurar `.env` com credenciais MySQL

### 9.2. Teste Unitário (via linha de comando)

```bash
# Testar manager
python3 src/backend/mysql_grant_manager.py \
  "TESTE.USER" "SELECT" "mysql.user" "ADMIN" \
  "127.0.0.1" "SRV-DEV" "curl/7.68" \
  "127.0.0.1:3306/mysql"

# Testar reporter
python3 src/backend/mysql_grant_reporter.py \
  "127.0.0.1:3306/mysql"
```

### 9.3. Teste Integrado (via frontend)

1. Acessar `index.cgi`
2. Selecionar SGBD = MySQL, Ambiente = DEV
3. Selecionar o banco cadastrado
4. Preencher formulário e submeter
5. Verificar alerta de sucesso
6. Acessar `audit.cgi`, selecionar o banco MySQL
7. Verificar registro na tabela

---

## Checklist de Verificação

- [ ] Corrigido `grant_manager.sh` linha 72 (remover `$JIRA_TICKET`, adicionar args de rastreamento)
- [ ] `mysql_grant_manager.py` lê 8 args e `.env`
- [ ] `mysql_grant_manager.py` executa GRANT e insere auditoria
- [ ] `mysql_grant_manager.py` retorna output padronizado (sucesso/erro)
- [ ] `mysql_grant_reporter.py` gera HTML no mesmo formato do Oracle
- [ ] DDL MySQL criado em `src/db/CREATE_TABLE_MYSQL_GRANT_CONTROL.sql`
- [ ] Event de revogação criado em `src/db/MYSQL_EVENT_AUTO_REVOKE_GRANTS.sql`
- [ ] Nenhuma senha hardcoded — tudo via `.env`
- [ ] Placeholders `%s` em todas as queries (sem concatenação)
- [ ] Testado manualmente via CLI e via frontend CGI

---

*Skill desenvolvida conforme diretrizes do projeto OGM — Engenharia de Confiabilidade / DBA Sênior*
