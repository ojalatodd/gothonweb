from flask import Flask, session, redirect, url_for, escape, request
from flask import render_template
import planisphere

app = Flask(__name__)

@app.route("/")
def index():
    # this is used to "setup" the session with starting values
    session['room_name'] = planisphere.START
    session['help'] = False
    return redirect(url_for("game"))

@app.route("/game", methods=['GET', 'POST'])
def game():
    room_name = session.get('room_name')

    if request.method == "GET":
        if room_name:
            room = planisphere.load_room(room_name)
            help = session['help']
            session['help'] = False
            return render_template("show_room.html", room=room, help=help)
        else:
            # why is this here? do you need it?
            return render_template("you_died.html")
    else:
        action = request.form.get('action')
        next_room = None

        if room_name and action:
            room = planisphere.load_room(room_name)
            if action == 'help':          
                 session['help'] = True
            else:
                next_room = room.go(action)

            if not next_room:
                session['room_name'] = planisphere.name_room(room)
                #return room_name
            else:
                session['room_name'] = planisphere.name_room(next_room)

            return redirect(url_for("game"))
        else: 
            return redirect(url_for("game"))



# YOU SHOULD CHANGE THIS IF YOU PUT IT ON THE INTERNET
app.secret_key = 'A0Zr98j/3yX R-XHH!jmN]LWX/,?RT'

if __name__ == "__main__":
    app.run()
