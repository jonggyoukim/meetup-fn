import io
import json
import logging
import smtplib
import email.utils
#python script for sending SMTP configuration with Oracle Cloud Infrastructure Email Delivery
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fdk import response


def handler(ctx, data: io.BytesIO = None):

# {
#   "imageName" : "Bob",
#   "imageSize" : "Bob",
#   "recipient" : "shiftyou@gmail.com",
# }


    IMAGE_NAME = "World"
    IMAGE_SIZE = "3x3"
    RECIPIENT = "jonggyou.kim@gmail.com"

    eee=""
    try:

        body = json.loads(data.getvalue())
        IMAGE_NAME = body.get("imageName")
        IMAGE_SIZE = body.get("imageSize")
        RECIPIENT = body.get("recipient")

        #------------------------------------------------------
        # Replace sender@example.com with your "From" address. This address must be verified.
        SENDER = 'functions@oracle-meetup.com'
        SENDERNAME = 'Oracle Korea Meetup'

        # Replace recipient@example.com with a "To" address. If your account is still in the sandbox, this address must be verified.
        #RECIPIENT  = 'changkeun.lee@oracle.com'
        #RECIPIENT = input("Email address:")

        # Replace the USERNAME_SMTP value with your Email Delivery SMTP username.
        # USERNAME_SMTP = 'ocid1.user.oc1..aaaaaaaavxvstubaurwcrxoriyfergdbeivbyncrjvgbouc2d735ulvlrhma@ocid1.tenancy.oc1..aaaaaaaazgoxwfw73lx33swagxcxnvzgthxepwplymt5cltauw7e5j7rcmla.6e.com'
        USERNAME_SMTP = 'ocid1.user.oc1..aaaaaaaavw35s62muv3e343ukhtsgiwxxkqh3kfdqzm7he5lx3fb5ofrvl6q@ocid1.tenancy.oc1..aaaaaaaazgoxwfw73lx33swagxcxnvzgthxepwplymt5cltauw7e5j7rcmla.1k.com'

        # Replace the PASSWORD_SMTP value with your Email Delivery SMTP password.
        # PASSWORD_SMTP = 'hHd8_WPtkKHuYW0L2o;$'
        PASSWORD_SMTP = '#r5da)$_P75+(PDvaBvC'

        # If you're using Email Delivery in a different region, replace the HOST value with an SMTP endpoint. Use port 25 or 587 to connect to the SMTP endpoint.
        HOST = "smtp.email.us-ashburn-1.oci.oraclecloud.com"
        PORT = 587


        # The subject line of the email.
        SUBJECT = 'Your contract is ready to review and sign'
        # ECONTRACT_SELLER_NAME = "Seller1"
        # ECONTRACT_SELLER_EMAIL = "seller1@eot.com"
        # ECONTRACT_URL = "https://econtract-apackrsct01.builder.ocp.oraclecloud.com/ic/builder/rt/econtract/1.0/webApps/econtractweb/?uuid=690ef1f4-c419-471a-b6b7-dfab2751735d"

        # The email body for recipients with non-HTML email clients.
        BODY_TEXT = ("Email Delivery Test\r\n"
                    "This email was sent through the Email Delivery SMTP "
                    "Interface using the Python smtplib package."
                    )
        code = "We Say Thanks!"
        # The HTML body of the email.

        templateHtmlFile = open('template.html', 'r')
        templateHtml = templateHtmlFile.read()
        templateHtmlFile.close()
        BODY_HTML = templateHtml.format(**locals())

        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = SUBJECT
        msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
        msg['To'] = RECIPIENT


        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(BODY_TEXT, 'plain')
        part2 = MIMEText(BODY_HTML, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)

        # Try to send the message.
        server = smtplib.SMTP(HOST, PORT)
        server.ehlo()
        server.starttls()
        #smtplib docs recommend calling ehlo() before & after starttls()
        server.ehlo()
        server.login(USERNAME_SMTP, PASSWORD_SMTP)
        server.sendmail(SENDER, RECIPIENT, msg.as_string())
        server.close()
        #---------------------------------------------------------


    except (Exception, ValueError) as ex:
        logging.getLogger().info('error parsing json payload: ' + str(ex))
        print('error parsing json payload: ' + str(ex))
        eee = str(ex)



    logging.getLogger().info("Inside Python Hello World function")
    print("Inside Python Hello World function")
    return response.Response(
        ctx, response_data=json.dumps(
          {
            "IMAGE_NAME": "Hello {0}".format(IMAGE_NAME),
            "recipient": "Hello {0}".format(RECIPIENT),
            "IMAGE_SIZE": "Hello {0}".format(IMAGE_SIZE),
            "exception": "Hello {0}".format(eee)
          }),
        headers={"Content-Type": "application/json"}
        )
