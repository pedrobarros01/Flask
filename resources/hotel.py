from flask_restful import Resource, reqparse
from models.site import SiteModel
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required
import sqlite3
from resources.filtros import normalizar_parametro_path, consulta_com_cidade, consulta_sem_cidade






path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrelas_min', type=float)
path_params.add_argument('estrelas_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('limit', type=int)
path_params.add_argument('offset', type=int)

class Hoteis(Resource):

    def get(self):
        connection = sqlite3.connect('banco.db')
        cursor = connection.cursor()
        dados = path_params.parse_args()
        dados_validos = {chave : valor for chave, valor in dados.items() if valor != None}
        parametros = normalizar_parametro_path(**dados_validos)

        if not parametros.get('cidade'):
            tupla = tuple([valores for valores in parametros.values()])
            resultado = cursor.execute(consulta_sem_cidade, tupla)
        else:
            tupla = tuple([valores for valores in parametros.values()])
            resultado = cursor.execute(consulta_com_cidade, tupla)
        hoteis = []

        for linha in resultado:
            hoteis.append({
                'hotel_id': linha[0],
                'nome': linha[1],
                'estrelas': linha[2],
                'diaria': linha[3],
                'cidade': linha[4],
                'site_id': linha[5]
            })
        return {'hoteis': hoteis}


class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="o campo precisa ser obrigatorio")
    argumentos.add_argument('estrelas', type=float, required=True, help="o campo precisa ser obrigatorio")
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')
    argumentos.add_argument('site_id', type=int, required=True, help="precisa do id do site deste hotel")

    def get(self, hotel_id):
        hotel = HotelModel.encontrar_hotel(hotel_id)
        if hotel:
            return hotel.json(), 200
        else:
            return {'message': 'hotel not found'}, 404
            #nao econtrado

    @jwt_required()
    def post(self, hotel_id):
        if HotelModel.encontrar_hotel(hotel_id):
            return{'message': f'Hotel id {hotel_id} already exists.'}, 400
        
        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        if not SiteModel.encontrar_por_id(dados['site_id']):
            return {'message': 'nao pode criar esse hotel, pois o id do site nao exite'}, 400

        try:

            hotel.salvar_hotel()
        except:
            return {'message': 'falha tecnica'}, 500 #erro do server interno
        return hotel.json(), 200 #sucesso
    
    @jwt_required()
    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel_encontrado = HotelModel.encontrar_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.atualizar_hotel(**dados)
            hotel_encontrado.salvar_hotel()
            return hotel_encontrado.json(), 200
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.salvar_hotel()
        except:
            return {'message': 'falha tecnica'}, 500
        return hotel.json(), 201 #criado um novo hotel
    
    @jwt_required()
    def delete(self, hotel_id):
        hotel = HotelModel.encontrar_hotel(hotel_id)
        if hotel:
            try: 
                hotel.deletar_hotel()
            except:
                return {'message': 'falha tecnica'}, 500
            return {'message': 'hotel delete'}
        return {'message': 'hotel not found'}, 404