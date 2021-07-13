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
    content = r.json()
    return content['token']


TOKEN = get_token()
waldur_client = wc.WaldurClient(waldur_url, TOKEN)

# waldur_client.create_project("1f8643e30e424c8cbfbb960301c20fb0", "test123", "1111")
# created a project with this line in local waldur


# test_project = waldur_client._get_project("73201e09c2724b4db6634fda8a3f7787")
# test_offering = waldur_client._get_offering("8eea8a6825da45a6bc0342574cdb0a97")
# test_plan = waldur_client._get_plan("f8afe3975cfa4dcc9a199b7ccf7c71bb")
# waldur_client.create_marketplace_order(project=test_project['uuid'], offering=test_offering['uuid'], plan=test_plan['uuid'])
# created an order with this line in local waldur

# 1.
def create_organization():
    # no features in WaldurClient atm
    return None


# 2.
def create_project(customer_id, name, backend_id):
    return waldur_client.create_project(customer_id, name, backend_id)


# 3.
def create_order(project, offering, plan, attributes=None, limits=None):
    return waldur_client.create_marketplace_order(project=project, offering=offering,
                                                  plan=plan, attributes=attributes, limits=limits)


# 4.
def create_new_member():
    # TODO
    return None


#create_project("1f8643e30e424c8cbfbb960301c20fb0", "test123", "1111")
#create_order("73201e09c2724b4db6634fda8a3f7787", "8eea8a6825da45a6bc0342574cdb0a97", "f8afe3975cfa4dcc9a199b7ccf7c71bb")