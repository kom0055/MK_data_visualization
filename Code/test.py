

import pymongo
import time
import random as r
import copy


connection=pymongo.MongoClient('0.0.0.0',27017) 
db=connection.meikang
c1=db.UserDetected
c2=db.ComponentStandard

count=c1.find_one({"num_id":2})
print(count)