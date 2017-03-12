
from flask_wtf import Form 
from wtforms import  SubmitField,SelectField
from wtforms.validators import Required

def get_component(collection):
	items=[]
	for data in c2.find():
		item=(data['num_id'],data['name'])
		items.append(item)
	return items

def get_data(collection1,collection2,key_component,key_words):
	data_less=copy.deepcopy(key_dict[key_words])
	data_proper=copy.deepcopy(key_dict[key_words])
	data_larger=copy.deepcopy(key_dict[key_words])
	data_sub={'过低':0,'过高':0,'正常':0}
	
	exmaple=c2.find_one({"name":key_component})
	componentid='d'+str(exmaple['num_id'])
	data_max = exmaple['maxium']
	data_min = exmaple['minium']

	for person in c1.find():
		if person[componentid]<data_min:
			data_less[person[key_words]]+=1
			data_sub['过低']+=1
		elif person[componentid]>data_max:
			data_larger[person[key_words]]+=1
			data_sub['过高']+=1
		else:
			data_proper[person[key_words]]+=1
			data_sub['正常']+=1

	data_list=[data_less,data_larger,data_proper,data_sub]

	return  data_list





class BloodComponentForm(Form):
	items=get_component(c2)
	items.insert(0,(0,''))
	status = SelectField('按成分查询',coerce=int,validators=[Required()],choices=items)
	submit =SubmitField('Submit')
	
