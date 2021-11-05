import webbrowser
import json
import requests

# Links that will be used in the later part of code.
class links:
    getToken = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token"
    getHomebaseName = "https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{0}/client/QueryProfile?profileId=common_public"
    setHomebaseName = "https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{0}/client/SetHomebaseName?profileId=common_public"

print("Homebase Name Changer v1.0.0 by PRO100KatYT\n")

# Getting the token and using it to login into an account.
reqToken = requests.post(links.getToken, headers={"Authorization": "basic ZWM2ODRiOGM2ODdmNDc5ZmFkZWEzY2IyYWQ4M2Y1YzY6ZTFmMzFjMjExZjI4NDEzMTg2MjYyZDM3YTEzZmM4NGQ=", "Content-Type": "application/x-www-form-urlencoded"}, data={"grant_type": "authorization_code", "token_type": "eg1", "code": input("Insert the auth code:\n")})
reqTokenText = json.loads(reqToken.text)
if "errorMessage" in reqTokenText:
    print(f"\nERROR: {reqTokenText['errorMessage']}")
    input("\nPress ENTER to close the program.\n") 
    exit()
else:
    access_token = reqTokenText["access_token"]
    account_id = reqTokenText["account_id"]
    displayName = reqTokenText["displayName"]
    print(f"\nLogged in as {displayName}.")

# Changing the Homebase name.
homebaseHeaders = {"Authorization": f"bearer {access_token}", "Content-Type": "application/json"}
reqGetHomebaseName = requests.post(links.getHomebaseName.format(account_id), headers=homebaseHeaders, data="{}")
reqSetHomebaseName = requests.post(links.setHomebaseName.format(account_id), headers=homebaseHeaders, json={"homebaseName": input("\nEnter a new Homebase name:\n")})
reqGetHomebaseNameText = json.loads(reqGetHomebaseName.text)
reqSetHomebaseNameText = json.loads(reqSetHomebaseName.text)
if "errorMessage" in reqSetHomebaseNameText:
    if "Validation Failed. Invalid fields were [homebaseName]" in reqSetHomebaseNameText['errorMessage']:
        print("ERROR: The Homebase name can't be blank.")
    else:
        print(f"\nERROR: {reqSetHomebaseNameText['errorMessage']}")
    input("\nPress ENTER to close the program.\n")
    exit()
else:
    print(f"\nThe Homebase name for {displayName} has been succesfully changed from {reqGetHomebaseNameText['profileChanges'][0]['profile']['stats']['attributes']['homebase_name']} to {reqSetHomebaseNameText['profileChanges'][0]['profile']['stats']['attributes']['homebase_name']}.")
    input("\nPress ENTER to close the program.\n")
    exit()