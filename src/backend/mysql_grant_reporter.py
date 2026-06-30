#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Placeholder — Aguardando implementação do colega.
# Interface esperada:
#   python3 mysql_grant_reporter.py <DB_CONN_STR>
#
# Saida (stdout):
#   Linhas <tr> HTML com dados de auditoria (mesmo formato do grant_reporter.sh)
#   Exemplo: <tr><td>1</td><td><strong>MARIA.SOUZA</strong></td>...

import sys


def main():
    if len(sys.argv) < 2:
        print("<tr><td colspan='9' class='text-center py-4 text-muted'>"
              "Uso: mysql_grant_reporter.py <DB_CONN_STR></td></tr>")
        sys.exit(1)

    db_conn_str = sys.argv[1]

    # ──────────────────────────────────────────────────────────────
    # TODO: Implementar consulta MySQL e geracao de linhas HTML
    # 1. Conectar ao MySQL usando mysql-connector-python
    # 2. SELECT * FROM tabela_auditoria ORDER BY id DESC
    # 3. Para cada linha, gerar: <tr><td>ID</td><td>USUARIO</td>...
    # 4. Retornar as linhas concatenadas no stdout
    # ──────────────────────────────────────────────────────────────

    print(f"<tr><td colspan='9' class='text-center py-4 text-warning'>"
          f"mysql_grant_reporter.py ainda nao implementado. "
          f"conn={db_conn_str}</td></tr>")
    sys.exit(0)


if __name__ == "__main__":
    main()
