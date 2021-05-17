import datetime as dt
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted



class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_show_time"

    def run(self, dispatcher: CollectingDispatcher, 
            tacker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=f"{dt.datetime.now()}")

        return []



class ActionCustomFallback(Action):
    """Executes the fallback action and goes back to the previous state
    of the dialogue"""

    def name(self) -> Text:
        return "custom_fallback_action"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Hi Leon!")

        # Revert user message which led to fallback.
        return [UserUtteranceReverted()]

        
class ActionAskAffirmation(Action):
    """Executes the fallback action and goes back to the previous state
    of the dialogue"""

    def name(self) -> Text:
        return "action_default_ask_affirmation"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        intent1 = tracker.latest_message['intent_ranking'][0].get("name")
        intent2 = tracker.latest_message['intent_ranking'][1].get("name")
        intent3 = tracker.latest_message['intent_ranking'][2].get("name")

        confidence1 = tracker.latest_message['intent_ranking'][0].get("confidence")
        confidence2 = tracker.latest_message['intent_ranking'][1].get("confidence")
        confidence3 = tracker.latest_message['intent_ranking'][2].get("confidence")

        string1 = "Meintest du " + str(intent1) + "? " + "Sicherheit: " + str(confidence1) + "."
        string2 = "Meintest du " + str(intent2) + "? " + "Sicherheit: " + str(confidence2) + "."
        string3 = "Meintest du " + str(intent3) + "? " + "Sicherheit: " + str(confidence3) + "."

        payload1 = "/" + str(intent1)
        payload2 = "/" + str(intent2)
        payload3 = "/" + str(intent3)

        buttons = []

        buttons.append({'title': string1, 'payload': payload1 })
        if confidence2 > 0.3:
            buttons.append({'title': string2, 'payload': payload2 })
        if confidence3 > 0.3:
            buttons.append({'title': string3, 'payload': payload3 })


        dispatcher.utter_message(text= "Ich bin mir nicht ganz sicher" , buttons=buttons)

        return [UserUtteranceReverted()]