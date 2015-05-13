import falcon
import luhn
api = application = falcon.API()

luhn = luhn.Resource()
api.add_route('/v1.0/utilities/luhn', luhn)
