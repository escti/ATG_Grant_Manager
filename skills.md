---
name: skills
description: Constituição do projeto OGM — regras imutáveis, fluxo de versão, gerenciamento de arquivos e índice de skills granulares
---

# 🧠 Skills & Diretrizes do Projeto OGM

Este documento é a **constituição** do projeto. Define as regras fundamentais e imutáveis. Para detalhes técnicos específicos, consulte as skills granulares em [`skills/`](skills/).

---

## 1. Princípios de Segurança (Core)

- **Sanitização de Input**: Toda entrada do usuário deve ser sanitizada. Consulte [`skills/backend.md`](skills/backend.md) para regras detalhadas de `tr -cd` e [`skills/database.md`](skills/database.md) para `DBMS_ASSERT` no Oracle.
- **Mínimo Privilégio**: Nunca use `SYS` ou `SYSTEM`. Use um usuário de serviço (`SVC_DBA`) com privilégios restritos.
- **Proteção de Credenciais**: Senhas apenas via `.env` com permissão `600`. Nunca no código.

## 2. Padrões de Código

- **Shell Script**: Caminhos absolutos para binários, validação explícita de `$?`, tratamento de erro sem `set -e`. Detalhes em [`skills/backend.md`](skills/backend.md).
- **CGI & Frontend**: Tabler (Bootstrap 5) com dark mode (`#0f1117`, `#1c1e2a`). Validação de estado antes de exibir formulários. Design system completo em [`skills/frontend.md`](skills/frontend.md).
- **Python**: Placeholders (`%s`) em queries, `python-dotenv` para configuração, conexões fechadas em `finally`. Detalhes em [`skills/backend.md`](skills/backend.md).
- **Banco de Dados**: `DBMS_ASSERT` no Oracle, tabela `GRANT_CONTROL` com colunas de rastreamento, job `DBMS_SCHEDULER` para revogação. Especificações DDL em [`skills/database.md`](skills/database.md).

## 3. Fluxo de Versão e CHANGELOG

Seguimos **Keep a Changelog** e **Semantic Versioning**:
- **PATCH (0.0.x)**: Correções de bugs, CSS, textos.
- **MINOR (0.x.0)**: Novas funcionalidades sem quebra de interface.
- **MAJOR (x.0.0)**: Mudanças arquiteturais, troca de framework.

> Toda alteração DEVE ter entrada no `CHANGELOG.md` e, se houver impacto visual, a versão no rodapé do `index.cgi` deve ser atualizada.

## 4. Gerenciamento de Arquivos

- Arquivos redundantes ou protótipos → mover para `_old/`.
- `docs/` → apenas documentação em Markdown.
- Scripts de instalação legados → converter para Markdown ou mover para `_old/`.

## 5. Workflow de Alterações

- **Commits**: Sempre perguntar "Deseja salvar as alterações no Git?" antes de commitar. Após o commit, perguntar "Deseja fazer push?".
- **Idioma**: Todo comentário técnico (Shell, Python, SQL, HTML, CSS) e toda mensagem de commit em **Português (Brasil)**. Sem inglês.

## 6. Índice de Skills Granulares

| Skill | Descrição |
|-------|-----------|
| [`skills/frontend.md`](skills/frontend.md) | Design System, paleta de cores, tipografia, dark mode, responsividade, componentes Bootstrap 5 |
| [`skills/backend.md`](skills/backend.md) | Shell Script (sanitização, CGI, paths), Python (scripts de banco, placeholders, dotenv) |
| [`skills/database.md`](skills/database.md) | DDL Oracle, DBMS_ASSERT, tabela GRANT_CONTROL, job de revogação automática |
| [`skills/mysql_backend.md`](skills/mysql_backend.md) | Implementação MySQL: scripts Python, DDLs MySQL, Event Scheduler, contrato de interface |

---

*Assuma a postura de um Engenheiro de Confiabilidade (SRE) / DBA Sênior ao interagir com este código.*
