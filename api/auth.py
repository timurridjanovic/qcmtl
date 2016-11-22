#import main handler
from qcmtl import Handler

#import error messages
from qcmtl import error_messages

#import models
from models.user_model import UserModel
from models.token_model import TokenModel

#import utilities
import logging

class Login(Handler):
    def post(self, version):
        token = self.request.get('token')
        if token:
            self.login_with_token(token)
            return
        
        email = self.request.get('email')
        password = self.request.get('password')
    
        if email and password:
            self.login_with_email_and_password(email, password)
            return

        self.throw_json_error({
            error_messages['error_key']: error_messages['request_error'],
            'error_types': { 'technical_error': 'Erreur technique. Veuillez reessayer plus tard.' }
        })
        return
        

    def login_with_token(self, token):
        token_model = TokenModel.get_by_id(int(token))

        if not token_model:
            self.throw_json_error({
                error_messages['error_key']: error_messages['token_error']
            })
            return
        
        user = token_model.user_key.get()
        self.render_json(self.query_to_json(user, 'user'))
        return

    def login_with_email_and_password(self, email, password):
        user = UserModel.is_valid_email_and_password(email, password)
        
        if not user:
            self.throw_json_error({
                error_messages['error_key']: error_messages['auth_error'],
                'error_types': { 'auth_error': 'Votre courriel et/ou votre mot de passe sont invalide.' }
            })
            return

        token = TokenModel.create_token(user.key)
        token_key = token.put()
        self.render_json({
            'user': self.query_to_json(user, None),
            'token': str(token_key.id())
        })
        return


class Logout(Handler):
    def post(self, version):
        token = self.request.get('token')
        if token:
            token_model = TokenModel.get_by_id(int(token))
            if token_model:
                token_model.key.delete()
                self.render_json({ 'loggedOut': True })
                return
        
        self.throw_json_error({
            error_messages['error_key']: error_messages['token_error'],
            'error_types': { 'technical_error': 'Erreur technique avec le token. Veuillez reessayer plus tard.' }
        })
        return


        
