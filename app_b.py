# app.py
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import SelectField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

class MyForm(FlaskForm):
    states = SelectField('States', choices=[])
    cities = SelectField('Cities', choices=[])

@app.route('/', methods=['GET', 'POST'])
def index():
    form = MyForm()

    if request.method == 'POST':
        selected_state = form.states.data
        selected_city = form.cities.data

        # Aqui você pode processar os valores selecionados
        print(f"Selected state: {selected_state}")
        print(f"Selected city: {selected_city}")

        # Você pode redirecionar para outra página ou exibir uma mensagem de sucesso
        return render_template('truco.html', form=form)

    return render_template('truco.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
