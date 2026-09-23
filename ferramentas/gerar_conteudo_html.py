#!/usr/bin/env python3
"""Junta todos os clientes de conteúdo num painel único em HTML.

Uso:
    python3 ferramentas/gerar_conteudo_html.py
    -> lê clientes/adspot/conteudo/*/cliente.json e grava
       clientes/adspot/conteudo/painel.html

    python3 ferramentas/gerar_conteudo_html.py --pagina saida.html
    -> também grava a versão para publicar como página no claude.ai (celular)

    python3 ferramentas/gerar_conteudo_html.py --dir outra/pasta --saida outra/painel.html
    -> usa outra pasta de clientes (útil para testar com dados de exemplo)

O painel é autossuficiente: abre direto no navegador, sem servidor.
"""
import argparse
import json
import re
from pathlib import Path

MODELO = Path(__file__).with_name("modelo-conteudo.html")
MARCADOR = "/*__DADOS__*/"
TIPOS_VALIDOS = {"post", "carrossel", "reel", "stories", "legenda", "roteiro"}
PILARES_VALIDOS = {
    "autoridade", "educacao", "engajamento", "branding",
    "prova_social", "vendas", "conversao",
}
STATUS_CONTEUDO_VALIDOS = {"ideia", "aprovado", "desenvolvido", "publicado", "descartado"}
CAMPOS_PERFIL_OBRIGATORIOS = [
    "nome", "segmento", "produtos_servicos", "publico_alvo",
    "diferenciais", "objetivos", "tom_de_voz",
]


def versao_pagina(html):
    """Tira o esqueleto do documento: a página publicada recebe o próprio <head> com charset e viewport."""
    for padrao in (r"<!DOCTYPE html>\s*", r"<html[^>]*>\s*", r"</?head>\s*", r"</?body>\s*", r"</html>\s*",
                   r'<meta charset="utf-8">\s*', r'<meta name="viewport"[^>]*>\s*'):
        html = re.sub(padrao, "", html, flags=re.I)
    return html


def validar_cliente(dados, origem):
    avisos = []
    c = dados.get("cliente") or {}
    nome = c.get("nome") or origem
    if not c.get("id"):
        avisos.append(f"{origem}: cliente sem 'id'")
    for campo in CAMPOS_PERFIL_OBRIGATORIOS:
        if not c.get(campo):
            avisos.append(f"{nome}: perfil sem '{campo}' — não gerar conteúdo que dependa disso sem perguntar")

    ids = set()
    for item in dados.get("conteudos") or []:
        rid = item.get("id")
        titulo = item.get("titulo") or rid or "(sem id)"
        if not rid:
            avisos.append(f"{nome}: conteúdo sem 'id' ({titulo})")
        elif rid in ids:
            avisos.append(f"{nome}: id de conteúdo repetido: {rid}")
        ids.add(rid)
        if item.get("tipo") not in TIPOS_VALIDOS:
            avisos.append(f"{nome}/{titulo}: tipo inválido ou ausente")
        if item.get("pilar") and item["pilar"] not in PILARES_VALIDOS:
            avisos.append(f"{nome}/{titulo}: pilar '{item['pilar']}' não está na lista dos sete pilares")
        if item.get("status") not in STATUS_CONTEUDO_VALIDOS:
            avisos.append(f"{nome}/{titulo}: status inválido ou ausente")

    for semana in dados.get("semanas") or []:
        sid = semana.get("id") or semana.get("data_inicio") or "(sem id)"
        for item in semana.get("itens") or []:
            if item.get("tipo") not in TIPOS_VALIDOS:
                avisos.append(f"{nome}/semana {sid}: item com tipo inválido ({item.get('dia')})")
            if not item.get("ideia_resumo") and item.get("status") == "ideia":
                avisos.append(f"{nome}/semana {sid}: item de {item.get('dia')} sem ideia resumida")

    return avisos


def carregar_clientes(diretorio):
    clientes = []
    avisos = []
    for arquivo in sorted(Path(diretorio).glob("*/cliente.json")):
        try:
            dados = json.loads(arquivo.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            avisos.append(f"{arquivo}: JSON inválido ({e})")
            continue
        dados.setdefault("conteudos", [])
        dados.setdefault("semanas", [])
        dados.setdefault("planejamento_mensal", [])
        dados.setdefault("banco_ideias", [])
        avisos += validar_cliente(dados, str(arquivo))
        clientes.append(dados)
    return clientes, avisos


def main():
    ap = argparse.ArgumentParser(description="Gera o painel de conteúdo a partir dos clientes cadastrados.")
    ap.add_argument("--dir", default="clientes/adspot/conteudo", help="pasta com <cliente>/cliente.json (padrão: clientes/adspot/conteudo)")
    ap.add_argument("--saida", default=None, help="onde gravar o painel (padrão: <dir>/painel.html)")
    ap.add_argument("--pagina", help="grava também a versão para publicar como página (celular)")
    args = ap.parse_args()

    diretorio = Path(args.dir)
    clientes, avisos = carregar_clientes(diretorio)
    if not clientes:
        raise SystemExit(f"Nenhum cliente.json encontrado em {diretorio}/*/cliente.json")

    payload = {"clientes": clientes}
    # Impede que um texto com "</script>" feche o bloco de dados antes da hora.
    embutido = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
    modelo = MODELO.read_text(encoding="utf-8")
    if MARCADOR not in modelo:
        raise SystemExit(f"marcador {MARCADOR} não encontrado no modelo")
    html = modelo.replace(MARCADOR, embutido)

    destino = Path(args.saida) if args.saida else diretorio / "painel.html"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(html, encoding="utf-8")

    for a in avisos:
        print(f"aviso: {a}")
    total_conteudos = sum(len(c.get("conteudos") or []) for c in clientes)
    print(f"{len(clientes)} cliente(s), {total_conteudos} conteúdo(s) -> {destino}")

    if args.pagina:
        Path(args.pagina).parent.mkdir(parents=True, exist_ok=True)
        Path(args.pagina).write_text(versao_pagina(html), encoding="utf-8")
        print(f"página para publicar -> {args.pagina}")


if __name__ == "__main__":
    main()
