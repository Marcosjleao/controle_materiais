from flask import Flask, render_template, request, redirect, url_for, session, send_file, jsonify, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from flask_mail import Mail, Message
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "chave_super_secreta"

# Configuração do e-mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER', 'seu_email@gmail.com')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASS', 'sua_senha')
mail = Mail(app)

# Criar Banco de Dados
def criar_banco():
    conn = sqlite3.connect('gestao_materiais.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        is_admin INTEGER NOT NULL DEFAULT 0
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS materiais (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        local TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Operante'
    )''')

    # Criar usuário admin se não existir
    cursor.execute('SELECT COUNT(*) FROM usuarios')
    if cursor.fetchone()[0] == 0:
        hashed_pw = generate_password_hash('admin123')
        cursor.execute("INSERT INTO usuarios (username, password, is_admin) VALUES (?, ?, ?)", ('admin', hashed_pw, 1))

    # Inserir materiais apenas se não existirem
    cursor.execute('SELECT COUNT(*) FROM materiais')
    if cursor.fetchone()[0] == 0:
        materiais = [
    ("Aparelhos de EPR completos", 3, "Cabine/Guarnição"),
    ("Cilindro reserva de ar respirável", 1, "Cabine/Guarnição"),
    ("Chave de mangueira para 1.5” e 2.5”", 1, "Cabine/Guarnição"),
    ("Kit primeiros socorros Scania", 1, "Cabine/Guarnição"),
    ("Chave de hidrante tipo T", 1, "Cabine/Guarnição"),
    ("Colete de sinalização", 1, "Cabine/Guarnição"),
    ("Pares de luva de vaqueta", 3, "Cabine/Guarnição"),
    ("Binóculos", 2, "Cabine/Guarnição"),
    ("Lanterna de LED recarregável", 3, "Cabine/Guarnição"),
    ("Fita zebrada", 1, "Cabine/Guarnição"),
    ("Extintor Gloria 2kg", 1, "Cabine/Guarnição"),
    ("Lanterna sinalizadora Wurth + carregadores", 1, "Cabine/Guarnição"),
    ("Aferidor de pressão dos pneus", 1, "Cabine/Guarnição"),
    ("Mangueira compressor caminhoneiro", 1, "Cabine/Guarnição"),
    ("Controle remoto com fio do guincho", 1, "Cabine/Guarnição"),
    ("Detector multigás MSA Altair + acessórios", 1, "Cabine/Guarnição"),
    ("Bomba elétrica de amostragem MSA", 1, "Cabine/Guarnição"),
    ("Serra sabre Bosch + carregador + baterias + lâminas", 1, "Lado Direito"),
    ("Caixa de ferramentas azul", 1, "Lado Direito"),
    ("Pás de campanha", 3, "Lado Direito"),
    ("Pás de bico", 2, "Lado Direito"),
    ("Corta frio", 1, "Lado Direito"),
    ("Terçado", 1, "Lado Direito"),
    ("Pulaski", 1, "Lado Direito"),
    ("Machado arrombador tipo bombeiro", 1, "Lado Direito"),
    ("Marreta", 1, "Lado Direito"),
    ("Martelo de borracha", 1, "Lado Direito"),
    ("Hooligan", 2, "Lado Direito"),
    ("Gerador portátil", 1, "Lado Direito"),
    ("Luz de cena portátil recarregável", 2, "Lado Direito"),
    ("Triângulo de resgate", 1, "Lado Direito"),
    ("Fita tubular 37 metros", 1, "Lado Direito"),
    ("Fita anel (60cm e 120cm)", 2, "Lado Direito"),
    ("Pares de luva de proteção elétrica", 2, "Lado Direito"),
    ("Fitas zebradas", 2, "Lado Direito"),
    ("Corda de salvamento de 30 metros", 1, "Lado Direito"),
    ("Cinta de içamento de carga", 1, "Lado Direito"),
    ("Rampas de proteção para mangueiras", 2, "Lado Direito"),
    ("Blocos de calço", 4, "Lado Direito"),
    ("Mochila costal flexível", 3, "Lado Direito"),
    ("Extintor de pó químico seco ABC", 1, "Lado Direito"),
    ("Extintor CO2 6kg", 1, "Lado Direito"),
    ("Cones de sinalização", 10, "Lado Direito"),
    ("Exaustor Leader 360", 1, "Lado Esquerdo"),
    ("Ventilador turbo", 1, "Lado Esquerdo"),
    ("Motobomba autoescorvante", 1, "Lado Esquerdo"),
    ("Cilindros reserva de ar respirável", 6, "Lado Esquerdo"),
    ("Mangueiras de incêndio 1.5\"", 10, "Lado Esquerdo"),
    ("Mangueiras de incêndio 2.5\"", 10, "Lado Esquerdo"),
    ("Filtros de sucção", 4, "Lado Esquerdo"),
    ("Divisor de duas saídas", 2, "Lado Esquerdo"),
    ("Reduções de 2.5\" para 1.5\"", 2, "Lado Esquerdo"),
    ("Adaptadores de rosca fêmea", 8, "Lado Esquerdo"),
    ("Manilha curva", 2, "Lado Esquerdo"),
    ("Esguicho tipo pistola", 5, "Lado Esquerdo"),
    ("Doseador fixo Leader", 1, "Lado Esquerdo"),
    ("Mangotes (2.5\" e 4\")", 6, "Parte Superior"),
    ("Abafadores", 4, "Parte Superior"),
    ("Croque", 1, "Parte Superior"),
    ("Enxada", 1, "Parte Superior"),
    ("Enxadeco", 2, "Parte Superior"),
    ("McLeod", 3, "Parte Superior"),
    ("Pulaski", 1, "Parte Superior"),
    ("Escada de dois lances de alumínio", 1, "Parte Superior"),
    ("Tripé de resgate", 1, "Parte Superior"),
    ("Câmera térmica", 1, "Alojamento Oficial"),
        ]
        cursor.executemany("INSERT INTO materiais (nome, quantidade, local, status) VALUES (?, ?, ?, 'Operante')", materiais)

    conn.commit()
    conn.close()

# Rota de Login
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/auth', methods=['POST'])
def auth():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('gestao_materiais.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user[2], password):
        session['user'] = username
        session['is_admin'] = user[3]
        return redirect(url_for('index', page=1))
    
    return "Credenciais inválidas!", 401

# Página Principal com Paginação
@app.route('/index/<int:page>')
def index(page):
    if 'user' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('gestao_materiais.db')
    cursor = conn.cursor()

    items_per_page = 10
    offset = (page - 1) * items_per_page

    cursor.execute('SELECT COUNT(*) FROM materiais')
    total_items = cursor.fetchone()[0]
    total_pages = (total_items // items_per_page) + (1 if total_items % items_per_page > 0 else 0)

    cursor.execute('SELECT * FROM materiais LIMIT ? OFFSET ?', (items_per_page, offset))
    materiais = cursor.fetchall()
    conn.close()

    return render_template("index.html", materiais=materiais, page=page, total_pages=total_pages)

# Atualizar Status do Material
@app.route('/atualizar_status', methods=['POST'])
def atualizar_status():
    if 'user' not in session:
        return redirect(url_for('login'))

    material_id = request.form['material_id']
    novo_status = request.form['status']

    conn = sqlite3.connect('gestao_materiais.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE materiais SET status = ? WHERE id = ?", (novo_status, material_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Status atualizado com sucesso!"})

# Gerar Relatório PDF com Observações e Logo corrigido
@app.route('/gerar_pdf', methods=['POST'])
def gerar_pdf():
    if 'user' not in session:
        return redirect(url_for('login'))

    observacao = request.form.get('observacao', '')

    conn = sqlite3.connect('gestao_materiais.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, quantidade, local, status FROM materiais")
    materiais = cursor.fetchall()
    conn.close()

    pdf_filename = "relatorio_materiais.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)

    # Adicionar logotipo (corrigido para não sobrepor o texto)
    logo_path = "static/logo.png"
    if os.path.exists(logo_path):
        c.drawImage(logo_path, 40, 650, width=100, height=100)  # Posição ajustada

    # Ajustar a posição do título mais para baixo para evitar sobreposição
    c.setFont("Helvetica-Bold", 14)
    c.drawString(160, 750, "Relatório de Materiais - ABT-53 3º GBM")
    
    c.setFont("Helvetica", 10)
    c.drawString(160, 735, f"Gerado em: {datetime.today().strftime('%d/%m/%Y %H:%M')}")

    # Ajustar a posição inicial do texto mais abaixo
    y = 700

    c.setFont("Helvetica", 10)
    for material in materiais:
        c.drawString(150, y, f"{material[0]} - {material[1]} ({material[2]} unidades) - {material[3]} - {material[4]}")
        y -= 20
        if y < 50:
            c.showPage()
            y = 750

    # Se o usuário digitou uma observação, adicionamos no final do PDF
    if observacao:
        c.drawString(150, y - 40, f"Observação: {observacao}")

    # Assinatura no final
    c.drawString(150, y - 80, "Assinatura do responsável: __________________________")
    c.drawString(350, y - 80, "Data: ____/____/______")

    c.save()
    return send_file(pdf_filename, as_attachment=True)


# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('is_admin', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    criar_banco()
    app.run(debug=True)
