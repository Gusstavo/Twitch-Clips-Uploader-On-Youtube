# TWITCH CLIPS UPLOADER ON YOUTUBE

Used to download clips from twitch channels and upload those clips to your youtube account.


## Installation

Requires [Python 3](https://www.python.org/) to run.

Install the dependencies:
```txt
requests==2.22.0
oauth2client==4.1.3
google-api-python-client==2.8.0
google-auth-httplib2==0.1.0
google-auth-oauthlib==0.4.4
```

Fill in the credentials files (twitch.json, youtube.json) on credentials folder to be able to run, this way:
+ twitch.json:
```json
{
    "CLIENT_ID": "YOUT CLIENT ID HERE",
    "CLIENT_SECRET": "YOUT CLIENT SECRET HERE",
    "GRANT_TYPE": "client_credentials"
}
````

+ youtube.json:
```json
{
    "installed":{
       "client_id":"YOUR CLIENT ID HERE",
       "project_id":"YOUR PROJECT ID ON GCP HERE",
       "auth_uri":"https://accounts.google.com/o/oauth2/auth",
       "token_uri":"https://oauth2.googleapis.com/token",
       "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
       "client_secret":"YOUR CLIENT SECRET HERE",
       "redirect_uris":[
          "urn:ietf:wg:oauth:2.0:oob",
          "http://localhost"
       ]
    }
}
````

## Run

To run just follow the model:

```sh
python3 uploaderclips.py --channel <twitch_channel_name> --limit <number_of_clips_to_search>
```