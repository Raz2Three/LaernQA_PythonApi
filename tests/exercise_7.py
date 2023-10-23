import requests

methods_in_list = ["GET", "POST", "PUT", "DELETE"]
methods_not_in_list = ["OPTIONS", "HEAD", "PATCH"]

# -----QUESTION 1
print("METHODS IN LIST---------->")
for method in methods_in_list:
    response = requests.request(method, "https://playground.learnqa.ru/ajax/api/compare_query_type")
    print(f"{method}: {response.text}")

# -----QUESTION 2
print("METHODS NOT IN LIST---------->")
for method in methods_not_in_list:
    response = requests.request(method, "https://playground.learnqa.ru/ajax/api/compare_query_type")
    print(f"{method}: {response.text}")

# -----QUESTION 3
print("METHODS IN LIST WITH PARAMS/PAYLOAD---------->")
for method in methods_in_list:
    if method == "GET":
        query_paramas = {"method": method}
        response = requests.request(method, "https://playground.learnqa.ru/ajax/api/compare_query_type",
                                    params=query_paramas)
        print(f"{method}: {response.text}")
    else:
        payload = {"method": method}
        response = requests.request(method, "https://playground.learnqa.ru/ajax/api/compare_query_type",
                                    data=payload)
        print(f"{method}: {response.text}")

# -----QUESTION 4
for method in methods_in_list:
    for method_2 in methods_in_list:
        if method == "GET":
            query_paramas = {"method": method_2}
            response = requests.request(method, "https://playground.learnqa.ru/ajax/api/compare_query_type",
                                        params=query_paramas)
            try:
                resp_json = response.json()
                success = resp_json.get("success", "=(")
                print(f"Method: {method}, Params method: {method_2}, Success: {success}")
            except:
                success = resp_json.get("success", "=(")
                print(f"Method: {method}, Params method: {method_2}, Success: {success}")

        else:
            payload = {"method": method}
            response = requests.request(method, "https://playground.learnqa.ru/ajax/api/compare_query_type",
                                        data=payload)
            try:
                resp_json = response.json()
                success = resp_json["success"]
                print(f"Method: {method}, Payload  method: {method_2}, Success: {success}")
            except:
                success = "=)"
                print(f"Method: {method}, Payload method: {method_2}, Success: {success}")
