from flask import Flask, redirect, url_for
from omxplayer.player import OMXPlayer

radio_title = 'SWR1'
radio_url = 'https://swr-swr1-bw.cast.addradio.de/swr/swr1/bw/aac/96/stream.aac'

player = OMXPlayer(radio_url, args=['-o', 'both'])
app = Flask(__name__)

@app.route('/')
def overview():
    return f'Currently playing {radio_title} at volume {player.volume()}'


@app.route('/+')
def volume_plus():
    player.set_volume(player.volume() + 0.1)
    return redirect(url_for('overview'))


@app.route('/-')
def volume_minus():
    player.set_volume(player.volume() - 0.1)
    return redirect(url_for('overview'))
