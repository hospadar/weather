weather
=======

What does it do?
========
A couple python utilities that pull weather data down from wunderground and create an HTML5 plot of temerature over time.

Why? For maple syrup!  The general idea is to watch the day/night temperature fluctuations until you have the right kind of freezing nights and warm days that make for good tapping

How? There's one script that pulls data down and stores it in a little local DB, and another script that makes a chart with the data.  You can view this chart with any modern web browser.

You'll need a weather underground api key.  You can get one for free for personal use here: http://www.wunderground.com/weather/api/

Usage:
use harvest.py to pull in temperature data for your desired locale.  You can have it grab the current data and add it to your cache or have it pull data for some other day that you specify.

You'll need to create a file called key.py which defines a variable WUNDER_KEY which should be set to your wunderground api key.
Also, if you don't live in michigan, you'll need to edit the base_url in harvest.py to match your location

Once you've harvested all the temp data you want, use make_chart.py to generate an html file with your chart.

Maybe put harvest.py and make_chart in a cron job?

See "python harvest.py -h" for more detailed usage
