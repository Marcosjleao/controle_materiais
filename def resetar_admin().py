def resetar_admin():
    conn = sqlite3.connect('gestao_materiais.db')
    cursor = conn.cursor()

    # Deletar usuário admin se já existir
    cursor.execute("DELETE FROM usuarios WHERE username = 'admin'")
    
    # Criar novo admin com senha padrão
    hashed_pw = generate_password_hash('admin123')
    cursor.execute('INSERT INTO usuarios (username, password, is_admin) VALUES (?, ?, ?)', 
                   ('admin', hashed_pw, 1))

    conn.commit()
    conn.close()

# **Chamar esta função apenas uma vez para recriar o admin**
resetar_admin()
