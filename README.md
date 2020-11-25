# Event Tracker

![](https://img.shields.io/badge/Python-3.6%2B-blue)  ![](https://img.shields.io/badge/Django-2.2%2B-green)


## Description
A microservice made with Django to track real-time events.

#### Behavior
Tracks real-time events.

#### Benefits
Real-time events are very useful to make decisions in real-time and show the current usage of modules.

#### Target Users
Platform Admins

#### Cloud

The app is running in  <abbr title="Heroku is a platform as a service (PaaS) that enables developers to build, run, and operate applications entirely in the cloud.">Herokus</abbr> platform. [See the App...](#)

## Testing on Local

 If you want to test in localhost there are a quick steps you can follow to try it.

`$ mkdir tracker`

`$ cd tracker/`

`$ git clone https://github.com/alexeipopov95/event-tracker.git .`

`$ cd event-tracker/`

`$ pip install -r requirements.txt`

`$ python manage.py makemigrations`

`$ python manage.py migrate`

`$ python manage.py create_random_events` <= this command will fill the database with some data. It takes less than 10 secconds.

`$ python manage.py createsuperuser --user username`

`$ PWD: ****`
`$ PWD again: ****`

`$ python manage.py runserver`

and you can access into the admin by the url localhost:8000/admin


## Endpoints

This is the response by default if something goes wrong:

		response = {
            'status' : False,
            'response' : None,
            'error' : {
                'internal' : <info>,
                'external' : <info>
            }
        }


#### POST
> count an ocurrency of an event

        /api/events/{EVENT_NAME}
		
		response = {
            'status' : True,
            'response' : 201,
        }
		ELSE status is False and response is 403
		
        
#### POST
> increase N times the ocurrencies of an event 

        /api/events/{EVENT_NAME}/{NUM}
		if created
		response = {
			status : True,
			response : 201
		}
		if updated
		response = {
			status : True,
			response : 204
		}
		else status False and response 404

        

#### GET
> list all the events between START_DATE and END_DATE 

		/api/events?start_date=YYYYMMDDHH&end_date=YYYYMMDD
		response = {
            'status'   : True,
            'response' : {
				[
					[{'date':'2020091112','event':'login','count':12}],
					[{'date':'2020091113','event':'login','count':2000}],
					[{'date':'2020091114','event':'login','count':5400}],
					[{'date':'2020091112','event':'resource/209','count':1}],
					[{'date':'2020091113','event':'resource/209','count':203}],
					[{'date':'2020091114','event':'resource/209','count':33}]
				]
			},
        }

#### GET
> list all the events stored historically

		/api/events/unique
		response = {
            'status'      : True,
            'response' : {
				[
					['event':'login','count':7512}],
					['event':'resource/209','count':237}],
				]
			},
        }

#### GET
> return a PNG/JPG file with a histogram chart showing the frecuency for a given event

		/api/events/histogram/{EVENT}/{YYYMMDD}
		Response:

![](http://tusigno.tk/histo.png)
