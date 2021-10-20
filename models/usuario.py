from sql_alchemy import banco


class UserModel(banco.Model):
    __tablename__ = 'usuarios'

    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40))
    senha = banco.Column(banco.String(40))

    def __init__(self, login, senha):
        self.login = login
        self.senha = senha

    
    def json(self):
        return {
            'user_id': self.user_id,
            'login': self.login
        }

    @classmethod
    def encontar_usuario(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()
        if user:
            return user
        return None

    @classmethod
    def encontrar_por_login(cls, login):
        user = cls.query.filter_by(login=login).first()
        if user:
            return user
        return None

    def salvar_usuario(self):
        banco.session.add(self)
        banco.session.commit()


    def deletar_usuario(self):
        banco.session.delete(self)
        banco.session.commit()    