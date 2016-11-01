#!/usr/bin/python

data_dict = {
	"Key_1": "value 1",
	"Key_2":"value 2",
	"nested_dict" : {
		"inner_dude_1" : "inner dude 1",
		"inner_dude_2" : "inner dude 2"
	}
		
}




def convert_dict_to_list(data_dict):
	data_list = []
	for key, value in data_dict.iteritems():
		cur_key = key
		cur_value = value
		if type(value) is dict:
			cur_value = str(value)
		key_value = "%s=%s" %(cur_key,cur_value)
		data_list.append(key_value) 
	return data_list

data_list = convert_dict_to_list(data_dict)
print str(data_list)