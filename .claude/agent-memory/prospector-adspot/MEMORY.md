# Memória — prospector-adspot

> O que este agente aprendeu rodando. Só jeito de trabalhar (métodos vão para `metodologia/prospeccao.md`, fatos da Adspot para `clientes/adspot/oferta.md`).
> Formato de cada entrada: **data · o que aprendi · por quê · como aplicar**.

## Aprendizados

- 2026-09-22 · Ambientes com rede restrita bloqueiam as APIs de CNPJ · A consulta volta erro de proxy/403 · Se `consulta_cnpj.py` falhar em todas as fontes, buscar o CNPJ na web (WebFetch em cnpj.biz / casadosdados) e marcar `fonte_cnpj` com o link usado; nunca preencher QSA de memória.

- 2026-09-22 · Com as APIs e sites de CNPJ bloqueados, o WebSearch devolve razão social, abertura e QSA a partir de econodata/casadosdados/cnpj.biz · os resumos da busca podem misturar empresas · como aplicar: sempre rodar `cnpj_valido()` no número, conferir se o endereço bate com o da clínica e registrar a URL de origem.
- 2026-09-22 · Nota "4,x (4)" do DentMap é o número de avaliações do próprio DentMap, não do Google · aparece igual em várias clínicas · como aplicar: não usar como nota do Google; buscar a nota em guia local ou no Maps.
- 2026-09-22 · Em dentista, o dono costuma aparecer como "Dra./Dr. Nome" na bio do Instagram ou em diretórios (Doctoralia, BoaConsulta, Guiamais) · é a validação externa mais rápida · como aplicar: buscar `"<nome do QSA>"` entre aspas antes de marcar `validado`.

- 2026-09-22 · Vitor pediu: **Instagram sempre, como padrão** (empresa + dono) · é o canal principal da abordagem e a vitrine que o Pacote vende · como aplicar: preencher `presenca.instagram.url` e `decisor.instagram` em todo lead; "não encontrado" só depois de 3 buscas.
- 2026-09-22 · Buscar o Instagram revelou que "Dentista do Povo" é rede nacional (Bauru, Campinas, Jundiaí…), o que o CNPJ local não mostrava · como aplicar: pesquisar o nome fantasia no Instagram antes de pontuar; vários perfis `@marca_cidade` = rede → descartar.

## Histórico de prospecções
<!-- data · cidade · nichos · nº de leads A/B · arquivo -->
- 2026-09-22 · Guarulhos/SP · dentista · 1 A + 5 B, 13 descartados (Dentista do Povo saiu por ser rede nacional; Atitud saiu com Instagram ativo) · `clientes/adspot/prospeccoes/2026-09-22_guarulhos_dentista.html`
