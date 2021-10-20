from flask_jwt_extended.utils import get_jwt
from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST
argumentos = reqparse.RequestParser()
argumentos.add_argument('login', type=str, required=True, help="login é obrigatório")
argumentos.add_argument('senha', type=str, required=True, help="senha é obrigatória")

class User(Resource):
    #/usuario/{user_id}
    def get(self, user_id):
        user = UserModel.encontar_usuario(user_id)
        if user:
            return user.json(), 200
        return {'message': 'usuario nao encontrado'}, 404
    
    @jwt_required()
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


    def post(self):
        dados = argumentos.parse_args()

        if UserModel.encontrar_por_login(dados['login']):
            return {'message':'usuario já existe'}, 404
        user = UserModel(**dados)
        try:
            user.salvar_usuario()
        except:
            return {'message': 'erro de servidor'}, 500
        return {'message': 'usuario criado com sucesso'}, 201


class Login(Resource):

    @classmethod
    def post(cls):
        dados = argumentos.parse_args()
        
        user = UserModel.encontrar_por_login(dados['login'])

        if user and safe_str_cmp(user.senha, dados['senha']):
            token_de_acesso = create_access_token(identity=user.user_id)
            return {'access_token': token_de_acesso}, 200
        return {'message': 'seu login ou sua senha estão incorretas'}, 401 #nao autorizado



class Logout(Resource):
    
    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti'] # pega o id do jwt
        BLACKLIST.add(jwt_id)
        return {'message': 'voce foi deslogado com sucesso'}, 200
     