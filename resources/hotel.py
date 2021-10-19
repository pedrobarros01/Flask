from flask_restful import Resource, reqparse
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
        return {'hoteis': hoteis}


class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    def pesquisa_se_existe(self, hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return None

    def get(self, hotel_id):
        hotel = self.pesquisa_se_existe(hotel_id)
        if hotel:
            return hotel
        else:
            return {'message': 'hotel not found'}, 404
            #nao econtrado

    def post(self, hotel_id):

        
        dados = Hotel.argumentos.parse_args()

        novo_hotel = {'hotel_id': hotel_id, **dados}
        hoteis.append(novo_hotel)
        return novo_hotel, 200 #sucesso
    
    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel = self.pesquisa_se_existe(hotel_id)
        novo_hotel = {'hotel_id': hotel_id, **dados}
        if hotel:
            hotel.update(novo_hotel)
            return novo_hotel, 200

        else:
            hoteis.append(novo_hotel)
        return novo_hotel, 201 #criado um novo hotel
    
    def delete(self, hotel_id):
        global hoteis
        hoteis_lista = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]
        hoteis = hoteis_lista
        return {'message': 'hotel delete'}