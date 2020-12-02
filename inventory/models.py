from flask_login import UserMixin
from inventory import login_manager
from inventory.main.routes import fg
from cloudant import Cloudant
from pathlib import Path
import json
g = Path("inventory/main", "vcap-local.json")

client = None
with open(g.absolute()) as f:
    vcap = json.load(f)
    creds = vcap['services']['cloudantNoSQLDB'][0]['credentials']
    user = creds['username']
    password = creds['password']
    url = 'https://' + creds['host']
    client = Cloudant(user, password, url=url, connect=True)

userdb = client["bolts-users"]


@login_manager.user_loader
def load_user(user_id):
    return User.getUser(int(user_id))


class User(UserMixin):
    id = int()
    token = str()
    slackid = str()

    def __repr__(self):
        return f"{self.id} {self.slackid}"

    @staticmethod
    def getUser(uid):
        selector = {"_id": {"$gt": {}}}
        result = fg(userdb, selector, fields=['_id', 'userid', 'token'])
        for each in result:
            if each["userid"] == str(uid):
                id = each["userid"]
                token = each["token"]
                slackid = each["_id"]
                return User()
                # break
        # result = self.database[slackid]
        
        
        pass

    @staticmethod
    def getSlack(uid):
        result = userdb[uid]
        id = int(result["userid"])
        token = result["token"]
        slackid = result["_id"]
        return User()