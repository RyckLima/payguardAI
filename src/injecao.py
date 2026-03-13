import  os 
from  flask  import  Flask , jsonify,  request ,  redirect ,  url_for 
from  werkzeug.utils  import  secure_filename
from  flask  import  send_from_directory
import requests
import json

UPLOAD_FOLDER  =  './data' 
ALLOWED_EXTENSIONS = {'json'}

app  =  Flask ( __name__ ) 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
app.config['MAX_CONTENT_LENGHT']= 16*1000*1000


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/injetar', methods=['POST'])
def upload_file():
    
    # check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}) , 400
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '': 
        return jsonify({'error': 'No file selected'}) , 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        path = os.path.join('data' , filename)

        try:
            with open(path , 'rb') as f:

                dados = json.load(f)

                campos_obrigatorios = ['user_id' , 'transacoes' , 'salario_bruto' , 'dia_pagamento']  

                for campo in campos_obrigatorios:
                    if campo not in dados:
                        return jsonify({'error': f'Campo obrigatório ausente: {campo}'}), 400
                    
                for i , transacao in enumerate(dados['transacoes']):
                    if 'descricao' not in transacao or 'valor' not in transacao:
                        return jsonify({'error': f'Erro na transação {i}: falta descricao ou valor'}), 400
                    
                return jsonify({'message': 'Upload realizado e dados validados com sucesso!'}), 201
            
        except json.JSONDecodeError:
            return jsonify({'error': 'Arquivo JSON inválido ou corrompido'}), 400
        except Exception as e:
            return jsonify({'error': f'Erro interno: {str(e)}'}), 500
                             
if __name__ == '__main__':
    app.run(debug=True)