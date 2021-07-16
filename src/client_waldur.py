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
from waldur_client import WaldurClient
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
wc = WaldurClient(waldur_url, TOKEN)


# 1.
def create_organization(name, email, address, registration_code,
                        backend_id, abbreviation="", bank_account="", bank_name="",
                        contact_details="", country="", display_name="", domain="",
                        homepage="", native_name="", latitude=None, longitude=None,
                        owners=None, phone_number="", postal="", support_users=None, vat_code=""):
    if support_users is None:
        support_users = []
    if owners is None:
        owners = []

    return wc.create_customer(name=name, email=email, address=address, registration_code=registration_code,
                              backend_id=backend_id, abbreviation=abbreviation, bank_account=bank_account,
                              bank_name=bank_name, contact_details=contact_details, country=country,
                              display_name=display_name, domain=domain, homepage=homepage,
                              native_name=native_name, latitude=latitude, longitude=longitude,
                              owners=owners, phone_number=phone_number, postal=postal,
                              support_users=support_users, vat_code=vat_code)


# 2.
def create_project(customer_id, name, backend_id=None):
    return wc.create_project(customer_id, name, backend_id)


# 3.
def create_order(project, offering, plan, attributes=None, limits=None):
    return wc.create_marketplace_order(project=project, offering=offering,
                                       plan=plan, attributes=attributes, limits=limits)


# 4.
def create_new_member():
    # TODO
    return None


def update_order():
    pass


def update_project():
    pass


def update_organization():
    pass
