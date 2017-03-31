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

class MainHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        email = self.request.get("email")

        usererror = self.request.get("usererror")
        if usererror:
            error_esc = cgi.escape(usererror, quote=True)
            error_element = '<b class = "error">' + error_esc + '</b>'
        else:
            error_element = ''

        user_form = """
        <form action="/welcome" method="post">
          <label>Username: </label>
          <input type="text" name="username" value="{0}"/>
        """.format(username) + error_element + "<br>"

        pass_form = """
          <label>Password: </label>
          <input type="text" name="password" /><br>
          <label>Confirm Password: </label>
          <input type="text" name="verify" /><br>
        """
        email_form = """
          <label>E-mail Address: </label>
          <input type="text" name="email" value="{0}" /><br>
          <input type="submit" value="Submit Form"/>
        """.format(email)




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
            self.redirect("/?usererror=" + usererror)
        elif valid_username(username):
            self.response.write("Welcome, " + username + "!")
        else:
            usererror = "{0} is not a valid Username".format(username)
            self.redirect("/?usererror=" + usererror)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', Welcome)
], debug=True)
