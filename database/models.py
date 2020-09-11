from pony.orm import *
from database.db import db


class Projectid(db.Entity):
    name = PrimaryKey(str)
    paymenthash = Required(str)
    allocatedapicalls = Required(str)
    usedapicalls = Required(int)


db.generate_mapping(create_tables=True)
