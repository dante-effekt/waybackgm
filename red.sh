#! /bin/bash

# Instalar paquetes necesarios
sudo apt-get install dnsmasq hostapd
sudo pip3 install -U python-magic

# Detener servicios
sudo systemctl stop dnsmasq
sudo systemctl stop hostapd

# Configurar /etc/dhcpcd.conf
echo "interface wlan0" | sudo tee -a /etc/dhcpcd.conf
echo "static ip_address=192.168.28.254/24" | sudo tee -a /etc/dhcpcd.conf
echo "nohook wpa_supplicant" | sudo tee -a /etc/dhcpcd.conf
sudo service dhcpcd restart

# Configurar /etc/dnsmasq.conf
echo "interface=wlan0" | sudo tee -a /etc/dnsmasq.conf
echo "dhcp-range=192.168.28.200,192.168.28.220,255.255.255.0,24h" | sudo tee -a /etc/dnsmasq.conf
sudo systemctl start dnsmasq

# Configurar /etc/hostapd/hostapd.conf
echo "interface=wlan0" | sudo tee -a /etc/hostapd/hostapd.conf
echo "driver=nl80211" | sudo tee -a /etc/hostapd/hostapd.conf
echo "ssid=fipy-DDR" | sudo tee -a /etc/hostapd/hostapd.conf
echo "wpa_passphrase=12345678" | sudo tee -a /etc/hostapd/hostapd.conf
echo "wpa=2" | sudo tee -a /etc/hostapd/hostapd.conf
echo "wpa_key_mgmt=WPA-PSK" | sudo tee -a /etc/hostapd/hostapd.conf
echo "wpa_pairwise=TKIP" | sudo tee -a /etc/hostapd/hostapd.conf
echo "hw_mode=g" | sudo tee -a /etc/hostapd/hostapd.conf
echo "channel=5" | sudo tee -a /etc/hostapd/hostapd.conf
echo "wmm_enabled=0" | sudo tee -a /etc/hostapd/hostapd.conf
echo "macaddr_acl=0" | sudo tee -a /etc/hostapd/hostapd.conf
echo "auth_algs=1" | sudo tee -a /etc/hostapd/hostapd.conf
echo "ignore_broadcast_ssid=0" | sudo tee -a /etc/hostapd/hostapd.conf
echo "rsn_pairwise=CCMP" | sudo tee -a /etc/hostapd/hostapd.conf

# Configurar /etc/default/hostapd
sudo sed -i 's/#DAEMON_CONF=.*$/DAEMON_CONF="\/etc\/hostapd\/hostapd.conf"/' /etc/default/hostapd

# Detener wpa_supplicant
sudo killall wpa_supplicant

# Habilitar y comenzar servicios
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl start hostapd

# Verificar servicios
sudo systemctl status hostapd
sudo systemctl status dnsmasq
