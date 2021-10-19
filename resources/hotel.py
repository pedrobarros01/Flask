from flask_restful import Resource
hoteis = [
    {
        'hotelId': 'alpha',
        'nome': 'AlphaHotel',
        'estrelas': 4.3,
        'diaria': 420.34,
        'cidade': 'Rio de Janeiro'
    },
    {
        'hotelId': 'bravo',
        'nome': 'BravoHotel',
        'estrelas': 4.4,
        'diaria': 380.90,
        'cidade': 'Santa Catarina'
    },
    {
        'hotelId': 'charlie',
        'nome': 'CharlieHotel',
        'estrelas': 3.9,
        'diaria': 320.20,
        'cidade': 'Rio de Janeiro'
    },
]
class Hoteis(Resource):
    def get(self):
        return {'hoteis': hoteis}