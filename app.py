import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A5, A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from io import BytesIO
from datetime import date
import calendar
import random

MESES = [
    "", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
]

DIAS = [
    "Segunda-feira", "Terça-feira", "Quarta-feira",
    "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"
]

FRASES_BIBLICAS = [
    '"Tudo posso naquele que me fortalece." — Filipenses 4:13',
    '"O Senhor é o meu pastor; nada me faltará." — Salmos 23:1',
    '"Entrega o teu caminho ao Senhor; confia nele." — Salmos 37:5',
    '"Seja forte e corajoso." — Josué 1:9',
    '"Para Deus nada é impossível." — Lucas 1:37',
]

FRASES_MOTIVACIONAIS = [
    "Um passo de cada vez também leva ao destino.",
    "Faça de hoje um dia que vale a pena lembrar.",
    "Pequenos progressos também são progresso.",
    "Você não precisa fazer tudo hoje. Faça o que importa.",
    "Organize seus planos e dê espaço aos seus sonhos.",
]

CORES = {
    "Rosa": "#D88FA0",
    "Azul": "#719AC5",
    "Verde": "#7FA98A",
    "Lilás": "#9A86B8",
    "Bege": "#B99C7A",
    "Preto": "#333333",
}


def cabecalho(pdf, largura, altura, titulo, cor):
    pdf.setFillColor(HexColor(cor))
    pdf.rect(0, altura - 25 * mm, largura, 25 * mm, fill=1, stroke=0)

    pdf.setFillColorRGB(1, 1, 1)
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawCentredString(largura / 2, altura - 16 * mm, titulo)


def linhas_anotacoes(pdf, largura, altura, inicio_y):
    pdf.setStrokeColor(HexColor("#BBBBBB"))
    y = inicio_y

    while y > 18 * mm:
        pdf.line(15 * mm, y, largura - 15 * mm, y)
        y -= 9 * mm


def gerar_agenda(nome, ano, tamanho, cor, incluir_biblicas, incluir_motivacionais):
    buffer = BytesIO()

    pagesize = A5 if tamanho == "A5" else A4
    largura, altura = pagesize

    pdf = canvas.Canvas(buffer, pagesize=pagesize)

    # CAPA
    pdf.setFillColor(HexColor(cor))
    pdf.rect(0, 0, largura, altura, fill=1, stroke=0)

    pdf.setFillColorRGB(1, 1, 1)

    pdf.setFont("Helvetica-Bold", 28)
    pdf.drawCentredString(
        largura / 2,
        altura / 2 + 25 * mm,
        "MINHA AGENDA"
    )

    pdf.setFont("Helvetica", 18)
    pdf.drawCentredString(
        largura / 2,
        altura / 2 + 8 * mm,
        nome
    )

    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawCentredString(
        largura / 2,
        altura / 2 - 8 * mm,
        str(ano)
    )

    pdf.setFont("Helvetica-Oblique", 10)
    pdf.drawCentredString(
        largura / 2,
        25 * mm,
        "Planos, sonhos e propósito."
    )

    pdf.showPage()

    # PÁGINA DE DADOS
    cabecalho(pdf, largura, altura, "Esta agenda pertence a", cor)

    pdf.setFillColorRGB(0.2, 0.2, 0.2)
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawCentredString(largura / 2, altura - 50 * mm, nome)

    pdf.setFont("Helvetica", 11)

    y = altura - 75 * mm

    for texto in [
        "Telefone:",
        "E-mail:",
        "Meu principal objetivo para este ano:",
    ]:
        pdf.drawString(18 * mm, y, texto)
        y -= 8 * mm
        pdf.line(18 * mm, y, largura - 18 * mm, y)
        y -= 15 * mm

    pdf.showPage()

    # CALENDÁRIOS MENSAIS
    cal = calendar.Calendar(firstweekday=0)

    for mes in range(1, 13):
        cabecalho(
            pdf,
            largura,
            altura,
            f"{MESES[mes]} {ano}",
            cor
        )

        semanas = cal.monthdayscalendar(ano, mes)

        margem = 10 * mm
        topo = altura - 40 * mm
        largura_util = largura - (2 * margem)
        largura_coluna = largura_util / 7

        dias_curto = ["SEG", "TER", "QUA", "QUI", "SEX", "SÁB", "DOM"]

        pdf.setFillColorRGB(0.2, 0.2, 0.2)
        pdf.setFont("Helvetica-Bold", 8)

        for i, dia_nome in enumerate(dias_curto):
            x = margem + i * largura_coluna
            pdf.drawCentredString(
                x + largura_coluna / 2,
                topo,
                dia_nome
            )

        y = topo - 8 * mm
        altura_linha = 18 * mm

        pdf.setFont("Helvetica", 9)

        for semana in semanas:
            for i, numero in enumerate(semana):
                x = margem + i * largura_coluna

                pdf.setStrokeColor(HexColor("#CCCCCC"))
                pdf.rect(
                    x,
                    y - altura_linha + 4 * mm,
                    largura_coluna,
                    altura_linha,
                    fill=0,
                    stroke=1
                )

                if numero:
                    pdf.setFillColorRGB(0.2, 0.2, 0.2)
                    pdf.drawString(
                        x + 2 * mm,
                        y,
                        str(numero)
                    )

            y -= altura_linha

        pdf.showPage()

    # CONTROLE DE HÁBITOS
    for mes in range(1, 13):
        cabecalho(
            pdf,
            largura,
            altura,
            f"Hábitos — {MESES[mes]}",
            cor
        )

        pdf.setFillColorRGB(0.2, 0.2, 0.2)
        pdf.setFont("Helvetica", 9)

        habitos = [
            "Hábito 1",
            "Hábito 2",
            "Hábito 3",
            "Hábito 4",
            "Hábito 5",
            "Hábito 6",
        ]

        y = altura - 42 * mm

        for habito in habitos:
            pdf.setFont("Helvetica-Bold", 9)
            pdf.drawString(12 * mm, y, habito)

            pdf.setFont("Helvetica", 6)

            x = 12 * mm

            for dia in range(1, 32):
                pdf.rect(x, y - 7 * mm, 4 * mm, 4 * mm, fill=0)
                pdf.drawCentredString(x + 2 * mm, y - 10 * mm, str(dia))
                x += 4.4 * mm

                if x > largura - 10 * mm:
                    break

            y -= 24 * mm

        pdf.showPage()

    # PÁGINAS DIÁRIAS SEM HORÁRIOS
    inicio = date(ano, 1, 1)
    total_dias = 366 if calendar.isleap(ano) else 365

    for deslocamento in range(total_dias):
        atual = date.fromordinal(inicio.toordinal() + deslocamento)

        titulo = (
            f"{DIAS[atual.weekday()]} — "
            f"{atual.day:02d} {MESES[atual.month].upper()}"
        )

        cabecalho(pdf, largura, altura, titulo, cor)

        pdf.setFillColorRGB(0.2, 0.2, 0.2)

        # Prioridades
        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawString(15 * mm, altura - 38 * mm, "PRIORIDADES")

        y = altura - 48 * mm

        for _ in range(3):
            pdf.rect(15 * mm, y, 4 * mm, 4 * mm, fill=0)
            pdf.line(
                23 * mm,
                y + 1 * mm,
                largura - 15 * mm,
                y + 1 * mm
            )
            y -= 10 * mm

        # Tarefas
        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawString(15 * mm, y - 2 * mm, "TAREFAS")

        y -= 13 * mm

        for _ in range(7):
            pdf.rect(15 * mm, y, 4 * mm, 4 * mm, fill=0)
            pdf.line(
                23 * mm,
                y + 1 * mm,
                largura - 15 * mm,
                y + 1 * mm
            )
            y -= 9 * mm

        # Anotações
        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawString(15 * mm, y - 2 * mm, "ANOTAÇÕES")

        linhas_anotacoes(
            pdf,
            largura,
            altura,
            y - 12 * mm
        )

        # Frase no rodapé
        frases = []

        if incluir_biblicas:
            frases += FRASES_BIBLICAS

        if incluir_motivacionais:
            frases += FRASES_MOTIVACIONAIS

        if frases:
            pdf.setFillColor(HexColor(cor))
            pdf.setFont("Helvetica-Oblique", 7)

            frase = random.choice(frases)

            if len(frase) > 75:
                frase = frase[:72] + "..."

            pdf.drawCentredString(
                largura / 2,
                9 * mm,
                frase
            )

        pdf.showPage()

    # PÁGINAS EXTRAS DE ANOTAÇÕES
    for numero in range(1, 11):
        cabecalho(
            pdf,
            largura,
            altura,
            f"Anotações {numero}",
            cor
        )

        linhas_anotacoes(
            pdf,
            largura,
            altura,
            altura - 40 * mm
        )

        pdf.showPage()

    pdf.save()

    buffer.seek(0)
    return buffer


# INTERFACE STREAMLIT

st.set_page_config(
    page_title="Minha Agenda Personalizada",
    page_icon="📔",
    layout="centered"
)

st.title("📔 Minha Agenda Personalizada")

st.write(
    "Crie uma agenda anual completa e baixe em PDF."
)

nome = st.text_input(
    "Nome na agenda",
    "Minha Agenda"
)

ano = st.number_input(
    "Ano",
    min_value=2025,
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

cor = CORES[cor_nome]

st.markdown("### Frases da agenda")

incluir_biblicas = st.checkbox(
    "Frases bíblicas",
    value=True
)

incluir_motivacionais = st.checkbox(
    "Frases motivacionais",
    value=True
)

st.markdown("### Sua agenda terá")

st.write("✓ Capa personalizada")
st.write("✓ Calendário de todos os meses")
st.write("✓ Controle mensal de hábitos")
st.write("✓ Página para cada dia sem horários")
st.write("✓ Prioridades e tarefas")
st.write("✓ Espaço para anotações")
st.write("✓ Páginas extras de anotações")
st.write("✓ Frases bíblicas e motivacionais")

if st.button(
    "✨ Gerar minha agenda",
    use_container_width=True
):
    with st.spinner("Criando sua agenda..."):
        pdf = gerar_agenda(
            nome,
            int(ano),
            tamanho,
            cor,
            incluir_biblicas,
            incluir_motivacionais
        )

    st.success("Sua agenda está pronta! 💖")

    st.download_button(
        "📥 Baixar agenda em PDF",
        data=pdf,
        file_name=f"minha_agenda_{ano}_{tamanho}.pdf",
        mime="application/pdf",
        use_container_width=True
    )
