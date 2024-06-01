Guarddog

The intent of this program is to watch log files for strange activity and send notifcations and kill the guarded process if something unwanted appears in a log.

Required libraries:

psutil, schedule

Setup instructions:

Enter things you want to match against in prohibited_words.txt

A Gmail app password is required, set this up:

Enable "Less secure app access" or Generate an App Password:

Less Secure App Access: Go to your Google Account settings. Navigate to "Security," scroll down to "Less secure app access," and turn it on.
App Password (recommended if you have 2-factor authentication enabled):
Go to your Google Account settings.
Navigate to the "Security" section and ensure 2-factor authentication is enabled.
In the "Signing in to Google" section, select "App passwords."
Follow the prompts to generate an app password for "Mail."

Create environment variable 
Open System Properties:

Press Win + R, type sysdm.cpl, and press Enter.
Go to the "Advanced" tab and click on "Environment Variables".

In the Environment Variables window, under the "User variables" section, click "New".

Set the variable name and value:

Variable name: EMAIL_PASSWORD
Variable value: your-app-password
Click "OK" to close the dialogs.