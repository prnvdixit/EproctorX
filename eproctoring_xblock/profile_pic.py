import hashlib

def get_pic_path(user_name) :
    string = "placeholder_secret_key" + user_name

    path =  "/edx/var/edxapp/media/profile-images/" + hashlib.md5(string.encode('utf-8')).hexdigest() + "_500.jpg"
    return path
