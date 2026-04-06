import sqlite3
import pandas as pd
import torch
from torch.utils.data import Dataset 

class PGDataSet(Dataset):

    def __init__(self , db_path):
        conn = sqlite3.connect(db_path)
        self.data = pd.read_sql_query(
            '''SELECT contratos.user_id , salario_bruto , dia_pagamento , SUM(valor) as total_transacoes
               FROM contratos
               JOIN transacoes 
               ON contratos.user_id = transacoes.user_id
               GROUP BY transacoes.user_id
            '''
            , conn)

        conn.close()

    def __len__(self):
        pass

    def __getitem__(self, key):
        pass

if __name__ == '__main__':
    # Aponta para o banco que o injecao.py criou
    dataset = PGDataSet('./data/_dbteste.db') 
    
    # Imprime o DataFrame resultante da sua query
    print(dataset.data)