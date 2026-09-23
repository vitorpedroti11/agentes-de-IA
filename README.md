# Agentes de IA — Adspot

Agentes do Claude Code da Adspot, montados no padrão de quatro arquivos: **agente, método, estado e memória**.

| Peça | Prospector Adspot | Conteúdo Adspot |
|---|---|---|
| O agente | `.claude/agents/prospector-adspot.md` | `.claude/agents/conteudo-adspot.md` |
| O método | `metodologia/prospeccao.md` | `metodologia/conteudo.md` |
| O estado | `clientes/adspot/oferta.md` | `clientes/adspot/conteudo/<cliente>/cliente.json` (um por cliente da agência) |
| A memória | `.claude/agent-memory/prospector-adspot/MEMORY.md` | `.claude/agent-memory/conteudo-adspot/MEMORY.md` |
| Ferramentas | `ferramentas/consulta_cnpj.py`, `ferramentas/gerar_html.py`, `ferramentas/modelo-prospeccao.html` | `ferramentas/gerar_conteudo_html.py`, `ferramentas/modelo-conteudo.html` |

## Prospector Adspot

Encontra restaurantes, colégios, salões de beleza, estética, dentistas e psicólogos com presença digital fraca, identifica o dono pelo CNPJ (quadro de sócios), pontua pelo ICP, recomenda **Site (R$ 1.000–1.500)** ou **Pacote Inicial (R$ 1.500/mês × 3)** e escreve a primeira abordagem. A entrega é uma página HTML feita para o celular, com filtros, status de cada lead, mensagens prontas para abrir no WhatsApp ou no Direct e cópia da lista para planilha.

### Como usar
No Claude Code, dentro deste repositório:

```
@prospector-adspot prospecte 10 leads de colégios e dentistas no bairro X, cidade Y
```

O resultado fica em `clientes/adspot/prospeccoes/` (um `.json` e um `.html`). A página é feita primeiro para o celular: botões de WhatsApp, Direct e Ligar em cada lead. Para abrir no telefone, o agente publica a lista como página privada no claude.ai e entrega o link.
Veja o formato em `clientes/adspot/prospeccoes/exemplo-ficticio.html` (dados fictícios).

### Ferramentas avulsas
```
python3 ferramentas/consulta_cnpj.py 12.345.678/0001-90     # dados da Receita + sócios + decisor sugerido
python3 ferramentas/gerar_html.py <prospeccao>.json         # gera a página visual
python3 ferramentas/gerar_html.py <prospeccao>.json --pagina saida.html   # + versão para publicar (celular)
```
Só usam a biblioteca padrão do Python 3.

### Antes da primeira rodada
Preencha em `clientes/adspot/oferta.md`: região de atuação, Instagram/WhatsApp da Adspot, cases e se a verba de anúncio está inclusa no pacote.

### Refinamento
Toda correção vira regra escrita: fato da Adspot → `oferta.md`; método → `metodologia/prospeccao.md`; jeito do agente trabalhar → memória do agente.

## Conteúdo Adspot

Cadastra clientes da agência com o perfil completo de marca (segmento, produtos, público, diferenciais, objetivos, tom de voz, identidade visual, palavras a usar/evitar, informações importantes) e usa esse perfil sempre que aquele cliente for selecionado. Cria posts, carrosséis, Reels, stories, legendas e roteiros; monta e desenvolve semanas e meses de conteúdo balanceados pelos sete pilares (autoridade, educação, engajamento, branding, prova social, vendas, conversão); mantém banco de ideias e histórico por cliente para nunca repetir gancho, tema ou CTA. A entrega é um painel único em HTML, no mesmo padrão visual do prospector, com Dashboard, Clientes, Criar Conteúdo, Criar Semana, Planejamento, Banco de Ideias e Histórico.

### Como usar
```
@conteudo-adspot cadastre o cliente <nome> com [perfil...]
@conteudo-adspot crie um reel para <cliente> sobre [tema]
@conteudo-adspot crie uma semana para <cliente> com 3 posts, 2 reels e stories de segunda a sexta
@conteudo-adspot desenvolva a semana completa / desenvolva o conteúdo de <dia>
@conteudo-adspot planejamento mensal de <mês> para <cliente>
@conteudo-adspot me dê 20 ideias de reels para <cliente>
```

O resultado fica em `clientes/adspot/conteudo/<cliente>/cliente.json` (um por cliente) e no painel único `clientes/adspot/conteudo/painel.html`, que junta todos os clientes. Veja o formato em `clientes/adspot/conteudo/studio-bela-exemplo/cliente.json` (dados fictícios).

**Importante:** o painel HTML não gera conteúdo sozinho — é o agente, aqui no chat, quem escreve. Os botões "🪄" do painel montam o pedido certo e copiam para você colar na conversa com o `@conteudo-adspot`; depois que o agente responde, ele já grava o resultado no `cliente.json` e regenera o painel. O painel guarda no navegador (localStorage) o cliente selecionado, aprovações e cadastros feitos direto na tela — cadastro feito só na tela precisa ser confirmado ao agente para virar arquivo no repositório (o botão "Copiar JSON do cliente" existe para isso).

### Ferramentas avulsas
```
python3 ferramentas/gerar_conteudo_html.py                                 # junta clientes/adspot/conteudo/*/cliente.json no painel
python3 ferramentas/gerar_conteudo_html.py --pagina saida.html             # + versão para publicar (celular)
```
Só usa a biblioteca padrão do Python 3.

### Refinamento
Fato de um cliente específico → dentro do `cliente.json` dele; método (pilares, formatos, regras de repetição) → `metodologia/conteudo.md`; jeito do agente trabalhar → memória do agente.
