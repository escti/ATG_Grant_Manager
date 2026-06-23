---
name: frontend
description: Regras de UI/UX, Design System e Padrões de Frontend para CGIs Bootstrap 5
---

# 🖥️ Skill: Frontend (CGI + Bootstrap 5)

## Design System

### Paleta de Cores (Imutável)
| Token | Hex | Uso |
|---|---|---|
| `bg-body` | `#121212` | Fundo da página (`body`) |
| `bg-card` | `#1e1e1e` | Cards, tabelas, containers |
| `bg-input` | `#2d2d2d` | Inputs, selects, textareas |
| `border-subtle` | `#333` / `#444` | Bordas de cards e inputs |
| `text-primary` | `#0d6efd` | Azul Oracle para títulos e botões |
| `text-body` | `#e0e0e0` | Corpo do texto |
| `text-muted` | `#6c757d` / `#adb5bd` | Labels e textos secundários |
| `text-xs` | `#6c757d` | Rodapés e notas legais |

**Proibido:** Usar cores legadas (ex: azul claro #00f, verde limão, vermelho sem contexto Bootstrap).

### Tipografia
- Família: `'Segoe UI', Tahoma, Geneva, Verdana, sans-serif`
- Tamanhos: `0.85rem` para `text-xs`, `1rem` para corpo
- Pesos: `700` para títulos (`header-title`), `600` para botões

### Dark Mode (Obrigatório)
- Atributo `<html data-bs-theme="dark">`
- Toda nova página DEVE iniciar com `data-bs-theme="dark"`
- `box-shadow` em cards: `0 10px 30px rgba(0,0,0,0.5)`

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
4. Bootstrap 5.3+ via CDN (única dependência)
5. Formulários com `method="POST"` em `index.cgi`, `method="GET"` em `audit.cgi`
6. Sanitização via `tr -cd` antes de qualquer output

### Footer (Versão)
- Deve conter: `&copy; {ano} DBA Team - Segurança & Auditoria | Versão: {semver}`
- {semver} deve ser atualizado a cada bump de versão no CHANGELOG
- Localização: dentro do card ou container principal, centralizado (`text-center`)

### Regras de Componentes
- **Alertas**: Classes Bootstrap (`alert-success`, `alert-danger`, `alert-info`) com `shadow-lg`
- **Botões**: `btn-primary` com cor `#0d6efd`, `hover: #0b5ed7`, transição `0.3s ease`, `transform: translateY(-2px)` no hover
- **Tabelas**: `table-dark table-striped table-hover w-100` + DataTables para paginação e busca
- **Select**: `form-select` com `bg-dark text-white border-secondary` (no audit.cgi)

### Boas Práticas
- Nunca usar JS inline além do necessário (apenas jQuery + DataTables no audit)
- Nunca usar frameworks CSS além do Bootstrap 5 (sem Tailwind, sem Material UI)
- Manter o tema escuro como **único** (não implementar toggle light/dark)
