#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re

header = """
<html>
  <head>
    <title>User Sign Up</title>
    <style type="text/css">
      .error {
            color: red;
      }
    </style>
  </head>
  <body>
"""
footer = """
</body>
</html>
"""


def valid_username(username):
    user_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return user_re.match(username)

def valid_password(password):
    password_re = re.compile(r"^.{3,20}$")
    return password_re.match(password)

def valid_email(email):
    email_re = re.compile(r"^[\S]+@[\S]+.[\S]+$")
    return email_re.match(email)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        email = self.request.get("email")

        usererror = self.request.get("usererror")
        usererror_element = ""
        if usererror:
            usererror_esc = cgi.escape(usererror, quote=True)
            usererror_element = '<b class = "error">' + usererror_esc + '</b>'
        else:
            error_element = ''

        passerror = self.request.get("passerror")
        passerror_element = ''
        if passerror:
            passerror_esc = cgi.escape(passerror, quote=True)
            passerror_element = '<b class="error">' + passerror_esc + '</b>'

        emailerror = self.request.get("emailerror")
        emailerror_element = ""
        if emailerror:
            emailerror_esc = cgi.escape(emailerror, quote=True)
            emailerror_element = '<b class="error">' + emailerror_esc + '</b>'


        user_form = """
        <form action="/welcome" method="post">
          <label>Username: </label>
          <input type="text" name="username" value="{0}"/>
        """.format(username) + usererror_element + "<br>"

        pass_form = """
          <label>Password: </label>
          <input type="password" name="password" />{0}<br>
          <label>Confirm Password: </label>
          <input type="password" name="verify" /><br>
        """.format(passerror_element)
        email_form = """
          <label>E-mail Address: </label>
          <input type="text" name="email" value="{0}" />{1}<br>
          <input type="submit" value="Submit Form"/>
        """.format(email, emailerror_element)




        form = user_form + pass_form + email_form

        self.response.write(header + form + footer)

class Welcome(webapp2.RequestHandler):
    def post(self):


        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        if username == "": #checks for username input
            usererror = "Please enter a Username"
            self.redirect("/?usererror=" + usererror + "&email=" + email)
        elif valid_username(username): #checks validity of username
            self.response.write("Welcome, " + username + "!")
        else:
            usererror = "{0} is not a valid Username".format(username)
            self.redirect("/?usererror=" + usererror + "&username=" + username + "&email=" + email)

        if password == "": #checks for password
            passerror = "Please enter a password"
            self.redirect("/?passerror=" + passerror + "&username=" + username + "&email=" + email)
        elif valid_password(password):
            if password == verify:
                self.response.write("")
            else:
                passerror = "Passwords do not match"
                self.redirect("/?passerror=" + passerror + "&username=" + username + "&email=" + email)
        else:
            passerror = "Password is not valid"
            self.redirect("/?passerror=" + passerror + "&username=" + username + "&email=" + email)

        if email == "":
            emailerror = "Please enter an email"
            self.redirect("/?emailerror=" + emailerror + "&username=" + username + "&email=" + email)
        elif valid_email(email):
            self.response.write("")
        else:
            emailerror = "{0} is not a valid E-mail".format(email)
            self.redirect("/?emailerror=" + emailerror + "&username=" + username + "&email=" + email)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', Welcome)
], debug=True)
