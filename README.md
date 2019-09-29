# Miner-Monitor
Python Script developed to monitor performance characteristics on a large number of L3,D3, &amp; S9 (ASIC) Miners

This script was authored at the request of the Network Operations Team from the GigaWatt Corporation. 

The script gathers the following information:
- Temperature
- Fan Speed
- Hash Rate

If any of these values exceed or fall below certain hard coded threshold values, the script issues an alert via the terminal.

The intent was to deploy the script on Network Monitoring stations a each mining site. Performance data would be gathered over HTTP and relayed to a database and/or the Zabbix application. 

During the initialization sequence, the script will take a variable number of host IPv4 addresses.

In testing, ten miners were monitored simultaneously. Output from the testing period is displayed in the images included within this repository.

