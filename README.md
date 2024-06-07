This is a python Azure function app which takes an input list of domains and checks quickly for open ports.
I've configured the app time out for the max of 10 mins for a Consumption-based subscription.

You will need to play with the number of domains and ports to ensure execution is completed wihtin that 10 mins window.
This is absolutely not a replacement for a proper external, nor a replacement for scanning with a better tool like Nmap.

Note that this will not check for open UDP ports, and it scans some common ports based on the Nmap port useage statistics available here: https://svn.nmap.org/nmap/nmap-services

You know the deal - only scan domains you own.

# Domains
The domains.txt file can take domains or IP addresses. Either wayteh function app will attempt to resovled them first, and will only scan domains/subdomains with DNS records

## Findings IP addresses
The following bash can be used with `az cli` to give a list of all public IP addresses across all subscriptions:
```
for s in `az account list --query "[].{id:id}" --output tsv`
 do
   #echo $s
   for pip in `az network public-ip list --subscription $s  --query "[].{ipAddress:ipAddress}" --out tsv`
      do
      echo $pip
      done
 done
```

# Findings Domains
SHRUG
