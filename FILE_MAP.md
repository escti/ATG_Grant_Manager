# 🗺️ Mapa de Arquivos do Projeto OGM (Oracle Grant Manager)

Este documento foi criado para servir como um mapa rápido e eficiente do repositório, permitindo que a IA (ou um novo desenvolvedor) entenda rapidamente a arquitetura, as regras do projeto e a função de cada arquivo sem precisar ler o conteúdo de todos eles, economizando tempo e tokens.

## 🧠 Regras do Projeto (Extraídas de `skills.md`)

Qualquer modificação neste projeto deve seguir rigorosamente as diretrizes do arquivo `skills.md`.

---

## 📂 Mapeamento de Arquivos Essenciais

Abaixo estão descritos todos os arquivos que **realmente importam** para o funcionamento e desenvolvimento do projeto, divididos por camada de arquitetura.

### 📌 Raiz do Repositório
*   `README.md`: Documentação principal. Explica a arquitetura, fluxo (Frontend -> Jira -> Backend -> Oracle) e requisitos gerais.
*   `skills.md`: O "cérebro" das diretrizes do projeto.
*   `CHANGELOG.md`: Histórico de versões (usando o padrão *Keep a Changelog*).
*   `.gitignore`: Arquivos ignorados pelo Git (importante manter o `.env` aqui).

### 🖥️ Frontend Web (`src/frontend/`)
Contém scripts CGI que geram a interface HTML com Bootstrap 5 (Dark Mode).
*   `index.cgi`: A interface principal de "autoatendimento" onde os usuários preenchem o form solicitando grant, validado contra um ticket do Jira.
*   `audit.cgi`: Painel de auditoria visual onde os administradores ou usuários podem ver o histórico de grants concedidos e revogados.

### ⚙️ Backend (Motor Shell/Python) (`src/backend/`)
Processa requisições do frontend, valida tickets e dispara comandos pro banco.
*   `grant_manager.sh`: O script core em shell. Pega a requisição, valida, sanitiza e chama o SQLPlus.
*   `grant_reporter.sh`: Script auxiliar para gerar relatórios de grants/auditoria.
*   `jira_validator.py`: Script Python chamado pelo bash para se comunicar via API com o Jira e confirmar se o ticket do solicitante é válido e está aprovado.
*   `tns_catalog.conf`: Configuração com os apontamentos de banco (TNS) para a aplicação ser multi-instância.
*   `.env` / `.env.example`: Arquivo (e seu template) que guarda as senhas sensíveis (Jira Token, Senha Banco, etc).

### 🗄️ Banco de Dados Oracle (`src/db/`)
Objetos que devem ser criados dentro do Oracle (no schema `SVC_DBA`).
*   `CREATE_TABLE_SVC_DBA.GRANT_CONTROL.sql`: DDL da tabela de auditoria que registra quem ganhou o grant e quando.
*   `SVC_DBA.JOB_AUTO_REVOKE_GRANTS.sql`: DDL do *Job Scheduler* nativo do Oracle que roda periodicamente para revogar acessos com mais de 15 dias.

### 📖 Documentação Adicional (`docs/`)
*   `installation.md`: Passo a passo para o SRE/Sysadmin subir o ambiente (Apache, Oracle Client, Python, etc).
*   `prompt_grant_manager.md`: Histórico/prompt descritivo do sistema.
