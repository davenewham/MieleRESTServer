=== SCOPE ===

This project implements a client for "Miele@home" based appliances, and a
REST-based server frontend to control the client. No official client exists for
the Miele@home protocol, as Miele wants you to use its "cloud".

=== SETUP ===

0) Resetting Miele device as needed

These instructions assume that the device is a blank configuration, and is not
currently connected to WiFi. If the device has already had step 2 or step 3
performed, it will not accept a new configuration without a reset. You can reset
the device if necessary through the local control panel.

1) Connecting Miele device to WiFi

Select "Miele@home" on the control panel of the Miele device. The device will
open its own access point with an SSID starting with "Miele@home".

Observe the SSID of the local access point:

	1a) If the SSID is "Miele@home" with no suffix, connect to the network with
	the PSK "secured-by-tls".

	1b) If the SSID is "Miele@home-{some suffix}", e.g. "Miele@home-TAA1234",
	connect to the network with your device's serial number shown on its
	sticker.

Open a DHCP server to give the Miele device an IP. 

Go to the "helpers" directory.

> cd helpers/

Edit the file "wifi.json" to contain the information of the WiFi you want the
Miele device to connect to.

*** I HIGHLY RECOMMEND FIREWALLING THIS NETWORK! ***

The Miele device will create outbound network traffic if not externally
prevented from doing so.

Run the pairing script with the IP of your Miele device. Example:

> ./provision-wifi.sh 10.0.0.5 

If successful, the Miele device will close its access point and connect to the
new WiFi. Some Miele devices will use an HTTPS endpoint for provisioning. The
provisioning script attempts both, HTTP first -- one or the other will fail.

2) Provisioning Miele Device with Cryptographic Keys

Connect to the same WiFi as the Miele device.

Generate device keys using the provided "generate-keys.py" script.

> ./generate-keys.py > provisioning/keys.json

Then run the provisioning script with the IP of your Miele device. Example:

./provision-keys.sh 192.168.1.50 ./keys.json

This will upload the generated device key to your Miele device. After this step,
your Miele device will stop responding to unencrypted/unsigned network commands.

3) 

Copy the example server configuration file in /etc/MieleRESTServer.config

Each device has a name, which is an internal handle by which the server
references it. Edit the file to enter the Miele device IPs and the same keys you
created in Step 3.

On all devices I have seen, the device route is identical to the device serial
number. Specify the device route as "auto" if you do not know. If "auto", the
server will detect it upon startup, and print it in the log. You can update the
config to include the route to save the auto-detection step on startup.

4)

Install the server with ./install.sh

5)

Test the server by navigating to: http://{YOUR_SERVER_IP}:5001/generate-summary/

You should see a JSON file that shows information from all configured devices.

6) Optional -- Home Assistant integration

If you want to use Home Assistant to query and display the device status, paste
the configuration fragment into your home assistant config.

=== TODO ===

Some Miele devices expose an internal binary protocol under the endpoint "DOP2".
Understanding this protocol is an ongoing reverse engineering effort.

There is some code that can make DOP2 requests and parse responses from the
Miele device, but so far, no useful information can be retrieved yet. 

It is possible to start some Miele devices remotely by sending {"ProcessAction"
: "1" } through a PUT request to the ProcessAction endpoint. I have not yet
explored under which conditions this is possible. A functional, but practically
useless, way of triggering this is to set up a timer on the local control panel,
and then sending ProcessAction=1 to cut the timer short and start the device
immediately. It is possible that the device can need to be programmed through
the DOP2 protocol to allow fully remote configuration and start.

Patches/pull requests welcome.

=== FURTHER READING ===

API capability docs:
https://www.miele.com/developer/assets/API_V1.x.x_capabilities_by_device.pdf

Notes from Miele devs (in German):
https://community.symcon.de/t/miele-home-xkm-3100w-protokollanalyse/43633/8
(Note: The test vectors provided with the Java programs linked in this forums
are wrong. The programs themselves do not run on current versions of Java.)


=== LICENSE AND DISCLAIMER ===

This program is licensed under GPLv3.

This program is solely based on independent reverse engineering and is not in any way
authorized, warranted or tested by Miele. Its use may void your warranty, or destroy
your Miele machines.
