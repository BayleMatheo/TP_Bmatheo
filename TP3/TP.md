## TP3-Rendu

### 1. Echange ARP

🌞**Générer des requêtes ARP**

```
marcel user :

[user1@localhost ~]$ ping 10.3.1.11
PING 10.3.1.11 (10.3.1.11) 56(84) bytes of data.
64 bytes from 10.3.1.11: icmp_seq=1 ttl=64 time=0.717 ms
64 bytes from 10.3.1.11: icmp_seq=2 ttl=64 time=0.633 ms
64 bytes from 10.3.1.11: icmp_seq=3 ttl=64 time=0.592 ms
--- 10.3.1.11 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2038ms
rtt min/avg/max/mdev = 0.592/0.647/0.717/0.052 ms
[user1@localhost ~]$ ip neigh show 10.3.1.11
10.3.1.11 dev enp0s8 lladdr 08:00:27:2a:0e:57 STALE

```
- L'adresse Mac associé a john est : 08:00:27:2a:0e:57

```
john user :

[user1@localhost ~]$ ping 10.3.1.12
PING 10.3.1.12 (10.3.1.12) 56(84) bytes of data.
64 bytes from 10.3.1.12: icmp_seq=1 ttl=64 time=0.632 ms
64 bytes from 10.3.1.12: icmp_seq=2 ttl=64 time=0.550 ms
64 bytes from 10.3.1.12: icmp_seq=3 ttl=64 time=0.586 ms
--- 10.3.1.12 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2056ms
rtt min/avg/max/mdev = 0.550/0.589/0.632/0.033 ms
[user1@localhost ~]$ arp -a
-bash: arp: command not found
[user1@localhost ~]$ arp
-bash: arp: command not found
[user1@localhost ~]$ ip neigh show 10.3.1.12
10.3.1.12 dev enp0s8 lladdr 08:00:27:8b:62:6f STALE

```
- on voit que l'adresse mac associé a l'IP de marcel est : 08:00:27:8b:62:6f

```
marcel user :

[user1@localhost ~]$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:8b:62:6f brd ff:ff:ff:ff:ff:ff
    inet 10.3.1.12/24 brd 10.3.1.255 scope global noprefixroute enp0s8
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:fe8b:626f/64 scope link
       valid_lft forever preferred_lft forever
```
- ici sur le client marcel on voit bien que son adresse mac est bien la bonne soit : 08:00:27:8b:62:6f


### 2. Analyse de trames

🌞**Analyse de trames**

 ```
marcel user :

[user1@localhost ~]$ sudo ip neigh flush all
[sudo] password for user1:
[user1@localhost ~]$ ip neigh show
10.3.1.50 dev enp0s8 lladdr 0a:00:27:00:00:11 REACHABLE
[user1@localhost ~]$ sudo tcpdump -i enp0s8 -c 10 -w tp3_arp.pcap arp
dropped privs to tcpdump
tcpdump: listening on enp0s8, link-type EN10MB (Ethernet), snapshot length 262144 bytes
^C4 packets captured
4 packets received by filter
0 packets dropped by kernel

```
```
john user :

[user1@localhost ~]$ sudo ip neigh flush all
[sudo] password for user1:
[user1@localhost ~]$ ip neigh show
10.3.1.50 dev enp0s8 lladdr 0a:00:27:00:00:11 REACHABLE
[user1@localhost ~]$ ping 10.3.1.12
PING 10.3.1.12 (10.3.1.12) 56(84) bytes of data.
64 bytes from 10.3.1.12: icmp_seq=1 ttl=64 time=1.14 ms
64 bytes from 10.3.1.12: icmp_seq=2 ttl=64 time=0.631 ms
64 bytes from 10.3.1.12: icmp_seq=3 ttl=64 time=0.501 ms
^C
--- 10.3.1.12 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2051ms
rtt min/avg/max/mdev = 0.501/0.757/1.139/0.275 ms

```


🦈 **Capture réseau `tp3_arp.pcapng`** qui contient un ARP request et un ARP reply 
- [tp3_arp](./tp3_arp.pcap)

## II. Routage

Vous aurez besoin de 3 VMs pour cette partie. **Réutilisez les deux VMs précédentes.**

| Machine  | `10.3.1.0/24` | `10.3.2.0/24` |
|----------|---------------|---------------|
| `router` | `10.3.1.254`  | `10.3.2.254`  |
| `john`   | `10.3.1.11`   | no            |
| `marcel` | no            | `10.3.2.12`   |

> Je les appelés `marcel` et `john` PASKON EN A MAR des noms nuls en réseau 🌻

```schema
   john                router              marcel
  ┌─────┐             ┌─────┐             ┌─────┐
  │     │    ┌───┐    │     │    ┌───┐    │     │
  │     ├────┤ho1├────┤     ├────┤ho2├────┤     │
  └─────┘    └───┘    └─────┘    └───┘    └─────┘
```

### 1. Mise en place du routage

🌞**Activer le routage sur le noeud `router`**

```
router :

[user1@localhost ~]$ sudo firewall-cmd --add-masquerade --zone=public --permanent
success

```

🌞**Ajouter les routes statiques nécessaires pour que `john` et `marcel` puissent se `ping`**

```
john user :

[user1@localhost ~]$ sudo nano /etc/sysconfig/network-scripts/route-enp0s8
[sudo] password for user1:
[user1@localhost ~]$ cat /etc/sysconfig/network-scripts/route-enp0s8
10.3.1.11 via 10.3.2.254 dev0 eth0
[user1@localhost ~]$ ip route show
10.3.1.0/24 dev enp0s8 proto kernel scope link src 10.3.1.11 metric 100
[user1@localhost ~]$ sudo nano /etc/sysconfig/network
[sudo] password for user1:
GATEWAY=10.3.1.254
[user1@localhost ~]$ sudo systemctl restart NetworkManager
[user1@localhost ~]$ ip route show
default via 10.3.1.254 dev enp0s8 proto static metric 100
10.3.1.0/24 dev enp0s8 proto kernel scope link src 10.3.1.11 metric 100
[user1@localhost ~]$ ping 10.3.2.12 //marcel user
PING 10.3.2.12 (10.3.2.12) 56(84) bytes of data.
64 bytes from 10.3.2.12: icmp_seq=1 ttl=63 time=1.32 ms
64 bytes from 10.3.2.12: icmp_seq=2 ttl=63 time=0.941 ms
64 bytes from 10.3.2.12: icmp_seq=3 ttl=63 time=1.31 ms

```
```
[user1@localhost ~]$ sudo nano /etc/sysconfig/network-scripts/route-enp0s8
[sudo] password for user1:
[user1@localhost ~]$ cat /etc/sysconfig/network-scripts/route-enp0s8
10.3.2.12 via 10.3.1.254 dev0 eth0
[user1@localhost ~]$ ip route show
default via 10.3.2.254 dev enp0s8 proto static metric 100
10.3.2.0/24 dev enp0s8 proto kernel scope link src 10.3.2.12 metric 100
[user1@localhost ~]$ sudo nano /etc/sysconfig/network
[user1@localhost ~]$ sudo systemctl restart NetworkManager
[user1@localhost ~]$ ping 10.3.1.11
PING 10.3.1.11 (10.3.1.11) 56(84) bytes of data.
64 bytes from 10.3.1.11: icmp_seq=1 ttl=63 time=1.02 ms
64 bytes from 10.3.1.11: icmp_seq=2 ttl=63 time=1.03 ms
64 bytes from 10.3.1.11: icmp_seq=3 ttl=63 time=1.11 ms
```


### 2. Analyse de trames

🌞**Analyse des échanges ARP**

`sudo ip neigh flush all` sur les trois noeud
- effectuez un `ping` de `john` vers `marcel`
  - **le `tcpdump` doit être lancé sur la machine `john`**
- essayez de déduire un les échanges ARP qui ont eu lieu
  - en regardant la capture et/ou les tables ARP de tout le monde
- répétez l'opération précédente (vider les tables, puis `ping`), en lançant `tcpdump` sur `marcel`
- **écrivez, dans l'ordre, les échanges ARP qui ont eu lieu, puis le ping et le pong, je veux TOUTES les trames** utiles pour l'échange

Par exemple (copiez-collez ce tableau ce sera le plus simple) :

| ordre | type trame  | IP source | MAC source              | IP destination | MAC destination            |
|-------|-------------|-----------|-------------------------|----------------|----------------------------|
| 1     | Requête ARP | 10.3.1.11 |`john`   `08:00.27:2a:0e`|   10.3.1.254   | Broadcast `FF:FF:FF:FF:FF` |
| 2     | Réponse ARP | 10.3.1.254|`router` `08:00:27:7f:51`|   10.3.1.11    | `marcel`  `08:00:27:2a:0e` |
| ...   | ...         | ...       | ...                     |                |                            |
| 1     | Ping        | 10.3.1.11 |`john`   `08:00:27:2a:0e`|   10.3.2.12    | `router`  `08:00:27:7f:51` |
| 2     | Pong        | 10.3.2.12 |`router` `08:00:27:2a:51`|   10.3.1.11    | `john`    `08:00:27:7f:51` |

> Vous pourriez, par curiosité, lancer la capture sur `marcel` aussi, pour voir l'échange qu'il a effectué de son côté.

🦈 **Capture réseau `tp3_routage_marcel.pcapng`**
[tp3_routage_marcel](./tp3_routage_marcel.pcap)

### 3. Accès internet

🌞**Donnez un accès internet à vos machines**

```
john user :

ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=112 time=30.1 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=112 time=23.2 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=112 time=24.0 ms
64 bytes from 8.8.8.8: icmp_seq=4 ttl=112 time=24.6 ms

``` 
```
router :

sudo nano /etc/resolv.conf

google.com 8.8.8.8

```
```
john user :

dig google.com

; <<>> DiG 9.16.23-RH <<>> google.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 28549
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 512
;; QUESTION SECTION:
;google.com.                    IN      A

;; ANSWER SECTION:
google.com.             52      IN      A       142.250.178.142

;; Query time: 32 msec
;; SERVER: 8.8.8.8#53(8.8.8.8)
;; WHEN: Fri Oct 28 12:05:34 CEST 2022
;; MSG SIZE  rcvd: 55
```

```
john user :

ping google.com
PING google.com (142.250.201.174) 56(84) bytes of data.
64 bytes from par21s23-in-f14.1e100.net (142.250.201.174): icmp_seq=1 ttl=112 time=22.1 ms
64 bytes from par21s23-in-f14.1e100.net (142.250.201.174): icmp_seq=2 ttl=112 time=21.9 ms
64 bytes from par21s23-in-f14.1e100.net (142.250.201.174): icmp_seq=3 ttl=112 time=22.1 ms
64 bytes from par21s23-in-f14.1e100.net (142.250.201.174): icmp_seq=4 ttl=112 time=22.5 ms

```

🌞**Analyse de trames**

- effectuez un `ping 8.8.8.8` depuis `john`
- capturez le ping depuis `john` avec `tcpdump`
- analysez un ping aller et le retour qui correspond et mettez dans un tableau :

| ordre | type trame | IP source          | MAC source              | IP destination | MAC destination         |     |
|-------|------------|--------------------|-------------------------|----------------|-------------------------|-----|
| 1     | ping       |`john` `10.3.1.11`  |`john`   `08:00:27:2a:0e`| `8.8.8.8`      |`router` `08:00:27:7f:51`|     |
| 2     | pong       |`DNS`  `8.8.8.8`    |`router` `08:00:27:7f:51`| `10.3.1.11`    |`john`   `08:00:27:2a:0e`| ... |

🦈 **Capture réseau `tp3_routage_internet.pcapng`**
[tp3_routage_internet](./tp3_routage_internet.pcap)

## III. DHCP

On reprend la config précédente, et on ajoutera à la fin de cette partie une 4ème machine pour effectuer des tests.

| Machine  | `10.3.1.0/24`      | `10.3.2.0/24` |
|----------|--------------------|---------------|
| `router` | `10.3.1.254`       | `10.3.2.254`  |
| `john`   | `10.3.1.11`        | no            |
| `bob`    | PAS POUR LE MOMENT | no            |
| `marcel` | no                 | `10.3.2.12`   |

```schema
   john               router              marcel
  ┌─────┐             ┌─────┐             ┌─────┐
  │     │    ┌───┐    │     │    ┌───┐    │     │
  │     ├────┤ho1├────┤     ├────┤ho2├────┤     │
  └─────┘    └─┬─┘    └─────┘    └───┘    └─────┘
   dhcp        │
  ┌─────┐      │
  │     │      │
  │     ├──────┘
  └─────┘
```

### 1. Mise en place du serveur DHCP

🌞**Sur la machine `john`, vous installerez et configurerez un serveur DHCP** (go Google "rocky linux dhcp server").


````
[user1@localhost /]$ journalctl -xeu dhcpd.service
Oct 13 15:06:52 localhost.localdomain systemd[1]: Starting DHCPv4 Server Daemon...
Oct 13 15:06:52 localhost.localdomain dhcpd[1924]: Server starting service.
Oct 13 15:06:52 localhost.localdomain systemd[1]: Started DHCPv4 Server Daemon
````
````
[user1@localhost ~]$ ip a
2: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:08:44:06 brd ff:ff:ff:ff:ff:ff
    inet 10.3.1.2/24 brd 10.3.1.255 scope global dynamic noprefixroute enp0s8
````
🌞**Améliorer la configuration du DHCP**

````
[user1@localhost ~]$ ip a
2: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:08:44:06 brd ff:ff:ff:ff:ff:ff
    inet 10.3.1.2/24 brd 10.3.1.255 scope global dynamic noprefixroute enp0s8
````
````
[user1@localhost ~]$ ping 10.3.1.254
PING 10.3.1.254 (10.3.1.254) 56(84) bytes of data.
64 bytes from 10.3.1.254: icmp_seq=1 ttl=64 time=0.639 ms
64 bytes from 10.3.1.254: icmp_seq=2 ttl=64 time=0.903 ms
64 bytes from 10.3.1.254: icmp_seq=3 ttl=64 time=0.584 ms
^C
--- 10.3.1.254 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2021ms
rtt min/avg/max/mdev = 0.584/0.708/0.903/0.139 ms
````
````
[user1@localhost ~]$ ip r s
default via 10.3.1.254 dev enp0s8 proto dhcp src 10.3.1.2 metric 100
10.3.1.0/24 dev enp0s8 proto kernel scope link src 10.3.1.2 metric 100
````
````
[user1@localhost ~]$ ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=112 time=23.9 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=112 time=24.2 ms
^C
--- 8.8.8.8 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 23.899/24.062/24.225/0.163 ms
````
````
[user1@localhost ~]$ dig google.com
;; ANSWER SECTION:
google.com.             300     IN      A       216.58.209.238
````
````
[user1@localhost ~]$ ping google.com
PING google.com (216.58.209.238) 56(84) bytes of data.
64 bytes from par10s29-in-f238.1e100.net (216.58.209.238): icmp_seq=1 ttl=247 time=29.0 ms
64 bytes from par10s29-in-f14.1e100.net (216.58.209.238): icmp_seq=2 ttl=247 time=22.9 ms
^C
--- google.com ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 22.884/25.957/29.030/3.073 ms
````

### 2. Analyse de trames

🌞**Analyse de trames**

- lancer une capture à l'aide de `tcpdump` afin de capturer un échange DHCP
- demander une nouvelle IP afin de générer un échange DHCP
- exportez le fichier `.pcapng`


🦈 **Capture réseau `tp3_dhcp.pcapng`**

[dhcp](./tp3_dhcp.pcap)