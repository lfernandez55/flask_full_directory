# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>

from __future__ import print_function  # Use print() instead of print
from flask import url_for


def test_page_urls0(client):
    # Visit home page
    response = client.get(url_for('books.home_page'), follow_redirects=True)
    assert response.status_code==200
    # Try to visit categories page while not logged in
    response = client.get(url_for('books.categories'), follow_redirects=True)
    assert b"Sign in" in response.data, "Prob with auth; not requiring sign in'"


def test_page_urls1(client):
    # Login as user and visit Categories page
    response = client.post(url_for('user.login'), follow_redirects=True,
                           data=dict(email='member@example.com', password='Password1'))
    assert response.status_code==200
    response = client.get(url_for('books.categories'), follow_redirects=True)
    assert b"Categories Page" in response.data, "Prob with auth; not allowing access to Categories page after sign in'"

    #While logged in try to access admin page you don't have privileges to access
    response = client.get(url_for('books.admin_books'), follow_redirects=True)
    assert b"You do not have permission to access" in response.data, "Prob with auth; not requiring admin privileges'"


def test_page_urls2(client):
    # # Logout
    response = client.get(url_for('user.logout'), follow_redirects=True)
    assert response.status_code==200
    #

def test_page_urls3(client):
    # # Login as admin and visit Admin page
    response = client.post(url_for('user.login'), follow_redirects=True,
                           data=dict(email='admin@example.com', password='Password1'))
    assert response.status_code==200
    response = client.get(url_for('books.admin_books'), follow_redirects=True)
    assert response.status_code==200
    assert b"SQL" in response.data, "Prob with auth; not allowing access to admin page after login as admin'"
    #
    # # Logout
    response = client.get(url_for('user.logout'), follow_redirects=True)
    assert response.status_code==200
