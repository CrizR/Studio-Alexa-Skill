import json
import requests
from requests.auth import HTTPDigestAuth
from src.util import Util


class StudioConnect(object):
    # Class for encapsulating login information and Https method calls
    username = ''
    password = ''
    api_key = ''
    token = ''

    def __setattr__(self, name: str, value: str) -> None:
        super().__setattr__(name, value)

    def __getattribute__(self, name: str) -> str:
        return super().__getattribute__(name)

    def reset_credentials(self):
        # Resets the credentials for this user
        self.username = ''
        self.password = ''
        self.api_key = ''
        self.token = ''

    def valid_input(self, items: []):
        # Determines if any of the given items are empty
        print("Validating Input")
        for item in items:
            if item == '' or item is None:
                raise ValueError("Illegal Input")
        return True

    def build_url(self, op_type: str, method_type: str):
        # Builds the url needed for retrieving data from the api
        print('Building URL')
        return "https://usstudio.inferencecommunications.com/studio_instance/studio-api/v1/" \
               + op_type \
               + "/" \
               + method_type\
               + "/"

    def build_url_v2(self, op_type: str, method_type: str):
        # Builds the v2 url needed for retrieving data from the api
        print('Building URL')
        return "https://usstudio.inferencecommunications.com/studio_instance/api/v1/outbound/call/" \
               + op_type \
               + "/" \
               + method_type\
               + "/"

    def retrieve_token(self):
        # Retrieves the token needed for authenticating the user
        self.valid_input([self.username, self.password, self.api_key])
        print("Retrieving Token")
        # Request Token
        data = requests.post(self.build_url('auth', 'get-token'), data={'apikey': self.api_key, "format": "json"},
                             auth=HTTPDigestAuth(self.username, self.password))
        print(data)
        # Parse JSON for Token
        try:
            new_token = json.loads(data.text)["result"]["token"]
            print('Token:' + new_token)
            self.__setattr__('token', new_token)
        except Exception:
            print("Could not extract token")
            return

    def list_all_scripts(self, intent: str) -> str:
        # Lists all the available scripts
        self.retrieve_token()
        self.valid_input([self.token])
        print("Listing Scripts")
        # List Scripts
        payload = {'token': self.token}
        data = requests.post(self.build_url('script', 'list-all'), data=payload)
        print(data)
        util = Util()
        try:
            data = json.loads(data.text)['result']['error']['message']
            print(data)
            return Util.build_response(util, "",
                                       Util.build_speechlet_response(
                                           util, intent, data, "", True))
        except Exception:
            print("Failed")
            return Util.build_response(util, "",
                                       Util.build_speechlet_response(
                                           util, intent, "Failed", "", True))

    def run_workflow(self, workflow_id: str, intent: str) -> str:
        # Runs the workflow that matches the given id
        self.retrieve_token()
        self.valid_input([self.token, workflow_id])
        print("Starting Workflow")
        # Run Workflow
        payload = {'token': self.token, 'workflow_id': workflow_id}
        data = requests.post(self.build_url('workflow', 'run'), data=payload)
        print(data)
        print(json.loads(data.text)['result'])
        util = Util()
        return Util.build_response(util, "", Util.build_speechlet_response(util,
            intent, "Initializing Workflow" + json.loads(data.text)['result'], "", True))

    def update_workflow(self, workflow_id: str, name: str, status: str, intent: str) -> str:
        # updates the workflow given the name and status arguments
        self.retrieve_token()
        self.valid_input([self.token, workflow_id, name, status])
        print("Updating Workflow")
        # Update Workflow
        payload = {'token': self.token, 'workflow_id': workflow_id, 'name': name, 'status': status}
        data = requests.post(self.build_url('workflow', 'update'), data=payload)
        print(data)
        print(json.loads(data.text)['result']['message'])
        util = Util()
        return Util.build_response(util, "", Util.build_speechlet_response(util,
            intent, "Updating Workflow" + json.loads(data.text)['result']['message'], "", True))

    def start_callout(self, phone_num: str, intent: str) -> str:
        # Stars a callout camapaign
        self.valid_input([self.api_key, phone_num])
        print("Starting Callout")
        data = requests.post(self.build_url_v2(self.api_key, phone_num))
        print(data)
        util = Util()
        return Util.build_response(util, "", Util.build_speechlet_response(util,
                                                                           intent, "Starting Campaign" +
                                                                           '',
                                                                           "", True))

