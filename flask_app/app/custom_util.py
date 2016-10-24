#!/usr/bin/python

def custom_print(obj, sepeartor='\n'):
    if type(obj) is dict:
        return custom_print_dict(obj, sepeartor)
    elif type(obj) is list:
        return custom_print_list(obj, sepeartor)
    else:
        return str(obj)

def custom_print_list(obj, sepeartor='\n'):
    final_string = []
    for current_item in obj:
        final_string.append(custom_print(current_item, sepeartor))
    final_string.append("*" * 10)
    return ("%s%s" % (sepeartor, sepeartor)).join(final_string)


def custom_print_dict(obj, sepeartor='\n'):
    final_string = []
    for key in obj:
        current_string = str(key) + " - " + custom_print(obj[key], sepeartor)
        final_string.append(current_string)
    final_string.append("#" * 10)
    return ("%s" % sepeartor).join(final_string)