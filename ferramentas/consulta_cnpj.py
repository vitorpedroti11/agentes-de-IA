#!/usr/bin/env python3
"""Consulta CNPJ em fontes públicas e devolve os dados no formato do lead.

Uso:
    python3 ferramentas/consulta_cnpj.py 12.345.678/0001-90 [outro_cnpj ...]
    python3 ferramentas/consulta_cnpj.py --arquivo cnpjs.txt --saida resultado.json

Fontes, em ordem: BrasilAPI -> CNPJ.ws (pública) -> ReceitaWS.
Só usa biblioteca padrão do Python.
"""
import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request

FONTES = [
    ("brasilapi", "https://brasilapi.com.br/api/cnpj/v1/{cnpj}"),
    ("cnpjws", "https://publica.cnpj.ws/cnpj/{cnpj}"),
    ("receitaws", "https://receitaws.com.br/v1/cnpj/{cnpj}"),
]

QUALIFICACOES_DECISOR = ("administrador", "titular", "presidente", "diretor")


def limpar(cnpj):
    return re.sub(r"\D", "", cnpj)


def formatar(cnpj):
    c = limpar(cnpj)
    return f"{c[:2]}.{c[2:5]}.{c[5:8]}/{c[8:12]}-{c[12:]}" if len(c) == 14 else cnpj


def cnpj_valido(cnpj):
    c = limpar(cnpj)
    if len(c) != 14 or c == c[0] * 14:
        return False

    def digito(base, pesos):
        resto = sum(int(d) * p for d, p in zip(base, pesos)) % 11
        return "0" if resto < 2 else str(11 - resto)

    d1 = digito(c[:12], [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
    d2 = digito(c[:12] + d1, [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
    return c[12:] == d1 + d2


def buscar(url):
    req = urllib.request.Request(url, headers={"User-Agent": "adspot-prospector/1.0", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _data_iso(valor):
    if not valor:
        return ""
    m = re.match(r"(\d{2})/(\d{2})/(\d{4})", valor)
    return f"{m.group(3)}-{m.group(2)}-{m.group(1)}" if m else valor[:10]


def _porte(valor):
    v = (valor or "").upper()
    if "MICRO EMPRESA" in v or v in ("ME", "01"):
        return "ME"
    if "PEQUENO" in v or v in ("EPP", "03"):
        return "EPP"
    return v.title() if v else ""


def normalizar_brasilapi(d):
    socios = [
        {"nome": s.get("nome_socio", ""), "qualificacao": s.get("qualificacao_socio", ""),
         "entrada": s.get("data_entrada_sociedade", "")}
        for s in d.get("qsa") or []
    ]
    endereco = ", ".join(filter(None, [
        f"{d.get('descricao_tipo_de_logradouro', '')} {d.get('logradouro', '')}".strip(),
        d.get("numero"), d.get("complemento"), d.get("bairro"),
        f"{d.get('municipio', '')}/{d.get('uf', '')}", d.get("cep"),
    ]))
    cnae = f"{d.get('cnae_fiscal', '')} - {d.get('cnae_fiscal_descricao', '')}".strip(" -")
    return {
        "razao_social": d.get("razao_social", ""),
        "nome_fantasia": d.get("nome_fantasia", ""),
        "situacao": d.get("descricao_situacao_cadastral", ""),
        "abertura": d.get("data_inicio_atividade", ""),
        "porte": "MEI" if d.get("opcao_pelo_mei") else _porte(d.get("porte") or d.get("descricao_porte")),
        "natureza_juridica": d.get("natureza_juridica", ""),
        "cnae": cnae,
        "capital_social": d.get("capital_social"),
        "endereco": endereco,
        "municipio": d.get("municipio", ""),
        "uf": d.get("uf", ""),
        "telefone": d.get("ddd_telefone_1", ""),
        "email": d.get("email") or "",
        "socios": socios,
    }


def normalizar_cnpjws(d):
    est = d.get("estabelecimento") or {}
    socios = [
        {"nome": s.get("nome", ""), "qualificacao": (s.get("qualificacao_socio") or {}).get("descricao", ""),
         "entrada": s.get("data_entrada", "")}
        for s in d.get("socios") or []
    ]
    cidade = (est.get("cidade") or {}).get("nome", "")
    uf = (est.get("estado") or {}).get("sigla", "")
    endereco = ", ".join(filter(None, [
        f"{est.get('tipo_logradouro', '')} {est.get('logradouro', '')}".strip(),
        est.get("numero"), est.get("complemento"), est.get("bairro"), f"{cidade}/{uf}", est.get("cep"),
    ]))
    atividade = est.get("atividade_principal") or {}
    simples = d.get("simples") or {}
    return {
        "razao_social": d.get("razao_social", ""),
        "nome_fantasia": est.get("nome_fantasia") or "",
        "situacao": est.get("situacao_cadastral", ""),
        "abertura": est.get("data_inicio_atividade", ""),
        "porte": "MEI" if simples.get("mei") == "Sim" else _porte((d.get("porte") or {}).get("descricao")),
        "natureza_juridica": (d.get("natureza_juridica") or {}).get("descricao", ""),
        "cnae": f"{atividade.get('subclasse', '')} - {atividade.get('descricao', '')}".strip(" -"),
        "capital_social": float(d["capital_social"]) if d.get("capital_social") else None,
        "endereco": endereco,
        "municipio": cidade,
        "uf": uf,
        "telefone": f"{est.get('ddd1', '')}{est.get('telefone1', '')}",
        "email": est.get("email") or "",
        "socios": socios,
    }


def normalizar_receitaws(d):
    if d.get("status") == "ERROR":
        raise ValueError(d.get("message", "erro ReceitaWS"))
    socios = [{"nome": s.get("nome", ""), "qualificacao": s.get("qual", ""), "entrada": ""} for s in d.get("qsa") or []]
    atividade = (d.get("atividade_principal") or [{}])[0]
    endereco = ", ".join(filter(None, [
        d.get("logradouro"), d.get("numero"), d.get("complemento"), d.get("bairro"),
        f"{d.get('municipio', '')}/{d.get('uf', '')}", d.get("cep"),
    ]))
    capital = d.get("capital_social")
    return {
        "razao_social": d.get("nome", ""),
        "nome_fantasia": d.get("fantasia", ""),
        "situacao": d.get("situacao", ""),
        "abertura": _data_iso(d.get("abertura")),
        "porte": "MEI" if (d.get("simei") or {}).get("optante") else _porte(d.get("porte")),
        "natureza_juridica": d.get("natureza_juridica", ""),
        "cnae": f"{atividade.get('code', '')} - {atividade.get('text', '')}".strip(" -"),
        "capital_social": float(capital) if capital else None,
        "endereco": endereco,
        "municipio": d.get("municipio", ""),
        "uf": d.get("uf", ""),
        "telefone": d.get("telefone", ""),
        "email": d.get("email", ""),
        "socios": socios,
    }


NORMALIZADORES = {"brasilapi": normalizar_brasilapi, "cnpjws": normalizar_cnpjws, "receitaws": normalizar_receitaws}


def sugerir_decisor(dados):
    """Aponta o provável decisor pelo QSA; para MEI/EI sem QSA, extrai o nome da razão social."""
    socios = dados.get("socios") or []
    for s in socios:
        if any(q in (s.get("qualificacao") or "").lower() for q in QUALIFICACOES_DECISOR):
            return {"nome": s["nome"], "qualificacao": s["qualificacao"], "origem": "QSA"}
    if socios:
        s = socios[0]
        return {"nome": s["nome"], "qualificacao": s.get("qualificacao", ""), "origem": "QSA (sem administrador explícito — validar)"}
    nome = re.sub(r"\s*\d{8,14}\s*$", "", dados.get("razao_social", "")).strip()
    if dados.get("porte") == "MEI" or "EMPRESARIO" in (dados.get("natureza_juridica") or "").upper():
        return {"nome": nome, "qualificacao": "Titular (MEI/EI)", "origem": "razão social"}
    return {"nome": "", "qualificacao": "", "origem": "não identificado — validar fora do CNPJ"}


def consultar(cnpj):
    c = limpar(cnpj)
    if not cnpj_valido(c):
        return {"numero": formatar(cnpj), "erro": "CNPJ inválido (dígito verificador)"}
    erros = []
    for nome, url in FONTES:
        try:
            dados = NORMALIZADORES[nome](buscar(url.format(cnpj=c)))
            dados["numero"] = formatar(c)
            dados["fonte"] = url.format(cnpj=c)
            dados["decisor_sugerido"] = sugerir_decisor(dados)
            return dados
        except (urllib.error.URLError, urllib.error.HTTPError, ValueError, KeyError, TimeoutError, OSError) as e:
            erros.append(f"{nome}: {e}")
            time.sleep(1)
    return {"numero": formatar(c), "erro": "; ".join(erros)}


def main():
    p = argparse.ArgumentParser(description="Consulta CNPJ e quadro de sócios (QSA).")
    p.add_argument("cnpjs", nargs="*", help="CNPJs com ou sem pontuação")
    p.add_argument("--arquivo", help="arquivo com um CNPJ por linha")
    p.add_argument("--saida", help="grava o JSON neste caminho em vez de imprimir")
    args = p.parse_args()

    cnpjs = list(args.cnpjs)
    if args.arquivo:
        with open(args.arquivo, encoding="utf-8") as f:
            cnpjs += [linha.strip() for linha in f if linha.strip()]
    if not cnpjs:
        p.error("informe ao menos um CNPJ")

    resultados = []
    for i, cnpj in enumerate(cnpjs):
        if i:
            time.sleep(0.5)
        resultados.append(consultar(cnpj))

    saida = json.dumps(resultados, ensure_ascii=False, indent=2)
    if args.saida:
        with open(args.saida, "w", encoding="utf-8") as f:
            f.write(saida)
        print(f"{len(resultados)} CNPJ(s) gravados em {args.saida}", file=sys.stderr)
    else:
        print(saida)


if __name__ == "__main__":
    main()
