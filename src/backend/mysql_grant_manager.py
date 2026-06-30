#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Placeholder — Aguardando implementação do colega.
# Interface esperada:
#   python3 mysql_grant_manager.py <USUARIO> <PRIVILEGIO> <OBJETO> <GRANTOR> <JIRA_TICKET> <DB_CONN_STR>
#
# Onde:
#   PRIVILEGIO   = "SELECT" | "INSERT, UPDATE, DELETE" | "SELECT, INSERT, UPDATE, DELETE"
#   DB_CONN_STR  = string de conexao MySQL (ex: host:porta/banco)
#
# Saida (stdout):
#   Sucesso → "Grant aplicado com sucesso em <OBJETO> para <USUARIO>."  + exit 0
#   Erro    → "ERRO: <mensagem>"                                         + exit 1

import sys


def main():
    if len(sys.argv) < 7:
        print("Uso: mysql_grant_manager.py <USUARIO> <PRIVILEGIO> <OBJETO> <GRANTOR> <JIRA_TICKET> <DB_CONN_STR>")
        sys.exit(1)

    usuario = sys.argv[1]
    privilegio = sys.argv[2]
    objeto = sys.argv[3]
    grantor = sys.argv[4]
    jira_ticket = sys.argv[5]
    db_conn_str = sys.argv[6]

    # ──────────────────────────────────────────────────────────────
    # TODO: Implementar conexao MySQL e execucao do GRANT
    # 1. Conectar ao MySQL usando mysql-connector-python
    # 2. Validar se usuario/objeto existem
    # 3. Executar: GRANT <privilegio> ON <objeto> TO <usuario>
    # 4. Inserir registro na tabela de auditoria
    # 5. Retornar saida padronizada
    # ──────────────────────────────────────────────────────────────

    print(f"ATENCAO: mysql_grant_manager.py ainda nao implementado. "
          f"Dados recebidos — usuario={usuario}, privilegio={privilegio}, "
          f"objeto={objeto}, grantor={grantor}, ticket={jira_ticket}, "
          f"conn={db_conn_str}")
    sys.exit(0)


if __name__ == "__main__":
    main()
