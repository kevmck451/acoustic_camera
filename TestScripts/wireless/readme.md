# Wireless Implementation

- Starting with this [Website](https://nims11.wordpress.com/2012/04/27/hostapd-the-linux-way-to-create-virtual-wifi-access-point/)

## Hardware: Setting Up & Testing
- check wifi card support
```zsh
iw list | grep "Supported interface modes" -A 8
```
- looking for AP capabilities
~~~
	Supported interface modes:
		 * IBSS
		 * managed
		 * AP
		 * AP/VLAN
		 * monitor
		 * mesh point
	Band 1:
		Capabilities: 0x17e
--
	Supported interface modes:
		 * IBSS
		 * managed
		 * AP
		 * P2P-client
		 * P2P-GO
		 * P2P-device
	Band 1:
		Capabilities: 0x1020

~~~
- it's listed, so moving on
- install hostapd
```zsh
sudo apt-get update && sudo apt-get install hostapd
```
- configure test hostapd
```zsh
nano ~/hostapd-test.conf
```
~~~
#change wlan to your wireless device
interface=wlan1
driver=nl80211
ssid=test
channel=1
~~~
- Start 'test' network and confirm working 
```zsh
sudo hostapd ~/hostapd-test.conf
```

### Start Here if testing not needed
- here's the complete ```/etc/hostapd/hostapd.conf``` file
```zsh
sudo nano /etc/hostapd/hostapd.conf
```
~~~
# sets the wifi interface to use
interface=wlan1

# driver to use, nl80211 works in most cases
driver=nl80211

# sets the ssid of the virtual wifi access point
ssid=Acoustic_Camera

# sets the mode of wifi, depends upon the devices you will be using. It can be a,b,g,n. Not all cards support 'n'.
hw_mode=g

# sets the channel for your wifi
channel=6

# macaddr_acl sets options for mac address filtering. 0 means "accept unless in deny list"
macaddr_acl=0

# setting ignore_broadcast_ssid to 1 will disable the broadcasting of ssid
ignore_broadcast_ssid=0

# Sets authentication algorithm
# 1 - only open system authentication
# 2 - both open system authentication and shared key authentication
# auth_algs=1
##### Sets WPA and WPA2 authentication (remove this section if you don't need encryption)#####
# wpa option sets which wpa implementation to use
# 1 - wpa only
# 2 - wpa2 only
# 3 - both
# wpa=3
# sets wpa passphrase required by the clients to authenticate themselves on the network
# wpa_passphrase=KeePGuessinG
# sets wpa key management
# wpa_key_mgmt=WPA-PSK
# sets encryption used by WPA
# wpa_pairwise=TKIP
# sets encryption used by WPA2
# rsn_pairwise=CCMP
ctrl_interface=/var/run/hostapd
ctrl_interface_group=0

~~~

```zsh
sudo hostapd /etc/hostapd/hostapd.conf
```


## Setting Up DHCP Server

```zsh
sudo apt-get install dnsmasq

# confirm file exists
cat /etc/dnsmasq.conf

# save original as backup
sudo cp /etc/dnsmasq.conf /etc/dnsmasq.conf.backup

# delete file so we can replace it 
sudo rm /etc/dnsmasq.conf
```
- create new one
```zsh
sudo nano /etc/dnsmasq.conf
```

~~~
interface=wlan1
dhcp-range=10.0.0.2,10.0.0.20,255.255.255.0,24h
dhcp-option=option:router,10.0.0.1
dhcp-authoritative
~~~

## Sharing the Internet
```zsh
sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"
```
```zsh
sudo iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE
sudo iptables -A FORWARD -i wlan0 -o wlan1 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i wlan1 -o wlan0 -j ACCEPT
```
```zsh
sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"
```

```zsh
sudo nano /etc/rc.local
```
- Add this line before exit 0:
~~~
iptables-restore < /etc/iptables.ipv4.nat
~~~

```zsh
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl start hostapd

sudo systemctl restart dnsmasq

```
```zsh
sudo reboot
```

## Start network on boot

- configure hostapd and dnsmasq to start at boot
```zsh
sudo systemctl enable hostapd; sudo systemctl enable dnsmasq
```

### Persist IP and Routing Configuration
```zsh
sudo nano /etc/dhcpcd.conf
```
- add this to the bottom of file
~~~
# Configuration for wlan1
interface wlan1
static ip_address=10.0.0.1/24
nohook wpa_supplicant

interface usb0
static ip_address=192.168.80.2/24

# Prefer wlan0 for default route
interface wlan0
static routers=192.168.0.1

# Add configuration to ignore routes for usb0
interface usb0
nogateway

# Set a lower metric for wlan0
interface wlan0
static ip_address=192.168.0.142/24
static routers=192.168.0.1
static domain_name_servers=192.168.0.1
metric 200
~~~

### Enable IP Forwarding and NAT Automatically
```zsh
sudo nano /etc/sysctl.conf
```
- uncomment line with this
~~~
net.ipv4.ip_forward=1
~~~
```zsh
sudo sysctl -p
sudo mkdir /etc/iptables
sudo iptables-save | sudo tee /etc/iptables/rules.v4 > /dev/null
sudo apt install iptables-persistent
sudo reboot
```

## Ensure compatability with FPGA ethernet over USB
- make sure fpga is plugged in so usb interface is up
```zsh
sudo ip addr add 192.168.80.2/24 dev usb0
sudo ip route del default via 192.168.0.1 dev wlan0
sudo ip route add default via 192.168.0.1 dev wlan0 metric 100
sudo ip route del default via 192.168.0.1 dev wlan0
sudo ip route del default via 192.168.80.1 dev usb0
sudo ip route add default via 192.168.0.1 dev wlan0 metric 100

```

- test if working
```zsh
ping 192.168.80.1
```
```zsh
ping google.com
```

### Add local host names
```zsh
sudo nano /etc/hosts
```
~~~
192.168.80.1    fpga
~~~

- make pi ip static
```zsh
sudo nano /etc/dhcpcd.conf 
```
~~~
interface eth0
static ip_address=10.0.0.13/24
static routers=10.0.0.1
static domain_name_servers=10.0.0.1
~~~

```zsh
# from macbook
ssh pi@papapi.local

# how to ssh into other devices
ssh nixos@fpga
ssh pi@acousticpi
```



### Random Commands for Troubleshooting
```zsh
ip route
ip route show default
sudo ip route del default via 192.168.80.1 dev usb0
```