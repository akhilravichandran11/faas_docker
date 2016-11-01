#!/usr/bin/python
import ast
string = "{'update_user': {101: 'Container To Be Spawned - ', 102: 'Container Spawned'}, 'update_function': {101: 'Container To Be Spawned - ', 102: 'Container Spawned'}, 'execute_function': {101: 'Container To Be Spawned - ', 102: 'Container Spawned'}, 'delete_user': {101: 'Container To Be Spawned - ', 102: 'Container Spawned'}, 'create_user': {101: 'Container To Be Spawned - ', 102: 'Container Spawned'}, 'request_status': {101: 'Container To Be Spawned - ', 102: 'Container Spawned'}, 'delete_function': {101: 'Container To Be Spawned - ', 102: 'Container Spawned'}, 'create_function': {101: 'Container To Be Spawned - ', 102: 'Container Spawned'}}"
data_dict = ast.literal_eval(string)

print data_dict["update_user"][101]

