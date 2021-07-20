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


import requests
from src.utils import USERNAME, PASSWORD


def get_token():
    WALDUR_AUTH = {'username': USERNAME, 'password': PASSWORD}
    r = requests.post('http://localhost/api-auth/password/', data=WALDUR_AUTH)
    content = r.json()
    return content['token']


TOKEN = get_token()