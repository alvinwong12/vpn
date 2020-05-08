# vpn
My personal VPN server


## Steps to provision a VPN Server
* Create and/or change into a new folder
* Setup terraform files
* run `sudo setup.py init`

#### To setup server certificates
* run `sudo setup.py server`

#### To setup client certificates
* run `sudo setup.py client <CLIENT_NAME>`

#### To setup .opvn profile
* run `sudo setup.py ovpn <CLIENT_NAME>`

---

## To Start the VPN Server
* run `sudo terraform apply` 
> **Should only be run after server certificates are setup**

## To setup connection to VPN with openvpn
* install .ovpn profile with openvpn


---

## Changing state of VPN Server

* `vpn.py <region> list` to list all vpn servers in this region
* `vpn.py <region> start <vpn_name>` to start this vpn server in this region
* `vpn.py <region> stop <vpn_name>` to stop this vpn server in this region

---
## Reference
* https://www.comparitech.com/blog/vpn-privacy/how-to-make-your-own-free-vpn-using-amazon-web-services/#Set_up_OpenVPN_on_the_server_and_client
* https://openvpn.net/community-resources/how-to/
