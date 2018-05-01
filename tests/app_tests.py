from nose.tools import *
from app import app
import planisphere

app.config['TESTING'] = True
web = app.test_client()

# Test a game where the player enters all right answers
def test_winning():
    rv = web.get('/', follow_redirects=True)
    assert_equal(rv.status_code, 200)
    assert_in(b"The Gothons of Planet Percal", rv.data)

    # Pretend we've loaded the main page. 
    # Question: is the session still alive? 
    data = {'action': 'tell a joke'}
    rv = web.post('/game', follow_redirects=True, data=data)
    assert_in(b"Laser", rv.data)

    # Now we are in Laser Weapon Armory
    data = {'action': '1234'}
    rv = web.post('/game', follow_redirects=True, data=data)
    assert_in(b"Bridge", rv.data)

    # Now we are on the Bridge. 
    data = {'action': 'slowly place the bomb'}
    rv = web.post('/game', follow_redirects=True, data=data)
    assert_in(b"Escape Pod", rv.data)

    # Now we are in the Escape Pod
    data = {'action': '2'}
    rv = web.post('/game', follow_redirects=True, data=data)
    # We should have won now.
    assert_in(b"The End", rv.data)

# Test a game where the player enters a wrong answer right away
def test_losing():
    rv = web.get('/', follow_redirects=True)
    assert_equal(rv.status_code, 200)
    assert_in(b"The Gothons of Planet Percal", rv.data)

    # We are in the Central Corridor
    data = {'action': 'shoot!'}
    rv = web.post('/game', follow_redirects=True, data=data)
    assert_in(b"Death", rv.data)


# Test a game where the player enters a choice that does't exist
def test_nonexistent_response():
    rv = web.get('/', follow_redirects=True)
    assert_equal(rv.status_code, 200)
    assert_in(b"The Gothons of Planet Percal", rv.data)

    # We are in the Central Corridor
    data = {'action': 'shoot'}
    rv = web.post('/game', follow_redirects=True, data=data)
    assert_in(b"Central Corridor", rv.data) # We should still be in the Central Corridor

#Test a game where the player clicks submit without entering anything
