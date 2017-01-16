##For better view, please use the raw view to check contents
Check Request Status:
  Description : Used to poll request status
  Example - http://localhost:80/request/check_status?requestId=8DB753A4-3A56-4175-855A-1FD12525D273
  URL - http://localhost:80/request/check_status - GET
    Required Params:
      - requestId
    Response Data:
      - Response
        {
          "requestParameters": null,
          "success": true,
          "requestType": "create_user",
          "requestId": "8DB753A4-3A56-4175-855A-1FD12525D273",
          "requestStatus": "User Created - Your userId is 3C2FE460-DCEF-4B2A-B966-E3099DEEEDF4",
          "result": "success"
        }
Create User:
  Description : Used to create a UserName and Password to access FAAS API features
  Example - http://localhost:80/user/create?userName=dude_test_2&password=qwerty123
  URL - http://localhost:80/user/create - POST
    Required Params:
      - userName
      - password
    Response Data:
      - Initial Response
        {
          "requestParameters": "{\"userName\": \"dude_test_7\", \"password\": \"qwerty123\"}",
          "success": true,
          "requestType": "create_user",
          "requestId": "8DB753A4-3A56-4175-855A-1FD12525D273",
          "requestStatus": "Container To Be Spawned - cc_user_create_cont_11.02.2016_3333",
          "result": "in_progress"
        }
      - Polled response through check_request_status
        {
          "requestParameters": null,
          "success": true,
          "requestType": "create_user",
          "requestId": "8DB753A4-3A56-4175-855A-1FD12525D273",
          "requestStatus": "User Created - Your userId is 3C2FE460-DCEF-4B2A-B966-E3099DEEEDF4",
          "result": "success"
        }
Update User:
  Description : Used to update a UserName and Password of exisiting User details
  Example - http://localhost:80/user/update?userName=dude_test_2&password=qwerty124
  URL - http://localhost:80/user/update - PUT
    Required Headers For Login:
      - userName
      - password
    Required Params:
      - userName
      - password
    Response Data:
      - Initial Response
        {
          "requestParameters": "{\"userName\": \"dude_test_2_1\", \"password\": \"qwerty124\"}",
          "success": true,
          "requestType": "update_user",
          "requestId": "63D5FB77-BCDF-4E09-8A2B-E8940CFD6473",
          "requestStatus": "Container To Be Spawned - cc_user_update_cont_11.02.2016_7605",
          "result": "in_progress"
        }
      - Polled response through check_request_status
        {
          "requestParameters": null,
          "success": true,
          "requestType": "update_user",
          "requestId": "63D5FB77-BCDF-4E09-8A2B-E8940CFD6473",
          "requestStatus": "User Details Updated - Your userId is 5EF0C253-5F32-4EFF-96A1-A64D0520B36C",
          "result": "success"
        }
Delete User:
  Description : Used to delete a User
  Example - http://localhost:80/user/delete
  URL - http://localhost:80/user/delete - DELETE
    Required Headers For Login:
      - userName
      - password
    Response Data:
      - Initial Response
        {
          "requestParameters": "{}",
          "success": true,
          "requestType": "delete_user",
          "requestId": "EB3409E6-6E4D-4ADE-94ED-B976463C5DFE",
          "requestStatus": "Container To Be Spawned - cc_user_delete_cont_11.02.2016_8236",
          "result": "in_progress"
        }
      - Polled response through check_request_status
        {
          "requestParameters": null,
          "success": true,
          "requestType": "delete_user",
          "requestId": "EB3409E6-6E4D-4ADE-94ED-B976463C5DFE",
          "requestStatus": "User Deleted",
          "result": "success"
        }
Create Function:
  Description : Used to create a Function
  Example - http://localhost:80/function/create?functionName=dude_func_1
  URL - http://localhost:80/function/create - POST
    Required Headers For Login:
      - userName
      - password
    Required Params:
      - functionName
    Required Request Data:
      - functionContent
    Response Data:
      - Initial Response
        {
          "requestParameters": "{\"functionName\": \"dude_func_6\"}",
          "success": true,
          "requestType": "create_function",
          "requestId": "7E500EFB-B250-426F-9CF4-6A34D4B58554",
          "requestStatus": "Container To Be Spawned - cc_function_create_cont_11.02.2016_7587",
          "result": "in_progress"
        }
      - Polled response through check_request_status
        {
          "requestParameters": null,
          "success": true,
          "requestType": "create_function",
          "requestId": "7E500EFB-B250-426F-9CF4-6A34D4B58554",
          "requestStatus": "Function Created - Your functionId is D84731BD-78FA-4080-A48E-CB66B38E282A",
          "result": "success"
        }
Update Function:
  Description : Used to update a Function already created
  Example - http://localhost:80/function/update?functionName=dude_func_5
  URL - http://localhost:80/function/update - PUT
    Required Headers For Login:
      - userName
      - password
    Required Params:
      - functionName
    Required Request Data:
      - functionContent
    Response Data:
      - Initial Response
        {
          "requestParameters": "{\"functionName\": \"dude_func_5\"}",
          "success": true,
          "requestType": "update_function",
          "requestId": "B4454BCF-5DAA-40A5-9C21-63E397C013F1",
          "requestStatus": "Container To Be Spawned - cc_function_update_cont_11.02.2016_9020",
          "result": "in_progress"
        }
      - Polled response through check_request_status
        {
          "requestParameters": null,
          "success": true,
          "requestType": "update_function",
          "requestId": "B4454BCF-5DAA-40A5-9C21-63E397C013F1",
          "requestStatus": "Function Updated - Your functionId is 3266A758-9AE8-468E-8985-2D9D386F2763",
          "result": "success"
        }
Delete Function:
  Description : Used to delete a Function already created
  Example - http://localhost:80/function/delete?functionName=dude_func_6
  URL - http://localhost:80/function/delete? - DELETE
    Required Headers For Login:
      - userName
      - password
    Required Params:
      - functionName
    Response Data:
      - Initial Response
        {
          "requestParameters": "{\"functionName\": \"dude_func_6\"}",
          "success": true,
          "requestType": "delete_function",
          "requestId": "7EEEA3CA-86C8-4D79-B140-DA86EB95FA76",
          "requestStatus": "Container To Be Spawned - cc_function_delete_cont_11.02.2016_2212",
          "result": "in_progress"
        }
      - Polled response through check_request_status
        {
          "requestParameters": null,
          "success": true,
          "requestType": "delete_function",
          "requestId": "7EEEA3CA-86C8-4D79-B140-DA86EB95FA76",
          "requestStatus": "Function Deleted",
          "result": "success"
        }
Execute Function:
  Description : Used to execute a Function already created
  Example - http://localhost:80/function/update?functionName=dude_func_5
  URL - http://localhost:80/function/update - PUT
    Required Headers For Login:
      - userName
      - password
    Required Params:
      - functionName
    Required Request JSON - Input and Output Data:
        - Example = {
            "input_data" : {
                    "val_1" : 10,
                    "val_2" : 5
                    },
            "output_data" : {
                    "fib_val_1" : "Madhat Output 1",
                    "fib_val_2" : "Madhat Output 2"
                    }
                    }
    Response Data:
      - Initial Response
        {
          "requestParameters": "{\"functionName\": \"dude_func_5\"}",
          "success": true,
          "requestType": "execute_function",
          "requestId": "982061C0-CA64-4E51-A5B8-4BF127104DE2",
          "requestStatus": "Container To Be Spawned - cc_function_execute_cont_11.02.2016_8419",
          "result": "in_progress"
        }
      - Polled response through check_request_status
      {
        "requestParameters": "{u'fib_val_2': 8, u'fib_val_1': 89, 'update_val': 'Code Updated'}",
        "success": true,
        "requestType": "execute_function",
        "requestId": "982061C0-CA64-4E51-A5B8-4BF127104DE2",
        "requestStatus": "Run was Succesfull",
        "result": "{'output_text': 'Inside Madhat Update0\\nInside Madhat Update1\\n', 'outputData': \"{u'fib_val_2': 8, u'fib_val_1': 89, 'update_val': 'Code Updated'}\"}"
      }
