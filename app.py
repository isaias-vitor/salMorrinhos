from flask import *
import forms
from os import getenv
from database import *
from dotenv import load_dotenv
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = getenv('SECRET_KEY_APP')
db = SupabaseClient()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

USERS = {
    'admin': {
        'password': '1234',
        'level':'leitor'
        }
}

class User(UserMixin):
    def __init__(self, username):
        self.id = username


@login_manager.user_loader
def load_user(user_id):
    if user_id in USERS:
        return User(user_id)
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'logado' in session: 
        if session['logado']:
            return redirect(url_for('index'))
    form_login = forms.Login()

    if form_login.validate_on_submit():
        username = form_login.usuario.data
        password = form_login.senha.data


        user = USERS.get(username)
        if user and user['password'] == password:

            session['logado'] = True
            session['nivel_acesso'] = user['level']

            user_obj = User(username)
            login_user(user_obj)
            flash('Login realizado com sucesso!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Usuário ou senha inválidos!', 'danger')

    return render_template('login.html', form=form_login)

@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    flash('Você saiu com sucesso!', 'infor')
    return redirect(url_for('login'))

@app.route("/")
@login_required
def index():
    funcoes = {
        'palavra': {
            'Anciões':(db.qtdCargos('1'), 1), 
            'Diáconos':(db.qtdCargos('2'), 2),
            'Cooperadores de Ofício Ministerial':(db.qtdCargos('3'), 3),            
            'Cooperadores de Jovens e Menores':(db.qtdCargos('4'), 4),            
        },
        'musica': {
            'Encarregados Regionais':(db.qtdCargos('5'), 5),
            'Encarregados Locais':(db.qtdCargos('6'), 6),
            'Examinadoras':(db.qtdCargos('7'), 7),
            'Instrutores':(db.qtdCargos('8'), 8),
            'Instrutoras':(db.qtdCargos('9'), 9),
            'Secretários do GEM':(db.qtdCargos('10'), 10),
        },
        'adm': {
            'Secretários do Setor':(db.qtdCargos('11'), 11),
            'Acessores Administrativos':(db.qtdCargos('12'), 12),
            'Conselho Fiscal':(db.qtdCargos('13'), 13),
            'Engenharia':(db.qtdCargos('23'), 23),
            'Conselho Jurídico':(db.qtdCargos('24'), 24),

        },
        'cargos': {
            'Brigadistas':(db.qtdCargos('14'), 14),
            'Porteiros':(db.qtdCargos('15'), 15),
            'Porteiros (RJM)':(db.qtdCargos('28'), 28),
            'Recepcionistas':(db.qtdCargos('16'), 16),
            'Recepcionistas (RJM)':(db.qtdCargos('29'), 29),
            'Auxiliares do Som':(db.qtdCargos('17'), 17),
            'Auxiliares do Som (RJM)':(db.qtdCargos('26'), 26),
            'Auxiliares de Escrita':(db.qtdCargos('18'), 18),
            'Auxiliares de Escrita (RJM)':(db.qtdCargos('27'), 27),
            'Preventiva':(db.qtdCargos('19'), 19),
            'Auxiliares de Corredores':(db.qtdCargos('20'), 20),
            'Patrimônio':(db.qtdCargos('21'), 21),
            'Auxiliares de Jovens':(db.qtdCargos('22'), 22),
            'Monitor de Segurança':(db.qtdCargos('25'), 25)
        }
    }
    return render_template('index.html', funcoes=funcoes)


@app.route('/cargos/<string:cargo>', methods=['GET', 'POST'])
@login_required
def cargos(cargo):
    lista_voluntarios = db.buscar_cargo(cargo)
    # lista_voluntarios = sorted(db.buscar_cargo(cargo), key = lambda x: x['nome'])

    busca_igrejas = db.buscar_comuns()
    lista_igrejas = {}
    for igreja in busca_igrejas:
        if igreja['setor'] not in lista_igrejas:
            lista_igrejas.setdefault(igreja['setor'],{})
        if igreja['cidade'] not in lista_igrejas[igreja['setor']]:
            lista_igrejas[igreja['setor']].setdefault(igreja['cidade'], [])
        lista_igrejas[igreja['setor']][igreja['cidade']].append(igreja['nome'])  
    

    # Formulário de adição de cargo
    form = forms.AdicionaCargos()
    form.setor.choices = list(lista_igrejas.keys())
    form.cidade.choices = list(lista_igrejas['Roxo Verde'].keys())
    form.comum.choices = lista_igrejas['Roxo Verde']['Montes Claros']
    if request.method == 'POST':
        adicionarVoluntario = db.inserir_cargo(
            nome = form.nome.data, 
            setor = form.setor.data, 
            cidade = form.cidade.data,
            comum = form.comum.data,
            cargo = cargo
        )

        return redirect(url_for('cargos', cargo=cargo))

    return render_template('voluntarios.html', lista_voluntarios=lista_voluntarios, form=form, titulo=db.cargos(int(cargo)), igrejas=lista_igrejas)


@app.route('/pessoas/<string:pessoa>', methods=['GET', 'POST'])
@login_required
def pessoas(pessoa):
    lista_responsabilidades = db.buscar_cargos_pessoa(pessoa) 

    igrejas = lista_igrejas()
    
    nome_pessoa = db.nomePessoa(pessoa)
    cargos = {
        'Ministério':[
            'Ancião',
            'Diácono',
            'Cooperador de Jovens e Menores',
            'Cooperador de Ofício Ministerial',
        ],
        'Música':[
            'Encarregado Regional',
            'Encarregado Local',
            'Examinadora',
            'Instrutor',
            'Instrutora',
            'Secretário do GEM',
        ],
        'Administração':[
            'Secretário do Setor',
            'Acessor Administrativo',
            'Conselho Fiscal',
            'Engenharia',
            'Conselho Jurídico',
        ],
        'Encargos Locais':[
            'Auxiliar de Jovens',
            'Porteiro',
            'Porteiro (RJM)',
            'Recepcionista',
            'Recepcionista (RJM)',
            'Auxiliar de Escrita',
            'Auxiliar de Escrita (RJM)',
            'Preventiva',
            'Auxiliar do Som',
            'Auxiliar do Som (RJM)',
            'Brigadista',
            'Monitor de Segurança',
            'Auxiliar de Corredores',
            'Patrimônio',
        ]
    }
    form_remove = forms.RemoveCargoPessoa()
    form_edit = forms.EditaCargoPessoa()
    form = forms.AdicionaCargoPessoa()
    form_edit.cargo.choices = cargos['Ministério']
    form.setor.choices = form_edit.setor.choices = list(igrejas.keys())
    form.cidade.choices = form_edit.cidade.choices = list(igrejas['Roxo Verde'].keys())
    form.comum.choices = form_edit.comum.choices = igrejas['Roxo Verde']['Montes Claros']
    if request.method == 'POST':
        formulario = request.form.get('submit')
        if formulario == 'Adicionar Responsabilidade':
            db.inserir_responsabilidade(
                id_pessoa = pessoa,
                nome_comum = form.comum.data,
                nome_cargo = form.cargo.data,
                nome_cidade = form.cidade.data
            )
        elif formulario == 'Editar Responsabilidade':
            db.editar_responsabilidade(
                id_pessoa = pessoa,
                nome_comum = form_edit.comum.data,
                nome_cargo = form_edit.cargo.data,
                obs = form_edit.obs.data,
                id_resp = form_edit.id_resp.data,
                resp_antiga = form_edit.resp_antiga.data
            )
        elif formulario == 'Remover':
            db.remover_responsabilidade(form_remove.id_resp.data)

        return redirect(url_for('pessoas', pessoa=pessoa))
    

    return render_template('pessoa.html', pessoa=nome_pessoa, responsabilidades=lista_responsabilidades, form=form, cargos=cargos, igrejas=igrejas, form_edit=form_edit, form_remove=form_remove)


@app.route('/comuns', methods=['GET', 'POST'])
@login_required
def comuns():
    comuns = sorted(db.buscar_comuns(), key = lambda x: x['nome'])

    igrejas = lista_igrejas()

    form = forms.AdicionaComuns()
    form.setor.choices = list(igrejas.keys())
    form.cidade.choices = list(igrejas['Roxo Verde'].keys())
    if request.method == 'POST':
        adicionarComum = db.inserir_comum(
            nome = form.nome.data,
            endereco = form.endereco.data,
            setor = form.setor.data,
            cidade = form.cidade.data,
            zona = form.zona.data,
            tipo = form.tipo.data,
            reforma = form.reforma.data,
            construcao = form.construcao.data,
            membros = form.membros.data
        )
        return redirect(url_for('comuns'))
    
    return render_template('comuns.html', comuns=comuns, form=form)


@app.route('/comum/<string:nome_comum>')
@login_required
def comum(nome_comum):
    cargos = {
        'Música':[
            'Encarregado Regional',
            'Encarregado Local',
            'Examinadora',
            'Instrutor',
            'Instrutora',
            'Secretário do GEM',
        ],
        'Administração':[
            'Secretário do Setor',
            'Acessor Administrativo',
            'Conselho Fiscal',
            'Engenharia',
            'Conselho Jurídico',
        ],
        'Encargos Locais':[
            'Auxiliar de Jovens',
            'Porteiro',
            'Porteiro (RJM)',
            'Recepcionista',
            'Recepcionista (RJM)',
            'Auxiliar de Escrita',
            'Auxiliar de Escrita (RJM)',
            'Preventiva',
            'Auxiliar do Som',
            'Auxiliar do Som (RJM)',
            'Brigadista',
            'Monitor de Segurança',
            'Auxiliar de Corredores',
            'Patrimônio',
        ]
    }
    
    dados_comum = db.buscar_comum(nome_comum)
    cargos_comum = db.buscar_cargos_comum(nome_comum)

    return(render_template('comum.html', nome_comum=nome_comum, dados_comum=dados_comum, cargos_comum=cargos_comum))


def lista_igrejas():
    busca_igrejas = db.buscar_comuns()
    lista_igrejas = {}
    for igreja in busca_igrejas:
        if igreja['setor'] not in lista_igrejas:
            lista_igrejas.setdefault(igreja['setor'],{})
        if igreja['cidade'] not in lista_igrejas[igreja['setor']]:
            lista_igrejas[igreja['setor']].setdefault(igreja['cidade'], [])
        lista_igrejas[igreja['setor']][igreja['cidade']].append(igreja['nome'])
            
    return lista_igrejas

if __name__ == "__main__":
    app.run(debug=True)