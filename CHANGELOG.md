# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v2.2.0] - 2026-06-30
### Added
- **Suporte Multi-SGBD**: Catálogo `tns_catalog.conf` agora possui 4º campo `dbtype` (oracle | mysql), preparando a infraestrutura para MySQL.
- **Roteamento MySQL**: `grant_manager.sh` e `grant_reporter.sh` agora detectam o tipo do banco e encaminham a requisição para scripts Python específicos (`mysql_grant_manager.py` / `mysql_grant_reporter.py`) quando `dbtype=mysql`.
- **Placeholders MySQL**: Criados `mysql_grant_manager.py` e `mysql_grant_reporter.py` (stubs) com a interface (contrato) documentada para o colega implementar a lógica real.
- **Nova Interface de Privilégios**: Dropdown unificado para Oracle e MySQL com opções `CONSULTA` (SELECT), `EDIÇÃO` (INSERT, UPDATE, DELETE) e `AMBAS` (SELECT, INSERT, UPDATE, DELETE).
- **Dependência Docker**: Instalação do pacote `mysql-connector-python` no `pip3` do Dockerfile.
- **Config MySQL**: Adicionada seção de configuração MySQL no `.env.example`.

### Changed
- **Deploy Script**: Renomeado `deploy.sh` → `deploy_OGM.sh` para melhor identificação do projeto.
- **Parser do Catálogo**: `index.cgi` e `audit.cgi` atualizados para ler 4 campos do `tns_catalog.conf` (compatível retroativo — 4º campo opcional, default `oracle`).

## [v2.1.0] - 2026-06-23
### Added
- **Skills Granulares**: Criado diretório `skills/` com três skills especializadas (`frontend.md`, `backend.md`, `database.md`) cada uma com frontmatter YAML, design system, regras imutáveis e checklist de verificação.
- **SUMMARY.md**: Novo arquivo curado na raiz do projeto com árvore de diretórios descritiva, tabela de navegação rápida e regras de ouro, permitindo que qualquer agente entenda o projeto lendo um único arquivo.
- **Frontmatter YAML**: Skills agora possuem metadados estruturados (`name` e `description`) para parse automatizado.

### Changed
- **skills.md**: Mantido como "Constituição" global do projeto, com as skills granulares atuando como extensões especializadas.
- **Footer**: Versão atualizada para `v2.1.0` nos CGIs (`index.cgi`, `audit.cgi`).

## [v2.0.6] - 2026-04-20
### Changed
- **Porta de Deploy**: Alterada a porta padrão de exposição do host de `80` para `8080` no `docker-compose.yml` para evitar conflitos com serviços de servidor web nativos (HTTPD/NGINX) já existentes no servidor de produção.

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
