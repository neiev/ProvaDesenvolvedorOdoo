# Questão 2: Modelagem e Arquitetura de Sistemas Web com API REST

# Você está trabalhando em um sistema de e-commerce.

# Modele classes em Python que representem os seguintes elementos: `Produto`, `Carrinho`, e `Pedido`.

# a) `Produto`: Deve ter atributos como `nome`, `preço` e `estoque`.

# b) `Carrinho`: Deve ser capaz de adicionar e remover produtos, calcular o total e finalizar a compra.

# c) `Pedido`: Deve conter informações sobre os produtos comprados e o total do pedido.

# Implemente também uma API REST para fornecer acesso a esses recursos.

from flask import Flask, request, jsonify

app = Flask(__name__)

class Produto:
    def __init__(self, nome, preco, estoque):
        self.nome = nome
        self.preco = preco
        self.estoque = estoque

class Carrinho:
    def __init__(self):
        self.produtos = []

    def adicionar_produto(self, produto):
        self.produtos.append(produto)

    def remover_produto(self, produto):
        if produto in self.produtos:
            self.produtos.remove(produto)

    def calcular_total(self):
        total = sum(produto.preco for produto in self.produtos)
        return total

class Pedido:
    def __init__(self, produtos, total):
        self.produtos = produtos
        self.total = total

carrinho = Carrinho()
pedidos = []

@app.route('/carrinho', methods=['GET'])
def listar_carrinho():
    produtos_no_carrinho = [produto.__dict__ for produto in carrinho.produtos]
    total = carrinho.calcular_total()
    return jsonify({"produtos": produtos_no_carrinho, "total": total})

@app.route('/carrinho/adicionar', methods=['POST'])
def adicionar_produto_carrinho():
    data = request.json
    nome = data.get('nome')
    preco = data.get('preco')
    estoque = data.get('estoque')
    produto = Produto(nome, preco, estoque)
    carrinho.adicionar_produto(produto)
    return jsonify({"mensagem": "Produto adicionado ao carrinho"})

@app.route('/carrinho/remover', methods=['POST'])
def remover_produto_carrinho():
    data = request.json
    nome = data.get('nome')
    for produto in carrinho.produtos:
        if produto.nome == nome:
            carrinho.remover_produto(produto)
            return jsonify({"mensagem": f"Produto '{nome}' removido do carrinho"})
    return jsonify({"mensagem": f"Produto '{nome}' não encontrado no carrinho"})

@app.route('/carrinho/finalizar', methods=['POST'])
def finalizar_compra():
    total = carrinho.calcular_total()
    pedido = Pedido(carrinho.produtos, total)
    pedidos.append(pedido)
    carrinho.produtos = {}
    return jsonify({'message': 'Compra finalizada com sucesso'})

if __name__ == '__main__':
    app.run(debug=True)