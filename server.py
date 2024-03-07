import os


import csv
import json
import smtplib
from email.message import EmailMessage

from flask import Flask, render_template, request, redirect
from twilio.rest import Client

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/works')
def works():
    with open("data/works.json") as works_file:
        works_list = json.load(works_file)
    return render_template('works.html', nested_works=enumerate(works_list))


@app.route('/works/<work_id>')
def work(work_id):
    file_path = os.path.join("data", "works", f"{work_id}.json")
    try:
        with open(file_path) as each_work_file:
            each_work = json.load(each_work_file)
        return render_template("work.html", work=each_work)
    except FileNotFoundError:
        return "Not Found", 404


# @app.route('/<string:page_name>')
# def html_page(page_name):
#     try:
#         return render_template(f'{page_name}.html')
#     except jinja2.exceptions.TemplateNotFound:
#         return "Template unavailable", 404


def write_to_file(data):
    with open('database.txt', mode='a') as database:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        file = database.write(f'\n{email},{subject},{message}')


def write_to_csv(data):
    with open('database.csv', mode='a') as database2:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        csv_writer = csv.writer(database2, delimiter=',', quotechar='|',
                                quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email, subject, message])


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == "POST":
        try:
            data = request.form.to_dict()
            write_to_csv(data)
            print(data)
            # code for sending sms

            account_sid = 'AC0e3bf30ec96263e8c9294c11569b5f63'
            auth_token = 'ae397ce8e9bec28fda899321be13cada'
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                messaging_service_sid='MG5d0e2bff038bc439e0c15a3f044ff380',
                body=data['email'] + " " + "contacted you with message " + data['message'],
                to='+918707689516'
            )

            print(message.sid)

            # code for sending sms
            # code for sending mail
            print('hereat61')
            email = EmailMessage()
            email['from'] = 'aakanksha1singh@outlook.com'
            email['to'] = data['email']
            email['subject'] = 'Connect with Aakanksha'

            email.set_content('Thankyou for connecting , i will reply to your message shortly')
            print('hereat61')
            with smtplib.SMTP(host='smtp.office365.com', port=587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.login('##Email_id_from_which_email_will_be_sent##', '##Email_password_from_which_email_will_be_sent##')
                smtp.send_message(email)
                print('Email is send successfully')

            # code for sending mail
            return redirect('/thankyou.html')
        except Exception as ex:
            print(ex)
            return 'did not save to database'
    else:
        return 'Sorry some error occurred, please try again!'


if __name__ == '__main__':
    app.run(debug=True)
