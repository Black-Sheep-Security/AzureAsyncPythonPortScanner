This is a python Azure function app which takes an input list of domains and checks quickly for open ports.
I've configured the app time out for the max of 10 mins for a Consumption-based subscription.

You will need to play with the number of domains and ports to ensure execution is completed wihtin that 10 mins window.
This is absolutely not a replacement for a proper external, nor a replacement for scanning with a better tool like Nmap.

Note that this will not check for open UDP ports, and it scans some common ports based on the Nmap port useage statistics available here: https://svn.nmap.org/nmap/nmap-services

You know the deal - only scan domains you own.
