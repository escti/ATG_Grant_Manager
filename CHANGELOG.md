# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v1.2.0] - 2026-04-13
### Added
- **Documentação Premium**: README.md reformulado com arquitetura em Mermaid e design visual melhorado.
- **Manual de Instalação**: Novo `docs/installation.md` substituindo o script de passos legados.
- **Template de Ambiente**: Adição do `.env.example` para facilitar a configuração segura de novos ambientes.
- **Skills do Agente**: `skills.md` atualizado com diretrizes de SRE/DBA Sênior e fluxos de segurança.

### Changed
- **Reorganização de Repositório**: Arquivos redundantes e scripts de instalação legados movidos para a pasta `_old/`.
- **Padronização de Idioma**: Toda a documentação técnica foi ajustada para Português (Brasil).

## [v1.1.0] - 2026-04-13
### Added
- **Multi-Banco (TNS)**: Seletor amigável de Catálogo de Redes (`tns_catalog.conf`).
- **Jira Gateway**: Adição do validador integrado da API Jira em Python pre-transação.
- **Formulários Refatorados**: Inputs com validação do Jira, Banners e Dropdowns.
- **Rodapés de UI** refletindo `v1.1.0`.

## [v1.0.0] - 2026-04-12
### Added
- Infraestrutura inicial estruturada com divisões de pastas (`src/frontend/`, `src/backend/`, `src/db/`).
- Documentações consolidadas (`README.md`, `skills.md`).
- Scripts Shell (backend): `grant_manager.sh`, `grant_reporter.sh`.
- CGIs UI (frontend): `index.cgi`, `audit.cgi`.
- Modelos DDL (banco): `CREATE_TABLE_SVC_DBA.GRANT_CONTROL.sql` e Job automatizado de expurgo.
- Implementação inicial de rodapés globais com captura dinâmica de versão.
