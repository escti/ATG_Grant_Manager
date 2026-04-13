# Oracle Grant Manager (OGM)

## Visão Geral
O Oracle Grant Manager é um sistema desenvolvido para automatizar de forma segura o processo de concessão de acessos em tabelas ou views para usuários nominais no Oracle, voltado diretamente para o usuário final (e não apenas para DBAs). Ele garante segurança corporativa ao conceder acessos temporários que são revogados automaticamente após 15 dias.

## Componentes da Solução
A arquitetura é leve e foi concebida nas seguintes camadas:
1. **Frontend (Interface Web)**: Scripts CGI (`index.cgi`, `audit.cgi`) utilizando HTML limpo com Bootstrap Dark Mode para prover uma interface amigável.
2. **Backend (Shell Script)**: Scripts em Bash instalados no servidor Linux (`grant_manager.sh`, `grant_reporter.sh`) responsáveis por se comunicarem usando SqlPlus com o banco Oracle para executar Grants e Consultas de auditoria.
3. **Banco de Dados (Oracle)**: Objetos DDL incluindo a tabela de controle de grants (`SVC_DBA.GRANT_CONTROL`) e um Job nativo (`DBMS_SCHEDULER`) para revogar (`REVOKE`) os grants expirados diariamente.

## Estrutura do Repositório
Para manter as melhores práticas e separar as camadas da aplicação, o repositório está subdividido em:
- `src/frontend/`: Componentes visíveis (HTML/CSS gerado via scripts CGI).
- `src/backend/`: Rotinas Shell com a lógica "oculta" do Grant e Report.
- `src/db/`: Scripts DDL para criar usuários, tabelas, sequences e schedulers no banco Oracle.
- `docs/`: Documentações de passos de instalação e documentação original.
- `_old/`: Arquivos redundantes gerados durante testes e prototipagem.

## Fluxo Operacional
1. O usuário (solicitante) acessa a interface web.
2. Preenche os dados de usuário alvo, privilégio (SELECT, INSERT, UPDATE, DELETE) e objeto desejado.
3. O Backend recebe requisição POST e envia de forma segura o comando de `GRANT` para o banco de dados Oracle.
4. O resultado vira um registro de auditoria, contendo uma data calculada de +15 dias a frente.
5. Em D+15, o Job do banco de dados, configurado na madrugada, varre a tabela e revoga automaticamente as permissões vencidas.