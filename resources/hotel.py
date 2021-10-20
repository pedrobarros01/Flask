import re
from flask_restful import Resource, reqparse
from models.hotel import HotelModel
hoteis = [
    {
        'hotel_id': 'alpha',
        'nome': 'AlphaHotel',
        'estrelas': 4.3,
        'diaria': 420.34,
        'cidade': 'Rio de Janeiro'
    },
    {
        'hotel_id': 'bravo',
        'nome': 'BravoHotel',
        'estrelas': 4.4,
        'diaria': 380.90,
        'cidade': 'Santa Catarina'
    },
    {
        'hotel_id': 'charlie',
        'nome': 'CharlieHotel',
        'estrelas': 3.9,
        'diaria': 320.20,
        'cidade': 'Rio de Janeiro'
    },
]



class Hoteis(Resource):

    def get(self):
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}


class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="o campo precisa ser obrigatorio")
    argumentos.add_argument('estrelas', type=float, required=True, help="o campo precisa ser obrigatorio")
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    def get(self, hotel_id):
        hotel = HotelModel.encontrar_hotel(hotel_id)
        if hotel:
            return hotel.json(), 200
        else:
            return {'message': 'hotel not found'}, 404
            #nao econtrado

    def post(self, hotel_id):
        if HotelModel.encontrar_hotel(hotel_id):
            return{'message': f'Hotel id {hotel_id} already exists.'}, 400
        
        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        try:

            hotel.salvar_hotel()
        except:
            return {'message': 'falha tecnica'}, 500 #erro do server interno
        return hotel.json(), 200 #sucesso
    
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
    
    def delete(self, hotel_id):
        hotel = HotelModel.encontrar_hotel(hotel_id)
        if hotel:
            try: 
                hotel.deletar_hotel()
            except:
                return {'message': 'falha tecnica'}, 500
            return {'message': 'hotel delete'}
        return {'message': 'hotel not found'}, 404