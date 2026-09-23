import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, A5
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, black, white
from io import BytesIO
from datetime import date
import calendar
import random


# =========================================================
# CONFIGURAÇÕES
# =========================================================

st.set_page_config(
    page_title="Minha Agenda",
    page_icon="🌷",
    layout="centered"
)

MESES = [
    "",
    "Janeiro", "Fevereiro", "Março", "Abril",
    "Maio", "Junho", "Julho", "Agosto",
    "Setembro", "Outubro", "Novembro", "Dezembro"
]

DIAS = [
    "Segunda-feira",
    "Terça-feira",
    "Quarta-feira",
    "Quinta-feira",
    "Sexta-feira",
    "Sábado",
    "Domingo"
]

CORES = {
    "Rosa": "#D88FA0",
    "Rosa claro": "#E8B7BF",
    "Pêssego": "#E6B89C",
    "Bege": "#D7C2AE",
    "Verde": "#91A88F",
    "Azul": "#7FA9C5",
    "Lavanda": "#A99AC5"
}

FONTES = {
    "Moderna": {
        "normal": "Helvetica",
        "negrito": "Helvetica-Bold",
        "italico": "Helvetica-Oblique"
    },
    "Clássica": {
        "normal": "Times-Roman",
        "negrito": "Times-Bold",
        "italico": "Times-Italic"
    },
    "Elegante": {
        "normal": "Times-Roman",
        "negrito": "Times-BoldItalic",
        "italico": "Times-Italic"
    },
    "Criativa": {
        "normal": "Courier",
        "negrito": "Courier-Bold",
        "italico": "Courier-Oblique"
    }
}

FRASES_BIBLICAS = [
    '"Tudo posso naquele que me fortalece." - Filipenses 4:13',
    '"O Senhor é o meu pastor; nada me faltará." - Salmos 23:1',
    '"Entrega o teu caminho ao Senhor; confia nele." - Salmos 37:5',
    '"Seja forte e corajoso." - Josué 1:9',
    '"Para Deus nada é impossível." - Lucas 1:37',
    '"Tudo tem o seu tempo determinado." - Eclesiastes 3:1',
    '"Alegrai-vos na esperança." - Romanos 12:12',
    '"Confia no Senhor de todo o teu coração." - Provérbios 3:5'
]

FRASES_MOTIVACIONAIS = [
    "Um passo de cada vez também leva ao destino.",
    "Faça de hoje um dia que vale a pena lembrar.",
    "Pequenos progressos também são progressos.",
    "Você não precisa fazer tudo hoje. Faça o que importa.",
    "Organize seus planos e dê espaço aos seus sonhos.",
    "Disciplina hoje é liberdade amanhã.",
    "O segredo é começar.",
    "Cada dia é uma nova oportunidade."
]


# =========================================================
# FUNÇÕES DE DESENHO
# =========================================================

def clarear_cor(hex_cor):
    """Cria uma versão muito clara da cor escolhida."""
    h = hex_cor.lstrip("#")
    r = int(h[0:2], 16)
    g = int(h[2:4], 16)
    b = int(h[4:6], 16)

    r = int(r + (255 - r) * 0.82)
    g = int(g + (255 - g) * 0.82)
    b = int(b + (255 - b) * 0.82)

    return HexColor(f"#{r:02X}{g:02X}{b:02X}")


def desenhar_folha(pdf, x, y, tamanho, cor, inclinacao=1):
    """Desenha uma pequena folha decorativa."""
    pdf.saveState()
    pdf.setFillColor(cor)
    pdf.setStrokeColor(cor)

    if inclinacao >= 0:
        pontos = [
            x, y,
            x + tamanho, y + tamanho * 0.25,
            x + tamanho * 0.75, y + tamanho
        ]
    else:
        pontos = [
            x, y,
            x - tamanho, y + tamanho * 0.25,
            x - tamanho * 0.75, y + tamanho
        ]

    caminho = pdf.beginPath()
    caminho.moveTo(pontos[0], pontos[1])
    caminho.curveTo(
        pontos[2], pontos[3],
        pontos[4], pontos[5],
        pontos[0], pontos[1]
    )
    pdf.drawPath(caminho, fill=1, stroke=0)
    pdf.restoreState()


def desenhar_flor(pdf, x, y, tamanho, cor):
    """Flor delicada feita com círculos."""
    pdf.saveState()
    pdf.setFillColor(cor)

    raio = tamanho * 0.28

    pdf.circle(x, y + tamanho * 0.35, raio, fill=1, stroke=0)
    pdf.circle(x + tamanho * 0.35, y, raio, fill=1, stroke=0)
    pdf.circle(x, y - tamanho * 0.35, raio, fill=1, stroke=0)
    pdf.circle(x - tamanho * 0.35, y, raio, fill=1, stroke=0)

    pdf.setFillColor(HexColor("#F4D6A0"))
    pdf.circle(x, y, tamanho * 0.17, fill=1, stroke=0)

    pdf.restoreState()


def decoracao_canto(pdf, largura, altura, cor, lado="esquerdo"):
    """Desenha folhas e flores discretas no canto."""
    cor_folha = HexColor("#8FA58B")
    cor_flor = HexColor(cor)

    pdf.saveState()

    if lado == "esquerdo":
        x = 9 * mm
        sinal = 1
    else:
        x = largura - 9 * mm
        sinal = -1

    y = altura - 12 * mm

    pdf.setStrokeColor(cor_folha)
    pdf.setLineWidth(0.8)

    pdf.line(
        x,
        y,
        x + sinal * 19 * mm,
        y - 26 * mm
    )

    desenhar_folha(
        pdf, x + sinal * 4 * mm,
        y - 6 * mm,
        6 * mm,
        cor_folha,
        sinal
    )

    desenhar_folha(
        pdf, x + sinal * 8 * mm,
        y - 13 * mm,
        5 * mm,
        cor_folha,
        -sinal
    )

    desenhar_folha(
        pdf, x + sinal * 12 * mm,
        y - 19 * mm,
        6 * mm,
        cor_folha,
        sinal
    )

    desenhar_flor(
        pdf,
        x + sinal * 5 * mm,
        y - 3 * mm,
        5 * mm,
        cor_flor
    )

    pdf.restoreState()


def titulo_pagina(
    pdf,
    largura,
    altura,
    texto,
    cor,
    fonte_negrito,
    tamanho=18,
    decorar=True
):
    """Cabeçalho limpo."""
    cor_principal = HexColor(cor)

    pdf.setFillColor(clarear_cor(cor))
    pdf.rect(
        0,
        altura - 27 * mm,
        largura,
        27 * mm,
        fill=1,
        stroke=0
    )

    pdf.setFillColor(cor_principal)
    pdf.setFont(fonte_negrito, tamanho)
    pdf.drawCentredString(
        largura / 2,
        altura - 17 * mm,
        texto
    )

    if decorar:
        decoracao_canto(
            pdf,
            largura,
            altura,
            cor,
            "esquerdo"
        )


def linha(pdf, x1, y, x2, cor="#B7B7B7"):
    pdf.setStrokeColor(HexColor(cor))
    pdf.setLineWidth(0.55)
    pdf.line(x1, y, x2, y)


def checkbox(pdf, x, y, tamanho=4 * mm):
    pdf.setStrokeColor(HexColor("#777777"))
    pdf.setLineWidth(0.7)
    pdf.rect(
        x,
        y,
        tamanho,
        tamanho,
        fill=0,
        stroke=1
    )


def texto_centralizado(
    pdf,
    texto,
    largura,
    y,
    fonte,
    tamanho,
    cor=black
):
    pdf.setFillColor(cor)
    pdf.setFont(fonte, tamanho)
    pdf.drawCentredString(
        largura / 2,
        y,
        texto
    )


# =========================================================
# CAPA
# =========================================================

def pagina_capa(
    pdf,
    largura,
    altura,
    nome,
    ano,
    cor,
    fontes
):
    principal = HexColor(cor)
    fundo = clarear_cor(cor)

    pdf.setFillColor(fundo)
    pdf.rect(
        0,
        0,
        largura,
        altura,
        fill=1,
        stroke=0
    )

    # moldura
    pdf.setStrokeColor(principal)
    pdf.setLineWidth(1.2)
    pdf.rect(
        8 * mm,
        8 * mm,
        largura - 16 * mm,
        altura - 16 * mm,
        fill=0,
        stroke=1
    )

    # flores
    decoracao_canto(
        pdf, largura, altura, cor, "esquerdo"
    )
    decoracao_canto(
        pdf, largura, altura, cor, "direito"
    )

    desenhar_flor(
        pdf,
        18 * mm,
        24 * mm,
        8 * mm,
        principal
    )

    desenhar_flor(
        pdf,
        largura - 18 * mm,
        24 * mm,
        8 * mm,
        principal
    )

    pdf.setFillColor(HexColor("#333333"))
    pdf.setFont(fontes["negrito"], 25)
    pdf.drawCentredString(
        largura / 2,
        altura * 0.62,
        "AGENDA"
    )

    pdf.drawCentredString(
        largura / 2,
        altura * 0.62 - 10 * mm,
        "DIÁRIA"
    )

    pdf.setFillColor(principal)
    pdf.setFont(fontes["italico"], 19)
    pdf.drawCentredString(
        largura / 2,
        altura * 0.49,
        nome
    )

    pdf.setFillColor(HexColor("#444444"))
    pdf.setFont(fontes["negrito"], 14)
    pdf.drawCentredString(
        largura / 2,
        altura * 0.42,
        str(ano)
    )

    pdf.setFont(fontes["italico"], 10)
    pdf.setFillColor(HexColor("#555555"))
    pdf.drawCentredString(
        largura / 2,
        25 * mm,
        "Planos, sonhos e propósito."
    )

    pdf.showPage()


# =========================================================
# DADOS PESSOAIS
# =========================================================

def pagina_dados(
    pdf,
    largura,
    altura,
    nome,
    cor,
    fontes
):
    titulo_pagina(
        pdf,
        largura,
        altura,
        "Meus Dados",
        cor,
        fontes["negrito"],
        19
    )

    margem = 20 * mm
    y = altura - 48 * mm

    pdf.setFillColor(HexColor("#333333"))
    pdf.setFont(fontes["negrito"], 15)
    pdf.drawString(
        margem,
        y,
        nome
    )

    y -= 19 * mm

    campos = [
        "Telefone:",
        "E-mail:",
        "Endereço:",
        "Emergência:",
        "Meu principal objetivo para este ano:"
    ]

    for campo in campos:
        pdf.setFont(fontes["normal"], 10)
        pdf.setFillColor(HexColor("#444444"))
        pdf.drawString(
            margem,
            y,
            campo
        )

        linha(
            pdf,
            margem,
            y - 5 * mm,
            largura - margem
        )

        y -= 21 * mm

    pdf.setFont(fontes["italico"], 10)
    pdf.setFillColor(HexColor(cor))
    pdf.drawCentredString(
        largura / 2,
        18 * mm,
        "Planos bem feitos conduzem a grandes sonhos."
    )

    pdf.showPage()


# =========================================================
# CALENDÁRIO ANUAL
# =========================================================

def pagina_calendario_anual(
    pdf,
    largura,
    altura,
    ano,
    cor,
    fontes
):
    titulo_pagina(
        pdf,
        largura,
        altura,
        f"Calendário {ano}",
        cor,
        fontes["negrito"],
        18
    )

    margem = 10 * mm
    topo = altura - 39 * mm

    colunas = 3
    linhas = 4

    largura_bloco = (
        largura - 2 * margem
    ) / colunas

    altura_bloco = (
        topo - 14 * mm
    ) / linhas

    cal = calendar.Calendar(
        firstweekday=0
    )

    for mes in range(1, 13):
        indice = mes - 1

        coluna = indice % 3
        linha_mes = indice // 3

        x = margem + coluna * largura_bloco
        y_topo = topo - linha_mes * altura_bloco

        pdf.setFillColor(HexColor(cor))
        pdf.setFont(fontes["negrito"], 8)

        pdf.drawCentredString(
            x + largura_bloco / 2,
            y_topo,
            MESES[mes].upper()
        )

        dias_semana = [
            "S", "T", "Q",
            "Q", "S", "S", "D"
        ]

        pdf.setFillColor(HexColor("#555555"))
        pdf.setFont(fontes["negrito"], 5.5)

        largura_dia = (
            largura_bloco - 4 * mm
        ) / 7

        for i, d in enumerate(dias_semana):
            pdf.drawCentredString(
                x + 2 * mm +
                i * largura_dia +
                largura_dia / 2,
                y_topo - 6 * mm,
                d
            )

        semanas = cal.monthdayscalendar(
            ano,
            mes
        )

        pdf.setFont(fontes["normal"], 5.5)

        for s, semana in enumerate(semanas):
            for d, numero in enumerate(semana):
                if numero:
                    pdf.drawCentredString(
                        x + 2 * mm +
                        d * largura_dia +
                        largura_dia / 2,
                        y_topo -
                        11 * mm -
                        s * 5 * mm,
                        str(numero)
                    )

    pdf.showPage()


# =========================================================
# PLANEJAMENTO MENSAL
# =========================================================

def pagina_planejamento_mensal(
    pdf,
    largura,
    altura,
    ano,
    mes,
    cor,
    fontes
):
    titulo_pagina(
        pdf,
        largura,
        altura,
        f"Planejamento — {MESES[mes]}",
        cor,
        fontes["negrito"],
        17
    )

    margem = 10 * mm
    topo = altura - 43 * mm

    cal = calendar.Calendar(
        firstweekday=0
    )

    semanas = cal.monthdayscalendar(
        ano,
        mes
    )

    largura_grade = largura - 2 * margem
    largura_celula = largura_grade / 7

    altura_grade = 73 * mm
    altura_celula = altura_grade / 6

    dias = [
        "SEG", "TER", "QUA",
        "QUI", "SEX", "SÁB", "DOM"
    ]

    pdf.setFont(fontes["negrito"], 7)
    pdf.setFillColor(HexColor("#444444"))

    for i, dia in enumerate(dias):
        pdf.drawCentredString(
            margem +
            i * largura_celula +
            largura_celula / 2,
            topo,
            dia
        )

    y_inicio = topo - 5 * mm

    pdf.setStrokeColor(HexColor("#C5C5C5"))
    pdf.setLineWidth(0.5)

    for r in range(7):
        y = y_inicio - r * altura_celula
        pdf.line(
            margem,
            y,
            margem + largura_grade,
            y
        )

    for c in range(8):
        x = margem + c * largura_celula
        pdf.line(
            x,
            y_inicio,
            x,
            y_inicio - 6 * altura_celula
        )

    pdf.setFont(fontes["normal"], 7)
    pdf.setFillColor(HexColor("#333333"))

    for r, semana in enumerate(semanas):
        for c, numero in enumerate(semana):
            if numero:
                pdf.drawString(
                    margem +
                    c * largura_celula +
                    2 * mm,
                    y_inicio -
                    r * altura_celula -
                    4 * mm,
                    str(numero)
                )

    y = y_inicio - 6 * altura_celula - 12 * mm

    pdf.setFillColor(HexColor(cor))
    pdf.setFont(fontes["negrito"], 10)
    pdf.drawString(
        margem,
        y,
        "Metas do mês"
    )

    pdf.drawString(
        largura / 2 + 3 * mm,
        y,
        "Importante"
    )

    for i in range(5):
        yy = y - 8 * mm - i * 8 * mm

        checkbox(
            pdf,
            margem,
            yy
        )

        linha(
            pdf,
            margem + 7 * mm,
            yy + 1 * mm,
            largura / 2 - 4 * mm
        )

        linha(
            pdf,
            largura / 2 + 3 * mm,
            yy + 1 * mm,
            largura - margem
        )

    pdf.showPage()


# =========================================================
# HÁBITOS
# =========================================================

def pagina_habitos(
    pdf,
    largura,
    altura,
    ano,
    mes,
    cor,
    fontes
):
    titulo_pagina(
        pdf,
        largura,
        altura,
        f"Meus Hábitos — {MESES[mes]}",
        cor,
        fontes["negrito"],
        17
    )

    margem = 9 * mm
    y = altura - 47 * mm

    total_dias = calendar.monthrange(
        ano,
        mes
    )[1]

    largura_disponivel = (
        largura - 2 * margem
    )

    largura_nome = 25 * mm

    largura_quadrado = (
        largura_disponivel -
        largura_nome
    ) / total_dias

    largura_quadrado = min(
        largura_quadrado,
        4.7 * mm
    )

    for habito in range(1, 7):
        pdf.setFillColor(HexColor("#333333"))
        pdf.setFont(fontes["negrito"], 8)

        pdf.drawString(
            margem,
            y + 1 * mm,
            f"Hábito {habito}"
        )

        x_inicio = margem + largura_nome

        for dia in range(1, total_dias + 1):
            x = (
                x_inicio +
                (dia - 1) *
                largura_quadrado
            )

            pdf.setStrokeColor(
                HexColor("#888888")
            )

            pdf.rect(
                x,
                y,
                largura_quadrado - 0.3,
                4 * mm,
                fill=0,
                stroke=1
            )

            pdf.setFont(
                fontes["normal"],
                4.5
            )

            pdf.drawCentredString(
                x +
                largura_quadrado / 2,
                y - 2.5 * mm,
                str(dia)
            )

        y -= 22 * mm

    pdf.setFillColor(HexColor(cor))
    pdf.setFont(fontes["negrito"], 10)
    pdf.drawString(
        margem,
        35 * mm,
        "Reflexão do mês"
    )

    for i in range(4):
        linha(
            pdf,
            margem,
            28 * mm - i * 7 * mm,
            largura - margem
        )

    pdf.showPage()


# =========================================================
# METAS
# =========================================================

def pagina_metas(
    pdf,
    largura,
    altura,
    cor,
    fontes
):
    titulo_pagina(
        pdf,
        largura,
        altura,
        "Minhas Metas",
        cor,
        fontes["negrito"],
        19
    )

    categorias = [
        "Pessoais",
        "Profissionais",
        "Espirituais",
        "Saúde e bem-estar"
    ]

    margem = 18 * mm
    y = altura - 50 * mm

    for categoria in categorias:
        pdf.setFillColor(HexColor(cor))
        pdf.setFont(fontes["negrito"], 11)

        pdf.drawString(
            margem,
            y,
            categoria
        )

        y -= 8 * mm

        for i in range(4):
            checkbox(
                pdf,
                margem,
                y
            )

            linha(
                pdf,
                margem + 7 * mm,
                y + 1 * mm,
                largura - margem
            )

            y -= 8 * mm

        y -= 7 * mm

    pdf.showPage()


# =========================================================
# FINANCEIRO
# =========================================================

def pagina_financeiro(
    pdf,
    largura,
    altura,
    cor,
    fontes
):
    titulo_pagina(
        pdf,
        largura,
        altura,
        "Controle Financeiro",
        cor,
        fontes["negrito"],
        18
    )

    margem = 10 * mm
    topo = altura - 48 * mm

    colunas = [
        ("Data", 0.15),
        ("Descrição", 0.43),
        ("Entrada", 0.21),
        ("Saída", 0.21)
    ]

    largura_total = largura - 2 * margem

    x = margem

    pdf.setFillColor(clarear_cor(cor))
    pdf.rect(
        margem,
        topo,
        largura_total,
        9 * mm,
        fill=1,
        stroke=0
    )

    pdf.setFillColor(HexColor("#333333"))
    pdf.setFont(fontes["negrito"], 7)

    xs = [margem]

    for titulo, proporcao in colunas:
        largura_col = largura_total * proporcao

        pdf.drawCentredString(
            x + largura_col / 2,
            topo + 3 * mm,
            titulo
        )

        x += largura_col
        xs.append(x)

    altura_linha = 8 * mm
    linhas = 14

    pdf.setStrokeColor(HexColor("#C4C4C4"))
    pdf.setLineWidth(0.5)

    for i in range(linhas + 1):
        y = topo - i * altura_linha
        pdf.line(
            margem,
            y,
            margem + largura_total,
            y
        )

    for xx in xs:
        pdf.line(
            xx,
            topo + 9 * mm,
            xx,
            topo - linhas * altura_linha
        )

    y_resumo = topo - linhas * altura_linha - 13 * mm

    pdf.setFillColor(HexColor(cor))
    pdf.setFont(fontes["negrito"], 10)
    pdf.drawString(
        margem,
        y_resumo,
        "Resumo do mês"
    )

    itens = [
        "Total de entradas:",
        "Total de saídas:",
        "Saldo:"
    ]

    for i, item in enumerate(itens):
        yy = y_resumo - 9 * mm - i * 8 * mm

        pdf.setFillColor(HexColor("#444444"))
        pdf.setFont(fontes["normal"], 8)

        pdf.drawString(
            margem,
            yy,
            item
        )

        linha(
            pdf,
            margem + 34 * mm,
            yy,
            largura - margem
        )

    pdf.showPage()


# =========================================================
# PÁGINA DIÁRIA
# =========================================================

def pagina_diaria(
    pdf,
    largura,
    altura,
    atual,
    cor,
    fontes,
    usar_biblica,
    usar_motivacional
):
    dia_semana = DIAS[
        atual.weekday()
    ]

    titulo = (
        f"{dia_semana} — "
        f"{atual.day:02d} "
        f"{MESES[atual.month].upper()}"
    )

    titulo_pagina(
        pdf,
        largura,
        altura,
        titulo,
        cor,
        fontes["negrito"],
        14,
        False
    )

    # decoração pequena
    decoracao_canto(
        pdf,
        largura,
        altura,
        cor,
        "direito"
    )

    margem = 14 * mm
    y = altura - 45 * mm

    # frase
    frase = None

    if usar_biblica and usar_motivacional:
        if atual.day % 2 == 0:
            frase = FRASES_BIBLICAS[
                atual.toordinal() %
                len(FRASES_BIBLICAS)
            ]
        else:
            frase = FRASES_MOTIVACIONAIS[
                atual.toordinal() %
                len(FRASES_MOTIVACIONAIS)
            ]

    elif usar_biblica:
        frase = FRASES_BIBLICAS[
            atual.toordinal() %
            len(FRASES_BIBLICAS)
        ]

    elif usar_motivacional:
        frase = FRASES_MOTIVACIONAIS[
            atual.toordinal() %
            len(FRASES_MOTIVACIONAIS)
        ]

    if frase:
        pdf.setFillColor(clarear_cor(cor))
        pdf.roundRect(
            margem,
            y - 15 * mm,
            largura - 2 * margem,
            15 * mm,
            3 * mm,
            fill=1,
            stroke=0
        )

        pdf.setFillColor(HexColor("#555555"))
        pdf.setFont(fontes["italico"], 7)

        # quebra simples
        if len(frase) > 58:
            metade = len(frase) // 2
            corte = frase.rfind(
                " ",
                0,
                metade
            )

            if corte == -1:
                corte = metade

            parte1 = frase[:corte]
            parte2 = frase[corte + 1:]

            pdf.drawCentredString(
                largura / 2,
                y - 6 * mm,
                parte1
            )

            pdf.drawCentredString(
                largura / 2,
                y - 10 * mm,
                parte2
            )

        else:
            pdf.drawCentredString(
                largura / 2,
                y - 8 * mm,
                frase
            )

        y -= 25 * mm

    # prioridades
    pdf.setFillColor(HexColor(cor))
    pdf.setFont(fontes["negrito"], 11)

    pdf.drawString(
        margem,
        y,
        "PRIORIDADES"
    )

    y -= 9 * mm

    for i in range(3):
        checkbox(
            pdf,
            margem,
            y
        )

        linha(
            pdf,
            margem + 8 * mm,
            y + 1 * mm,
            largura - margem
        )

        y -= 10 * mm

    y -= 4 * mm

    # tarefas
    pdf.setFillColor(HexColor(cor))
    pdf.setFont(fontes["negrito"], 11)

    pdf.drawString(
        margem,
        y,
        "TAREFAS"
    )

    y -= 9 * mm
    
            
        

        
        
            
============================================================
    # NOVO LAYOUT DA PÁGINA DIÁRIA
    # Modelo limpo com área de escrita
    # ============================================================

    margem = 14 * mm

    # ------------------------------------------------------------
    # ÁREA "IMPORTANTE"
    # ------------------------------------------------------------

    y_importante = y - 20 * mm

    pdf.setFillColor(HexColor(cor))
    pdf.setFont(fontes["negrito"], 10)

    pdf.drawString(
        margem,
        y_importante,
        "Importante:"
    )

    # Caixa suave para anotações importantes
    pdf.setFillColor(clarear_cor(cor))
    pdf.roundRect(
        margem,
        y_importante - 22 * mm,
        largura * 0.58,
        18 * mm,
        3 * mm,
        fill=1,
        stroke=0
    )

    # ------------------------------------------------------------
    # INDICADORES DECORATIVOS
    # ------------------------------------------------------------

    raio = 4 * mm
    inicio_x = largura - margem - 30 * mm
    circulo_y = y_importante - 10 * mm

    pdf.setFillColor(HexColor(cor))

    for i in range(3):
        pdf.circle(
            inicio_x + i * 10 * mm,
            circulo_y,
            raio,
            fill=1,
            stroke=0
        )

    # Dias da semana pequenos
    pdf.setFillColor(HexColor("#555555"))
    pdf.setFont(fontes["normal"], 6)

    dias_curto = ["S", "T", "Q", "Q", "S", "S", "D"]

    texto_dias = "  ".join(dias_curto)

    pdf.drawCentredString(
        largura - margem - 20 * mm,
        circulo_y - 9 * mm,
        texto_dias
    )

    # ------------------------------------------------------------
    # ÁREA PRINCIPAL PARA ESCREVER
    # ------------------------------------------------------------

    inicio_linhas = y_importante - 34 * mm
    fim_linhas = 57 * mm

    pdf.setStrokeColor(HexColor("#B8B8B8"))
    pdf.setLineWidth(0.35)

    y_linha = inicio_linhas

    while y_linha > fim_linhas:

        pdf.line(
            margem,
            y_linha,
            largura - margem,
            y_linha
        )

        y_linha -= 8 * mm

    # ------------------------------------------------------------
    # BLOCO INFERIOR — PRIORIDADES
    # ------------------------------------------------------------

    base_y = 18 * mm

    largura_esquerda = (largura - 3 * margem) / 2
    largura_direita = largura_esquerda

    pdf.setFillColor(HexColor(cor))
    pdf.setFont(fontes["negrito"], 9)

    pdf.drawString(
        margem,
        base_y + 28 * mm,
        "Prioridades:"
    )

    pdf.setFillColor(clarear_cor(cor))

    for i in range(4):

        pdf.roundRect(
            margem,
            base_y + (20 - i * 6) * mm,
            largura_esquerda,
            4.5 * mm,
            2 * mm,
            fill=1,
            stroke=0
        )

    # ------------------------------------------------------------
    # BLOCO INFERIOR — RESUMO DO DIA
    # ------------------------------------------------------------

    x_resumo = margem * 2 + largura_esquerda

    pdf.setFillColor(HexColor(cor))
    pdf.setFont(fontes["negrito"], 9)

    pdf.drawString(
        x_resumo,
        base_y + 28 * mm,
        "Resumo do dia:"
    )

    pdf.setFillColor(clarear_cor(cor))

    pdf.roundRect(
        x_resumo,
        base_y,
        largura_direita,
        24 * mm,
        3 * mm,
        fill=1,
        stroke=0
    )

    # ------------------------------------------------------------
    # PEQUENA DECORAÇÃO NOS CANTOS INFERIORES
    # Usa a mesma função floral já existente na agenda
    # ------------------------------------------------------------

    decoracao_canto(
        pdf,
        largura,
        altura,
        cor,
        "esquerdo"
    )

    # Finaliza a página diária
    pdf.showPage()
            
        

        






    

    
    
        

    

    
        
        
            
        
            
            
        

        

    







    
    
    
                                     
    

    
        

    
        
        
    
        
        
        
        


    

    
    

    
        
            
            
            
        
            
       

     

    
    )

    pdf.showPage()


# =========================================================
# GERAR PDF
# =========================================================

def gerar_agenda(
    nome,
    ano,
    tamanho,
    cor_nome,
    fonte_nome,
    biblicas,
    motivacionais,
    paginas_anotacoes
):
    buffer = BytesIO()

    pagesize = A5 if tamanho == "A5" else A4
    largura, altura = pagesize

    pdf = canvas.Canvas(
        buffer,
        pagesize=pagesize
    )

    cor = CORES[cor_nome]
    fontes = FONTES[fonte_nome]

    # CAPA
    pagina_capa(
        pdf,
        largura,
        altura,
        nome,
        ano,
        cor,
        fontes
    )

    # DADOS
    pagina_dados(
        pdf,
        largura,
        altura,
        nome,
        cor,
        fontes
    )

    # CALENDÁRIO ANUAL
    pagina_calendario_anual(
        pdf,
        largura,
        altura,
        ano,
        cor,
        fontes
    )

    # CADA MÊS
    for mes in range(1, 13):

        pagina_planejamento_mensal(
            pdf,
            largura,
            altura,
            ano,
            mes,
            cor,
            fontes
        )

        pagina_habitos(
            pdf,
            largura,
            altura,
            ano,
            mes,
            cor,
            fontes
        )

        pagina_metas(
            pdf,
            largura,
            altura,
            cor,
            fontes
        )

        pagina_financeiro(
            pdf,
            largura,
            altura,
            cor,
            fontes
        )

        total_dias = calendar.monthrange(
            ano,
            mes
        )[1]

        for dia in range(
            1,
            total_dias + 1
        ):
            atual = date(
                ano,
                mes,
                dia
            )

            pagina_diaria(
                pdf,
                largura,
                altura,
                atual,
                cor,
                fontes,
                biblicas,
                motivacionais
            )

    # ANOTAÇÕES EXTRAS
    for numero in range(
        1,
        paginas_anotacoes + 1
    ):
        pagina_anotacoes(
            pdf,
            largura,
            altura,
            cor,
            fontes,
            numero
        )

    pdf.save()

    buffer.seek(0)

    return buffer


# =========================================================
# INTERFACE STREAMLIT
# =========================================================

st.title("🌷 Minha Agenda Personalizada")

st.write(
    "Crie uma agenda anual bonita, limpa e personalizada."
)

st.divider()

nome = st.text_input(
    "Nome na agenda",
    value="Minha Agenda"
)

ano = st.number_input(
    "Ano",
    min_value=2024,
    max_value=2100,
    value=2027,
    step=1
)

tamanho = st.selectbox(
    "Tamanho da agenda",
    ["A5", "A4"]
)

cor_nome = st.selectbox(
    "Cor da agenda",
    list(CORES.keys())
)

st.subheader("✍️ Estilo da escrita")

fonte_nome = st.selectbox(
    "Fonte da agenda",
    [
        "Elegante",
        "Moderna",
        "Clássica",
        "Criativa"
    ]
)

if fonte_nome == "Elegante":
    st.caption(
        "Visual delicado e sofisticado."
    )

elif fonte_nome == "Moderna":
    st.caption(
        "Visual limpo e minimalista."
    )

elif fonte_nome == "Clássica":
    st.caption(
        "Visual tradicional e refinado."
    )

else:
    st.caption(
        "Visual diferente e descontraído."
    )

st.subheader("💬 Frases da agenda")

biblicas = st.checkbox(
    "Frases bíblicas",
    value=True
)

motivacionais = st.checkbox(
    "Frases motivacionais",
    value=True
)

st.subheader("📝 Páginas extras")

paginas_anotacoes = st.slider(
    "Quantidade de páginas extras de anotações",
    min_value=2,
    max_value=20,
    value=6
)

st.subheader("Sua agenda terá")

st.write("✓ Capa personalizada com detalhes florais")
st.write("✓ Página de dados pessoais")
st.write("✓ Calendário anual")
st.write("✓ Planejamento de todos os meses")
st.write("✓ Controle mensal de hábitos")
st.write("✓ Metas")
st.write("✓ Controle financeiro")
st.write("✓ Página para cada dia sem horários")
st.write("✓ Prioridades e tarefas")
st.write("✓ Espaço para anotações")
st.write("✓ Frases bíblicas e motivacionais")
st.write("✓ Escolha de cores")
st.write("✓ Escolha do estilo de fonte")
st.write("✓ Detalhes florais discretos")

st.divider()

if st.button(
    "✨ Gerar minha agenda",
    use_container_width=True
):
    with st.spinner(
        "Criando sua agenda..."
    ):
        pdf_buffer = gerar_agenda(
            nome=nome,
            ano=int(ano),
            tamanho=tamanho,
            cor_nome=cor_nome,
            fonte_nome=fonte_nome,
            biblicas=biblicas,
            motivacionais=motivacionais,
            paginas_anotacoes=paginas_anotacoes
        )

    st.success(
        "Sua agenda ficou pronta! 🌷"
    )

    nome_arquivo = (
        f"minha_agenda_{int(ano)}_{tamanho}.pdf"
    )

    st.download_button(
        label="📥 Baixar minha agenda em PDF",
        data=pdf_buffer,
        file_name=nome_arquivo,
        mime="application/pdf",
        use_container_width=True
    )
