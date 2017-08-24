from src.studio_connect import StudioConnect
from src.util import Util


def lambda_handler(event, context):
    APPID = 'amzn1.ask.skill.10a3c58d-75f9-4d1e-8c30-87313bf0b2c1'
    # Checks if program is called from a valid APPID
    if event['session']['application']['applicationId'] != APPID:
        raise ValueError("Invalid Application ID")
    # If it's an Intent Request...
    if event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"])
    # If it's a Launch Request...
    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    # If it's a Session Ended Request...
    if event["request"]["type"] == "SessionEndedRequest":
        return on_session_ended(event["request"], event["session"])

    return ''


def on_session_ended(request, session):
    # Say out goodbye to the user of the Alexa Skill
    util = Util()
    return Util.build_response(util, "",
                               Util.build_speechlet_response(
                                   util, '', "Goodbye", "", False))


def on_launch(request_id, session):
    # Welcome the User to the App
    util = Util()
    return Util.build_response(util, "",
                           Util.build_speechlet_response(
                               util, '', "Welcome to Studio", "", False))


def on_intent(intent_request, session):
    # Determines what intent has been called and what to do.
        intent_name = intent_request["intent"]["name"]
        sc = StudioConnect()
        sc.__setattr__('username', 'chris.risley@inferencesolutions.com')
        sc.__setattr__('password', 'a4c7ddf204e717f1')
        sc.__setattr__('api_key', '0667adce38adb35dc52bd808bb60c297')
        if intent_name == "Run_Workflow":
            return sc.run_workflow(intent_request["intent"]["slots"]['Workflow_ID']['value'], intent_name)
        if intent_name == "Update_Workflow":
            slots = intent_request["intent"]["slots"]
            return sc.update_workflow(slots['Workflow_ID']['value'],
                                      slots['Workflow_Name']['value'],
                                      slots['Workflow_Status']['value'],
                                      intent_name)
        if intent_name == "List_Scripts":
            return sc.list_all_scripts(intent_name)
        if intent_name == "Start_Callout":
            sc.__setattr__('api_key', '0972703c8a5e515ca6a1926b992fe62d61f12dd7')
            return sc.start_callout('16505211067', intent_name)
