#!/usr/bin/python

request_types = {
    "request_status": "Request Check Status",
    "create_user": "Create User",
    "update_user": "Update User Details",
    "delete_user": "Delete User",
    "create_function": "Create Function",
    "update_function": "Update Function Details",
    "delete_function": "Delete Function",
    "execute_function": "Execute Function",
    "docker_service_remove" : "Remove Docker Service"
}

container_image_names = {
    "create_user": "cc_user_create",
    "update_user": "cc_user_update",
    "delete_user": "cc_user_delete",
    "create_function": "cc_function_create",
    "update_function": "cc_function_update",
    "delete_function": "cc_function_delete",
    "execute_function": "cc_function_execute"
}

container_names = {
    "create_user": "cc_user_create",
    "update_user": "cc_user_update",
    "delete_user": "cc_user_delete",
    "create_function": "cc_function_create",
    "update_function": "cc_function_update",
    "delete_function": "cc_function_delete",
    "execute_function": "cc_function_execute"
}

service_image_names = {
    "create_user": "192.168.1.9:5000/cc_user_create",
    "update_user": "192.168.1.9:5000/cc_user_update",
    "delete_user": "192.168.1.9:5000/cc_user_delete",
    "create_function": "192.168.1.9:5000/cc_function_create",
    "update_function": "192.168.1.9:5000/cc_function_update",
    "delete_function": "192.168.1.9:5000/cc_function_delete",
    "execute_function": "192.168.1.9:5000/cc_function_execute"
}


service_names = {
    "create_user": "cc_user_create",
    "update_user": "cc_user_update",
    "delete_user": "cc_user_delete",
    "create_function": "cc_function_create",
    "update_function": "cc_function_update",
    "delete_function": "cc_function_delete",
    "execute_function": "cc_function_execute"
}

status_codes = {
    "request_status": {
        101 : "Container To Be Spawned - ",
        102 : "Container Spawned"
    },
    "create_user": {
        101 : "Container To Be Spawned - ",
        102 : "Container Spawned"
    },
    "update_user": {
        101 : "Container To Be Spawned - ",
        102 : "Container Spawned"
    },
    "delete_user": {
        101 : "Container To Be Spawned - ",
        102 : "Container Spawned"
    },
    "create_function": {
        101 : "Container To Be Spawned - ",
        102 : "Container Spawned"
    },
    "update_function": {
        101 : "Container To Be Spawned - ",
        102 : "Container Spawned"
    },
    "delete_function": {
        101 : "Container To Be Spawned - ",
        102 : "Container Spawned"
    },
    "execute_function": {
        101 : "Container To Be Spawned - ",
        102 : "Container Spawned"
    }
}