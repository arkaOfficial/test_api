import falcon

from look.images import Resource, CasbinAuth

api = application = falcon.API()

api.add_route('/images', Resource())
api.add_route('/auth', CasbinAuth())