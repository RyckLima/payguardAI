import sqlite3
import pandas as pd
import torch
from torch.utils.data import Dataset 

class PGDataSet(Dataset):

    def __init__(self , db_path):
        conn = sqlite3.connect(db_path)
        self.data = pd.read_sql_query(
            '''SELECT
                user_id,
                strftime('%Y-%m', data) as mes,
                SUM(CASE WHEN valor > 0 THEN valor ELSE 0 END) AS total_receitas,
                SUM(CASE WHEN valor < 0 THEN valor ELSE 0 END) AS total_despesas,
                SUM(valor) AS saldo_mensal
                FROM (SELECT * FROM transacoes)
                GROUP BY user_id, mes;
            '''
            , conn)

        conn.close()

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        row = self.data.iloc[idx]
        
        features = row[['total_receitas', 'total_despesas']].values.astype('float32')
        
        label = 1 if row['saldo_mensal'] > 0 else 0
        
        return features, label
    
if __name__ == '__main__':
    # Aponta para o banco que o injecao.py criou
    dataset = PGDataSet('./data/_dbteste.db') 
    
    print(dataset.data)

    features, label = dataset[0]
    print(f"--- Teste GetItem ---")
    print(f"Features (Receitas, Despesas): {features}")
    print(f"Label (Saudável): {label}")