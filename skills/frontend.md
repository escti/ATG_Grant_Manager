---
name: frontend
description: Regras de UI/UX, Design System e Padrões de Frontend para CGIs Bootstrap 5
---

# 🖥️ Skill: Frontend (CGI + Bootstrap 5)

## Design System

### Paleta de Cores (Imutável) — Tema Tabler Dark Mode
| Token | Hex | Uso |
|---|---|---|
| `bg-body` | `#0f1117` | Fundo da página (`body`, `.page`) |
| `bg-card` | `#1c1e2a` | Cards, tabelas, containers, stat-cards |
| `bg-sidebar` | `#15171e` | Barra lateral (`navbar-vertical`) |
| `bg-input` | `#252836` | Inputs, selects, textareas, filtros DataTables |
| `border-default` | `#2a2d3a` | Bordas de cards, sidebar, footer, cabeçalho de tabela, divisores |
| `border-input` | `#33364a` | Bordas de inputs e selects |
| `text-body` | `#e6e7ed` | Corpo do texto, títulos (`page-title`) |
| `text-muted` | `#8b8fa3` | Labels, subtítulos, textos secundários, badges-soft-secondary |
| `text-label` | `#a0a4b8` | Labels de formulário (`form-label`) |
| `brand-start` | `#1a5fb4` | Tom inicial do gradiente do botão primário e sidebar ativo |
| `brand-end` | `#3584e4` | Tom final do gradiente do botão primário, sidebar ativo, links |
| `badge-success` | `#2ed573` | Badge e alerta de sucesso |
| `badge-danger` | `#ff4757` | Badge e alerta de erro |
| `badge-warning` | `#ffb74d` | Badge de aviso |
| `badge-info` | `#62a0ea` | Badge de informação e versão |
| `stat-value` | `#ffffff` | Valor numérico nos cards de estatística |

**Proibido:** Usar cores legadas (ex: azul claro #00f, verde limão, vermelho sem contexto Bootstrap).

### Tipografia
- Família: `'Segoe UI', Tahoma, sans-serif`
- Tamanhos: `0.85rem` para `text-xs`, `1rem` para corpo
- Pesos: `700` para títulos (`header-title`), `600` para botões

### Dark Mode (Obrigatório)
- Atributo `<html data-bs-theme="dark">`
- Toda nova página DEVE iniciar com `data-bs-theme="dark"`
- Cards com borda `1px solid #2a2d3a` e `border-radius: 12px` (sem box-shadow)

### Responsividade (Mobile-First)
- Container centralizado: `container d-flex justify-content-center align-items-center min-vh-100`
- Formulários em grid: `col-md-8 col-lg-6` para largura máxima controlada
- Inputs empilhados em mobile (`col-md-6` vira largura total)
- Tabelas sempre em `table-responsive` para scroll horizontal em viewports pequenas
- Select de banco + botão "Conceder Permissões" no audit devem quebrar para coluna em mobile (usar `flex-wrap` ou `d-flex flex-column flex-md-row`)

## Padrões de Código

### Estrutura do HTML
1. `<!DOCTYPE html>` + `<html data-bs-theme="dark">`
2. `<meta charset="UTF-8">` + `<meta name="viewport">`
3. CSS inline para Dark Mode (evitar carregamento extra)
4. **Tabler** via CDN (`@tabler/core@1.4.0`) + Bootstrap Icons + DataTables (no audit)
5. Formulários com `method="POST"` em `index.cgi`, `method="GET"` em `audit.cgi`
6. Sanitização via `tr -cd` antes de qualquer output

### Footer (Versão)
- Elemento `<footer class="footer">` fora do card, no final da `.page-wrapper`
- Conteúdo: `&copy; {ano} DBA Team &mdash; Seguranca &amp; Auditoria`
- Versão em `<span class="badge-soft-info px-2">v{semver}</span>` ao lado direito
- No audit.cgi, incluir também "Atualizado em: {data}" antes da versão

### Regras de Componentes
- **Alertas**: Classes Bootstrap (`alert-success`, `alert-danger`, `alert-info`) com `shadow-lg`
- **Botões**: `btn-primary` com gradiente `linear-gradient(135deg, #1a5fb4, #3584e4)`, `border-radius: 8px`, hover com `transform: translateY(-1px)` e `box-shadow` azul
- **Tabelas**: `table-dark table-striped table-hover w-100` + DataTables para paginação e busca
- **Select**: `form-select` com `bg-dark text-white border-secondary` (no audit.cgi)

### Boas Práticas
- JS mínimo: função `filtrarBancos()` inline no `index.cgi` + jQuery + DataTables no `audit.cgi`
- Nunca usar frameworks CSS além do Bootstrap 5 (sem Tailwind, sem Material UI)
- Manter o tema escuro como **único** (não implementar toggle light/dark)
