version = "1.2.0"
print(f"Homebase Name Changer v{version} by PRO100KatYT\n")

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

# Start a new requests session.
session = requests.Session()

# Error with a custom message.
def customError(text):
    input(f"ERROR: {text}\n\nPress ENTER to close the program.\n")
    exit()

# Input loop until it's one of the correct values.
def validInput(text, values):
    response = input(f"{text}\n")
    print()
    while True:
        if response in values: break
        response = input("You priovided a wrong value. Please input it again.\n")
        print()
    return response

# Get the text from a request and check for errors.
def requestText(request):
    requestText = json.loads(request.text)
    if "errorMessage" in requestText:
        if "Validation Failed. Invalid fields were [homebaseName]" in requestText['errorMessage']: customError("The Homebase name can't be blank.")
        else: customError(requestText['errorMessage'])
    return requestText

# Get the token and use it to login into an account.
isLoggedIn = validInput("Are you logged into your Epic account that you would like the program to use in your browser?\nType 1 if yes and press ENTER.\nType 2 if no and press ENTER.\n", ["1", "2"])
input("The program is going to open an Epic Games webpage.\nTo continue, press ENTER.\n")
if isLoggedIn == "1": loginLink = links.loginLink1
else: loginLink = links.loginLink2
webbrowser.open_new_tab(loginLink)
print(f"If the program didnt open it, copy this link to your browser: {loginLink}\n")
reqToken = requestText(session.post(links.getToken, headers={"Authorization": "basic ZWM2ODRiOGM2ODdmNDc5ZmFkZWEzY2IyYWQ4M2Y1YzY6ZTFmMzFjMjExZjI4NDEzMTg2MjYyZDM3YTEzZmM4NGQ=", "Content-Type": "application/x-www-form-urlencoded"}, data={"grant_type": "authorization_code", "token_type": "eg1", "code": input("Insert the auth code:\n")}))
access_token, account_id, displayName = reqToken["access_token"], reqToken["account_id"], reqToken["displayName"]
print(f"\nLogged in as {displayName}.")

# Change the Homebase name.
homebaseHeaders = {"Authorization": f"bearer {access_token}", "Content-Type": "application/json"}
reqGetHomebaseName = requestText(session.post(links.profileRequest.format(account_id, "QueryProfile"), headers=homebaseHeaders, data="{}"))
reqSetHomebaseName = requestText(session.post(links.profileRequest.format(account_id, "SetHomebaseName"), headers=homebaseHeaders, json={"homebaseName": input("\nEnter a new Homebase name:\n")}))
oldHomebaseName, newHomebaseName = [reqGetHomebaseName['profileChanges'][0]['profile']['stats']['attributes']['homebase_name'], reqSetHomebaseName['profileChanges'][0]['profile']['stats']['attributes']['homebase_name']]
input(f"\nThe Homebase name for {displayName} has been succesfully changed from {oldHomebaseName} to {newHomebaseName}.\n\nPress ENTER to close the program.\n")
exit()