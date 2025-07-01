from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, IntegerField,TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length

class AdicionaCargos(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=5, max=256)])
    setor = SelectField('Setor', choices=[
        ('Roxo Verde', 'Roxo Verde'),
    ])
    cidade = SelectField('Cidade', choices=[
        ('Montes Claros', 'Montes Claros'), 
        ('Juramento', 'Juramento'),
        ('Itacambira', 'Itacambira'),
        ('Glaucilândia', 'Glaucilândia')
    ], validators=[DataRequired()])
    comum = SelectField('Comum', choices=[
        ('Delfino Magalhães', 'Delfino Magalhães'), 
        ('Jardim Alegre', 'Jardim Alegre'), 
        ('Jardim Primavera', 'Jardim Primavera'), 
        ('Morrinhos', 'Morrinhos'), 
        ('Roxo Verde', 'Roxo Verde'), 
        ('Santo Antônio', 'Santo Antônio'),
        ('Vila Anália', 'Vila Anália'),
        ('Vila Sion', 'Vila Sion')
    ], validators=[DataRequired()])
    submit = SubmitField('Salvar')

class AdicionaComuns(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=5, max=256)])
    endereco = StringField('Endereço', validators=[DataRequired(), Length(min=1, max=256)])
    setor = SelectField('Setor', validators=[DataRequired()])
    cidade = SelectField('Cidade', validators=[DataRequired()])
    zona = SelectField('Zona', choices=[
        ('Urbana', 'Urbana'),
        ('Rural', 'Rural'), 
    ], validators=[DataRequired()])
    tipo = SelectField('Tipo', choices=[
        ('Casa de Oração', 'Casa de Oração'), 
        ('Salão', 'Salão'),
        ('Residencial', 'Residencial'),
        ('Apoio DARP', 'Apoio DARP')
    ], validators=[DataRequired()])
    reforma = SelectField('Reforma', choices=[
        ('Não', 'Não'), 
        ('Sim', 'Sim'),
    ], validators=[DataRequired()])
    construcao = SelectField('Construção', choices=[
        ('Não', 'Não'), 
        ('Sim', 'Sim'),
    ], validators=[DataRequired()])
    membros = IntegerField('Membros', validators=[DataRequired()])
    submit = SubmitField('Salvar')

class AdicionaCargoPessoa(FlaskForm):
    tipo_cargo = SelectField('Tipo', choices=[
        'Ministério',
        'Música',
        'Administração',
        'Encargos Locais'
    ],validators=[DataRequired()])
    cargo = SelectField('Tipo', validators=[DataRequired()])
    setor = SelectField('Setor', validators=[DataRequired()])
    cidade = SelectField('Cidade', validators=[DataRequired()])
    comum = SelectField('Cidade', validators=[DataRequired()])
    obs = TextAreaField('Observações')
    submit = SubmitField('Salvar')

class EditaCargoPessoa(FlaskForm):
    tipo_cargo = SelectField('Tipo', choices=[
        'Ministério',
        'Música',
        'Administração',
        'Encargos Locais'
    ],validators=[DataRequired()])
    cargo = SelectField('Tipo', validators=[DataRequired()])
    setor = SelectField('Setor', validators=[DataRequired()])
    cidade = SelectField('Cidade', validators=[DataRequired()])
    comum = SelectField('Cidade', validators=[DataRequired()])
    obs = TextAreaField('Observações')
    id_resp = StringField('ID Responsabilidade')
    resp_antiga = StringField('Responsabilidade Antiga')
    submit = SubmitField('Salvar')

class RemoveCargoPessoa(FlaskForm):
    id_resp = StringField()
    submit = SubmitField('Remover')
