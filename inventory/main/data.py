""" Helper code to minimize main code """


class Objects(object):
    emptyItem = {"_id": "0000", "_rev": "0-0", "name": "", "nickname": "", "part": "", "partNo": "",
                 "partType": "", "partMfg": "", "location": "", "serial": "", "quantity": "", "description": "", "multi_serial": ""}


class Slack(object):
    def __init__(self, obj):
        self.name = obj["name"]
        self.num = obj["_id"]
        self.q = obj["quantity"]
        self.location = obj["location"]

    def __str__(self):
        return f"#{self.num} {self.name}\nQuantity: {self.q}\nLocation: {self.location}"


def getUser(user, client):
    try:
        result = client.client.users_info(user=user)
        return result
    except:
        return None


def newSlackUser(request):
    doc = {"_id": request['authed_user']['id'], "userid":{},
           "token": request['authed_user']['access_token']}
    return doc


def fg(db, s={"_id": {"$gt": {}}}, fields=[], **kwargs):
    """ Auto fetcher for db queries
    :param db: Database
    :param s: Selector
    :param fields: Fields """
    return db.get_query_result(s, fields, **kwargs)


def newPartsDoc(request):
    doc = {"_id": request["part"], "name": request["partName"], "nickname": request["partNickname"], "partNo": request["partno"], "partType": request["partType"], "partMfg": request["partMfg"], "part": int(request["partno"]),
           "location": "", "serial": request["serialno"], "quantity": request["quantity"], "description": "", "multi_serial": False}
    return doc


def getLatestNo(db):
    l = fg(db, fields=["_id"], sort=[{"_id": "desc"}])
    for each in l:
        return str(int(each["_id"]) + 1)


def delTags(x):
    if "_id" in x and "_rev" in x:
        x.pop("_id")
        x.pop("_rev")
    return x
