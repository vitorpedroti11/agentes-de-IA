#!/usr/bin/env python3
"""Converte a prospecção (JSON) na página visual (HTML).

Uso:
    python3 ferramentas/gerar_html.py clientes/adspot/prospeccoes/2026-09-22_cidade_nichos.json
    -> grava o .html ao lado do .json

O HTML é autossuficiente: pode abrir direto no navegador, sem servidor.
"""
import json
import sys
from pathlib import Path

MODELO = Path(__file__).with_name("modelo-prospeccao.html")
MARCADOR = "/*__DADOS__*/"
PRIORIDADES = {"A", "B", "C"}


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
        if not (lead.get("mensagens") or {}).get("whatsapp"):
            avisos.append(f"{nome}: sem mensagem de WhatsApp")
    return avisos


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    origem = Path(sys.argv[1])
    dados = json.loads(origem.read_text(encoding="utf-8"))
    avisos = validar(dados)

    # Impede que um texto com "</script>" feche o bloco de dados antes da hora.
    embutido = json.dumps(dados, ensure_ascii=False).replace("</", "<\\/")
    modelo = MODELO.read_text(encoding="utf-8")
    if MARCADOR not in modelo:
        raise SystemExit(f"marcador {MARCADOR} não encontrado no modelo")
    destino = origem.with_suffix(".html")
    destino.write_text(modelo.replace(MARCADOR, embutido), encoding="utf-8")

    for a in avisos:
        print(f"aviso: {a}", file=sys.stderr)
    print(f"{len(dados['leads'])} leads -> {destino}")


if __name__ == "__main__":
    main()
