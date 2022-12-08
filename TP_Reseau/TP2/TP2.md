🌞 **Mettez en place une configuration réseau fonctionnelle entre les deux machines**

```
 Adresse IPv4. . . . . . . . . . . . . .: 172.16.32.1
 Adresse IPv4. . . . . . . . . . . . . .: 172.16.32.2
 Adresse Broadcast        = 172.16.35.255
 (commande utiliser : ipconfig )
```

🌞 **Prouvez que la connexion est fonctionnelle entre les deux machines**

```
ping 172.16.32.2

Envoi d’une requête 'Ping'  172.16.32.2 avec 32 octets de données :
Réponse de 172.16.32.2 : octets=32 temps=1 ms TTL=128
Réponse de 172.16.32.2 : octets=32 temps=1 ms TTL=128
Réponse de 172.16.32.2 : octets=32 temps=1 ms TTL=128
Réponse de 172.16.32.2 : octets=32 temps=1 ms TTL=128

Statistiques Ping pour 172.16.32.2:
    Paquets : envoyés = 4, reçus = 4, perdus = 0 (perte 0%),
Durée approximative des boucles en millisecondes :
    Minimum = 1ms, Maximum = 1ms, Moyenne = 1ms
```

🌞 **Wireshark it**

-   **déterminez, grâce à Wireshark, quel type de paquet ICMP est envoyé par `ping`**
```
Quand il y a écrit request c'est celui qu'on envoie.
Et celui où il y a écrit reply c'est celui reçu en retour.
```

🦈 **PCAP qui contient les paquets ICMP qui vous ont permis d'identifier les types ICMP**

[ma capture pcap ICMP](./ping_icmp.pcapng)

🌞 **Check the ARP table**

```
arp -a

Interface : 172.16.32.1 --- 0xe
  Adresse Internet      Adresse physique      Type
  172.16.32.2           34-73-5a-ea-15-f2     dynamique

ipconfig

Passerelle par défaut. . . . . . . . . : 10.33.19.254
```

🌞 **Manipuler la table ARP**

```
arp -d
arp -a 

Interface : 172.16.32.1 --- 0xe
  Adresse Internet      Adresse physique      Type
  224.0.0.22            01-00-5e-00-00-16     statique

ping 172.16.32.2

Envoi d’une requête 'Ping'  172.16.32.2 avec 32 octets de données :
Réponse de 172.16.32.2 : octets=32 temps=1 ms TTL=128
Réponse de 172.16.32.2 : octets=32 temps=1 ms TTL=128
Réponse de 172.16.32.2 : octets=32 temps<1ms TTL=128
Réponse de 172.16.32.2 : octets=32 temps=1 ms TTL=128

Statistiques Ping pour 172.16.32.2:
    Paquets : envoyés = 4, reçus = 4, perdus = 0 (perte 0%),
Durée approximative des boucles en millisecondes :
    Minimum = 0ms, Maximum = 1ms, Moyenne = 0ms

arp -a

Interface : 172.16.32.1 --- 0xe
  Adresse Internet      Adresse physique      Type
  172.16.32.2           34-73-5a-ea-15-f2     dynamique
  172.16.35.255         ff-ff-ff-ff-ff-ff     statique
  224.0.0.22            01-00-5e-00-00-16     statique
  224.0.0.251           01-00-5e-00-00-fb     statique
  224.0.0.252           01-00-5e-00-00-fc     statique
  239.255.255.250       01-00-5e-7f-ff-fa     statique
```

🌞 **Wireshark it**

```
src : (08:8f:c3:8b:df:d6) (moi qui request vers le broadcast je ne sais pas pourquoi d'ailleurs) dst : (broadcast ff:ff:ff:ff:ff:ff)
```

🦈 **PCAP qui contient les trames ARP**

[ma capture pcap ARP](./ARP_Reply_request.pcapng)

🌞 **Wireshark it**

```
Discover
Offer
Request
ACK
```

🦈 **PCAP qui contient l'échange DORA**

[Ma capture PCAP DORA](./DORA_DHCP.pcapng)

