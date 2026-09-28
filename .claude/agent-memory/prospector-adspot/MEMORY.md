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

- 2026-09-23 · Estética em Guarulhos é nicho saturado: franquias (GiO, Virtuosa, Estetic Face, Hamonir, AD Clinic, Maislaser, Bestlaser, Royal Face, Emporium da Beleza) e independentes com 10 mil+ seguidores · de ~35 candidatos, só 2 passaram · como aplicar: em estética, mapear 4x a quantidade pedida e checar franquia pelo nome antes de buscar CNPJ; avisar o Vitor cedo quando o nicho não render volume.
- 2026-09-23 · Muitas esteticistas usam CNPJ em nome próprio (razão = nome da pessoa) ou nenhum CNPJ encontrável por nome fantasia · como aplicar: buscar `"<nome da profissional>" CNPJ Guarulhos`; se a razão for o nome da pessoa, tratar como empresa individual (capacidade incerta → oferta de Site).
- 2026-09-23 · Gancho que funciona em estética: comparar a autoridade real (anos, formação) com o tamanho do Instagram frente a concorrentes locais, sem citar nomes · hipótese a validar com as respostas.

- 2026-09-23 · Vitor pediu: **HTML para acessar no celular, como padrão** · a abordagem é feita no telefone · como aplicar: não mexer no layout mobile do modelo; gerar sempre com `--pagina`, publicar como página privada e entregar o link. Na página publicada downloads são bloqueados, por isso a planilha vai para a área de transferência ("Copiar planilha").

- 2026-09-23 · Automotivo não estava nos nichos: adicionado à metodologia (oficinas, funilaria, estética automotiva, revendas) · como aplicar: excluir redes (Muniz, FlipWash, concessionárias); em revenda, a dor é giro de estoque (tráfego), não identidade.
- 2026-09-23 · Regra de posts ajustada: muitos posts com poucos seguidores = falta de distribuição (dor), não agência · Stock Car (996 posts, 3,8 mil) e Dra. Manoela (825, 4,7 mil) mostraram o padrão.
- 2026-09-23 · Nunca escrever na mensagem que o Vitor "passou" ou "visitou" o lugar: usar "vi" (site, Maps, Instagram).

- 2026-09-23 · Vitor quer revendas de carros (lojas que vendem carro) como alvo · em revenda, o gancho é giro de estoque: vídeo padrão por carro + anúncio por faixa de preço ou modelo · a Av. Timóteo Penteado (Vila Hulda) concentra revendas; Auto Shopping Internacional reúne dezenas de lojas.
- 2026-09-23 · Mensagens de leads do mesmo nicho tendem a sair parecidas · como aplicar: antes de gravar, comparar o começo das mensagens de WhatsApp de todos os leads; cada uma precisa de um ângulo próprio (tamanho do estoque, ausência de pátio, concorrência no shopping, base de seguidores).

## Páginas publicadas (atualizar o mesmo link ao refazer a lista)
- Dentistas em Guarulhos → https://claude.ai/artifact/TubffLDRXwXNQpQYXjyZjD
- Estética em Guarulhos → https://claude.ai/artifact/1D6F1EQJwzFNip82o1Uwgb
- Automotivo em Guarulhos → https://claude.ai/artifact/GkCpfdEdPxRDSj1FRb2BYE
- Lojas de Carros em Guarulhos → https://claude.ai/artifact/LBJQ8sYgUujMPqmfQwz9Zi
- Imobiliárias pelo Brasil (2026-09-28) → ainda não publicada (ferramenta de páginas/Artifact não estava disponível para este agente nesta sessão); abrir o HTML local pelo caminho do arquivo

## Histórico de prospecções
<!-- data · cidade · nichos · nº de leads A/B · arquivo -->
- 2026-09-22 · Guarulhos/SP · dentista · 1 A + 5 B, 13 descartados (Dentista do Povo saiu por ser rede nacional; Atitud saiu com Instagram ativo) · `clientes/adspot/prospeccoes/2026-09-22_guarulhos_dentista.html`
- 2026-09-23 · Guarulhos/SP · estética · 0 A + 2 B, 13 grupos descartados (nicho saturado) · `clientes/adspot/prospeccoes/2026-09-23_guarulhos_estetica.html`
- 2026-09-23 · Guarulhos/SP · automotivo · 0 A + 6 B, 8 grupos descartados · `clientes/adspot/prospeccoes/2026-09-23_guarulhos_automotivo.html`
- 2026-09-23 · Guarulhos/SP · revendas de carros · 0 A + 8 B, 6 grupos descartados · `clientes/adspot/prospeccoes/2026-09-23_guarulhos_revendas.html`
- 2026-09-28 · Brasil (várias cidades) · imobiliária (nicho novo) · 0 A + 5 B, 7 grupos descartados · `clientes/adspot/prospeccoes/2026-09-28_brasil_imobiliaria.html`

## Aprendizados (continuação)
- 2026-09-28 · Nesta sessão as APIs de CNPJ (`consulta_cnpj.py`) e o WebFetch direto em páginas de CNPJ/redes sociais estavam bloqueados pelo proxy de rede (erro 403/EGRESS_BLOCKED em quase todo domínio, incluindo Instagram, Facebook, econodata, cnpj.biz, casadosdados) · só o WebSearch funcionava · como aplicar: quando isso acontecer, usar WebSearch com o número do CNPJ entre aspas + "sócio administrador quadro societário" — os resumos de busca de Econodata/Serasa/Casa dos Dados costumam trazer o QSA mesmo sem abrir a página; sempre registrar que a fonte é um resultado de busca, não a consulta direta.
- 2026-09-28 · Imobiliárias de porte médio (dentistas, restaurantes etc. saturados) quase sempre já têm algum site pronto de portal imobiliário — a maioria dos candidatos em cidades de 50–150 mil habitantes tinha site · como aplicar: mapear em várias cidades pequenas/médias (4–5x a quantidade pedida) e aceitar como "sem site" só depois de confirmar em pelo menos 2 buscas que não existe nenhum domínio próprio; imobiliárias 100% sem presença digital (nem Instagram) são um risco maior (pode estar inativa) — prefira as que têm Instagram ativo mas nenhum site.
- 2026-09-28 · Quando o nome do sócio-administrador do CNPJ bate com o nome usado na marca/bio do Instagram da própria empresa (ex.: empresa "Edson Imóveis" administrada por "Edson Henrique da Silva"), isso já vale como validação externa (`validado: true`) — não precisa achar um perfil pessoal separado.
