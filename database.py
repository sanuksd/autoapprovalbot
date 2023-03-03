from pymongo import MongoClient
from configs import cfg

client = MongoClient(cfg.MONGO_URI)

users = client['main']['users']
groups = client['main']['groups']

def already_db(user_id):
        user = users.find_one({"user_id" : str(user_id)})
        if not user:
            return False
        return True

def already_dbg(chat_id):
        group = groups.find_one({"chat_id" : str(chat_id)})
        if not group:
            return False
        return True

def add_user(user_id):
    in_db = already_db(user_id)
    if in_db:
        return
    return users.insert_one({"user_id": str(user_id)}) 

def remove_user(user_id):
    in_db = already_db(user_id)
    if not in_db:
        return 
    return users.delete_one({"user_id": str(user_id)})
    
def add_group(chat_id):
    in_db = already_dbg(chat_id)
    if in_db:
        return
    return groups.insert_one({"chat_id": str(chat_id)})

def all_users():
    user = users.find({})
    usrs = len(list(user))
    return usrs

def all_groups():
    group = groups.find({})
    grps = len(list(group))
    return grps

def ban_user(self, user_id, ban_reason="No Reason"):

        ban_status = dict(

            is_banned=True,

            ban_reason=ban_reason

        )

        self.col.update_one({'id': user_id}, {'$set': {'ban_status': ban_status}})

def get_ban_status(self, id):

        default = dict(

            is_banned=False,

            ban_reason=''

        )

        user = self.col.find_one({'id':int(id)})

        if not user:

            return default

        return user.get('ban_status', default)

db = MongoClient(cfg.MONGO_URI)
