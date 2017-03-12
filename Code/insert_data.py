

import pymongo
import time
import random as r
import copy


connection=pymongo.MongoClient('0.0.0.0',27017) 
db=connection.meikang
c1=db.UserDetected
c2=db.ComponentStandard
province_dict={
'北京':0,'上海':0,'天津':0,'重庆':0,'黑龙江':0,'吉林':0,'辽宁':0,
'江苏':0,'山东':0,'安徽':0,'河北':0,'河南':0,'湖北':0,'湖南':0,
'江西':0,'陕西':0,'山西':0,'四川':0,'青海':0,'海南':0,'广东':0,
'贵州':0,'浙江':0,'福建':0,'台湾':0,'甘肃':0,'云南':0,'内蒙古':0,
'宁夏':0,'新疆':0,'西藏':0,'广西':0,
'香港':0,'澳门':0}
sex_list=['男','女']
province_list=list((copy.deepcopy(province_dict)).keys())

last_name=['赵','钱','孙','李','周','吴','郑','王','冯','陈','楮','卫','蒋','沈','韩','杨',
'朱','秦','尤','许','何','吕','施','张','孔','曹','严','华','金','魏','陶','姜']
middle_name=['玉','明','龙','芳','军','玲','娜','丽','鹏','如']
first_name=['','国','月','智','辉','音','欣']
count=c1.find().count()+2
for i in range(300):
	name=r.choice(last_name)+r.choice(middle_name)+r.choice(first_name)
	count+=1
	c1.insert({
	"name":name,
	"num_id":count,
    "birthyear":r.randint(1917,2016),
    "age" : 0,
    "age_range" : '',
    "sex" : r.choice(sex_list),
    "province" : r.choice(province_list),
    "d1" : r.uniform(1,60),
    "d2" : r.uniform(1,60),
    "d3" : r.uniform(1,30),
    "d4" : r.uniform(0,15),
    "d5" : r.uniform(0.5,15),
    "d6" : r.uniform(0.1,30),
    "d7" : r.uniform(10,160),
    "d8" : r.uniform(1,80),
    "d9" : r.uniform(20,90),
    "d10" : r.uniform(40,100),
    "d11" : r.uniform(5,50),
    "d12" : r.uniform(0,15),
    "d13" : r.uniform(1,60),
    "d14" : r.uniform(0,30),
    "d15" : r.uniform(20,160),
    "d16" : r.uniform(0.1,25),
    "d17" : r.uniform(50,530),
    "d18" : r.uniform(0,15),
    "d19" : r.uniform(0,5),
    "d20" : r.uniform(0,15),
    "d21" : r.uniform(0,2),
    "d22" : r.uniform(0,5),
    "d23" : r.uniform(15,50),
    "d24" : r.uniform(5,50)
	})
	
#print(c1.find().count())
#print(c2.find().count())