# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v2.0.5] - 2026-04-20
### Fixed
- **Conflito de Pacotes DNF**: Removido o uso de curingas (`*`) na instalação do Oracle Instant Client que forçava o `dnf` a baixar todas as versões históricas (19.10, 19.19, 19.28) simultaneamente e gerar conflito de dependência (`libclntsh.so`). A versão foi fixada para a mais recente e estável do repositório (`19.28-basic`).

## [v2.0.4] - 2026-04-20
### Fixed
- **Nomenclatura de Pacotes ARM**: Ajustada a diretiva de instalação do `dnf` no Dockerfile para utilizar curingas (`oracle-instantclient*-basic`), resolvendo o erro `No match for argument` causado pela presença da numeração de versão (ex: `19.19`) nos nomes dos pacotes do repositório OCI/ARM.

## [v2.0.3] - 2026-04-20
### Fixed
- **Resolução de Repositório OCI**: Resolvido o erro de `404 Not Found` injetando diretamente o arquivo `.repo` oficial (`ol8_oracle_instantclient`) com a variável `$basearch` no Dockerfile, contornando a indisponibilidade ou mudança de caminhos dos pacotes de release em imagens mínimas da Oracle.

## [v2.0.2] - 2026-04-20
### Fixed
- **Estabilidade de Build**: Alterada a lógica de instalação do Oracle Instant Client para download direto via RPM por arquitetura (`arch`), eliminando dependência de busca de nomes de repositórios que variavam entre OCI e ambientes locais.

## [v2.0.1] - 2026-04-20
### Fixed
- **Deploy OCI/ARM**: Ajustada a instalação do Oracle Instant Client no Dockerfile para utilizar o repositório de desenvolvedor, resolvendo falhas de build em instâncias ARM da OCI.
- **Cleanup de Configuração**: Removido aviso de "version is obsolete" no `docker-compose.yml`.

## [v2.0.0] - 2026-04-20
### Added
- **Arquitetura Docker**: Suporte nativo para conteinerização via Docker Compose em servidores Oracle Linux 8 (ARM).
- **Deploy Automatizado**: Novo script `deploy.sh` que faz pull direto do GitHub e provisiona a infraestrutura.

### Changed
- **Ajuste Híbrido no Backend**: Scripts `grant_manager.sh` e `grant_reporter.sh` atualizados para reconhecer dinamicamente instalações do Oracle Instant Client em contêineres e manter compatibilidade com instalações Bare Metal legado.

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
