from pony.orm import *
from database.db import db


class Projectid(db.Entity):
    name = PrimaryKey(str)
    paymenthash = Required(str)
    allocatedapicalls = Required(str)
    usedapicalls = Required(int)

    project_ids = Set('')


db.generate_mapping(create_tables=True)

