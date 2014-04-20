### TrackerDash - Simple Data Analytics Server and Dashboard

TrackerDash is a data analytics and dashboard tool written in Python2.7 using Twisted-Klein which is ran locally.

###Supported Browsers:

Chrome (any)
Safari (any)

###Licence Informaion:

While TrackerDash is Beerware (look it up), this project makes extensive use of Highcharts JS and has it's own set of licenses.
To see if you need to purchase a Highcharts licence to deploy locally please see their FAQ page. (http://shop.highsoft.com/faq)

### Pre requisites:
In order for TrackerDash to run, a mongodb server must be running locally, see their [latest documentation](http://docs.mongodb.org/manual/installation/) on how to do this and get it running in your environment.

### Installation
clone the source code: `git clone https://github.com/wedgieedward/TrackerDash.git`

go to the TrackerDash directory: `cd TrackerDash`

run setup.py:  `sudo python setup.py install`

run setup.py:  `sudo python setup.py install`
test installation was successful run:  `sudo python setup.py test`

### Start TrackerDash server

To start TrackerDash normally: `python TrackerDash.py`

To see a list of available commands: `python TrackerDash.py --help`

_By default, the application will listen on your local network IP Address on port 8090. To listen on a specific port use the -p <port number> command on runtime. You can use -l to run the server on localhost_
