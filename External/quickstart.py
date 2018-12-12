from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('/home/spicebot/token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('/home/spicebot/credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


if __name__ == '__main__':
    main()


"""
    if not os.path.exists("/home/spicebot/quickstart.py"):
        stderr("Auth Program Missing, Copying")
        os.system("sudo cp " + str(bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)]["directory_main"]) + "External/quickstart.py /home/spicebot/quickstart.py")
        os.system("sudo chown -R " + str(os_dict["user"]) + ":sudo /home/spicebot/quickstart.py")

    if not os.path.exists("/home/spicebot/credentials.json"):
        stderr("Credentials File Missing, Copying")
        try:
            CLIENTID = bot.memory["botdict"]["tempvals"]['ext_conf']["google"]["clientid"]
            SECRET = bot.memory["botdict"]["tempvals"]['ext_conf']["google"]["clientsecret"]
        except Exception as e:
            bot.memory["botdict"]["tempvals"]['google'] = None
            stderr("Error loading google calendar auth")
            bot_startup_requirements_set(bot, "auth_google")
            return

        f = open("/home/spicebot/credentials.json", "w+")
        textwrite = str('{"installed":{"client_id":"' + CLIENTID + '","project_id":"spicebot-1536234792000","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://www.googleapis.com/oauth2/v3/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"' + SECRET + '","redirect_uris":["urn:ietf:wg:oauth:2.0:oob","http://localhost"]}}')
        f.write(textwrite)
        f.close()

    # sayline = True
    # for line in os.popen(str("sudo python /home/spicebot/quickstart.py --noauth_local_webserver")):
    #    if line.startswith("Traceback"):
    #        sayline = False
    #    if sayline:
    #        stderr(line)

    try:
        os.system("sudo chown -R " + str(os_dict["user"]) + ":sudo /home/spicebot/token.json")
    except Exception as e:
        stderr("Error loading permissions on auth file")
"""
