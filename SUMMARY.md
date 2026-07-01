# 📋 SUMMARY — Oracle Grant Manager (OGM)

**Stack:** Bash CGI + Bootstrap 5.3 + Python 3 + Oracle 19c  
**Versão Atual:** `v2.5.0`  
**Padrão:** Keep a Changelog + Semantic Versioning

---

## 🧭 Navegação Rápida

| Se você quer... | Leia este arquivo |
|---|---|
| Entender visão geral do projeto | `README.md` |
| Saber o que cada arquivo faz | `FILE_MAP.md` |
| Regras imutáveis do projeto | `skills.md` |
| Skills de Frontend (UI/UX, Dark Mode) | `skills/frontend.md` |
| Skills de Backend (Shell, Python, sanitização) | `skills/backend.md` |
| Skills de Database (Oracle, DDL, segurança) | `skills/database.md` |
| Ver histórico de versões | `CHANGELOG.md` |
| Instalar o sistema | `docs/installation.md` |

---

## 📂 Árvore de Diretórios (Descritiva)

```
/
├── skills.md                  # Constituição global do projeto
├── skills/                    # Skills granulares por domínio
│   ├── frontend.md            #   Design system, UI/UX, Bootstrap 5
│   ├── backend.md             #   Shell/Python, sanitização, segurança
│   └── database.md            #   Oracle DDL, DBMS_ASSERT, jobs
├── SUMMARY.md                 # ← você está aqui
├── CHANGELOG.md               # Histórico de versões (Keep a Changelog)
├── FILE_MAP.md                # Mapa detalhado de cada arquivo
├── README.md                  # Documentação principal com arquitetura
├── .gitignore
├── docker-compose.yml         # Orquestração Docker
├── Dockerfile                 # Build da imagem (Oracle Linux 8)
├── deploy_OGM.sh              # Deploy automatizado
│
├── src/
│   ├── frontend/              # CGIs da interface web
│   │   ├── index.cgi          #   Formulário de solicitação de grants
│   │   └── audit.cgi          #   Painel de auditoria com DataTables
│   ├── backend/               # Motor de processamento
│   │   ├── grant_manager.sh   #   Core: executa o grant via sqlplus
│   │   ├── grant_reporter.sh  #   Relatórios de auditoria
│   │   ├── jira_validator.py  #   Validação de tickets Jira
│   │   ├── tns_catalog.conf   #   Catálogo de bancos (multi-instância)
│   │   └── .env.example       #   Template de credenciais
│   └── db/                    # DDLs do Oracle
│       ├── CREATE_TABLE_SVC_DBA.GRANT_CONTROL.sql
│       └── SVC_DBA.JOB_AUTO_REVOKE_GRANTS.sql
│
├── docs/
│   ├── installation.md        # Manual de instalação para SRE
│   └── prompt_grant_manager.md
│
└── _old/                      # Arquivos legados (não modificar)
```

---

## 🔒 Regras de Ouro (Extraídas das Skills)

1. **Dark Mode obrigatório** — toda página com `data-bs-theme="dark"` e paleta `#121212`/`#1e1e1e`
2. **Sanitização total** — todo input de usuário passa por `tr -cd` antes do Shell ou sqlplus
3. **DBMS_ASSERT** — nomes de objetos Oracle SEMPRE validados com `DBMS_ASSERT.SQL_OBJECT_NAME`
4. **Mínimo Privilégio** — `SVC_DBA` nunca tem `DBA` role
5. **Bootstrap 5 exclusivo** — sem Tailwind, sem Material UI, sem frameworks extras
6. **Versão no Footer** — todo bump de versão atualiza `index.cgi` e `audit.cgi`
7. **Keep a Changelog** — toda alteração concluída gera entrada no `CHANGELOG.md`
8. **Confirmação de Git** — ao final de cada alteração, perguntar ao usuário se deseja commitar antes de prosseguir
9. **Idioma pt-BR** — comentários no código e mensagens de commit sempre em Português (Brasil)

---

> 📌 *Este arquivo é o ponto de partida para qualquer agente (IA ou humano) que precise entender o projeto rapidamente.*
