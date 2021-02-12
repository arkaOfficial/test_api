import json
import falcon
import base64
from logging import info
import casbin
from look.casbin_pymongo_adapter.adapter import Adapter

B64_PADDING="==="

class Resource(object):

    def on_get(self, req, resp):
        doc = {
            'images': [
                {
                    'href': '/images/1eaf6ef1-7f2d-4ecc-a8d5-6e8adba7cc0e.png'
                }
            ]
        }

        # Create a JSON representation of the resource
        resp.body = json.dumps(doc, ensure_ascii=False)

        # The following line can be omitted because 200 is the default
        # status returned by the framework, but it is included here to
        # illustrate how this may be overridden as needed.
        resp.status = falcon.HTTP_200


class CasbinAuth(object):

    def on_get(self, request, response):
        try:
            request.headers.get('AUTHORIZATION')
            encoded_token = request.headers.get('AUTHORIZATION').split(' ')[-1]
            request.context['bearer'] = encoded_token
            token_body = base64.b64decode(encoded_token.split('.')[1] + B64_PADDING)
            body = json.loads(token_body)
        except:
            response.body = json.dumps({"error":"Send Valid Auth Token Pls (-_-) "})
            response.status = falcon.HTTP_401
            return

        # load policy from commons s3 and store it in cache
        #adapter = Adapter(dbname='casbin_test', host='mongos0.moengage.com')
        #casbin_sqlalchemy_adapter.Adapter()

        adapter = Adapter('mongos0.moengage.com', "casbin_policies")
        e = casbin.Enforcer("conf/casbin_model.conf", "conf/casbin_policy.csv")
        #e = casbin.Enforcer("conf/casbin_model.conf", adapter, True)
        sub =  body["role"] # the user that wants to access a resource.
        obj = "LoginSettings"  # the resource that is going to be accessed.
        act = "Write"  # the operation that the user performs on the resource.

        info("role ",sub, " | policy ",e.get_policy())
        if e.enforce(sub, obj, act):
            # permit alice to read data1
            response.status = falcon.HTTP_200
        else:
            # deny the request, show an error
            response.status =falcon.HTTP_403