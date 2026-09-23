#!/usr/bin/env python3
"""Gera a ADSPOT AI: a central que reúne os agentes já existentes num só lugar.

Não recria nem altera nenhum agente. Só lê o que o Prospector Adspot e o
Conteúdo Adspot já geraram (os `.html` deles) e monta um índice/manifesto
em volta, para abrir os dois a partir de um único lugar.

Uso:
    python3 ferramentas/gerar_central.py
    -> lê clientes/adspot/prospeccoes/*.html e clientes/adspot/conteudo/painel.html
       e grava central/adspot-ai.html

Rodar de novo sempre que uma nova prospecção for gerada ou o painel de
conteúdo for atualizado — como já era preciso rodar `gerar_html.py` e
`gerar_conteudo_html.py`.
"""
import argparse
import json
import re
from pathlib import Path

MODELO = Path(__file__).with_name("modelo-central.html")
MARCADOR = "/*__DADOS__*/"
DADOS_RE = re.compile(r'<script id="dados" type="application/json">(.*?)</script>', re.S)
TITULO_RE = re.compile(r"<title>(.*?)</title>", re.S | re.I)

RAIZ = Path(__file__).resolve().parent.parent
PASTA_PROSPECCOES = RAIZ / "clientes/adspot/prospeccoes"
PAINEL_CONTEUDO = RAIZ / "clientes/adspot/conteudo/painel.html"


def ler_json_embutido(html):
    m = DADOS_RE.search(html)
    if not m:
        return None
    texto = m.group(1).strip().replace("<\\/", "</")
    try:
        return json.loads(texto)
    except json.JSONDecodeError:
        return None


def titulo_de(html, alternativa):
    m = TITULO_RE.search(html)
    return (m.group(1).strip() if m and m.group(1).strip() else alternativa)


def listar_prospeccoes():
    """Cada prospecção do Prospector Adspot é um arquivo .html próprio (uma lista por nicho/cidade).
    A central só lista o que já existe — não gera nem reescreve nenhum."""
    itens = []
    if not PASTA_PROSPECCOES.exists():
        return itens
    for arquivo in sorted(PASTA_PROSPECCOES.glob("*.html")):
        html = arquivo.read_text(encoding="utf-8")
        dados = ler_json_embutido(html) or {}
        p = dados.get("prospeccao") or {}
        leads = dados.get("leads") or []
        prio_a = sum(1 for l in leads if l.get("prioridade") == "A")
        itens.append({
            "arquivo": "../" + str(arquivo.relative_to(RAIZ)).replace("\\", "/"),
            "titulo": titulo_de(html, arquivo.stem),
            "cidade": p.get("cidade", ""),
            "regiao": p.get("regiao", ""),
            "data": p.get("data", ""),
            "nichos": p.get("nichos", []),
            "demonstracao": bool(p.get("demonstracao")),
            "total_leads": len(leads),
            "prioridade_a": prio_a,
        })
    # mais recentes primeiro (sort estável); exemplo fictício sempre por último
    itens.sort(key=lambda i: i["data"], reverse=True)
    itens.sort(key=lambda i: i["demonstracao"])
    return itens


def dados_conteudo():
    """O Conteúdo Adspot já tem um painel único e permanente — a central só aponta pra ele."""
    if not PAINEL_CONTEUDO.exists():
        return None
    html = PAINEL_CONTEUDO.read_text(encoding="utf-8")
    dados = ler_json_embutido(html) or {}
    clientes = dados.get("clientes") or []
    total_conteudos = sum(len(c.get("conteudos") or []) for c in clientes)
    return {
        "arquivo": "../" + str(PAINEL_CONTEUDO.relative_to(RAIZ)).replace("\\", "/"),
        "titulo": titulo_de(html, "Painel de Conteúdo"),
        "clientes": [c.get("cliente", {}).get("nome", "") for c in clientes],
        "total_clientes": len(clientes),
        "total_conteudos": total_conteudos,
    }


def main():
    ap = argparse.ArgumentParser(description="Gera a central ADSPOT AI a partir dos agentes já existentes.")
    ap.add_argument("--saida", default=str(RAIZ / "central/adspot-ai.html"), help="onde gravar a central")
    args = ap.parse_args()

    manifesto = {
        "prospeccao": listar_prospeccoes(),
        "conteudo": dados_conteudo(),
    }

    modelo = MODELO.read_text(encoding="utf-8")
    if MARCADOR not in modelo:
        raise SystemExit(f"marcador {MARCADOR} não encontrado no modelo")
    embutido = json.dumps(manifesto, ensure_ascii=False).replace("</", "<\\/")
    html = modelo.replace(MARCADOR, embutido)

    destino = Path(args.saida)
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(html, encoding="utf-8")

    print(f"{len(manifesto['prospeccao'])} prospecção(ões) · "
          f"{'painel de conteúdo encontrado' if manifesto['conteudo'] else 'sem painel de conteúdo'} "
          f"-> {destino}")
    if not manifesto["prospeccao"]:
        print("aviso: nenhuma prospecção encontrada em clientes/adspot/prospeccoes/*.html")
    if not manifesto["conteudo"]:
        print("aviso: clientes/adspot/conteudo/painel.html não encontrado — rode gerar_conteudo_html.py primeiro")


if __name__ == "__main__":
    main()
