import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A5, A4
from reportlab.lib.units import mm
from io import BytesIO
from datetime import date
import calendar

MESES = [
    "", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
]
DIAS = [
    "Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira",
    "Sexta-feira", "Sábado", "Domingo"
]

def gerar_agenda(nome, ano, tamanho, hora_inicio, hora_fim):
    buffer = BytesIO()
    pagesize = A5 if tamanho == "A5" else A4
    largura, altura = pagesize
    pdf = canvas.Canvas(buffer, pagesize=pagesize)

    # Capa
    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawCentredString(largura/2, altura/2 + 12*mm, "AGENDA DIÁRIA")
    pdf.setFont("Helvetica", 16)
    pdf.drawCentredString(largura/2, altura/2, nome)
    pdf.setFont("Helvetica", 13)
    pdf.drawCentredString(largura/2, altura/2 - 10*mm, str(ano))
    pdf.showPage()

    inicio = date(ano, 1, 1)
    total_dias = 366 if calendar.isleap(ano) else 365

    for deslocamento in range(total_dias):
        atual = date.fromordinal(inicio.toordinal() + deslocamento)

        margem = 12 * mm
        topo = altura - 14 * mm

        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawString(margem, topo, DIAS[atual.weekday()].upper())

        pdf.setFont("Helvetica-Bold", 17)
        data_txt = f"{atual.day:02d} {MESES[atual.month].upper()} {atual.year}"
        pdf.drawString(margem, topo - 8*mm, data_txt)

        pdf.setLineWidth(0.6)
        pdf.line(margem, topo - 12*mm, largura - margem, topo - 12*mm)

        y = topo - 20*mm
        horas = list(range(hora_inicio, hora_fim + 1))
        espaco_disponivel = altura - 70*mm
        passo = min(8*mm, espaco_disponivel / max(len(horas), 1))

        pdf.setFont("Helvetica", 8)
        for hora in horas:
            pdf.drawString(margem, y, f"{hora:02d}:00")
            pdf.line(margem + 14*mm, y - 1*mm, largura - margem, y - 1*mm)
            y -= passo

        # Rodapé útil
        y2 = 30 * mm
        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawString(margem, y2, "PRIORIDADES")
        pdf.setFont("Helvetica", 8)
        for i in range(3):
            yy = y2 - (i+1)*5*mm
            pdf.rect(margem, yy, 3*mm, 3*mm)
            pdf.line(margem + 6*mm, yy + 1*mm, largura - margem, yy + 1*mm)

        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawRightString(largura - margem, 8*mm, f"{atual.strftime('%d/%m/%Y')}")
        pdf.showPage()

    pdf.save()
    buffer.seek(0)
    return buffer.getvalue()

st.set_page_config(page_title="Gerador de Agenda Diária", page_icon="📔", layout="centered")

st.title("📔 Gerador de Agenda Diária")
st.write("Preencha os campos abaixo e gere sua agenda personalizada em PDF.")

nome = st.text_input("Nome na agenda", "Minha Agenda")
ano = st.number_input("Ano", min_value=2024, max_value=2100, value=2027, step=1)
tamanho = st.selectbox("Tamanho", ["A5", "A4"])

col1, col2 = st.columns(2)
with col1:
    hora_inicio = st.number_input("Primeiro horário", min_value=0, max_value=23, value=6)
with col2:
    hora_fim = st.number_input("Último horário", min_value=0, max_value=23, value=22)

if hora_fim < hora_inicio:
    st.error("O último horário precisa ser maior ou igual ao primeiro.")
else:
    if st.button("Gerar minha agenda", type="primary", use_container_width=True):
        with st.spinner("Criando a agenda..."):
            arquivo = gerar_agenda(nome, int(ano), tamanho, int(hora_inicio), int(hora_fim))
        st.success("Agenda criada!")
        st.download_button(
            "Baixar agenda em PDF",
            data=arquivo,
            file_name=f"agenda_diaria_{ano}_{tamanho}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

st.caption("Primeira versão do seu robô gerador de agendas.")
