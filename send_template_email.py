
import email, smtplib, ssl, csv

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import getpass

subject = "Bioinformatics Career Fair - Uppsala University"
sender_email = "msc.bioinformatics.uu@gmail.com"
password =  getpass.getpass()

body = """To whom it may concern,

We are the Career Fair team for the Bioinformatics program at Uppsala University.

We are happy to invite you to a career-event with soon to be graduates from the Uppsala University masters program in Bioinformatics. The purpose of the day is to connect employers with graduates to further science-to-industry connections and to inform the students about non-academic opportunities in life- and data-science. We think {company} is doing interesting work in the field of Bioinformatics and that you would be a good fit for this fair.

This year’s cohort is largely international. You can expect an ambitious group skilled in data analysis and statistics, with a strong biological background. You can expect around 50 students at the event.

The event will take place at Uppsala University on April 23rd, in the afternoon. There will be a station with a table and chairs for you to organize as you wish. During the event, you will be offered complimentary coffee and fika.

Please confirm your attendance by the 13th of April by replying to this email.

If you have any questions about the arrangements, don’t hesitate to contact us.

We hope to see you at the event!

Best regards,
The MSc bioinformatics career team.

"""

context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    with open("contacts_file.csv", "r", encoding='utf-8') as contacts:
        reader = csv.reader(contacts)
        # next(reader)  # Skip header row
        for company, email in reader:
            form_body=body.format(company=company)

            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = email
            message["Subject"] = subject

            # Add body to email
            message.attach(MIMEText(form_body, "plain"))

            filename = "BioinformaticsCareerfair_poster.pdf"  # In same directory as script

            # Open PDF file in binary mode
            with open(filename, "rb") as attachment:
                # Add file as application/octet-stream
                # Email client can usually download this automatically as attachment
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            # Encode file in ASCII characters to send by email
            encoders.encode_base64(part)

            # Add header as key/value pair to attachment part
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}",
            )

            # Add attachment to message and convert message to string
            message.attach(part)
            text = message.as_string()

            server.sendmail(
                sender_email,
                email,
                text,
            )
