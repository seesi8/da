import json
import re

def extract_ids(json_str):
    # Load the JSON string into a Python dictionary
    data = json.loads(json_str)
    # Extract all keys which are IDs from the dictionary
    first_key = next(iter(data))
    ids = [(key if key != "questions" else None) for key, value in data[first_key].items()]
    ids = [x for x in ids if x is not None]
    return ids

def replace_items(query, new_ids):
    # Find the portion of the query string that contains the items list
    items_start = query.find("\"items\":")
    if items_start == -1:
        return query  # Return the original query if no items list is found

    # Cut the query at the point where items list starts
    pre_items = query[:items_start + 8]  # Include the length of "\"items\":"
    post_items = query[items_start:].split(']', 1)[1]  # Split after the closing bracket of the items list

    # Construct the new items list from new_ids
    new_items = [{'id': f'{id}---1', 'reference': id} for id in new_ids]
    new_items_str = json.dumps(new_items)  # Convert list of dictionaries to JSON string

    # Combine the parts into a new query string
    new_query = f'{pre_items}{new_items_str}{post_items}'
    return new_query

# Example usage
# student_responses = "{\"228490232\": {\"FT6503\": [\"D\"], \"questions\": {\"f624fc4532330fcdd3d236e65b839e4a\": [\"D\"], \"3daa88fdef5dc4fa78e4ded6acfef798\": [\"D\"], \"5897cfb230a0e6b5dd8247c8f9c13c5c\": [\"C\"], \"295e52103998d191777f23c4b461f5f6\": [\"A\"], \"d0ea3f4f2c2b75a2203996c8000dca4b\": [\"C\"], \"327b140202852e459963d4e380f210b5\": [\"C\"], \"05a6e3ea6dafeaf5e91c67ed7cad306a\": [\"B\"], \"3581ffd54cbe1912838830d46896aeb4\": [\"A\"], \"622bb6e859e473b8f7e883fe1add010c\": [\"A\"], \"09d36962a5654378ade66dd673f6c5d2\": [\"A\"], \"59b77dc5930dfd528de54a38eb4c876d\": [\"B\"], \"f3b894aca031467799e572a6d3c2f943\": [\"C\"], \"1143c2293b1bcd5ddd0d07bef3caf4a6\": [\"C\"], \"ebd6d8df3b69ff983dc4670766ff8d36\": [\"A\"], \"e06e5bdf1b8587deec65ba5b29028d9e\": [\"B\"], \"9ac0c196a6e6b4d7d193b44561665ea1\": [\"B\"], \"886ac5a96f3264ae1e1277f0313e6e8f\": [\"C\"], \"bdc4895f32985fbf172642e3ad64666f\": [\"A\"], \"1e2b40178d446c1334927a93083160dd\": [\"D\"], \"57c73bfa80e9186409fa59079526f7c1\": [\"C\"], \"2ed95d89496219db4ae319e25e36de80\": [\"D\"], \"24c813e055fb6c519fdd1bbcd90d550a\": [\"C\"], \"36306f8e5ed48342bb66aa0e8b59002b\": [\"B\"], \"835329f9d926255445cb9600aed0fbe1\": [\"C\"], \"b9740da2ce3e83934109f7507cf07c92\": [\"C\"], \"713b2d1fbe08bf928c356e673ef1ba37\": [\"A\"], \"9f2e02504dff4387236aac320e83b1af\": [\"B\"], \"1e3d52701589e5e5de1ec8a2cc910883\": [\"D\"], \"d581cd921d3e51a467534c280883df2b\": [\"D\"], \"7280fcb3b18dbe1a04fb5ffe9b36a92b\": [\"A\"], \"0e208d65ebd100b097546762703c6f9a\": [\"A\"], \"e368c2bd61c5c6a3b32acce0fb07df17\": [\"A\"], \"4cbc742437467b666da90eb16c1a44c2\": [\"A\"], \"7705c0044a55ea0abc4c7e3c3d192966\": [\"D\"], \"81507d9edba710159491b5a6b0699214\": [\"B\"], \"468d095b3c24c9af805cdf8ca6b61d0a\": [\"D\"], \"b9c8a71038166909622b499638e731bb\": [\"D\"], \"e4af3f6803b5c0ed60eacdb1d3d2f7f3\": [\"C\"], \"71ff22226981e0f9bf8182b4c3a756c6\": [\"D\"], \"4e9972f98b399dfd662ff600a7ff4f90\": [\"C\"], \"d59a5943a7a8555353e01fb32feb73ea\": [\"C\"], \"d04bb670c74b8b48e2ae67ad9eb776fa\": [\"B\"], \"6e1316791e7e38327f8aea0efd6e204d\": [\"C\"], \"cf5e85b788c6052dc76b0f250d03621e\": [\"B\"], \"334aeeeada80ba422db48b33825cf91c\": [\"D\"], \"6d24f0103f3d43a213e61e043edc0cf3\": [\"D\"], \"42b5232f2cde444fdf035a2ec8692ec2\": [\"D\"], \"639da78195deb7ef02689abd576fd8e5\": [\"A\"]}, \"FT6502\": [\"D\"], \"FT6504\": [\"C\"], \"VH943512\": [\"A\"], \"VH943504\": [\"C\"], \"VH943508\": [\"C\"], \"FT6492\": [\"B\"], \"FT6494\": [\"A\"], \"FT6493\": [\"A\"], \"VH929369\": [\"A\"], \"VH929367\": [\"B\"], \"VH929366\": [\"C\"], \"VR004224\": [\"C\"], \"VR004227\": [\"A\"], \"VR004225\": [\"B\"], \"VR004226\": [\"B\"], \"FT579301\": [\"C\"], \"FT579300\": [\"A\"], \"FT579302\": [\"D\"], \"FT6222\": [\"C\"], \"VH943419\": [\"D\"], \"VH943380\": [\"C\"], \"VH943414\": [\"B\"], \"VH944246\": [\"C\"], \"VH963221\": [\"C\"], \"VH944247\": [\"A\"], \"VH944254\": [\"B\"], \"FT571077\": [\"D\"], \"FT571074\": [\"D\"], \"FT571075\": [\"A\"], \"VR597621\": [\"A\"], \"VR597620\": [\"A\"], \"VR597619\": [\"A\"], \"VR597622\": [\"D\"], \"FT559733\": [\"B\"], \"FT559732\": [\"D\"], \"FT559734\": [\"D\"], \"FT6488\": [\"C\"], \"FT6489\": [\"D\"], \"FT561114\": [\"C\"], \"FT561115\": [\"C\"], \"FT561113\": [\"B\"], \"VH921068\": [\"C\"], \"VH921075\": [\"B\"], \"VH921071\": [\"D\"], \"VH935970\": [\"D\"], \"VR183508\": [\"D\"], \"VR183507\": [\"A\"]}}"
student_responses = input("Input Student Respones: ")
query_string = "action=get&security={\"consumer_key\":\"gHpBBB2lEYn2EDoS\",\"domain\":\"apclassroom.collegeboard.org\",\"timestamp\":\"20250404-0245\",\"user_id\":\"228490232\",\"signature\":\"$02$300926dca276e6d2b35aa50d6c91940466ef47f5b61f46562674a7cb2a7f6f24\"}&request={\"user_id\":\"228490232\",\"session_id\":\"\",\"retrieve_tags\":true,\"organisation_id\":537,\"dynamic_items\":{\"data_table_seed\":\"seed\",\"seed_with_item_id\":true}}&usrequest={\"items\":[{\"id\":\"VH921024---1\",\"reference\":\"VH921024\"},{\"id\":\"VH921028---1\",\"reference\":\"VH921028\"},{\"id\":\"VH930290---1\",\"reference\":\"VH930290\"},{\"id\":\"VH930291---1\",\"reference\":\"VH930291\"},{\"id\":\"VH930259---1\",\"reference\":\"VH930259\"}]}"

# Get new IDs from the student responses
new_ids = extract_ids(student_responses)
# Replace the IDs in the query string
print(new_ids)
new_query_string = replace_items(query_string, new_ids)
print(new_query_string)
