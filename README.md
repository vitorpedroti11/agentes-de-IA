# Agentes de IA — Adspot

Agentes do Claude Code da Adspot, montados no padrão de quatro arquivos: **agente, método, estado e memória**.

| Peça | Arquivo |
|---|---|
| O agente | `.claude/agents/prospector-adspot.md` |
| O método | `metodologia/prospeccao.md` |
| O estado | `clientes/adspot/oferta.md` |
| A memória | `.claude/agent-memory/prospector-adspot/MEMORY.md` |
| Ferramentas | `ferramentas/consulta_cnpj.py`, `ferramentas/gerar_html.py`, `ferramentas/modelo-prospeccao.html` |

## Prospector Adspot

Encontra restaurantes, colégios, salões de beleza, estética, dentistas e psicólogos com presença digital fraca, identifica o dono pelo CNPJ (quadro de sócios), pontua pelo ICP, recomenda **Site (R$ 1.000–1.500)** ou **Pacote Inicial (R$ 1.500/mês × 3)** e escreve a primeira abordagem. A entrega é uma página HTML com filtros, status de cada lead, mensagens prontas para copiar/abrir no WhatsApp e exportação CSV.

### Como usar
No Claude Code, dentro deste repositório:

```
@prospector-adspot prospecte 10 leads de colégios e dentistas no bairro X, cidade Y
```

O resultado fica em `clientes/adspot/prospeccoes/` (um `.json` e um `.html`). Abra o `.html` no navegador.
Veja o formato em `clientes/adspot/prospeccoes/exemplo-ficticio.html` (dados fictícios).

### Ferramentas avulsas
```
python3 ferramentas/consulta_cnpj.py 12.345.678/0001-90     # dados da Receita + sócios + decisor sugerido
python3 ferramentas/gerar_html.py <prospeccao>.json         # gera a página visual
```
Só usam a biblioteca padrão do Python 3.

### Antes da primeira rodada
Preencha em `clientes/adspot/oferta.md`: região de atuação, Instagram/WhatsApp da Adspot, cases e se a verba de anúncio está inclusa no pacote.

### Refinamento
Toda correção vira regra escrita: fato da Adspot → `oferta.md`; método → `metodologia/prospeccao.md`; jeito do agente trabalhar → memória do agente.
