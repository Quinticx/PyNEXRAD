from flask import Flask, send_file
import radar
app = Flask('app')


@app.route('/')
def index():
	try:
		samples = radar.download("klsx")
		plot = radar.plot(samples[0])

		return send_file(plot, mimetype='image/png')
	except:
		return "Sorry, an error occured. Please try again later. :("


@app.route('/<site>')
def site(site):
	try:
		print(site)
		samples = radar.download(site)
		plot = radar.plot(samples[0])

		return send_file(plot, mimetype='image/png')
	except:
		return "Sorry, an error occured. Please try again later. :("


app.run(host='0.0.0.0', port=8080)
