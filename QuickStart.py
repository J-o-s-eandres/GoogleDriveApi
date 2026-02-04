from pydrive2.auth import GoogleAuth

# Initialize GoogleAuth with the settings file (no LoadSettingsFile method exists)
gauth = GoogleAuth(settings_file='settings.yaml')
# Run the local webserver auth flow
gauth.LocalWebserverAuth()
# Force-save credentials to `credentials_module.json` if obtained
if getattr(gauth, 'credentials', None):
    gauth.SaveCredentialsFile('credentials_module.json')
    print('Credentials saved to credentials_module.json')
else:
    print('No credentials obtained; check auth flow and settings.yml')

