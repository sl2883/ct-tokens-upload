import csv
import json
import http.client
import time

##### CONSTANTS #####

ANDROID_PREFIX = '__g'
IOS_PREFIX = '-g'
PROFILE_FILE_NAME = 'profiles.csv'
API_PATH = "api.clevertap.com"

PROJECT_ID = 'TEST-779-684-5Z6Z'
PROJECT_PASSCODE = '2957bd1d8e72415982f9ab679832bdbc'

BUCKET_MAX = 100

COLUMN_USER_ID = "User Id"
COLUMN_DEVICE_ID = "Device ID"

COLUMN_DEVICE_OS = "Device OS"
COLUMN_TOKEN = "Token"
COLUMN_CTID = "ctid"

COLUMN_NAME = "Name"
COLUMN_EMAIL = "Email Address"

COLUMN_EMAIL_OPT_IN = "Email Opt In?"
COLUMN_PUSH_OPT_IN = "Push Opt In?"

COLUMN_CT_TYPE = "ct-type"

CT_TOKEN_TYPE_FCM = "fcm"
CT_TOKEN_TYPE_APNS = "apns"

VAL_ANDROID = "Android OS"
VAL_IOS = "ios"

STR_OBJECT_ID = "objectId"
STR_TS = "ts"
STR_TYPE = "type"
STR_HISTORICAL_DATA = "Historical_data"
STR_YES = "Yes"
STR_IDENTITY = "identity"
STR_PROFILE_DATA = "profileData"
STR_PROFILE = "profile"
STR_NAME = "Name"
STR_EMAIL = "Email"

STR_TOKEN_ID = "id"
STR_TOKEN = "token"
STR_TOKEN_DATA = "tokenData"

STR_TRUE = "TRUE"
STR_FALSE = "FALSE"

STR_MSG_PUSH = "MSG-push"
STR_MSG_EMAIL = "MSG-email"

STR_D = "d"

LOGS_STATUS = 1

##### CONSTANTS END HERE #####

def logger(str):
    """Logs the strings on console based on the LOGS_STATUS parameter. If 1, prints.

    Args:
        str (String): Value to be printed
    """    
    if(LOGS_STATUS == 1):
        print(str)

def remove_dashes_from_string(str):
    """Function to remove dashes from  a string and return the updated string

    Args:
        str (String): Input string

    Returns:
        String: Output String without dashes
    """    
    return str.replace('-', '').lower()

def get_ctid_from_hash_string(hashed, prefix):
    """Function to convert a string with hashes into CT id format

    Args:
        hashed (String): Input String
        prefix (String): Android prefix or IOS prefix

    Returns:
        String: Well formed CT id
    """    
    trimmed = remove_dashes_from_string(hashed)
    appended = prefix + trimmed
    return appended

def get_ctid_from_idfa(idfa):
    """Function to get CT id from IDFA

    Args:
        idfa (String): Apple identifier

    Returns:
        String: Well formated CT id
    """    
    return get_ctid_from_hash_string(idfa, IOS_PREFIX)

def get_ctid_from_adid(adid):
    """Function to get CT id from ADID

    Args:
        adid (String): Android identifier

    Returns:
        String: Well formated CT id
    """    
    return get_ctid_from_hash_string(adid, ANDROID_PREFIX)

def get_ctid_from_device_id(device_id, prefix):
    """Function to convert device_id to CT id

    Args:
        device_id (String): Device id of the user
        prefix (String): Based on android or ios, the prefix can be different

    Returns:
        String: Well formatted CT id
    """    
    return get_ctid_from_hash_string(device_id, prefix)

def get_ctid_from_user_id(user_id, prefix):
    """Function to convert user id to CT id

    Args:
        user_id (String): user identifier
        prefix (String): Based on android or id, the prefix can be different

    Returns:
        String: Well formatted CT id from user id
    """    
    return get_ctid_from_hash_string(user_id, prefix)

def get_ctid_android(device_id, user_id):
    """Function to get CT id from device id (if available) or user_id for Android

    Args:
        adid (String): Device identifier
        user_id (String): user identifier

    Raises:
        Exception: if user id or adid doesn't exist, raise exception

    Returns:
        String: Well formatted CT id
    """    
    if len(device_id) > 0:
        return get_ctid_from_device_id(device_id, ANDROID_PREFIX)
    elif len(user_id) > 0:
        return get_ctid_from_user_id(user_id, ANDROID_PREFIX)
    else:
        raise Exception("To get ctid, either adid or user id must exist for android")

def get_ctid_ios(device_id, user_id):
    """Function to get CT id from device_id (if available) or user id for ios

    Args:
        idfa (String): device identifier
        user_id (String): user identifier

    Raises:
        Exception: if user id or idfa doesn't exist, raise exception

    Returns:
        String: Well formatted CT id
    """    
    if len(device_id) > 0:
        return get_ctid_from_device_id(device_id, IOS_PREFIX)
    elif len(user_id) > 0:
        return get_ctid_from_user_id(user_id, IOS_PREFIX)
    else:
        raise Exception("To get ctid, either idfa or user id must exist for ios")

def get_profile_payload(ctid, identity, name, email, msg_email, msg_push):
    """Function to get a payload json for a user

    Args:
        ctid (String): Clevertap identifier
        identity (String): User identifier

    Returns:
        JSON: Profile json
    """    
    profile = {}
    profile[STR_OBJECT_ID] = ctid
    profile[STR_TS] = round(time.time())
    profile[STR_TYPE] = STR_PROFILE
    
    data = {}
    data[STR_HISTORICAL_DATA] = STR_YES
    if len(identity) > 0:
        data[STR_IDENTITY] = identity

    if len(name) > 0:
        data[STR_NAME] = name

    if len(email) > 0:
        data[STR_EMAIL] = email
    
    if len(msg_email) > 0:
        if msg_email == STR_TRUE:
            data[STR_MSG_EMAIL] = True
        else:
            data[STR_MSG_EMAIL] = False

    if len(msg_push) > 0:
        if msg_push == STR_TRUE:
            data[STR_MSG_PUSH] = True
        else:
            data[STR_MSG_PUSH] = False

    profile[STR_PROFILE_DATA] = data

    return profile

def get_profiles_list(profiles):
    """Function to get list of profile jsons from profiles object

    Args:
        profiles (List): List pf profile objects

    Returns:
        List: List of profile jsons
    """    
    logger("---get_profiles_list")
    profiles_list = []
    for profile in profiles:
        print(profile)
        profiles_list.append(get_profile_payload(
            profile[COLUMN_CTID], 
            profile[COLUMN_USER_ID], 
            profile[COLUMN_NAME], 
            profile[COLUMN_EMAIL],
            profile[COLUMN_EMAIL_OPT_IN],
            profile[COLUMN_PUSH_OPT_IN]
            ))
    
    return profiles_list

def get_profiles_payload(profiles):
    """Function to get complete payload for Upload profiles API

    Args:
        profiles (List): List of profiles to be uploaded

    Returns:
        JSON: Payload JSON
    """    
    logger("--get_profiles_payload")
    payload = {}
    payload[STR_D] = get_profiles_list(profiles)

    return payload
    
def get_token_payload(token, type, ctid):
    """Function to get token JSON from token value, type and CleverTap

    Args:
        token (String): Device token
        type (String): fcm/apns etc.
        ctid (String): Clevertap id

    Returns:
        JSON: Token Json
    """    
    token_payload = {}
    token_payload[STR_TYPE] = STR_TOKEN
    token_payload[STR_OBJECT_ID] = ctid

    data = {}
    data[STR_TOKEN_ID] = token
    data[STR_TYPE] = type

    token_payload[STR_TOKEN_DATA] = data

    return token_payload

def get_tokens_list(tokens):
    """Function to get the list of token jsons from profile objects

    Args:
        tokens (List): List of profile objects

    Returns:
        List: Tokens list
    """    
    logger("---get_tokens_list")
    tokens_list = []
    for token in tokens:
        tokens_list.append(get_token_payload(token[COLUMN_TOKEN], token[COLUMN_CT_TYPE], token[COLUMN_CTID]))
    
    return tokens_list    

def get_tokens_payload(tokens):
    """Function get get token payload for Upload profiles API

    Args:
        tokens (List): List of profiles with token value

    Returns:
        JSON: Tokens payload Json
    """    
    logger("--get_tokens_payload")
    payload = {}
    payload[STR_D] = get_tokens_list(tokens)

    return payload


def upload_api(payload):
    """Function to call the main upload api to send data to clevertap

    Args:
        payload (JSON): upload payload
    """    
    logger("-upload_api")
    logger(json.dumps(payload))
    conn = http.client.HTTPSConnection(API_PATH)
    headers = {
        'X-CleverTap-Account-Id': PROJECT_ID,
        'X-CleverTap-Passcode': PROJECT_PASSCODE,
        'Content-Type': 'application/json'
    }

    conn.request("POST", "/1/upload", json.dumps(payload), headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    return

def get_profiles():
    """CSV reader to get profiles

    Returns:
        List: List of profiles in CSV (including header)
    """    
    with open(PROFILE_FILE_NAME, newline='') as csvfile:
        profiles = csv.reader(csvfile, delimiter=',', quotechar='|')
        return profiles
    

def convert_profiles(header, profiles):
    """Function CSV rows to profile objects using header row

    Args:
        header (List): Strings in header
        profiles (List): Profile rows

    Returns:
        List: Profiles list
    """    
    logger("--convert_profiles")
    converted_profiles = []
    for profile in profiles:
        new_profile = {}
        index = 0
        for header_val in header:
            new_profile[header_val] = profile[index]
            index += 1
        converted_profiles.append(new_profile)

    return converted_profiles

def update_profiles(header, old_profiles):
    """Function to go through each row & create a CT id, create profiles and then upload

    Args:
        header (List): String list of headers
        old_profiles (List): rows of profiles
    """    
    logger("-update_profiles")
    profiles = convert_profiles(header, old_profiles)
    for profile in profiles:
        if profile[COLUMN_DEVICE_OS] == VAL_ANDROID:
            profile[COLUMN_CTID] = get_ctid_android(profile[COLUMN_DEVICE_ID], profile[COLUMN_DEVICE_ID])
            profile[COLUMN_CT_TYPE] = CT_TOKEN_TYPE_FCM
        else:
            profile[COLUMN_CTID] = get_ctid_ios(profile[COLUMN_DEVICE_ID], profile[COLUMN_DEVICE_ID])
            profile[COLUMN_CT_TYPE] = CT_TOKEN_TYPE_APNS

    profile_payload = get_profiles_payload(profiles)
    upload_api(profile_payload)

    token_payload = get_tokens_payload(profiles)
    upload_api(token_payload)

    return

def main():
    """Main function to read CSV, create buckets of profile and ensures 3 API calls per second
    """    
    with open(PROFILE_FILE_NAME, newline='') as csvfile:
        profiles = csv.reader(csvfile, delimiter=',', quotechar='|')
        index = 0
        current_bucket = []
        for profile in profiles:
            if index == 0:
                header = profile
            else:
                current_bucket.append(profile)
                if len(current_bucket) >= BUCKET_MAX:
                    update_profiles(header, current_bucket)
                    current_bucket = []
                    if index % 3 == 0:
                        time.sleep(1)
            index += 1
        
        if len(current_bucket) > 0:
            logger("bucket size: " + str(len(current_bucket)))
            update_profiles(header, current_bucket)


main()