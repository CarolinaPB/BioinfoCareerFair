import csv, smtplib, ssl
import getpass

message = """Subject: Bioinformatics Career Fair - Uppsala University

To whom it may concern,

We are the Career Fair team for the Bioinformatics program at Uppsala University.

We are happy to invite you to a career-event with soon to be graduates from the Uppsala University masters program in Bioinformatics. The purpose of the day is to connect employers with graduates to further science-to-industry connections and to inform the students about non-academic opportunities in life- and data-science. We think {company} is doing interesting work in the field of Bioinformatics and that you would be a good fit for this fair.

This year’s cohort is largely international. You can expect an ambitious group skilled in data analysis and statistics, with a strong biological background. You can expect around 50 students at the event.

The event will take place at Uppsala University on April 23rd, in the afternoon. There will be a station with a table and chairs for you to organize as you wish. During the event, you will be offered complimentary coffee and fika.

Please confirm your attendance by the 13th of April by replying to this email.

If you have any questions about the arrangements, don’t hesitate to contact us.

We hope to see you at the event!

Best regards,
The MSc bioinformatics career team."""

message =message.replace(u"\u2019", "'")

from_address = "msc.bioinformatics.uu@gmail.com"
password = getpass.getpass()

context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(from_address, password)
    with open("contacts_file.csv", "r", encoding='utf-8') as contacts:
        reader = csv.reader(contacts)
        # next(reader)  # Skip header row
        for company, email in reader:
            server.sendmail(
                from_address,
                email,
                message.format(company=company),
            )
