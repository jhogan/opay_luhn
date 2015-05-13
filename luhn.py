import falcon
import json
from datetime import datetime

class Resource(object):
    def on_post(self, req, resp):
        """ Accept iin, bin, sponsor and account in the posted json, calculate
        luhn checksum, and return cc number with luhn chksum as well as the
        date generated in a json string. """

        # TODO: Add lots of error handling for json data
        d = json.loads(req.stream.read())

        # Get cc with luhn check digit appended to the end
        cc = ccwithluhn(d['iin'], d['bin'], d['sponsor'], d['account'])
        utcnow = datetime.utcnow().strftime("%Y-%m-%d %H:%M")

        resp.body = json.dumps({"cardnumber": cc, "datetime_generated": utcnow})
        resp.status = falcon.HTTP_200

def ccwithluhn(iin, bin, sponsor, acct):
    """ Take cc numbers, concatentate them, then return with an appended luhn
    check digit. """

    cc = iin + bin + sponsor + acct # cc without check digit
    chksum = luhnchksum(cc)
    return cc + str(chksum)

def luhnchksum(card_number):
    """ Calculate and return luhn checksum digit. """
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d*2))
    return checksum % 10
        
