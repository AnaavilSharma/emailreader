from login_mailFetch_calendar_integrated import USER_FILE
from F_ReadAndSumm import *



user_info = retrieve_email_credentials(USER_FILE)

summarize_event(read_emails(user_info))
