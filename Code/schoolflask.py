

from flask import Flask, render_template,session,url_for,redirect,request,jsonify
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_script import Manager
#from datetime import datetime
from flask_wtf import Form 
from wtforms import StringField, SubmitField,BooleanField,SelectField
from wtforms.validators import Required
import chartkick
import pymongo
import copy
import time



connection=pymongo.Connection('0.0.0.0',27017) 
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
sex_dict={'男':0,'女':0}
age_dict={'0-9岁':0,'10-19岁':0,'20-29岁':0,'30-19岁':0,'40-49岁':0,
'50-59岁':0,'60-69岁':0,'70-79岁':0,'80-89岁':0,'90-150岁':0}

key_dict={'sex':copy.deepcopy(sex_dict),
'province':copy.deepcopy(province_dict),'age_range':copy.deepcopy(age_dict)}


age_range_list=['0-9岁','10-19岁','20-29岁','30-19岁','40-49岁',
'50-59岁','60-69岁','70-79岁','80-89岁','90-150岁']
		

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.jinja_env.add_extension("chartkick.ext.charts")

moment = Moment(app)
bootstrap =Bootstrap(app)
manager = Manager(app)




def get_component(collection):
	items=[]
	for data in c2.find():
		item=(data['num_id'],data['name'])
		items.append(item)
	return items

def get_data(key_component,key_words):
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

	data_list=[data_less,data_larger,data_proper,data_sub,data_min,data_max]

	return  data_list
'''
def get_string(flag):
	key_component=(c2.find_one({'num_id':1}))['name']
	return key_component
'''
def count_age():
	for data in c1.find():
		birthyear=data["birthyear"]
		age= time.localtime()[0]-birthyear
		c1.update({"num_id":data['num_id']},{"$set":{"age":age}})
		index_age=age//10
		if index_age<9:
			c1.update({"num_id":data['num_id']},{"$set":{"age_range":age_range_list[index_age]}})
		else:
			c1.update({"num_id":data['num_id']},{"$set":{"age_range":age_range_list[9]}})
		



class BloodComponentForm(Form):
	items=get_component(c2)
	items.insert(0,(0,''))
	status = SelectField('按成分查询',coerce=int,validators=[Required()],choices=items)
	submit =SubmitField('确定')
	



@app.route('/')
def index():
    return render_template('index.html')




@app.route('/sex', methods=['GET','POST'])
def sex():
	
	form =BloodComponentForm()
	
	
	

	if form.validate_on_submit():
		session['status']=form.status.data
		flag=session.get('status')
		key_component=(c2.find_one({'num_id':flag}))['name']
		data_list=get_data(key_component,'sex')
		session['text']=key_component
		session['status']=form.status.data
		session['data_less']=data_list[0]
		session['data_larger']=data_list[1]
		session['data_proper']=data_list[2]
		session['data_sub']=data_list[3]
		session['data_min']=data_list[4]
		session['data_max']=data_list[5]
		return redirect(url_for('sex'))
	
	return render_template('sex.html',text=session.get('text'),
		data_less=session.get('data_less'),data_larger=session.get('data_larger'),
		data_proper=session.get('data_proper'),
		data_sub=session.get('data_sub'),data_min=session.get('data_min'),
		data_max=session.get('data_max'),form=form)



@app.route('/age',methods=['GET','POST'])
def age():
	count_age()
	form =BloodComponentForm()
	if form.validate_on_submit():
		session['status']=form.status.data
		flag=session.get('status')
		key_component=(c2.find_one({'num_id':flag}))['name']
		data_list=get_data(key_component,'age_range')
		session['text']=key_component
		session['status']=form.status.data
		session['data_less']=data_list[0]
		session['data_larger']=data_list[1]
		session['data_proper']=data_list[2]
		session['data_sub']=data_list[3]
		session['data_min']=data_list[4]
		session['data_max']=data_list[5]
		
		return redirect(url_for('age'))
	return render_template('age.html',text=session.get('text'),
		data_less=session.get('data_less'),data_larger=session.get('data_larger'),
		data_proper=session.get('data_proper'),data_min=session.get('data_min'),
		data_max=session.get('data_max'),
		data_sub=session.get('data_sub'),form=form)

	
@app.route('/area',methods=['GET','POST'])
def area():
	form =BloodComponentForm()
	if form.validate_on_submit():
		session['status']=form.status.data
		flag=session.get('status')
		key_component=(c2.find_one({'num_id':flag}))['name']
		data_list=get_data(key_component,'province')
		session['text']=key_component
		session['status']=form.status.data
		session['data_less']=data_list[0]
		session['data_larger']=data_list[1]
		session['data_proper']=data_list[2]
		session['data_sub']=data_list[3]
		
		
		return redirect(url_for('area'))
	return render_template('area.html',text=session.get('text'),
		data_less=session.get('data_less'),data_larger=session.get('data_larger'),data_proper=session.get('data_proper'),
		data_sub=session.get('data_sub'),data_min=session.get('data_min'),
		data_max=session.get('data_max'),form=form)

	

	

@app.route('/viewmap',methods=['GET','POST'])
def viewmap():
	flag=session.get('status')
	if request.method == "POST":
		people_num=0
		#flag=1
		key_component=(c2.find_one({'num_id':flag}))['name']
		data_list=get_data(key_component,'province')
		data_list_less=[]
		data_list_larger=[]
		data_list_proper=[]
		province_list=list((copy.deepcopy(province_dict)).keys())
		
		for i  in range(0,3):
			for k,v in data_list[i].items():
				if v>people_num:
					people_num = v
		
		for province_id in province_list:
			data_list_less.append({'name':province_id,'value':(data_list[0])[province_id]})
			data_list_larger.append({'name':province_id,'value':(data_list[1])[province_id]})
			data_list_proper.append({'name':province_id,'value':(data_list[2])[province_id]})

		return jsonify(data_less=data_list_less,data_larger=data_list_larger,
			data_proper=data_list_proper,people_num=people_num,key_component=key_component) 
        
	return render_template('viewmap.html')

if __name__=="__main__":
	app.run(debug=True)

