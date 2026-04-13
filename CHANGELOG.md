# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v1.1.0] - $(date +%Y-%m-%d)
### Added
- **Multi-Banco (TNS)**: Seletor amigável de Catálogo de Redes (`tns_catalog.conf`).
- **Jira Gateway**: Adição do validador integrado da API Jira em Python pre-transação.
- **Formulários Refatorados**: Inputs com validação do Jira, Banners e Dropdowns.
- **Rodapés de UI** refletindo \`v1.1.0\`.

## [v1.0.0] - 2026-04-13
### Added
- Infraestrutura inicial estruturada com divisões de pastas (`src/frontend/`, `src/backend/`, `src/db/`).
- Documentações consolidadas (`README.md`, `skills.md`).
- Scripts Shell (backend): `grant_manager.sh`, `grant_reporter.sh`.
- CGIs UI (frontend): `index.cgi`, `audit.cgi`.
- Modelos DDL (banco): `CREATE_TABLE_SVC_DBA.GRANT_CONTROL.sql` e Job automatizado de expurgo.
- Implementação inicial de rodapés globais com captura dinâmica de versão.
