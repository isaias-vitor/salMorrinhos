from supabase import create_client
from enum import Enum
from os import getenv

class cargos(Enum):
    Ancião = 1
    Diácono = 2
    CooperadorDeOfícioMinisterial = 3
    CooperadorDeJovensEMenores = 4
    EncarregadoLocal = 5
    EncarregadoRegional = 6

class SupabaseClient:
    def __init__(self):
        self.url = getenv('SUPABASE_URL')
        self.key = getenv('SUPABASE_KEY')
        self.client = create_client(self.url, self.key)

    def cargos(self, id):
        if type(id) == int:
            match id:
                case 1: return 'Ancião'
                case 2: return 'Diácono'
                case 3: return 'Cooperador de Ofício Ministerial'
                case 4: return 'Cooperador de Jovens e Menores'
                case 5: return 'Encarregado Regional'
                case 6: return 'Encarregado Local'
                case 7: return 'Examinadora'
                case 8: return 'Instrutor'
                case 9: return 'Instrutora'
                case 10: return 'Secretário do GEM'
                case 11: return 'Secretário do Setor'
                case 12: return 'Acessores Administrativos'
                case 13: return 'Conselho Fiscal'
                case 14: return 'Brigadista'
                case 15: return 'Porteiro'
                case 16: return 'Recepcionista'
                case 17: return 'Auxiliar de Som'
                case 18: return 'Auxiliar de Escrita'
                case 19: return 'Preventiva'
                case 20: return 'Auxiliar de Corredores'
                case 21: return 'Patrimônio'
                case 22: return 'Auxiliar de Jovens'
                case 23: return 'Auxiliar de Banheiros'
                case 24: return 'Conselho Jurídico'
                case 25: return 'Monitor de Segurança'
                case 26: return 'Auxiliar do Som (RJM)'
                case 27: return 'Auxiliar de Escrita (RJM)'
                case 28: return 'Porteiro (RJM)'
                case 29: return 'Recepcionista (RJM)'
        elif type(id) == str:
            match id:
                case 'Ancião': return 1
                case 'Diácono': return 2
                case 'Cooperador de Ofício Ministerial': return 3
                case 'Cooperador de Jovens e Menores': return 4
                case 'Encarregado Regional': return 5
                case 'Encarregado Local': return 6
                case 'Examinadora':return 7
                case 'Instrutor': return 8
                case 'Instrutora': return 9
                case 'Secretário do GEM': return 10
                case 'Secretário do Setor': return 11
                case 'Acessores Administrativos': return 12
                case 'Conselho Fiscal': return 13
                case 'Brigadista': return 14
                case 'Porteiro': return 15
                case 'Recepcionista': return 16
                case 'Auxiliar do Som': return 17
                case 'Auxiliar de Escrita': return 18
                case 'Preventiva': return 19
                case 'Auxiliar de Corredores': return 20
                case 'Patrimônio': return 21
                case 'Auxiliar de Jovens': return 22
                case 'Engenharia': return 23
                case 'Conselho Jurídico': return 24
                case 'Monitor de Segurança': return 25
                case 'Auxiliar de Som (RJM)': return 26
                case 'Auxiliar de Escrita (RJM)': return 27
                case 'Porteiro (RJM)': return 28
                case 'Recepcionista (RJM)': return 29
    
    def qtdCargos(self, cargo):
        busca = self.client.table('voluntarios').select('*').contains('funcoes', [cargo]).execute()
        return len(busca.data)

    def nomePessoa(self, id):
        try:
            busca = self.client.table('voluntarios').select('nome').eq('id', id).execute()
            return busca.data[0]['nome']
        except:
            return None
    
    
    def inserir_cargo(self, nome, comum, cidade, setor, cargo) -> dict:
        try:
            insert_cargo = self.client.table('voluntarios').insert({
                'nome':nome,
                'comum':comum,
                'cidade':cidade,
                'setor':setor,
                'funcoes': [cargo]
            }).execute()
            print(comum)
            id = self.client.table('voluntarios').select('id').eq('nome', nome).execute()
            id = id.data[0]['id']
            comum = self.client.table('comuns').select('id').eq('nome', comum).execute()
            comum = comum.data[0]['id']
            print(comum)
            insert_respons = self.client.table('responsabilidades').insert({
                'id_comum':comum,
                'id_voluntario':int(id),
                'funcao':cargo
            }).execute()
        except:
            print('Erro ao  no banco de dados!')
            return None
    
    def inserir_comum(self, nome, endereco, setor, cidade, zona, tipo, reforma, construcao, membros) -> dict:
        try:
            response = self.client.table('comuns').insert({
                'nome':nome,
                'endereco':endereco,
                'setor':setor,
                'cidade':cidade,
                'zona':zona,
                'tipo':tipo,
                'reforma':False if(reforma == 'Não') else True,
                'construcao':False if(construcao == 'Não') else True,
                'membros':membros
            }).execute()
            return response.data
        except:
            print('Erro ao inserir no banco de dados!')
            return None

    def inserir_responsabilidade(self, id_pessoa, nome_comum, nome_cargo, nome_cidade):
        try:
            # Inserção na tabela de responsabilidades
            id_comum = self.client.table('comuns').select('id').eq('nome', nome_comum).eq('cidade', nome_cidade).execute()
            id_comum = id_comum.data[0]['id']
            id_funcao = self.cargos(nome_cargo)
            insercao = self.client.table('responsabilidades').insert({
                'id_comum':id_comum,
                'id_voluntario':id_pessoa,
                'funcao':id_funcao
            }).execute()
            # Inserção na tabela de voluntarios
            lista_funcoes = self.client.table('voluntarios').select('funcoes').eq('id', id_pessoa).execute()
            lista_funcoes = lista_funcoes.data[0]['funcoes']
            lista_funcoes.append(id_funcao)
            insercao_pessoa = self.client.table('voluntarios').update({
                'funcoes':lista_funcoes
            }).eq('id', id_pessoa).execute()

        except:
            print('Erro ao inserir no banco de dados!')
            return None  


    def buscar_cargo(self, cargo): 
        try:
            respons = self.client.table('voluntarios').select('id', 'nome', 'comum', 'cidade', 'setor').contains('funcoes', [cargo]).execute()
            return respons.data
        except:     
            print('Erro ao buscar na tabela')
            return None
        
    def buscar_comuns(self):
        try:
            busca = self.client.table('comuns').select('nome', 'cidade', 'setor', 'zona', 'tipo').execute()
            return busca.data
        except:
            print('Erro ao buscar na tabela comuns!')
            return None
    
    def buscar_comum(self, comum):
        try:
            busca = self.client.table('comuns').select('*').eq('nome', comum).execute()
            return busca.data[0]
        except:
            print('Erro ao buscar na tabela comuns!')
            return None

    def buscar_cargos_comum(self, nome_comum):
        try:
            busca_id = self.client.table('comuns').select('id').eq('nome', nome_comum).execute()
            busca_id = busca_id.data[0]['id']   
            busca = self.client.table('responsabilidades').select('*').eq('id_comum', busca_id).execute()
            lista_cargos = {
                'ministerio':{
                    'anciaes':[],
                    'diaconos':[],
                    'coop_oficiais':[],
                    'coop_jovens':[]
                },
                'musica':{
                    'enc_regionais':[],
                    'enc_locais':[],
                    'examinadoras':[],
                    'instrutores':[],
                    'instrutoras':[],
                    'sec_gem':[]
                },
                'adm':{
                    'sec_setor':[],
                    'acessor_adm':[],
                    'cons_fiscal':[],
                    'engenharia':[],
                    'cons_juridico':[]
                },
                'enc_locais':{
                    'brigadistas':[],
                    'porteiros':[],
                    'porteiros_rjm':[],
                    'recepcionistas':[],
                    'recepcionistas_rjm':[],
                    'aux_som':[],
                    'aux_som_rjm':[],
                    'aux_escrita':[],
                    'aux_escrita_rjm':[],
                    'preventiva':[],
                    'aux_corr':[],
                    'patrimonio':[],
                    'aux_jovens':[],
                    'monitor_seg':[]
                }
            }
            for voluntario in busca.data:
                nome_voluntario = self.nomePessoa(int(voluntario['id_voluntario']))
                dados = {'id':voluntario['id_voluntario'], 'nome':nome_voluntario, 'funcao':self.cargos(voluntario['funcao'])}
                match voluntario['funcao']:
                    case 1: lista_cargos['ministerio']['anciaes'].append(dados)
                    case 2: lista_cargos['ministerio']['diaconos'].append(dados)
                    case 3: lista_cargos['ministerio']['coop_oficiais'].append(dados)
                    case 4: lista_cargos['ministerio']['coop_jovens'].append(dados)
                    case 5: lista_cargos['musica']['enc_regionais'].append(dados)
                    case 6: lista_cargos['musica']['enc_locais'].append(dados)
                    case 7: lista_cargos['musica']['examinadoras'].append(dados)
                    case 8: lista_cargos['musica']['instrutores'].append(dados)
                    case 9: lista_cargos['musica']['instrutoras'].append(dados)
                    case 10: lista_cargos['musica']['sec_gem'].append(dados)
                    case 11: lista_cargos['adm']['sec_setor'].append(dados)
                    case 12: lista_cargos['adm']['acessor_adm'].append(dados)
                    case 13: lista_cargos['adm']['cons_fiscal'].append(dados)
                    case 14: lista_cargos['enc_locais']['brigadistas'].append(dados)
                    case 15: lista_cargos['enc_locais']['porteiros'].append(dados)
                    case 16: lista_cargos['enc_locais']['recepcionistas'].append(dados)
                    case 17: lista_cargos['enc_locais']['aux_som'].append(dados)
                    case 18: lista_cargos['enc_locais']['aux_escrita'].append(dados)
                    case 19: lista_cargos['enc_locais']['preventiva'].append(dados)
                    case 20: lista_cargos['enc_locais']['aux_corr'].append(dados)
                    case 21: lista_cargos['enc_locais']['patrimonio'].append(dados)
                    case 22: lista_cargos['enc_locais']['aux_jovens'].append(dados)
                    case 23: lista_cargos['enc_locais']['engenharia'].append(dados)
                    case 24: lista_cargos['enc_locais']['cons_juridico'].append(dados)
                    case 25: lista_cargos['enc_locais']['monitor_seg'].append(dados)
                    case 26: lista_cargos['enc_locais']['aux_som'].append(dados)
                    case 27: lista_cargos['enc_locais']['aux_escrita_rjm'].append(dados)
                    case 28: lista_cargos['enc_locais']['porteiros_rjm'].append(dados)
                    case 29: lista_cargos['enc_locais']['recepcionistas_rjm'].append(dados)
            return lista_cargos
        except:
            print('Erro ao buscar!')
            return None

    def buscar_cargos_pessoa(self, id_pessoa):
        try:
            busca = self.client.table('responsabilidades').select('*').eq('id_voluntario', id_pessoa).execute()
            responsabilidades = []
            for respons in busca.data:
                cargo = respons['funcao']
                match cargo:
                    case 1: cargo = 'Ancião'
                    case 2: cargo = 'Diácono'
                    case 3: cargo = 'Cooperador Oficial'
                    case 4: cargo = 'Cooperador de Jovens'
                    case 5: cargo = 'Encarregado Regional'
                    case 6: cargo = 'Encarregado Local'
                    case 7: cargo = 'Examinadora' 
                    case 8: cargo = 'Instrutor' 
                    case 9: cargo = 'Instrutora' 
                    case 10: cargo = 'Secretário do GEM' 
                    case 11: cargo = 'Secretário do Setor' 
                    case 12: cargo = 'Acessor Administrativos' 
                    case 13: cargo = 'Conselho Fiscal' 
                    case 14: cargo = 'Brigadista' 
                    case 15: cargo = 'Porteiro' 
                    case 16: cargo = 'Recepcionista' 
                    case 17: cargo = 'Auxiliar do Som' 
                    case 18: cargo = 'Auxiliar de Escrita' 
                    case 19: cargo = 'Preventiva' 
                    case 20: cargo = 'Auxiliar de Corredores' 
                    case 21: cargo = 'Patrimônio' 
                    case 22: cargo = 'Auxiliar de Jovens' 
                    case 23: cargo = 'Engenharia' 
                    case 24: cargo = 'Conselho Jurídico' 
                    case 25: cargo = 'Monitor de Segurança' 
                    case 26: cargo = 'Auxiliar do Som (RJM)'
                    case 27: cargo = 'Auxiliar de Escrita (RJM)'
                    case 28: cargo = 'Porteiro'
                    case 29: cargo = 'Recepcionista'

                comum = self.client.table('comuns').select('nome', 'setor', 'cidade').eq('id', respons['id_comum']).execute()
                responsabilidades.append({
                    'cargo':cargo,
                    'comum':comum.data[0]['nome'],
                    'setor':comum.data[0]['setor'],
                    'cidade':comum.data[0]['cidade'],
                    'observacao':respons['obs'],
                    'id_resp':respons['id']
                })
                
            return responsabilidades
        except:
            print('Erro ao buscar!')
            return None
        
    def buscar_pessoa(self, id):
        try:
            busca = self.client.table('voluntarios').select('*').eq('id', id).execute()
            return busca.data[0]
        except:
            print('Erro ao buscar!')
            return None
        

    def editar_responsabilidade(self, id_pessoa, nome_comum, nome_cargo, id_resp, obs, resp_antiga):
        try:
            self.client.table('responsabilidades').update({
                'id_comum':self.buscar_comum(nome_comum)['id'],
                'id_voluntario':id_pessoa,
                'funcao':self.cargos(nome_cargo),
                'obs':obs
                }).eq('id', id_resp).execute()
            id_resp_antiga = self.cargos(resp_antiga)
            id_resp_atual = self.cargos(nome_cargo)
            busca = self.client.table('voluntarios').select('funcoes').eq('id', id_pessoa).execute()
            busca = busca.data[0]['funcoes']
            if id_resp_antiga in busca: busca.remove(id_resp_antiga)
            busca.append(id_resp_atual)
            self.client.table('voluntarios').update({'funcoes':busca}).eq('id', id_pessoa).execute()
        except:
            print('Erro ao atualizar!')
            return None
        

    def remover_responsabilidade(self, id_resp):
        try:
            delete = self.client.table('responsabilidades').delete().eq('id',id_resp).execute()
            return print('Responsabilidade excluida com sucesso!')
        except:
            return print('Erro ao excluir!')
