from flask_restful import Resource, reqparse
from models.site import SiteModel


class Sites(Resource):
    def get(self):
        return{'sites': [site.json() for site in SiteModel.query.all()]}

class Site(Resource):
    def get(self, url):
        site = SiteModel.encontar_site_por_url(url)
        if site:
            return site.json(), 200
        return {'message': 'site nao encontrado'}, 404 #not found

    def post(self, url):
        if SiteModel.encontar_site_por_url(url):
            return {'message': f' o site {url} ja esta cadastrado'}, 400 #bad request
        site = SiteModel(url)
        try:
            site.salvar_site()
        except:
            return {'message': 'erro de servidor'}, 500 #erro de servidor
        return site.json(), 200 #sucesso


    def delete(self, url):
        site = SiteModel.encontar_site_por_url(url)
        if site:
            try:
                site.deletar_site()
            except:
                return {'message': 'erro de servidor'}, 500
            return {'message': 'site deletado'}, 200
        return {'message': 'site não existe para o delete'}, 404