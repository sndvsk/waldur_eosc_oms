# waldur_eosc_oms

Test resource

	https://marketplace-3.docker-fid.grid.cyf-kr.edu.pl/services/nordic-test-resource-1

Test provider

	https://marketplace-3.docker-fid.grid.cyf-kr.edu.pl/providers/tnp



Integration idea

1. Create a Waldur offering matching the one in EOSC Beta MP
2. Poll /api/v1/oms/{oms_id}/events

   a. Check if there are new requests

3. If new requests

   a. Waldur Organization = Get or create organization based on project affiliation data from EOSC MP

   b. Waldur Project = get or create project based on project data

   c. Waldur Order = create a new order for the offering using info from EOSC MP

   d. Add new members into the project if not yet present based on the info about the request.


# TODO how to use this repo