from flask_restful import Api
from . import endpoint

api = Api(prefix='/api')

api.add_resource(endpoint.UserRegistration, '/registration')
api.add_resource(endpoint.UserLogin, '/login')
api.add_resource(endpoint.GetCurrency, '/currency')
api.add_resource(endpoint.SaveCurrency, '/save')

# tests and haven't implemented endpoints
api.add_resource(endpoint.TestApi, '/test')
api.add_resource(endpoint.UserLogoutAccess, '/logout/access')
api.add_resource(endpoint.UserLogoutRefresh, '/logout/refresh')
api.add_resource(endpoint.TokenRefresh, '/token/refresh')
api.add_resource(endpoint.SecretResource, '/secret')

