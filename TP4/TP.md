# TP4 : TCP, UDP et services réseau

Dans ce TP on va explorer un peu les protocoles TCP et UDP. 

**La première partie est détente**, vous explorez TCP et UDP un peu, en vous servant de votre PC.

La seconde partie se déroule en environnement virtuel, avec des VMs. Les VMs vont nous permettre en place des services réseau, qui reposent sur TCP et UDP.  
**Le but est donc de commencer à mettre les mains de plus en plus du côté administration, et pas simple client.**

Dans cette seconde partie, vous étudierez donc :

- le protocole SSH (contrôle de machine à distance)
- le protocole DNS (résolution de noms)
  - essentiel au fonctionnement des réseaux modernes


# I. First steps

Faites-vous un petit top 5 des applications que vous utilisez sur votre PC souvent, des applications qui utilisent le réseau : un site que vous visitez souvent, un jeu en ligne, Spotify, j'sais po moi, n'importe.

🌞 **Déterminez, pour ces 5 applications, si c'est du TCP ou de l'UDP**

- avec Wireshark, on va faire les chirurgiens réseau
- déterminez, pour chaque application :
  - IP et port du serveur auquel vous vous connectez
  - le port local que vous ouvrez pour vous connecter

- Overwatch   
(server) IP : 34.85.161.55  
(server) Port : 26564  
(local) Port : 58002  
```
PS C:\Windows\system32> netstat -b -n -p udp -a

Connexions actives

  Proto  Adresse locale         Adresse distante       État
 [dashost.exe]
  UDP    0.0.0.0:58002          *:*

```

![Overwatch in game](./Overwatch-in-game.pcapng)

- Spotify  
(server) IP :  35.186.224.25  
(server) Port :  443  
(local) Port :  52867  

```
PS C:\Windows\system32> netstat -b -n -p udp -a

Connexions actives

  Proto  Adresse locale         Adresse distante       État
 [Spotify.exe]
  UDP    0.0.0.0:52867          35.186.224.25:443

```
![Spotify TCP](./Spotify-TCP.pcapng)  

- Chrome    
(server) IP : 142.250.110.188  
(server) Port : 5228  
(local) Port : 62305  

![Chrome TCP](./Chrome-TCP.pcapng)  

- Youtube   
(server) IP : 51.124.78.146  
(server) Port :  443  
(local) Port : 58504

![Youtube TCP](./youtube-TCP.pcapng)

- Battle.net   
(server) IP : 162.247.241.14  
(server) Port : 443  
(local) Port : 53869  

```
netstat -b -n
 [Battle.net.exe]
  TCP    10.33.16.237:53869     162.247.241.14:443     ESTABLISHED

```
![Battle net TCP](./Battle-net_TCP.pcapng)  

🦈🦈🦈🦈🦈 **Bah ouais, captures Wireshark à l'appui évidemment.** Une capture pour chaque application, qui met bien en évidence le trafic en question.

# II. Mise en place

## 1. SSH

![3-way handshake](./SSH.pcapng)

![VM](./SSH1.pcapng)

![Fin de connexion](./SSH2.pcapng)
```
PS C:\Windows\system32> netstat -b -n

Connexions actives

  Proto  Adresse locale         Adresse distante       État 
  [ssh.exe]
  TCP    10.4.1.1:50734         10.4.1.11:22           ESTABLISHED
 
```
```
[user@node1 ~]$ss -tnp
tcp    CLOSE-WAIT  1       0                  10.33.17.145:47532    51.144.164.215:22    users:(("code",pid=6682,fd=24)) 
```

# III. DNS

## 2. Setup

```bash
[user@dns-server ~]$ sudo cat /etc/named.conf

options {
        listen-on port 53 { 127.0.0.1; any; };
        listen-on-v6 port 53 { ::1; };
        directory       "/var/named";
        dump-file       "/var/named/data/cache_dump.db";
        statistics-file "/var/named/data/named_stats.txt";
        memstatistics-file "/var/named/data/named_mem_stats.txt";
        secroots-file   "/var/named/data/named.secroots";
        recursing-file  "/var/named/data/named.recursing";
        allow-query     { localhost; any; };
        allow-query-cache { localhost; any; };
        /* 
         - If you are building an AUTHORITATIVE DNS server, do NOT enable recursion.
         - If you are building a RECURSIVE (caching) DNS server, you need to enable 
           recursion. 
         - If your recursive DNS server has a public IP address, you MUST enable access 
           control to limit queries to your legitimate users. Failing to do so will
           cause your server to become part of large scale DNS amplification 
           attacks. Implementing BCP38 within your network would greatly
           reduce such attack surface 
        */
        recursion yes;

        dnssec-validation yes;

        managed-keys-directory "/var/named/dynamic";
        geoip-directory "/usr/share/GeoIP";

        pid-file "/run/named/named.pid";
        session-keyfile "/run/named/session.key";

        /* https://fedoraproject.org/wiki/Changes/CryptoPolicy */
        include "/etc/crypto-policies/back-ends/bind.config";
};

logging {
        channel default_debug {
                file "data/named.run";
                severity dynamic;
        };
};

zone "tp4.b1" IN {
        type master;
        file "tp4.b1.db";
        allow-update { none; };
        allow-query {any; };
};

zone "1.4.10.in-addr.arpa" IN {
     type master;
     file "tp4.b1.rev";
     allow-update { none; };
     allow-query { any; };
};

include "/etc/named.rfc1912.zones";
include "/etc/named.root.key";

```

```bash
[user@dns-server ~]$ sudo cat  /var/named/tp4.b1.db
$TTL 86400
@ IN SOA dns-server.tp4.b1. admin.tp4.b1. (
    2019061800 ;Serial
    3600 ;Refresh
    1800 ;Retry
    604800 ;Expire
    86400 ;Minimum TTL
)

@ IN NS dns-server.tp4.b1.

dns-server IN A 10.4.1.201
node1      IN A 10.4.1.11
```

```bash
[user@dns-server ~]$ sudo cat  /var/named/tp4.b1.rev
$TTL 86400
@ IN SOA dns-server.tp4.b1. admin.tp4.b1. (
    2019061800 ;Serial
    3600 ;Refresh
    1800 ;Retry
    604800 ;Expire
    86400 ;Minimum TTL
)

; Infos sur le serveur DNS lui même (NS = NameServer)
@ IN NS dns-server.tp4.b1.

;Reverse lookup for Name Server
201 IN PTR dns-server.tp4.b1.
11 IN PTR node1.tp4.b1.
```
```bash
[user@dns-server ~]$ sudo systemctl status named
● named.service - Berkeley Internet Name Domain (DNS)
     Loaded: loaded (/usr/lib/systemd/system/named.service; enabled; vendor preset: disabled)
     Active: active (running) since Fri 2022-11-10 10:36:35 CEST; 14min ago
   Main PID: 1764 (named)
      Tasks: 5 (limit: 2684)
     Memory: 14.5M
        CPU: 33ms
     CGroup: /system.slice/named.service
             └─1764 /usr/sbin/named -u named -c /etc/named.conf
```
```
[user@dns-server ~]$ sudo ss -tpunl
Address:Port    Process                              
udp      UNCONN    0         0                 10.4.1.201:53                0.0.0.0:*        users:(("named",pid=1764,fd=19))
```

```
[user@dns-server ~]$ sudo firewall-cmd --list-all
[user@dns-server ~]$ sudo firewall-cmd --add-port=53/udp --permanent
success
[user@dns-server ~]$ sudo firewall-cmd --reload
success
[user@dns-server ~]$ sudo firewall-cmd --list-all
public (active)
  target: default
  icmp-block-inversion: no
  interfaces: enp0s8
  sources: 
  services: cockpit dhcpv6-client ssh
  ports: 53/udp
  protocols: 
  forward: yes
  masquerade: no
  forward-ports: 
  source-ports: 
  icmp-blocks: 
  rich rules: 

```

## 3. Test


```
[user@node1 ~]$ sudo cat  /etc/sysconfig/network-scripts/ifcfg-enp0s8 
DEVICE=enp0s8

BOOTPROTO=static
ONBOOT=yes

IPADDR=10.4.1.11
NETMASK=255.255.255.0

GATEWAY=10.4.1.254
DNS1=10.4.1.201
```
```
[user@node1 ~]$ dig google.com

; <<>> DiG 9.16.23-RH <<>> google.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 59836
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 65494
;; QUESTION SECTION:
;google.com.                    IN      A

;; ANSWER SECTION:
google.com.             199     IN      A       142.250.74.238

;; Query time: 30 msec
;; SERVER: 10.0.2.3#53(10.0.2.3)
;; WHEN: Fri Oct 28 17:23:08 CEST 2022
;; MSG SIZE  rcvd: 55

[user@node1 ~]$ dig dns-server.tp4.b1

; <<>> DiG 9.16.23-RH <<>> dns-server.tp4.b1
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NXDOMAIN, id: 19984
;; flags: qr rd ra; QUERY: 1, ANSWER: 0, AUTHORITY: 1, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 65494
;; QUESTION SECTION:
;dns-server.tp4.b1.             IN      A

;; AUTHORITY SECTION:
.                       86369   IN      SOA     a.root-servers.net. nstld.verisign-grs.com. 2022102800 1800 900 604800 86400

;; Query time: 59 msec
;; SERVER: 10.0.2.3#53(10.0.2.3)
;; WHEN: Fri Oct 28 17:23:36 CEST 2022
;; MSG SIZE  rcvd: 121
```


```
sudo cat  /etc/resolv.conf 

nameserver 10.4.1.201
nameserver 127.0.0.53
options edns0 trust-ad
search .

```

```
PS C:\Windows\system32> nslookup node1.tp4.b1 10.4.1.201
Serveur :   dns-server.tp4.b1
Address:  10.4.1.201

Nom :    node1.tp4.b1
Address:  10.4.1.11

```

**[DNS](./Dns.pcapng)**

