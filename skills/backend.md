---
name: backend
description: Regras de Shell Script, Python e Segurança no Backend do OGM
---

# ⚙️ Skill: Backend (Shell + Python)

## Shell Script (Bash CGI e Automação)

### Sanitização de Input (IMPERATIVO)
- **Sempre** sanitizar com `tr -cd` antes de usar qualquer variável em comandos:
  - `[:alnum:]_` para usuários, grantors, db_ids
  - `[:alnum:]_$.` para objetos
  - `[:alpha:]` para privilégios

- **Nunca** usar `eval` com dados do usuário (exceto no pattern `eval $(echo "$POST_DATA" | awk ...)` que é o padrão aceito para parse de POST em CGI)
- Nunca passar strings não sanitizadas para sqlplus

### Tratamento de Erro
- Verificar `$?` após cada comando crítico (sqlplus, python, curl)
- `set -e` é opcional — prefira validação explícita com `if [ $? -eq 0 ]`
- Mensagens de erro devem ser capturadas (`2>&1`) e retornadas ao usuário via alerta HTML

### Paths e Dependências
- Usar caminhos absolutos para binários: `/usr/bin/sqlplus`, `/usr/bin/python3`, `/usr/bin/curl`
- Arquivos de configuração (`.conf`, `.env`) em `/usr/local/bin/`
- Fallback para caminho relativo `$(dirname "$0")/../backend/` quando executado em ambiente de desenvolvimento

### CGI Conventions
- `echo "Content-type: text/html"` + linha vazia antes do HTML
- Usar `cat <<EOF` para renderizar HTML (não concatenar strings)
- Variáveis PHP-like: `$VAR` dentro de heredoc, escapar `$` literal como `\$`

### urldecode
- Usar a função `urldecode()` padrão:
  ```bash
  urldecode() { : "${*//+/ }"; echo -e "${_//%/\\x}"; }
  ```

## Python (Scripts de Banco)

### Estrutura
- Scripts independentes para cada SGBD (ex: `mysql_grant_manager.py`, `mysql_grant_reporter.py`)
- Dependências mínimas: `python-dotenv` para carregar `.env`, conector específico do SGBD (`mysql-connector-python`)
- Usar `os.getenv()` ou `dotenv.load_dotenv()` para credenciais
- Retornar strings simples para o shell (não JSON complexo)
- `sys.exit(0)` para sucesso, `sys.exit(1)` para erro

### Segurança
- Nunca logar tokens ou senhas
- Usar `.env` carregado via `python-dotenv` (arquivo com permissão 600)
- Usar **placeholders** (`%s`) em todas as queries — nunca concatenar strings SQL
- Fechar conexões (`conn.close()`) em blocos `finally` ou usar context managers

## Gerais do Backend

### Tratamento de Config
- `tns_catalog.conf`: formato `ID|LABEL|CONEXÃO|TIPO_DB|AMBIENTE`, linhas com `#` são comentários (ex: `OGMLAB|Laboratório (OGMLAB)|(DESCRIPTION=...)|oracle|DEV`)
- Sempre verificar se o arquivo de catálogo existe antes de ler
- Fallback: `/usr/local/bin/tns_catalog.conf` → `./src/backend/tns_catalog.conf`

### Regras de Versionamento
- A versão no backend não precisa ser refletida (é o frontend que exibe)
- Mas os scripts não devem conter strings de versão hardcoded (para evitar duplicidade)
