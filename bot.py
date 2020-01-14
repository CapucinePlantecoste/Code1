"""
LISTE DES INTENTIONS

1. Réservation de salle
2. Bonjour
3. Veut ne plus avoir à faire à un BOT (gérer l'énervement)
4. Obtention de l'emploi du temps
5. Adresse de l'école

"""
from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount
import json
import os.path
from pprint import pprint
from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from msrest.authentication import CognitiveServicesCredentials

SUBSCRIPTION_KEY_ENV_NAME = "LUIS_AUTHORING_KEY"#Modification

class MyBot(ActivityHandler):
    
    async def on_message_activity(self, turn_context: TurnContext):        
        
        await turn_context.send_activity(f"Tu as dit '{ turn_context.activity.text }'")#cette variable est le mot que l'utilisateur rentre
        
        monType = type (turn_context.activity.text)
        print (monType)#j'affiche le type : il est toujours de type str
        if turn_context.activity.text.isdigit():#si on peut le convertir en type int 
            turn_context.activity.text= int (turn_context.activity.text) #on le convertit en type int  
        
            if turn_context.activity.text%2==0:#si c'est pair 
                await turn_context.send_activity(f"C'est pair")
        
            else :#si c'est impair
                await turn_context.send_activity(f"C'est impair")

        CWD = os.path.dirname(__file__)
        print ("coucou1")#lui s'affiche, ca marche 

        authoring_key = "1e58a4a4242342afb484f85352ef5c72"

        def runtime(authoring_key): 
            print ("coucou2")#ne s'affiche pas 
            client = LUISRuntimeClient(
                'https://westus.api.cognitive.microsoft.com',
                CognitiveServicesCredentials(authoring_key),
            )

            print ("coucou3") #ne s'affiche pas car je ne rentre pas dans le def 

            luis_result = client.prediction.resolve("echo-bot")

            try :

                query = 'https://westus.api.cognitive.microsoft.com/luis/prediction/v3.0/apps/7d7790aa-e24d-425f-a286-9ca3fac558a2/slots/production/predict?subscription-key=1e58a4a4242342afb484f85352ef5c72&verbose=true&show-all-intents=true&log=true&query=YOUR_QUERY_HERE' #MODIFICATION
                print("Executing query: {}".format(query))
                result = client.prediction.resolve("7d7790aa-e24d-425f-a286-9ca3fac558a2", query)#Problème ici, le client n'est pas reconnu 

                print("\nDetected intent: {} (score: {:d}%)".format(
                    result.top_scoring_intent.intent,
                    int(result.top_scoring_intent.score*100)
                ))
                print("Detected entities:")
                for entity in result.entities:
                    print("\t-> Entity '{}' (type: {}, score:{:d}%)".format(entity.entity,entity.type, int(entity.additional_properties['score']*100)))
                print("\nComplete result object as dictionnary")
                pprint(result.as_dict())

            except Exception as err:
                print("Encountered exception. {}".format(err))
        
    async def on_members_added_activity(self, members_added: ChannelAccount,turn_context: TurnContext):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")


if __name__ == "__main__":
    import sys
    import os.path
    sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))
    from tools import execute_samples
    execute_samples(globals(), SUBSCRIPTION_KEY_ENV_NAME)
 #je ne sais pas a quoi ca sert 
    

