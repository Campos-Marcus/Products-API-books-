from sql_alchemy import banco

class LivroModel(banco.Model):
	#mapeando que essa classe é uma tabela no db
	__tablename__='livros'
	
	livro_id = banco.Column(banco.Float, primary_key=True)
	nome = banco.Column(banco.String(80))
	preco = banco.Column(banco.Float(precision=1))
	quantidade = banco.Column(banco.Float(precision=2))
	

	def __init__(self, livro_id, nome, preco, quantidade):
		self.livro_id = livro_id
		self.nome = nome
		self.preco = preco
		self.quantidade = quantidade

	def json(self):
		return {
			'livro_id': self.livro_id,
			'nome': self.nome,
			'preco': self.preco,
			'quantidade': self.quantidade,	
		}

	#cls é abreviação do nome da classe	
	@classmethod
	def find_livro(cls, livro_id):
		livro = cls.query.filter_by(livro_id=livro_id).first() #SSELECT * FROM livros where livro_id =  $livro_id
		if livro:
			return livro
		return None

	def save_livro(self):
		banco.session.add(self)
		banco.session.commit()

	def update_livro(self, nome, preco, quantidade):
		self.nome = nome
		self.preco = preco
		self.quantidade = quantidade		

	def delete_livro(self):
		banco.session.delete(self)
		banco.session.commit()