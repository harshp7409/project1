import boto3
from datetime import datetime, timezone

iam = boto3.client('iam')
list_data = []
list_user = []

def get_access_key():
    try:
        paginator = iam.get_paginator('list_users')
        for page in paginator.paginate():
            print("page",page)
            for user in page['Users']:

                 paginator = iam.get_paginator('list_access_keys')
                 for response in paginator.paginate(UserName=user['UserName']):
                     # print(response)
                     data = response.get('AccessKeyMetadata')
                     print("DATA",data)
                     # res = [ sub['gfg'] for sub in test_list ]
                     i = data[0]['AccessKeyId']
                     j = data[0]['UserName']
                     print("Value", i)
                     print("JJ",j)
                     list_data.append(i)
                     list_user.append(j)
                     # dict_1['AccessKeyId'] = i
                     # dict_1['UserName'] = j

                 # print("final_list",list_data)
                 # print("DICT",dict_1)

    except:
        print("Something went wrong")

    return list_data , list_user

def update_operation():

    get_access_key()
    final_list = list_data
    print("final_list",final_list)
    final_user = list_user
    print("final_user", final_user)
    res_dict = {final_list[k]: final_user[k] for k in range(len(final_list))}
    print("res_dict",res_dict)


    for i in final_list:
        response_lastused = iam.get_access_key_last_used(AccessKeyId=i)
        response_lastused_key = response_lastused['AccessKeyLastUsed']
        print("response_lastused_key",response_lastused_key)
        print("response_lastused_key",response_lastused_key['ServiceName'])
        key = 'LastUsedDate'
        if key in response_lastused_key:
            print(f"Yes, key: '{key}' exists in dictionary")
            today = datetime.now(timezone.utc)
            print("TODAY",today)
            difference = response_lastused_key['LastUsedDate'] - today
            td = difference.days
            print("Days difference",td)
            if td <= -10:
                iam.update_access_key(AccessKeyId=i,Status='Inactive',UserName=res_dict.get(i))

        else:
            print(f"No, key: '{key}' does not exists in dictionary")


if __name__ == '__main__':
    update_operation()