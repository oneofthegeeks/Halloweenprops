Follow this video from Network Chuck.

https://www.youtube.com/watch?v=B_krqlk_cXo

He also followed these intructions to get rasbien with all the bells and whistles and get the web server running.

https://towardsdatascience.com/python-webserver-with-flask-and-raspberry-pi-398423cc6f5d

this is a branch with my changes




Python WebServer With Flask and Raspberry Pi
Marcelo Rovai
Towards Data Science
Marcelo Rovai


Let’s create a simple WebServer to control things in your home. There are a lot of ways to do that. For example, on my tutorial: IoT — Controlling a Raspberry Pi Robot Over Internet With HTML and Shell Scripts Only, we have explored how to control a robot over the local network using the LIGHTTPD WebServer. For this project here, we will use FLASK, a very simple and free microframework for Python. With Flask, will be very simple to control Raspberry GPIOs over the internet.

After you read this tutorial, please give a visit to its continuation: From Data to Graph: a Web Jorney With Flask and SQLite

1. Introduction
Flask is called a micro framework because it does not require particular tools or libraries. It has no database abstraction layer, form validation, or any other components where pre-existing third-party libraries provide common functions. However, Flask supports extensions that can add application features as if they were implemented in Flask itself.

On this tutorial, we will use a Raspberry Pi as a local Web Server, where we will control via a simple webpage, 3 of its GPIOs programmed as outputs (acting as actuators) and monitor 2 of its GPIOs, programmed as inputs (sensors).


The above block diagram shows what we want to accomplish

and the video below can give a hint about it:


Note that what you will learn here in terms of Python WebServer using Flask can be applied directly to any Linux/OS machine and with some adaptations to Windows PCs (unfortunately, not my area of expertise).

2. Installing FLASK and Setting Your RPi WebServer

Flask Installation
The first thing to do is to install Flask on your Raspberry Pi. Go to Terminal and enter:

sudo apt-get install python3-flask
The best when you start a new project is to create a folder where to have your files organized. For example:

mkdir rpiWebServer
The above command will create a folder named “Server”. There we will save our python files (application):

/home/pi/Documents/Server
On this folder, let’s create 2 other sub-folders: static for CSS and eventually JavaScript files and templates for HTML files (or more precisely, Jinja2 templates. But do not worry about that). Go to your newer created folder:

cd rpiWebServer
And create the 2 new sub-folders:

mkdir static
and

mkdir templates
The final folder “tree”, will look like:

/rpiWebServer
    /static
    /templates
The Python WebServer Application
Now, let’s create our first python WebServer with Flask:

Open your Python3 IDE, Thonny or Geany.
Copy the “Hello Word” code below on your IDE and save it for example, as helloWorld.py
from flask import Flask
app = Flask(__name__)
@app.route('/')
def index():
    return 'Hello world'
if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
What the above code does is:

1. Load the Flask module into your Python script:

from flask import Flask
2. Create a Flask object called app:

app = Flask(__name__)
3. Run the index() function when someone accesses the root URL (‘/’) of the server. In this case, only send the text “Hello World!” to the client’s web browser thru “return”

def index():
   return "Hello Word"
4. Once this script is running from the command line at the terminal, the server starts to “listen” on port 80, reporting any errors:

if __name__ == '__main__':
   app.run(debug=True, port=80, host='0.0.0.0')
Raspberry PI IP Address:
If you are not sure about your RPi IP address, run on your terminal:

ifconfig
At wlan0: section you will find it. In my case:

10.0.1.27
Running the Application
Now, run the above application program:

sudo python3 helloWorld.py
On the first picture above you can see what will appear on your terminal. The application will be running unless you type [CTRL] + [C].


Now you must open any web browser that is connected to same wifi network as your Raspberry and type its IP address as shown in the second picture above. The “Hello World” should appear in your browser as shown in the picture above.


Note that there are 2 lines at bottom of the above picture. The lines show that the two different web browsers requested the root URL and our server returned HTTP status code 200 for “OK”. I entered with our RPi Server address on both, the RPI itself (10.1.0.27) and on my Mac (10.1.0.10). For each new request, a new line will appear on the terminal as far the application is running.

3. Creating a Proper Server Web Page

Let’s sophisticated our “Hello World” application, creating an HTML template and a CSS file for styling our page. This is, in fact, important, otherwise, you would complicate the Python Script putting all on it.

Templates

Creating an HTML file that will be located in the “template” sub-folder, we can use separate files with placeholders for spots where you want dynamic data to be inserted.

So, we will create a file named index.html, that will be saved on /templates. You can use any Text editor to create your HTML file. Can be Geany, “nano” at Terminal or the RPi Text Editor (LeafPad) that is located under “Accessories” Main Menu.

GEANY can be used to work with all project files at same time (.py; .html and .css) it’s a good option with bigger and more complex projects

OK, let’s create /templates/index.html:

<!DOCTYPE html>
   <head>
      <title>{{ title }}</title>
   </head>
   <body>
      <h1>Hello, World!</h1>
      <h2>The date and time on the server is: {{ time }}</h2>
   </body>
</html>
Observe that anything in double curly braces within the HTML template is interpreted as a variable that would be passed to it from the Python script via the render_template function.

Now, let’s create a new Python script. We will name it helloWorldTemplate.py:

'''
Code created by Matt Richardson 
for details, visit:  http://mattrichardson.com/Raspberry-Pi-Flask/inde...
'''
from flask import Flask, render_template
import datetime
app = Flask(__name__)
@app.route("/")
def hello():
   now = datetime.datetime.now()
   timeString = now.strftime("%Y-%m-%d %H:%M")
   templateData = {
      'title' : 'HELLO!',
      'time': timeString
      }
   return render_template('index.html', **templateData)
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
Note that we create a formatted string("timeString") using the date and time from the "now" object, that has the current time stored on it.

Next important thing on the above code, is that we created a dictionary of variables (a set of keys, such as the title that is associated with values, such as HELLO!) to pass into the template. On “return”, we will return the index.htmltemplate to the web browser using the variables in the templateData dictionary.

Execute the Python script:

sudo python3 helloWorldTemplate.py
Open any web browser and enter with your RPi IP address. The above picture shows the result.

Note that the page’s content changes dinamicly any time that you refresh it with the actual variable data passed by Python script. In our case, “title” is a fixed value, but “time” change it every second.

Now let’s include some styling on our page, creating a CSS file and stored it on /static/style.css:

body {
   background: blue;
   color: yellow;
}
You must also modify the index.html file to inform it to look for the style.css file. You do this inserting the “link” at “head”:

<!DOCTYPE html>
   <head>
      <title>{{ title }}</title>
      <link rel="stylesheet" href="../static/style.css/">
   </head>
   <body>
      <h1>Hello, World!</h1>
      <h2>The date and time on the server is: {{ time }}</h2>
   </body>
</html>
Remember that index.html is “under” /template and style.css is “under” /static, so, note that you must tell the HTML to go “up” and “down” again to look for the static subfolder: ../static/style.css.

The picture below shows the webpage with the new style!


For a more detailed Flask overview with Raspberry Pi, visit the Raspberry Pi Organization project : python-web-server-with-flask.

4. The Hardware

The hardware is very simple. Only follow the above electrical connections.

5. Reading GPIO Status
Let’s now read the status of our “sensors”, by monitoring their GPIOs.

The Python script
Let’s create a new Python script and named it app.py:

'''
	Raspberry Pi GPIO Status and Control
'''
import RPi.GPIO as GPIO
from flask import Flask, render_template
app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
button = 20
senPIR = 16
buttonSts = GPIO.LOW
senPIRSts = GPIO.LOW
   
# Set button and PIR sensor pins as an input
GPIO.setup(button, GPIO.IN)   
GPIO.setup(senPIR, GPIO.IN)
	
@app.route("/")
def index():
	# Read Sensors Status
	buttonSts = GPIO.input(button)
	senPIRSts = GPIO.input(senPIR)
	templateData = {
      'title' : 'GPIO input Status!',
      'button'  : buttonSts,
      'senPIR'  : senPIRSts
      }
	return render_template('index.html', **templateData)
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
Look that what we are doing is only defining GIPOs 20 and 16 as input, reading its values and storing them on 2 variables: buttonSts and senPIRSts. inside the function index(), we will pass those values to our web page thru “button” ad “senPIR” variables that are part of our variable dictionary: templateData.

Once you create app.py, run it on your terminal:

python3 app.py
The template
Let’s also create a new index.html to show the GPIO status of both sensors:

<!DOCTYPE html>
   <head>
      <title>{{ title }}</title>
      <link rel="stylesheet" href='../static/style.css'/>
   </head>
   <body>
	  <h1>{{ title }}</h1>
      <h2>Button pressed:  {{ button }}</h1>
      <h2>Motion detected: {{ senPIR }}</h2>
   </body>
</html>
Do not forget to refresh the page to see the results.

Press the button or make a movement in front of PIR sensor and refresh the page.

The picture shows the webpage.


6. Controlling GPIOs
Now that we know how to “read” GPIO Status, let’s change them. What we will do will “command” via webpage the “actuators”. We have 3 LEDs connected to Raspberry GPIOs. Commanding them remotely we will change their status from LOW to HIGH and vice-versa. Instead of LEDs, we could have relays controlling your room lamp and/or fan for example.

The python script
Let’s create a new Python script and named it app.py:

'''
	Raspberry Pi GPIO Status and Control
'''
import RPi.GPIO as GPIO
from flask import Flask, render_template, request
app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#define actuators GPIOs
ledRed = 13
ledYlw = 19
ledGrn = 26
#initialize GPIO status variables
ledRedSts = 0
ledYlwSts = 0
ledGrnSts = 0
# Define led pins as output
GPIO.setup(ledRed, GPIO.OUT)   
GPIO.setup(ledYlw, GPIO.OUT) 
GPIO.setup(ledGrn, GPIO.OUT) 
# turn leds OFF 
GPIO.output(ledRed, GPIO.LOW)
GPIO.output(ledYlw, GPIO.LOW)
GPIO.output(ledGrn, GPIO.LOW)
	
@app.route("/")
def index():
	# Read Sensors Status
	ledRedSts = GPIO.input(ledRed)
	ledYlwSts = GPIO.input(ledYlw)
	ledGrnSts = GPIO.input(ledGrn)
	templateData = {
              'title' : 'GPIO output Status!',
              'ledRed'  : ledRedSts,
              'ledYlw'  : ledYlwSts,
              'ledGrn'  : ledGrnSts,
        }
	return render_template('index.html', **templateData)
	
@app.route("/<deviceName>/<action>")
def action(deviceName, action):
	if deviceName == 'ledRed':
		actuator = ledRed
	if deviceName == 'ledYlw':
		actuator = ledYlw
	if deviceName == 'ledGrn':
		actuator = ledGrn
   
	if action == "on":
		GPIO.output(actuator, GPIO.HIGH)
	if action == "off":
		GPIO.output(actuator, GPIO.LOW)
		     
	ledRedSts = GPIO.input(ledRed)
	ledYlwSts = GPIO.input(ledYlw)
	ledGrnSts = GPIO.input(ledGrn)
   
	templateData = {
              'ledRed'  : ledRedSts,
              'ledYlw'  : ledYlwSts,
              'ledGrn'  : ledGrnSts,
	}
	return render_template('index.html', **templateData)
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
What we have new on above code is the new “route”:

@app.route("/<deviceName>/<action>")
From the webpage, calls will be generated with the format:

http://10.0.1.27/ledRed/on
or

http://10.0.1.27/ledRed/off
For the above example, ledRed is the “deviceName” and on or off are examples of possible “action”.

Those routes will be identified and properly “worked”. The main steps are:

Convert the string “ledRED”, for example, on its equivalent GPIO pin. The integer variable ledRed is equivalent to GPIO13. We will store this value on variable “actuator”
For each actuator, we will analyze the “action”, or “command” and act properly. If “action = on” for example, we must use the command: GPIO.output(actuator, GPIO.HIGH)
Update the status of each actuator
Update the variable library
Return the data to index.html
The template
Let’s now create an index.html to show the GPIO status of each actuator and more important, create “buttons” to send the commands:

<!DOCTYPE html>
   <head>
      <title>GPIO Control</title>
      <link rel="stylesheet" href='../static/style.css'/>
   </head>
   <body>
		<h1>Actuators</h1>
		<h2> Status </h2>
		<h3> RED LED ==>  {{ ledRed  }}</h3>
		<h3> YLW LED ==>  {{ ledYlw  }}</h3>
		<h3> GRN LED ==>  {{ ledGrn  }}</h3>
		<br>
		<h2> Commands </h2>
		<h3> 
			RED LED Ctrl ==> 
			<a href="/ledRed/on" class="button">TURN ON</a>  
			<a href="/ledRed/off"class="button">TURN OFF</a>
		</h3>
		<h3> 
			YLW LED Ctrl ==> 
			<a href="/ledYlw/on" class="button">TURN ON</a>  
			<a href="/ledYlw/off"class="button">TURN OFF</a>
		</h3>
		<h3> 
			GRN LED Ctrl ==> 
			<a href="/ledGrn/on" class="button">TURN ON</a>  
			<a href="/ledGrn/off"class="button">TURN OFF</a>
		</h3>
		
   </body>
</html>
Only to give a better “fell”, I create a class “button”. You can only keep the normal link if you want.

Below the style.css file:

body {
	background: blue;
	color: yellow;
}
.button {
  font: bold 15px Arial;
  text-decoration: none;
  background-color: #EEEEEE;
  color: #333333;
  padding: 2px 6px 2px 6px;
  border-top: 1px solid #CCCCCC;
  border-right: 1px solid #333333;
  border-bottom: 1px solid #333333;
  border-left: 1px solid #CCCCCC;
}
The picture shows the website for controlling our actuators.


7. Integrating Sensors and Actuators

Now, we must put together the 2 parts that we developed before. The final Python script is shown below:

'''
	Raspberry Pi GPIO Status and Control
'''
import RPi.GPIO as GPIO
from flask import Flask, render_template, request
app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#define sensors GPIOs
button = 20
senPIR = 16
#define actuators GPIOs
ledRed = 13
ledYlw = 19
ledGrn = 26
#initialize GPIO status variables
buttonSts = 0
senPIRSts = 0
ledRedSts = 0
ledYlwSts = 0
ledGrnSts = 0
# Define button and PIR sensor pins as an input
GPIO.setup(button, GPIO.IN)   
GPIO.setup(senPIR, GPIO.IN)
# Define led pins as output
GPIO.setup(ledRed, GPIO.OUT)   
GPIO.setup(ledYlw, GPIO.OUT) 
GPIO.setup(ledGrn, GPIO.OUT) 
# turn leds OFF 
GPIO.output(ledRed, GPIO.LOW)
GPIO.output(ledYlw, GPIO.LOW)
GPIO.output(ledGrn, GPIO.LOW)
	
@app.route("/")
def index():
	# Read GPIO Status
	buttonSts = GPIO.input(button)
	senPIRSts = GPIO.input(senPIR)
	ledRedSts = GPIO.input(ledRed)
	ledYlwSts = GPIO.input(ledYlw)
	ledGrnSts = GPIO.input(ledGrn)
	templateData = {
      		'button'  : buttonSts,
      		'senPIR'  : senPIRSts,
      		'ledRed'  : ledRedSts,
      		'ledYlw'  : ledYlwSts,
      		'ledGrn'  : ledGrnSts,
      	}
	return render_template('index.html', **templateData)
	
@app.route("/<deviceName>/<action>")
def action(deviceName, action):
	if deviceName == 'ledRed':
		actuator = ledRed
	if deviceName == 'ledYlw':
		actuator = ledYlw
	if deviceName == 'ledGrn':
		actuator = ledGrn
   
	if action == "on":
		GPIO.output(actuator, GPIO.HIGH)
	if action == "off":
		GPIO.output(actuator, GPIO.LOW)
		     
	buttonSts = GPIO.input(button)
	senPIRSts = GPIO.input(senPIR)
	ledRedSts = GPIO.input(ledRed)
	ledYlwSts = GPIO.input(ledYlw)
	ledGrnSts = GPIO.input(ledGrn)
   
	templateData = {
	 	'button'  : buttonSts,
      		'senPIR'  : senPIRSts,
      		'ledRed'  : ledRedSts,
      		'ledYlw'  : ledYlwSts,
      		'ledGrn'  : ledGrnSts,
	}
	return render_template('index.html', **templateData)
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
And the final index.html:

<!DOCTYPE html>
   <head>
      <title>GPIO Control</title>
      <link rel="stylesheet" href='../static/master.css'/>
   </head>
   <body>
		<h1>RPi GPIO Control</h1>
		<h2> Sensor Status </h2>
		<h3> BUTTON ==>  {{ button  }}</h3>
		<h3> MOTION ==>  {{ senPIR  }}</h3>
		<br>
		
		<h2> Actuator Status </h2>
		<h3> RED LED ==>  {{ ledRed  }}</h3>
		<h3> YLW LED ==>  {{ ledYlw  }}</h3>
		<h3> GRN LED ==>  {{ ledGrn  }}</h3>
		<br>
		<h2> Commands </h2>
		<h3> 
			RED LED Ctrl ==> 
			<a href="/ledRed/on" class="button">TURN ON</a>  
			<a href="/ledRed/off"class="button">TURN OFF</a>
		</h3>
		<h3> 
			YLW LED Ctrl ==> 
			<a href="/ledYlw/on" class="button">TURN ON</a>  
			<a href="/ledYlw/off"class="button">TURN OFF</a>
		</h3>
		<h3> 
			GRN LED Ctrl ==> 
			<a href="/ledGrn/on" class="button">TURN ON</a>  
			<a href="/ledGrn/off"class="button">TURN OFF</a>
		</h3>
		
   </body>
</html>
The picture shows the final webpage.


8. Going Further With Templates
As we discussed briefly before, the render_template() function invokes the Jinja2 template engine that comes bundled with the Flask framework. Jinja2 substitutes {{ … }} blocks with the corresponding values, given by the arguments provided in the render_template() call.

But this is substitution is not only what Jinja2 can do. For example, templates also support control statements, given inside {% … %} blocks. We can change our index.html template in order to add conditional statements to deploy a specific button depending on actuator real value. In other words, “toggle” the actuator condition. Let’s rewrite the status and command part of index.html, using conditional statement :

<!DOCTYPE html> 
  <head> 
     <title>GPIO Control</title> 
     <link rel="stylesheet" href='../static/master.css'/> 
  </head> 
  <body> 
		<h1>RPi GPIO Control</h1> 
		<h2> Sensor Status </h2> 
		<h3> BUTTON ==>  {{ button  }}</h3> 
		<h3> MOTION ==>  {{ senPIR  }}</h3> 
		<br> 
		<h2> Actuator Status & Control </h2> 
		<h3> RED LED ==>  {{ ledRed  }}  ==>   
			{% if  ledRed   == 1 %} 
				<a href="/ledRed/off"class="button">TURN OFF</a> 
			{% else %} 
				<a href="/ledRed/on" class="button">TURN ON</a>  
			{% endif %}	 
		</h3> 
		<h3> YLW LED ==>  {{ ledYlw  }}  ==>   
			{% if  ledYlw   == 1 %} 
				<a href="/ledYlw/off"class="button">TURN OFF</a> 
			{% else %} 
				<a href="/ledYlw/on" class="button">TURN ON</a>  
			{% endif %}	 
		</h3> 
		<h3> GRN LED ==>  {{ ledGrn  }}  ==>   
			{% if  ledGrn   == 1 %} 
				<a href="/ledGrn/off"class="button">TURN OFF</a> 
			{% else %} 
				<a href="/ledGrn/on" class="button">TURN ON</a>  
			{% endif %}	 
		</h3> 
  </body> 
</html>
The picture below shows the result:


This is only a small taste of what can be done with Python and Flask. If you really want to go deeper with Flask, you can follow the great tutorial from Miguel Grimberg: The Flask Mega Tutorial,

9. Conclusion

As always, I hope this project can help others find their way into the exciting world of electronics!

For details and final code, please visit my GitHub depository: RPi-Flask-WebServer

And to learn how to work with data, graphics, and databases, you can also see my tutorial: From Data to Graph. a Web Jorney With Flask and SQLite

For more projects, please visit my blog: MJRoBot.org

Saludos from the south of the world!

See you at my next tutorial!

Thank you,

Marcelo

Web Development
Flask
Python
Raspberry Pi
Web Server
No rights reserved

 by the author.

459


9


Marcelo Rovai
Towards Data Science
Written by Marcelo Rovai
1.3K Followers
·
Writer for 
Towards Data Science

Engineer, MBA, Master in Data Science. Passionate to share knowledge about Data Science and Electronics with focus on Physical Computing, IoT and Robotics.

Follow

More from Marcelo Rovai and Towards Data Science
Real-Time Face Recognition: An End-To-End Project
Marcelo Rovai
Marcelo Rovai

in

Towards Data Science

Real-Time Face Recognition: An End-To-End Project
Learn step by step, how to use a PiCam to recognize faces in real-time.
Mar 12, 2018
1.2K
19
5 AI Projects You Can Build This Weekend (with Python)
Shaw Talebi
Shaw Talebi

in

Towards Data Science

5 AI Projects You Can Build This Weekend (with Python)
From beginner-friendly to advanced

Oct 8
3.3K
58
GenAI with Python: Build Agents from Scratch (Complete Tutorial)
Mauro Di Pietro
Mauro Di Pietro

in

Towards Data Science

GenAI with Python: Build Agents from Scratch (Complete Tutorial)
with Ollama, LangChain, LangGraph (No GPU, No APIKEY)

Sep 29
1.8K
24
From Data to Graph: a Web Jorney With Flask and SQLite
Marcelo Rovai
Marcelo Rovai

From Data to Graph: a Web Jorney With Flask and SQLite
Capturing real data (RPi/DHT22), saving them in a database (SQLite), creating graphs (Matplotlib) and presenting them on a web page…
Mar 17, 2018
192
10
See all from Marcelo Rovai
See all from Towards Data Science
Recommended from Medium
Build a Beautiful Weather App with Flask and OpenWeather API: A Step-by-Step Guide
Kuldeepkumawat
Kuldeepkumawat

Build a Beautiful Weather App with Flask and OpenWeather API: A Step-by-Step Guide
Introduction:

Aug 9
1
The resume that got a software engineer a $300,000 job at Google.
Alexander Nguyen
Alexander Nguyen

in

Level Up Coding

The resume that got a software engineer a $300,000 job at Google.
1-page. Well-formatted.

Jun 1
24K
484
Lists



Coding & Development
11 stories
·
862 saves



Predictive Modeling w/ Python
20 stories
·
1613 saves
Principal Component Analysis for ML
Time Series Analysis
deep learning cheatsheet for beginner
Practical Guides to Machine Learning
10 stories
·
1966 saves

AI-generated image of a cute tiny robot in the backdrop of ChatGPT’s logo

ChatGPT
21 stories
·
848 saves
Building Web Applications using Flask
Mohsin Shaikh
Mohsin Shaikh

Building Web Applications using Flask
Welcome to this comprehensive guide on Flask, a lightweight web framework in Python. Flask is popular for its simplicity and flexibility…

Jun 2
How Python, Django, and Blockchain Can Revolutionize US Elections
Kaïss Bouali, PSPO™, ITIL™, Oracle Cloud Associate
Kaïss Bouali, PSPO™, ITIL™, Oracle Cloud Associate

How Python, Django, and Blockchain Can Revolutionize US Elections
Introduction

Aug 19
3
SSH Raspberry Pi via Cell Phone
Shilleh
Shilleh

SSH Raspberry Pi via Cell Phone
Learn how to control your raspberry pi remotely with your cell phone via the SSH protocol. Thankfully the Termius app, available on Android…

May 5
1
Fetching price data from Gate.io
Fadai Mammadov
Fadai Mammadov

in

Coinmonks

Fetching price data from Gate.io
Crypto programming in Python

May 19
20
See more recommendations
Help

Status

About

Careers

Press

Blog

Privacy

Terms

Text to speech

Teams
