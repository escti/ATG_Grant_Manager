Crie o escopo completo, a DDL da tabela de controle e o script shell para um sistema de gerenciamento de grants temporários no Oracle, com as seguintes especificações:

**1. Escopo do Projeto:**
* O sistema deve ser implementado em **shell script (Oracle Linux 8)**.
* O objetivo é conceder privilégios temporários no Oracle e realizar o **revoke automático após 15 dias**.
* Todas as operações (grant/revoke) devem ser registradas e auditadas em uma tabela de controle chamada **SVC\_DBA.GRANT\_CONTROL**.

**2. DDL da Tabela SVC\_DBA.GRANT\_CONTROL:**
* Crie a DDL completa para esta tabela, incluindo a coluna `DATA_EXPIRACAO` calculada para 15 dias.

**3. Script Shell (`grant_manager.sh`):**
* O script deve realizar a concessão de grants e a inserção do registro na tabela de controle.
* **Credenciais Fixas (Hardcoded):**
    * `DB_USER` = `SVC_DBA`
    * `DB_PASS` = `svcpasswd`
    * `DB_TNS` = `DELTA1`
* **Variáveis Solicitadas ao Usuário:**
    * `USUARIO_GRANTED` (Usuário ou Role que recebe o grant)
    * `PRIVILEGIO`
    * `OBJETO` (Obrigatório, no formato `SCHEMA.TABELA/VIEW`)
    * `GRANTOR` (Quem executa o script)
* **Validação de Grants:**
    * Apenas os privilégios `SELECT`, `INSERT`, `DELETE` e `UPDATE` são permitidos.
    * É obrigatório que o usuário especifique o SCHEMA e a TABELA/VIEW no campo `OBJETO` (validar formato `SCHEMA.OBJETO`).
* **Lógica de Execução:**
    * O script deve gerar os comandos `GRANT` e `INSERT` em memória.
    * O comando `GRANT` deve ser executado via `sqlplus` com as credenciais fixas.
    * Após a execução do `GRANT`, o status e as observações (incluindo qualquer erro do banco de dados) devem ser inseridos na tabela `SVC_DBA.GRANT_CONTROL`.
    * Em caso de erro no `GRANT`, o status na tabela deve ser `ERRO` e a mensagem de erro registrada na coluna `OBSERVACOES`.

Gere o escopo em html, a DDL em SQL e o script em Shell.