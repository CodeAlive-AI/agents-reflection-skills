<p align="center">
  <img src="https://img.shields.io/badge/Claude_Code-Marketplace-blueviolet?style=for-the-badge" alt="Claude Code Marketplace">
  <img src="https://img.shields.io/badge/Plugins-1-blue?style=for-the-badge" alt="1 Plugin">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="MIT License">
</p>

<h1 align="center">Claude Code Reflection Skills</h1>

<p align="center">
  <strong>Um marketplace de meta-habilidades que permitem ao Claude Code se autoconfigurar</strong>
</p>

<p align="center">
  Chega de editar arquivos JSON na mão. É só pedir pro Claude configurar tudo pra você.
</p>

<p align="center">
  <a href="README.md">English</a> •
  <a href="README.ru.md">Русский</a> •
  <a href="README.zh.md">中文</a>
</p>

---

## Instalação

```bash
# Passo 1: Adicione o marketplace
/plugin marketplace add https://github.com/CodeAlive-AI/claude-code-reflection-skills.git

# Passo 2: Instale o plugin
/plugin install claude-code-reflection-skills@claude-code-reflection-skills
```

---

## O Que Está Incluído

O plugin **claude-code-reflection-skills** oferece 7 habilidades:

| Habilidade | O Que Faz |
|------------|-----------|
| **claude-mcp-manager** | Conecta a bancos de dados, GitHub e APIs via servidores MCP |
| **claude-hooks-manager** | Auto-formatação, auto-testes, log de comandos |
| **claude-settings-manager** | Configura permissões, sandbox e seleção de modelo |
| **claude-subagents-manager** | Cria agentes especializados para tarefas específicas |
| **claude-skills-manager** | Organiza e compartilha habilidades entre projetos |
| **claude-plugins-manager** | Empacota e publica seus próprios plugins |
| **optimizing-claude-code** | Audita repositórios e otimiza o CLAUDE.md |

> **Leve:** As descrições de todas as 7 habilidades juntas usam menos de 500 tokens na janela de contexto.

---

## Exemplos de Uso

### claude-mcp-manager

> Conecta a bancos de dados, GitHub e APIs via servidores MCP

**Conectar ao Banco de Dados**
> *"Conecta o Claude ao meu banco PostgreSQL"*

Instala o [servidor MCP de banco de dados](https://github.com/modelcontextprotocol/servers), configura a string de conexão. Agora você pode consultar seus dados de forma conversacional.

**Integração com GitHub**
> *"Conecta o Claude ao GitHub pra ele poder criar PRs e gerenciar issues"*

Instala o [servidor MCP oficial do GitHub](https://github.com/github/github-mcp-server). O Claude passa a criar branches, PRs e trabalhar com issues diretamente.

**Atualizar Chaves de API**
> *"Atualiza minha chave de API do CodeAlive na config do MCP"*

Edita seu `~/.claude.json` ou `.mcp.json` para atualizar as chaves. Perfeito pra rotacionar credenciais sem reinstalar nada.

**Atualização em Massa**
> *"Muda o timeout de todos os meus servidores MCP pra 120 segundos"*

Atualiza a configuração de todos os servidores MCP de uma vez. Ajusta timeouts, variáveis de ambiente ou argumentos de comando em massa.

---

### claude-hooks-manager

> Auto-formatação, auto-testes, log de comandos

**Auto-Formatação de Código**
> *"Roda o Prettier nos arquivos TypeScript depois de cada edição"*

Adiciona um hook PostToolUse. Todo arquivo que o Claude mexer é formatado automaticamente — acabou a inconsistência de estilo.

**Auto-Execução de Testes**
> *"Roda o pytest sempre que o Claude editar arquivos Python"*

Adiciona um hook PostToolUse para arquivos `*.py`. Feedback instantâneo se alguma mudança quebrou algo.

**Log de Comandos**
> *"Registra todo comando que o Claude executar num arquivo de auditoria"*

Adiciona um hook PreToolUse que grava os comandos em `~/.claude/command-log.txt`. Rastro completo de auditoria.

**Bloquear Comandos Perigosos**
> *"Adiciona um hook que bloqueia comandos rm -rf globais"*

Adiciona um hook PreToolUse que rejeita comandos destrutivos antes de executar. Proteção contra perda acidental de dados.

**Exigir Confirmação**
> *"Adiciona um hook que pede permissão pro usuário em comandos com 'db reset'"*

Adiciona um hook PreToolUse que pausa e pede confirmação para resets de banco de dados ou outras operações sensíveis.

---

### claude-settings-manager

> Configura permissões, sandbox e seleção de modelo

**Ativar Modo Sandbox**
> *"Liga o modo sandbox pra o Claude poder trabalhar sem pedir permissão pra cada comando"*

Ativa o [sandboxing nativo](https://www.anthropic.com/engineering/claude-code-sandboxing) — reduz os pedidos de permissão em 84% mantendo seu sistema seguro.

**Bloquear Acesso a Segredos**
> *"Bloqueia o Claude de ler arquivos .env e qualquer coisa em /secrets"*

Adiciona regras de negação nas permissões. Arquivos sensíveis ficam protegidos mesmo se o Claude tentar acessá-los.

**Trocar de Modelo**
> *"Usa o modelo Opus neste projeto"*

Atualiza as configurações para usar `claude-opus-4-5` — raciocínio mais apurado para decisões arquiteturais complexas.

**Compartilhar Configuração do Time**
> *"Configura as settings do projeto pra todo mundo ter a mesma config do Claude"*

Cria `.claude/settings.json` no escopo do projeto. Um commit e todo o time recebe a mesma configuração.

---

### claude-subagents-manager

> Cria agentes especializados para tarefas específicas

**Criar um Revisor de Código**
> *"Cria um subagente revisor que só pode ler arquivos, usando Opus pra qualidade"*

Cria um [subagente personalizado](https://code.claude.com/docs/en/sub-agents) com `tools: Read, Grep, Glob` e `model: opus`. Reviews de código completos e detalhados.

**Criar um Executor de Testes**
> *"Cria um subagente que roda testes e reporta falhas"*

Cria um agente especializado em rodar suítes de teste com acesso limitado a ferramentas por segurança.

---

### claude-skills-manager

> Organiza e compartilha habilidades entre projetos

**Listar Habilidades Disponíveis**
> *"Mostra todas as minhas habilidades instaladas"*

Lista habilidades dos escopos de usuário e projeto com seus gatilhos e descrições.

**Mover Habilidades Entre Escopos**
> *"Move essa habilidade pro meu escopo de usuário pra eu poder usar em todo lugar"*

Move habilidades entre escopos de projeto e usuário para disponibilidade mais ampla ou restrita.

---

### claude-plugins-manager

> Empacota e publica seus próprios plugins

**Criar um Plugin**
> *"Cria um novo plugin com minhas habilidades personalizadas"*

Gera a estrutura de um novo plugin com manifesto, README e diretórios de habilidades.

**Publicar no GitHub**
> *"Publica meu plugin no GitHub"*

Empacota seu plugin e cria um release no GitHub para outros instalarem.

---

### optimizing-claude-code

> Audita repositórios e otimiza o CLAUDE.md

**Auditar Prontidão do Projeto**
> *"Verifica se esse repo tá bem configurado pro Claude Code"*

Executa uma auditoria completa analisando arquivos CLAUDE.md, configurações, configs de MCP e estrutura do projeto. Retorna recomendações priorizadas (P0/P1/P2) com sugestões específicas de melhoria.

**Otimizar CLAUDE.md**
> *"Revisa meu CLAUDE.md e sugere melhorias"*

Avalia a qualidade do arquivo de memória: estrutura, concisão, validação de @import, seções essenciais (comandos, arquitetura, convenções). Fornece edições concretas pra deixar seu projeto mais amigável pro agente.

---

## Requisitos

- Claude Code CLI versão 1.0.33 ou superior
- Python 3.x (para scripts das habilidades)
- CLI `gh` (opcional, para funcionalidades de publicação de plugins)

---

## Estrutura

```
claude-code-reflection-skills/
├── .claude-plugin/
│   └── marketplace.json         (catálogo do marketplace)
├── plugins/
│   └── claude-code-reflection-skills/
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── skills/
│       │   ├── claude-mcp-manager/
│       │   ├── claude-hooks-manager/
│       │   ├── claude-settings-manager/
│       │   ├── claude-subagents-manager/
│       │   ├── claude-skills-manager/
│       │   ├── claude-plugins-manager/
│       │   └── optimizing-claude-code/
│       ├── LICENSE
│       └── README.md
├── CLAUDE.md
├── LICENSE
└── README.md
```

---

## Saiba Mais

- [Guia de Servidores MCP](https://code.claude.com/docs/en/mcp)
- [Documentação de Hooks](https://code.claude.com/docs/en/hooks-guide)
- [Subagentes Personalizados](https://code.claude.com/docs/en/sub-agents)
- [Sandboxing](https://code.claude.com/docs/en/sandboxing)

---

## Licença

MIT — veja [LICENSE](LICENSE)

---

<p align="center">
  <sub>Feito com Claude Code</sub>
</p>
