# bull_runner


The rocky.py inside the voice_agent directory can be run to get updates on the buses.

The typical way to run this application is >python rocky.py <route_name> and <stop_name>

Eg - python rocky.py c and skipper road. ("C" is the route. "Skipper road" is the stop name).

The app also accepts incomplete stop names. For instance, "skipper" matches "skipper road" and gives the timing for the next bus on this route.

