# 🛠️ Guia de Instalação - Oracle Grant Manager (OGM)

Este guia descreve os passos necessários para implantar o sistema OGM em um servidor **Oracle Linux 8**.

## 1. Preparação do Banco de Dados

### 1.1. Criação dos Objetos de Controle
Conecte-se como `SYS` ou um usuário com privilégios de DBA e execute os scripts localizados em `src/db/`:

1.  Execute `CREATE_TABLE_SVC_DBA.GRANT_CONTROL.sql` para criar a tabela de auditoria e a sequence.
2.  Execute `SVC_DBA.JOB_AUTO_REVOKE_GRANTS.sql` para configurar o job de revogação automática (DBMS_SCHEDULER).

### 1.2. Usuário de Serviço (`SVC_DBA`)
Certifique-se de que o usuário `SVC_DBA` tenha permissões para:
- Realizar `GRANT` em objetos de outros schemas (concedido via `GRANT ANY OBJECT PRIVILEGE` ou permissões específicas).
- Inserir/Atualizar na tabela `GRANT_CONTROL`.

---

## 2. Configuração do Servidor Web (Apache)

Instale e configure o Apache para suportar a execução de scripts CGI.

```bash
# Instalar Apache
sudo dnf install -y httpd

# Habilitar e Iniciar
sudo systemctl enable --now httpd

# Liberar Firewall (Porta 80)
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --reload

# Configurar SELinux (Permitir conexão ao Banco)
sudo setsebool -P httpd_can_network_connect 1
sudo setsebool -P httpd_can_network_connect_db 1
```

---

## 3. Implantação dos Scripts

### 3.1. Scripts de Backend
Mova os arquivos de `src/backend/` para `/usr/local/bin/` e ajuste as permissões:

```bash
sudo cp src/backend/* /usr/local/bin/
sudo chown root:apache /usr/local/bin/grant_manager.sh
sudo chmod 750 /usr/local/bin/grant_manager.sh
```

### 3.2. Scripts de Frontend (CGI)
Mova os arquivos de `src/frontend/` para `/var/www/cgi-bin/`:

```bash
sudo cp src/frontend/* /var/www/cgi-bin/
sudo chown root:apache /var/www/cgi-bin/*.cgi
sudo chmod 755 /var/www/cgi-bin/*.cgi
```

---

## 4. Configuração de Ambiente (`.env`)

Crie o arquivo `/usr/local/bin/.env` com base no `.env.example`:

```bash
# Configurações do Banco Oracle
DB_USER=SVC_DBA
DB_PASS=sua_senha_segura

# Configurações da API Jira
JIRA_BASE_URL=https://sua-instancia.atlassian.net
JIRA_USER=usuario@empresa.com.br
JIRA_API_TOKEN=seu_token_api
JIRA_APPROVAL_FIELD=customfield_10100
JIRA_EXPECTED_APPROVAL_VALUE=Aprovado
```

---

## 5. Teste da Aplicação

1. Acesse: `http://<IP-DO-SERVIDOR>/cgi-bin/index.cgi`.
2. Tente realizar um grant para um usuário de teste.
3. Verifique o resultado na tela e na aba "Ver Auditoria" (`audit.cgi`).

> [!CAUTION]
> **Segurança**: Nunca deixe as permissões dos scripts de backend abertas (`777`). O usuário do Apache (`apache`) deve ser o único (além do root) capaz de executar o `grant_manager.sh`.
