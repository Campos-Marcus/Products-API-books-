from flask_restful import Resource, reqparse
#reqparse, vai receber os argumentos da requisição
from models.livro import LivroModel
livros = [
		{

		'livro_id': 1,
		'nome': 'O senhor dos aneis',
		'quantidade' : 3,
		'preco': 30.75

		},

		{

		'livro_id': 2,
		'nome': 'Sherlock Holmes',
		'quantidade': 5,
		'diaria': 30.34

		},

		{

		'livro_id': 3,
		'nome': 'O triste fim de Policarpo Quaresma',
		'quantidade' : 4,
		'preco': 44.34

		}
]

#mostra todos os livros
class Livros(Resource):
	def get(self):
		return {'livros': [livro.json() for livro in LivroModel.query.all()]} #SELECT * from Livros


class Livro(Resource):

	atributos = reqparse.RequestParser()

	#dados que serão permitidos 
	atributos.add_argument('nome', type= str, required=True, help= "The field 'nome' cannot be left blank")
	atributos.add_argument('preco', type=float, required= True, help = "The field 'estrelas' cannot be left blank")
	atributos.add_argument('quantidade', type=int, required=False)

	#CRUD
	#Busca por igualdade (id)
	def get(self, livro_id):
		livro = LivroModel.find_livro(livro_id)

		#se existe livro...
		if livro:
			return livro.json()
		#senão... mensagem de erro	
		return {'message': 'Livro not found.'}, 404 #not found

	#Cria um novo item
	def post(self, livro_id):

		if LivroModel.find_livro(livro_id):
			return {"message": "Livro id '{}' already exists.".format(livro_id)}, 400 #Bad request

		dados = Livro.atributos.parse_args()
		livro = LivroModel(livro_id, **dados)

		#Salvar no banco de dados
		try:
			livro.save_livro()
		except:
			return{'message':'An internal error ocurred trying to save livro.'} ,500 #Internal server error
		return livro.json()

	#Altera um item já existente, ou cria um novo caso não exista
	def put(self, livro_id):

		dados = Livro.atributos.parse_args()		

		#se livro já existir, vai atualizar,
		#senão, vai criar
		livro_encontrado  = LivroModel.find_livro(livro_id)
		if livro_encontrado:
			livro_encontrado.update_livro(**dados)
			livro_encontrado.save_livro()
			return livro_encontrado.json(), 200
		livro = LivroModel(livro_id, **dados)	

		try:
			livro.save_livro()
		except:
			return{'message':'An internal error ocurred trying to save livro.'} ,500 #Internal server error
		
		return livro.json(), 201 #criado

	#deleta um item
	def delete(self, livro_id):
		livro = LivroModel.find_livro(livro_id)
		if livro:
			try:
				livro.delete_livro()
			except:
				return{'message':'An error has occured trying to delete livro.'}, 500
			return {'message': 'livro deleted.'}
		return {'message': 'livro not found'} , 404