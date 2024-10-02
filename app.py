from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

livros = []

# Função para encontrar livro por ID
def encontrar_livro(id):
    return next((livro for livro in livros if livro['id'] == id), None)

# Rota para obter todos os livros
@app.route('/livros', methods=['GET'])
def obter_livros():
    return jsonify(livros), 200

# Rota para obter um livro por ID
@app.route('/livros/<int:id>', methods=['GET'])
def obter_livro(id):
    livro = encontrar_livro(id)
    if livro:
        return jsonify(livro), 200
    return jsonify({'erro': 'Livro não encontrado'}), 404

# Rota para criar um novo livro
@app.route('/livros', methods=['POST'])
def criar_livro():
    novo_livro = request.get_json()
    if not all(k in novo_livro for k in ('nome', 'data', 'autor', 'preco', 'disponibilidade')):
        return jsonify({'erro': 'Dados inválidos'}), 400

    novo_livro['id'] = len(livros) + 1
    livros.append(novo_livro)
    return jsonify(novo_livro), 201

# Rota para atualizar um livro existente
@app.route('/livros/<int:id>', methods=['PUT'])
def atualizar_livro(id):
    livro = encontrar_livro(id)
    if livro:
        dados_atualizados = request.get_json()
        livro.update(dados_atualizados)
        return jsonify(livro), 200
    return jsonify({'erro': 'Livro não encontrado'}), 404

# Rota para deletar um livro
@app.route('/livros/<int:id>', methods=['DELETE'])
def deletar_livro(id):
    livro = encontrar_livro(id)
    if livro:
        livros.remove(livro)
        return jsonify({'mensagem': 'Livro removido com sucesso'}), 200
    return jsonify({'erro': 'Livro não encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)