from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

shopping_list = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_product', methods=['POST'])
def add_product():
    product = request.form.get('product')
    if product:
        shopping_list.append(product)
        return jsonify({'message': f'{product} foi adicionado à lista de compras!', 'shopping_list': shopping_list})
    return jsonify({'error': 'Nenhum produto foi fornecido'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Alterei a porta para 5001
