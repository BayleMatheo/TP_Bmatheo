**🌞 Affichez les infos des cartes réseau de votre PC**

- Carte réseau sans fil Wi-Fi, 4C-03-4F-88-B2-5B, 10.33.19.129
- Carte Ethernet Ethernet, 08-8F-C3-8B-DF-D6 et adresse IP de l'interface Ethernet (indisponible car déconnecté du réseau)

**🌞 Affichez votre gateway**

- ipconfig 
10.33.19.254
**🌞 Déterminer la MAC de la passerelle**

- arp -a
00-c0-e7-e0-04-4e
**🌞 Trouvez comment afficher les informations sur une carte IP (change selon l'OS)**

- Open panneau config, réseau et internet, centre réseau et partage, wifi-Ynov, détails et TADAA.
- 10.33.19.129, 4C-03-4F-88-B2-5B et 10.33.19.254

## 2. Modifications des informations

### A. Modification d'adresse IP (part 1)  

🌞 Utilisez l'interface graphique de votre OS pour **changer d'adresse IP** :

- Panneau Config, Réseau Internet,centre réseau et partage, wi-fi , Propriétés , IPV4
- 10.33.19.69
255.255.255.0
10.33.19.254
🌞 **Il est possible que vous perdiez l'accès internet.** Que ce soit le cas ou non, expliquez pourquoi c'est possible de perdre son accès internet en faisant cette opération.

- C'est possible de perdre l'accés car si 2 personnes on la même adresse IP alors la première connecté sera prioritaire et la deuxieme n'aura rien tant que la première est connecté.

---

# II. Exploration locale en duo

Owkay. Vous savez à ce stade :

- afficher les informations IP de votre machine
- modifier les informations IP de votre machine
- c'est un premier pas vers la maîtrise de votre outil de travail

On va maintenant répéter un peu ces opérations, mais en créant un réseau local de toutes pièces : entre deux PCs connectés avec un câble RJ45.

## 1. Prérequis

- deux PCs avec ports RJ45
- un câble RJ45
- **firewalls désactivés** sur les deux PCs

## 2. Câblage

Ok c'est la partie tendue. Prenez un câble. Branchez-le des deux côtés. **Bap.**

## Création du réseau (oupa)

Cette étape pourrait paraître cruciale. En réalité, elle n'existe pas à proprement parlé. On ne peut pas "créer" un réseau.

**Si une machine possède une carte réseau, et si cette carte réseau porte une adresse IP**, alors cette adresse IP se trouve dans un réseau (l'adresse de réseau). Ainsi, **le réseau existe. De fait.**  

**Donc il suffit juste de définir une adresse IP sur une carte réseau pour que le réseau existe ! Bap.**

## 3. Modification d'adresse IP

🌞 **Modifiez l'IP des deux machines pour qu'elles soient dans le même réseau**

- change Ip adress, PC1 = 10.10.10.88
								PC2 = 10.10.10.222
🌞 **Vérifier à l'aide d'une commande que votre IP a bien été changée**

- ipconfig 
ipv4 : 10.10.10.88    (PC1)
ipv4 : 10.10.10.222  (PC2)
🌞 **Vérifier que les deux machines se joignent**

- la commande marche pour les deux :
ping 10.10.10.88 
ping 10.10.10.222

🌞 **Déterminer l'adresse MAC de votre correspondant**

- arp -a
Interface : 10.10.10.88 
Adresse Internet        Adresse Physique(MAC)
10.10.10.222              **34-73-5a-ea-15-f2**



## 4. Utilisation d'un des deux comme gateway

Ca, ça peut toujours dépann irl. Comme pour donner internet à une tour sans WiFi quand y'a un PC portable à côté, par exemple.

L'idée est la suivante :

- vos PCs ont deux cartes avec des adresses IP actuellement
  - la carte WiFi, elle permet notamment d'aller sur internet, grâce au réseau YNOV
  - la carte Ethernet, qui permet actuellement de joindre votre coéquipier, grâce au réseau que vous avez créé :)
- si on fait un tit schéma tout moche, ça donne ça :

```schema
  Internet           Internet
     |                   |
    WiFi                WiFi
     |                   |
    PC 1 ---Ethernet--- PC 2
    
- internet joignable en direct par le PC 1
- internet joignable en direct par le PC 2
```

- vous allez désactiver Internet sur une des deux machines, et vous servir de l'autre machine pour accéder à internet.

```schema
  Internet           Internet
     X                   |
     X                  WiFi
     |                   |
    PC 1 ---Ethernet--- PC 2
    
- internet joignable en direct par le PC 2
- internet joignable par le PC 1, en passant par le PC 2
```

- pour ce faiiiiiire :
  - désactivez l'interface WiFi sur l'un des deux postes
  - s'assurer de la bonne connectivité entre les deux PCs à travers le câble RJ45
  - **sur le PC qui n'a plus internet**
    - sur la carte Ethernet, définir comme passerelle l'adresse IP de l'autre PC
  - **sur le PC qui a toujours internet**
    - sur Windows, il y a une option faite exprès (google it. "share internet connection windows 10" par exemple)
    - sur GNU/Linux, faites le en ligne de commande ou utilisez [Network Manager](https://help.ubuntu.com/community/Internet/ConnectionSharing) (souvent présent sur tous les GNU/Linux communs)
    - sur MacOS : toute façon vous avez pas de ports RJ, si ? :o (google it sinon)

---

🌞**Tester l'accès internet**

- ping 8.8.8.8
Envoi d’une requête 'Ping' 8.8.8.8 avec 32 octets de données : 
Réponse de 8.8.8.8 : octets=32 temps=22 ms TTL=113 
Réponse de 8.8.8.8 : octets=32 temps=22 ms TTL=113 
Réponse de 8.8.8.8 : octets=32 temps=21 ms TTL=113 
Réponse de 8.8.8.8 : octets=32 temps=23 ms TTL=113

🌞 **Prouver que la connexion Internet passe bien par l'autre PC**

- tracert -d 8.8.8.8 Détermination de l’itinéraire vers 8.8.8.8 avec un maximum de 30 sauts. 
1 ms * 2 ms 192.168.137.1 
2 * * * Délai d’attente de la demande dépassé. 
3. 7 ms 6 ms 5 ms 10.33.19.254 
4. 7 ms 5 ms 5 ms 77.196.149.137 
5. 10 ms 11 ms 8 ms 212.30.97.108 
6. 27 ms 21 ms 20 ms 77.136.172.222 
7. 22 ms 22 ms 21 ms 77.136.172.221 
8. 24 ms 23 ms 23 ms 194.6.144.186 
9. 24 ms 23 ms 23 ms 194.6.144.186 
10. 24 ms 22 ms 22 ms 72.14.194.30 
11. 24 ms 23 ms 22 ms 172.253.69.49 
12. 22 ms 23 ms 22 ms 108.170.238.107 
13. 23 ms 22 ms 23 ms 8.8.8.8