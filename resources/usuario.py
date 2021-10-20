from flask_restful import Resource, reqparse
from models.usuario import UserModel


class User(Resource):
    #/usuario/{user_id}
    def get(self, user_id):
        user = UserModel.encontar_usuario(user_id)
        if user:
            return user.json(), 200
        return {'message': 'usuario nao encontrado'}, 404
    
    def delete(self, user_id):
        user = UserModel.encontar_usuario(user_id)
        if user:
            try:
                user.deletar_usuario()
            except:
                return {'message': 'erro de servidor'}, 500
            return {'message': 'usuario foi deletado'}, 200
        return {'message': 'usuario nao foi deletado'}, 404



class Cadastro(Resource):
    #/cadastro
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('login', type=str, required=True, help="login é obrigatório")
    argumentos.add_argument('senha', type=str, required=True, help="senha é obrigatória")

    def post(self):
        dados = Cadastro.argumentos.parse_args()

        if UserModel.encontrar_por_login(dados['login']):
            return {'message':'usuario já existe'}, 404
        user = UserModel(**dados)
        try:
            user.salvar_usuario()
        except:
            return {'message': 'erro de servidor'}, 500
        return {'message': 'usuario criado com sucesso'}, 201