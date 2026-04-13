# Skills do Agent

Este arquivo consolida as instruções (skills) e boas práticas absolutas para o agente de IA e equipe de desenvolvimento que atuam no projeto **Oracle Grant Manager (OGM)**.

## 1. Regras de Código Shell e CGI
- **Sanitização Obrigatória**: SEMPRE valide o input do usuário na camada CGI com utilitários nativos ou regex para evitar _Command Injection_.
- **Segurança Transacional**: O script bash responsável por realizar a conexão ao banco via SqlPlus não pode ser lido por usuários randômicos. Mantenha os binários restritos e endereçados a caminhos absolutos como `/usr/local/bin/...`.
- **Mínimo Privilégio Oracle**: Proteja a _engine_ barrando execuções de DDL ou privilégios globais (`ANY PRIVILEGE`) e certifique-se que qualquer permissão seja logada na tabela temporal de expurgo no DB (`GRANT_CONTROL`).

## 2. Controle de Versão (CHANGELOG.md)
Nenhuma feature, ajuste visual ou correção de bug é "apenas feita". Todo conjunto de alterações concluído e testado gera um **Bump de Versão**.
- Você deve manter na raiz do projeto o arquivo `CHANGELOG.md`. O formato segue estritamente o padrão [Keep a Changelog](https://keepachangelog.com/).
- **Versionamento Semântico e Tracking:** 
  - `vX.0.0` (Maior: nova página inteira, novo motor grande ou break de interface).
  - `v0.X.0` (Menor: novo componente adicionado, modal, novas colunas/tabelas de relatórios).
  - `v0.0.X` (Patch: ajuste de cor de botão, alteração de margem, tipografia, fixes pequenos).
- Terminada a tarefa técnica, crie o bloco da nova versão com data e _bullet points_ claros no CHANGELOG.
- Atualize rigorosamente a **tag de versão v_X.X.X no Rodapé global** de interfaces (`index.cgi` e relatórios).

## 3. Comportamento UI/UX e Layout (Arquiteto de Software Sênior)
Como garantidor da integridade sistêmica e visual da ferramenta:
1. **Paleta de Cores e Tematização Dark Mode**: Nosso ecossistema respeita estritamente o sombreamento já incorporado, derivado do Bootstrap. 
   - Body Background: `#121212` 
   - Backgrounds Secundários (Cards/Tabelas): `#1e1e1e` a `#2d2d2d`
   - Realce Interativo Oracle (Primary): `#0d6efd` | *(Focus: rgba(13, 110, 253, 0.25))*
   - Textos puros: `#fff`, `#e0e0e0`  | Textos muteds/Hints: `#adb5bd`
   > Nunca injete uma cor "nova" ou paletas de arco-íris avulsas sem justificar o rompimento visual com a paleta oficial em voga documentada aqui.
2. **Layout Funcional e Responsividade Móvel**: As CGIs estão arquitetadas em contêineres e grids móveis responsivos do Bootstrap 5 (`col-md-*`, `w-100`). **NUNCA** modifique grids estruturais (`display flex`, flexbox nativo, paddings estruturais) ou adicione classes CSS customizadas na árvore que inviabilizem a exibição do front em telas finas ou em smartphones, pois DBAs acionam grants remotamente.
3. Ao finalizar uma tarefa focada no Front-end ou em rotinas de banco, **gere o Tracking Correto** engatilhando todas as notas da release.

*Committe com responsabilidade e aja sempre com a prudência de um Engenheiro Sênior.*
