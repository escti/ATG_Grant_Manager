-- ==============================================================================
-- Migration v2.5.0 — Adicionar colunas de auditoria de origem (cliente)
-- ==============================================================================
-- Objetivo: Rastrear IP, nome da maquina e User-Agent do solicitante
-- ==============================================================================

ALTER TABLE SVC_DBA.GRANT_CONTROL ADD (
    CLIENTE_IP     VARCHAR2(45),   -- IP do cliente (REMOTE_ADDR)
    MAQUINA        VARCHAR2(128),  -- Nome da maquina (reverse DNS)
    USER_AGENT     VARCHAR2(512)   -- User-Agent do navegador
);

COMMIT;

-- Colunas sao opcionais (NULL OK) para manter compatibilidade com registros existentes
COMMENT ON COLUMN SVC_DBA.GRANT_CONTROL.CLIENTE_IP IS 'Endereco IP do cliente que solicitou o grant';
COMMENT ON COLUMN SVC_DBA.GRANT_CONTROL.MAQUINA IS 'Nome resolvido da maquina via reverse DNS';
COMMENT ON COLUMN SVC_DBA.GRANT_CONTROL.USER_AGENT IS 'User-Agent do navegador do solicitante';
