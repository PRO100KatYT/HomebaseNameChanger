print("Homebase Name Changer v1.1.0 by PRO100KatYT\n")

try:
    import json
    import requests
    import webbrowser
except Exception as emsg:
    input(f"ERROR: {emsg}. To run this program, please install it.\n\nPress ENTER to close the program.")
    exit()

# Links that will be used in the later part of code.
class links:
    loginLink1 = "https://www.epicgames.com/id/api/redirect?clientId=ec684b8c687f479fadea3cb2ad83f5c6&responseType=code"
    loginLink2 = "https://www.epicgames.com/id/logout?redirectUrl=https%3A%2F%2Fwww.epicgames.com%2Fid%2Flogin%3FredirectUrl%3Dhttps%253A%252F%252Fwww.epicgames.com%252Fid%252Fapi%252Fredirect%253FclientId%253Dec684b8c687f479fadea3cb2ad83f5c6%2526responseType%253Dcode"
    getToken = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token"
    profileRequest = "https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{0}/client/{1}?profileId=common_public"

# Getting the token and using it to login into an account.
isLoggedIn = input("Are you logged into your Epic account that you would like the program to use in your browser?\nType 1 if yes and press ENTER.\nType 2 if no and press ENTER.\n")
while True:
    if (isLoggedIn == "1" or isLoggedIn == "2"): break
    else: isLoggedIn = input("\nYou priovided a wrong value. Please input it again.\n")
input("\nThe program is going to open an Epic Games webpage.\nTo continue, press ENTER.\n")
if isLoggedIn == "1": loginLink = links.loginLink1
else: loginLink = links.loginLink2
webbrowser.open_new_tab(loginLink)
print(f"If the program didnt open it, copy this link to your browser: {loginLink}\n")
reqToken = requests.post(links.getToken, headers={"Authorization": "basic ZWM2ODRiOGM2ODdmNDc5ZmFkZWEzY2IyYWQ4M2Y1YzY6ZTFmMzFjMjExZjI4NDEzMTg2MjYyZDM3YTEzZmM4NGQ=", "Content-Type": "application/x-www-form-urlencoded"}, data={"grant_type": "authorization_code", "token_type": "eg1", "code": input("Insert the auth code:\n")})
reqTokenText = json.loads(reqToken.text)
if "errorMessage" in reqTokenText:
    print(f"\nERROR: {reqTokenText['errorMessage']}")
    input("\nPress ENTER to close the program.\n") 
    exit()
access_token = reqTokenText["access_token"]
account_id = reqTokenText["account_id"]
displayName = reqTokenText["displayName"]
print(f"\nLogged in as {displayName}.")

# Changing the Homebase name.
homebaseHeaders = {"Authorization": f"bearer {access_token}", "Content-Type": "application/json"}
reqGetHomebaseName = requests.post(links.profileRequest.format(account_id, "QueryProfile"), headers=homebaseHeaders, data="{}")
reqSetHomebaseName = requests.post(links.profileRequest.format(account_id, "SetHomebaseName"), headers=homebaseHeaders, json={"homebaseName": input("\nEnter a new Homebase name:\n")})
reqGetHomebaseNameText = json.loads(reqGetHomebaseName.text)
reqSetHomebaseNameText = json.loads(reqSetHomebaseName.text)
if "errorMessage" in reqSetHomebaseNameText:
    if "Validation Failed. Invalid fields were [homebaseName]" in reqSetHomebaseNameText['errorMessage']: print("ERROR: The Homebase name can't be blank.")
    else: print(f"\nERROR: {reqSetHomebaseNameText['errorMessage']}")
    input("\nPress ENTER to close the program.\n")
    exit()
print(f"\nThe Homebase name for {displayName} has been succesfully changed from {reqGetHomebaseNameText['profileChanges'][0]['profile']['stats']['attributes']['homebase_name']} to {reqSetHomebaseNameText['profileChanges'][0]['profile']['stats']['attributes']['homebase_name']}.")
input("\nPress ENTER to close the program.\n")
exit()