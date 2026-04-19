# 🧠 Skills & Diretrizes do Projeto OGM

Este documento define as "skills" fundamentais e as boas práticas que devem ser seguidas por qualquer agente (humano ou IA) ao modificar este repositório.

## 1. Princípios de Segurança (Core)

- **Sanitização de Input**: Toda entrada de usuário em scripts CGI deve ser sanitizada para remover caracteres perigosos antes de ser passada para o Shell ou SQL (`tr`, `sed`, regex).
- **DBMS_ASSERT**: No banco de dados, utilize obrigatoriamente `DBMS_ASSERT.SQL_OBJECT_NAME` e `DBMS_ASSERT.ENQUOTE_NAME` para prevenir SQL Injection.
- **Mínimo Privilégio**: Nunca use o usuário `SYS` ou `SYSTEM` para operações de backend. Use um usuário de serviço (`SVC_DBA`) com privilégios restritos.
- **Proteção de Credenciais**: Senhas nunca devem estar no código. Use variáveis de ambiente via `.env` e garanta que o arquivo tenha permissões `600`.

## 2. Padrões de Código e UI

- **Shell Script**:
    - Use caminhos absolutos para binários (`/usr/bin/sqlplus`, `/usr/bin/python3`).
    - Sempre valide o código de retorno (`$?`) de comandos críticos.
    - Utilize `set -e` apenas se necessário, prefira tratamento de erro explícito.
- **CGI & Frontend**:
    - Utilize Bootstrap 5 (CDN) para garantir responsividade.
    - Mantenha o **Dark Mode** como padrão (palette: `#121212`, `#1e1e1e`).
    - Valide o estado do banco antes de exibir formulários (ex: verificar se o catálogo TNS está acessível).

## 3. Fluxo de Versão e CHANGELOG

Seguimos rigorosamente o **Keep a Changelog** e **Semantic Versioning**:

1.  **PATCH (0.0.x)**: Pequenas correções de bugs, ajustes de CSS ou textos.
2.  **MINOR (0.x.0)**: Novas funcionalidades que não quebram a interface (ex: novo filtro, novo banco no catálogo).
3.  **MAJOR (x.0.0)**: Mudanças arquiteturais, troca de framework ou alteração completa de fluxo.

> [!IMPORTANT]
> Toda alteração concluída DEVE ser acompanhada de uma entrada no `CHANGELOG.md` e, se houver impacto visual, a versão no rodapé da interface (`index.cgi`) deve ser atualizada.

## 4. Gerenciamento de Arquivos

- Arquivos redundantes, protótipos ou scripts de "apoio" que não fazem parte do core devem ser movidos para a pasta `_old/`.
- A pasta `docs/` deve conter apenas documentação em Markdown. Scripts de instalação legados devem ser limpos ou convertidos.

---
*Assuma a postura de um Engenheiro de Confiabilidade (SRE) / DBA Sênior ao interagir com este código.*
