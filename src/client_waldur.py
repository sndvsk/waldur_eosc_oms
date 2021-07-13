# TODO README.md integration idea 3. task

# from curl requests in localhost -> developer tools
# Request method : POST
# 1.Waldur Organization -> http://localhost/api/customers/
# 2.Waldur Project      -> http://localhost/api/projects/
# 3.Waldur Order        -> http://localhost/api/marketplace-offerings/
# 4.Add new members     -> http://localhost/api/user-invitations/
#   Cancel invitation -> http://localhost/api/user-invitations/<invitation_id>/cancel/

# Remove organization is not working
# http://localhost/api/support-issues/
# Status Code: 424 Failed Dependency
# {"detail":"Extension is disabled."}


import os
import waldur_client as wc
import requests

USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')
waldur_url = "http://localhost/api/"


def get_token():
    WALDUR_AUTH = {'username': USERNAME, 'password': PASSWORD}
    r = requests.post('http://localhost/api-auth/password/', data=WALDUR_AUTH)
    token = r.json()
    return token['token']


TOKEN = get_token()
waldur_client = wc.WaldurClient(waldur_url, TOKEN)


# waldur_client.create_project("1f8643e30e424c8cbfbb960301c20fb0", "test123", "1111")
# created a project with this line in local waldur

# 1.
def create_organization():
    return None


# 2.
def create_project():
    return None


# 3.
def create_order():
    return None


# 4.
def create_new_member():
    return None
