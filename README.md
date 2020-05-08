# vpn
My personal VPN server


## Steps to provision a VPN Server
* run `sudo setup.py init`

### To setup server certificates
* run `sudo setup.py server`

### To setup client certificates
* run `sudo setup.py client <CLIENT_NAME>`

### To setup .opvn profile
* run `sudo setup.py ovpn <CLIENT_NAME>`


* run `sudo terraform apply`
* install .ovpn profile with openvpn
