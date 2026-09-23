#!/usr/bin/env python3
"""Converte a prospecção (JSON) na página visual (HTML).

Uso:
    python3 ferramentas/gerar_html.py clientes/adspot/prospeccoes/2026-09-22_cidade_nichos.json
    -> grava o .html ao lado do .json

    python3 ferramentas/gerar_html.py <json> --pagina <arquivo.html>
    -> também grava a versão para publicar como página no claude.ai (abre no celular)

O HTML é autossuficiente e feito primeiro para o celular: abre direto no navegador, sem servidor.
"""
import argparse
import json
import re
from pathlib import Path

MODELO = Path(__file__).with_name("modelo-prospeccao.html")
MARCADOR = "/*__DADOS__*/"
PRIORIDADES = {"A", "B", "C"}
NICHOS_PLURAL = {
    "restaurante": "Restaurantes", "colegio": "Colégios", "salao": "Salões",
    "estetica": "Estética", "dentista": "Dentistas", "psicologo": "Psicólogos",
}


def titulo(dados):
    p = dados.get("prospeccao") or {}
    nichos = [NICHOS_PLURAL.get(n, n) for n in p.get("nichos") or []]
    cidade = (p.get("cidade") or "").split("/")[0].strip()
    nome = " e ".join(nichos) if 0 < len(nichos) <= 2 else "Leads"
    return f"{nome} em {cidade}" if cidade else nome


def versao_pagina(html):
    """Tira o esqueleto do documento: a página publicada recebe o próprio <head> com charset e viewport."""
    for padrao in (r"<!DOCTYPE html>\s*", r"<html[^>]*>\s*", r"</?head>\s*", r"</?body>\s*", r"</html>\s*",
                   r'<meta charset="utf-8">\s*', r'<meta name="viewport"[^>]*>\s*'):
        html = re.sub(padrao, "", html, flags=re.I)
    return html


def validar(dados):
    avisos = []
    leads = dados.get("leads")
    if not isinstance(leads, list):
        raise SystemExit("JSON inválido: falta a lista 'leads'.")
    ids = set()
    for i, lead in enumerate(leads):
        nome = lead.get("nome_fantasia") or f"lead {i}"
        lead.setdefault("id", f"lead-{i}")
        if lead["id"] in ids:
            raise SystemExit(f"id repetido: {lead['id']}")
        ids.add(lead["id"])
        if lead.get("prioridade") not in PRIORIDADES:
            avisos.append(f"{nome}: prioridade ausente ou inválida")
        if not (lead.get("cnpj") or {}).get("numero"):
            avisos.append(f"{nome}: sem CNPJ")
        if not (lead.get("decisor") or {}).get("nome"):
            avisos.append(f"{nome}: dono não identificado")
        ig = (lead.get("presenca") or {}).get("instagram") or {}
        if not ig.get("url") and "não encontrado" not in (ig.get("status") or ""):
            avisos.append(f"{nome}: sem Instagram da empresa (preencher ou marcar status 'não encontrado' após buscar)")
        if not (lead.get("decisor") or {}).get("instagram"):
            avisos.append(f"{nome}: sem Instagram do dono (preencher ou 'não encontrado')")
        if not (lead.get("mensagens") or {}).get("whatsapp"):
            avisos.append(f"{nome}: sem mensagem de WhatsApp")
    return avisos


def main():
    ap = argparse.ArgumentParser(description="Gera a página da prospecção a partir do JSON.")
    ap.add_argument("json", help="arquivo da prospecção")
    ap.add_argument("--pagina", help="grava também a versão para publicar como página (celular)")
    args = ap.parse_args()

    origem = Path(args.json)
    dados = json.loads(origem.read_text(encoding="utf-8"))
    avisos = validar(dados)

    # Impede que um texto com "</script>" feche o bloco de dados antes da hora.
    embutido = json.dumps(dados, ensure_ascii=False).replace("</", "<\\/")
    modelo = MODELO.read_text(encoding="utf-8")
    if MARCADOR not in modelo:
        raise SystemExit(f"marcador {MARCADOR} não encontrado no modelo")
    html = modelo.replace(MARCADOR, embutido)
    html = re.sub(r"<title>.*?</title>", f"<title>{titulo(dados)}</title>", html, count=1)
    destino = origem.with_suffix(".html")
    destino.write_text(html, encoding="utf-8")

    for a in avisos:
        print(f"aviso: {a}")
    print(f"{len(dados['leads'])} leads -> {destino}")
    if args.pagina:
        Path(args.pagina).parent.mkdir(parents=True, exist_ok=True)
        Path(args.pagina).write_text(versao_pagina(html), encoding="utf-8")
        print(f"página para publicar -> {args.pagina}")


if __name__ == "__main__":
    main()
