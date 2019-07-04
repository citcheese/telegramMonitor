"""
Quick functions to alert on errors with script

change login creds to your own and change to/from email addresses
"""

def Py2send_email(SUBJECT, TEXT, HTML):
    import smtplib, ssl
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    sender_email = ""  # Enter your address
    receiver_email = ""  # Enter receiver address
    msg = MIMEMultipart('alternative')
    msg['Subject'] = SUBJECT
    msg['From'] = sender_email
    msg['To'] = receiver_email
    # message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
    port = 465  # For SSL
    text = TEXT
    html = HTML
    # Create a secure SSL context
    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html.encode("utf8"), 'html')
    msg.attach(part1)
    msg.attach(part2)
    context = ssl.create_default_context()

    server=smtplib.SMTP_SSL("smtp.gmail.com", port)
    server.login("", "") #Emaillogin,password
    server.sendmail(sender_email, receiver_email, msg.as_string())


def Py3send_email(SUBJECT, TEXT, HTML):
    import smtplib, ssl
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    sender_email = ""  # Enter your address
    receiver_email = ""  # Enter receiver address
    msg = MIMEMultipart('alternative')
    msg['Subject'] = SUBJECT
    msg['From'] = sender_email
    msg['To'] = receiver_email
    # message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
    port = 465  # For SSL
    text = TEXT
    html = HTML
    # Create a secure SSL context
    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("", "")
        server.sendmail(sender_email, receiver_email, msg.as_string())
