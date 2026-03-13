import sqlite3
import json

def criar_tabelas(banco):
    conn = sqlite3.connect(f"./data/{banco}.db")
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT ,
                user_id TEXT UNIQUE NOT NULL
                );
                ''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS transacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT ,
                user_id TEXT NOT NULL ,
                data TEXT NOT NULL ,
                descricao TEXT NOT NULL,
                valor REAL NOT NULL,
                FOREIGN KEY (user_id) REFERENCES usuarios(user_id) 
                );''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS contratos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT UNIQUE NOT NULL,
                salario_bruto REAL NOT NULL,
                dia_pagamento INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES usuarios (user_id)
                );''')

    conn.commit()
    conn.close()

def subir_dados(banco ,path):

    with open(path , 'r') as f:
        dados = json.load(f)

    conn = sqlite3.connect(f"./data/{banco}.db")
    cursor = conn.cursor()

    cursor.execute("INSERT OR IGNORE INTO usuarios (user_id) VALUES (?)", (dados['user_id'],))

    cursor.execute("""
        INSERT OR REPLACE INTO contratos (user_id, salario_bruto, dia_pagamento)
        VALUES (?, ?, ?)
    """, (dados['user_id'], dados['salario_bruto'], dados['dia_pagamento']))

    for t in dados['transacoes']:
        # Aqui você faz a limpeza/ajuste antes do execute
        valor_limpo = float(t['valor']) 
        
        cursor.execute("""
            INSERT INTO transacoes (user_id, data, descricao, valor)
            VALUES (?, ?, ?, ?)
        """, (dados['user_id'], t['data'], t['descricao'], valor_limpo))
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    print('Testando ....')
    criar_tabelas('_dbteste')
    subir_dados('_dbteste' , './data/teste_load_payguard.json')
    print('Teste concluído !')