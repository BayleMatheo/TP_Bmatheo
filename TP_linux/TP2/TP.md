## 1. Analyse du service

On va, dans cette première partie, analyser le service SSH qui est en cours d'exécution.

🌞 **S'assurer que le service `sshd` est démarré**

```powershell
[tp2_linux@Primush ~]$ systemctl status sshd
● sshd.service - OpenSSH server daemon
     Loaded: loaded (/usr/lib/systemd/system/sshd.service; enabled; vendor pr>     Active: active (running) since Mon 2022-12-05 11:37:23 CET; 9min ago
       Docs: man:sshd(8)
             man:sshd_config(5)
   Main PID: 725 (sshd)
      Tasks: 1 (limit: 11116)
     Memory: 5.6M
        CPU: 101ms
     CGroup: /system.slice/sshd.service
             └─725 "sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups"

Dec 05 11:37:23 localhost systemd[1]: Starting OpenSSH server daemon...
Dec 05 11:37:23 localhost sshd[725]: Server listening on 0.0.0.0 port 22.
Dec 05 11:37:23 localhost sshd[725]: Server listening on :: port 22.
Dec 05 11:37:23 localhost systemd[1]: Started OpenSSH server daemon.
Dec 05 11:43:34 localhost.localdomain sshd[4134]: Accepted password for tp2_l>Dec 05 11:43:34 localhost.localdomain sshd[4134]: pam_unix(sshd:session): ses>Dec 05 11:44:56 Primush sshd[4165]: Accepted password for tp2_linux from 10.2>Dec 05 11:44:56 Primush sshd[4165]: pam_unix(sshd:session): session opened fo>lines 1-20/20 (END)
```


🌞 **Analyser les processus liés au service SSH**


```powershell
[tp2_linux@localhost ~]$ ps -ef | grep sshd
root         728       1  0 09:10 ?        00:00:00 sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups
root        1252     728  0 09:30 ?        00:00:00 sshd: tp2_linux [priv]
tp2_lin+    1256    1252  0 09:30 ?        00:00:00 sshd: tp2_linux@pts/0
tp2_lin+    1380    1257  0 10:34 pts/0    00:00:00 grep --color=auto sshd
```

🌞 **Déterminer le port sur lequel écoute le service SSH**

```powershell
[tp2_linux@localhost ~]$ ss | grep ssh
tcp   ESTAB  0      52                        10.2.2.3:ssh           10.2.2.2:63340
```

🌞 **Consulter les logs du service SSH**

```powershell
[tp2_linux@localhost log]$ journalctl | tail -10
Dec 06 10:01:01 localhost.localdomain anacron[1324]: Will run job `cron.daily' in 35 min.
Dec 06 10:01:01 localhost.localdomain anacron[1324]: Jobs will be executed sequentially
Dec 06 10:01:01 localhost.localdomain run-parts[1326]: (/etc/cron.hourly) finished 0anacron
Dec 06 10:01:01 localhost.localdomain CROND[1310]: (root) CMDEND (run-parts /etc/cron.hourly)
Dec 06 10:36:01 localhost.localdomain anacron[1324]: Job `cron.daily' started
Dec 06 10:36:01 localhost.localdomain anacron[1324]: Job `cron.daily' terminated
Dec 06 10:36:01 localhost.localdomain anacron[1324]: Normal exit (1 job run)
Dec 06 10:38:47 localhost.localdomain sudo[1392]: tp2_linux : TTY=pts/0 ; PWD=/home/tp2_linux ; USER=root ; COMMAND=/bin/journalctl var/log
Dec 06 10:38:47 localhost.localdomain sudo[1392]: pam_unix(sudo:session): session opened for user root(uid=0) by tp2_linux(uid=1001)
Dec 06 10:38:47 localhost.localdomain sudo[1392]: pam_unix(sudo:session): session closed for user root
```

## 2. Modification du service

Dans cette section, on va aller visiter et modifier le fichier de configuration du serveur SSH.

Comme tout fichier de configuration, celui de SSH se trouve dans le dossier `/etc/`.

Plus précisément, il existe un sous-dossier `/etc/ssh/` qui contient toute la configuration relative au protocole SSH

🌞 **Identifier le fichier de configuration du serveur SSH**

```powershell
[tp2_linux@localhost ~]$ cd /etc/ssh/
[tp2_linux@localhost ssh]$ ls
moduli        sshd_config.d           ssh_host_ed25519_key.pub
ssh_config    ssh_host_ecdsa_key      ssh_host_rsa_key
ssh_config.d  ssh_host_ecdsa_key.pub  ssh_host_rsa_key.pub
sshd_config   ssh_host_ed25519_key
```
- C'est le fichier ssh_config

🌞 **Modifier le fichier de conf**
```powershell
[tp2_linux@localhost ~]$ cd /etc/ssh/
[tp2_linux@localhost ssh]$ echo $RANDOM
23721
[tp2_linux@localhost ssh]$ sudo nano sshd_config
[sudo] password for tp2_linux:
[tp2_linux@localhost ssh]$ sudo cat sshd_config | grep Port
Port 23721
```

```powershell
[tp2_linux@localhost ssh]$ sudo firewall-cmd --add-port=23721/tcp --permanent
success
[tp2_linux@localhost ssh]$ sudo firewall-cmd --reload
success
[tp2_linux@localhost ssh]$ sudo firewall-cmd --list-all
public (active)
  target: default
  icmp-block-inversion: no
  interfaces: enp0s8 enp0s9
  sources:
  services: cockpit dhcpv6-client ssh
  ports: 23721/tcp 22/tcp
  protocols:
  forward: yes
  masquerade: no
  forward-ports:
  source-ports:
  icmp-blocks:
  rich rules:
```
🌞 **Redémarrer le service**

```powershell
[tp2_linux@localhost ~]$ sudo systemctl restart firewalld
```

🌞 **Effectuer une connexion SSH sur le nouveau port**

```powershell
PS C:\Users\Bayle> ssh tp2_linux@10.2.2.3 -p 23721
```

> Je vous conseille de remettre le port par défaut une fois que cette partie est terminée.

✨ **Bonus : affiner la conf du serveur SSH**

- faites vos plus belles recherches internet pour améliorer la conf de SSH
- par "améliorer" on entend essentiellement ici : augmenter son niveau de sécurité
- le but c'est pas de me rendre 10000 lignes de conf que vous pompez sur internet pour le bonus, mais de vous éveiller à divers aspects de SSH, la sécu ou d'autres choses liées

# II. Service HTTP

Dans cette partie, on ne va pas se limiter à un service déjà présent sur la machine : on va ajouter un service à la machine.

On va faire dans le *clasico* et installer un serveur HTTP très réputé : NGINX.  
Un serveur HTTP permet d'héberger des sites web.

Un serveur HTTP (ou "serveur Web") c'est :

- un programme qui écoute sur un port (ouais ça change pas ça)
- il permet d'héberger des sites web
  - un site web c'est un tas de pages html, js, css
  - un site web c'est aussi parfois du code php, python ou autres, qui indiquent comment le site doit se comporter
- il permet à des clients de visiter les sites web hébergés
  - pour ça, il faut un client HTTP (par exemple, un navigateur web)
  - le client peut alors se connecter au port du serveur (connu à l'avance)
  - une fois le tunnel de communication établi, le client effectuera des requêtes HTTP
  - le serveur répondra à l'aide du protocole HTTP

> Une requête HTTP c'est "donne moi tel fichier HTML". Une réponse c'est "voici tel fichier HTML" + le fichier HTML en question.

Ok bon on y va ?

## 1. Mise en place

🌞 **Installer le serveur NGINX**

```powershell
[tp2_linux@localhost ~]$ sudo dnf install nginx
[tp2_linux@localhost ~]$ sudo systemctl enable nginx
Created symlink /etc/systemd/system/multi-user.target.wants/nginx.service → /usr/lib/systemd/system/nginx.service.
```

🌞 **Démarrer le service NGINX**

🌞 **Déterminer sur quel port tourne NGINX**

```powershell
[tp2_linux@localhost ~]$ cat /etc/nginx/nginx.conf | grep listen
        listen       80;
        listen       [::]:80;
[tp2_linux@localhost ~]$  sudo firewall-cmd --add-port=80/tcp --permanent
success
```

> **NB : c'est la dernière fois que je signale explicitement la nécessité d'ouvrir un port dans le firewall.** Vous devrez vous-mêmes y penser lorsque nécessaire. **Toutes les commandes liées au firewall doivent malgré tout figurer dans le compte-rendu.**

🌞 **Déterminer les processus liés à l'exécution de NGINX**
```powershell
[tp2_linux@localhost ~]$ ps -ef | grep nginx
root         825       1  0 22:16 ?        00:00:00 nginx: master process /usr/sbin/nginx
nginx        826     825  0 22:16 ?        00:00:00 nginx: worker process
nginx        827     825  0 22:16 ?        00:00:00 nginx: worker process
tp2_lin+    1221    1203  0 22:17 pts/0    00:00:00 grep --color=auto nginx
```

🌞 **Euh wait**

```bash
Bayle@Ynov-Matheo MINGW64 ~ (master)
$ curl http://10.2.2.3:80 | head -n 7
<!doctype html>
<html>
  <head>
    <meta charset='utf-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <title>HTTP Server Test Page powered by: Rocky Linux</title>
    <style type="text/css">

```

## 2. Analyser la conf de NGINX

🌞 **Déterminer le path du fichier de configuration de NGINX**
```powershell
[tp2_linux@localhost ~]$ ls -al /etc/nginx/nginx.conf
-rw-r--r--. 1 root root 2334 Oct 31 16:37 /etc/nginx/nginx.conf
```

🌞 **Trouver dans le fichier de conf**

```powershell
cat: nginx.conf: No such file or directory
[tp2_linux@localhost ~]$ cat /etc/nginx/nginx.conf | grep "server {" -A 16
    server {
        listen       80;
        listen       [::]:80;
        server_name  _;
        root         /usr/share/nginx/html;

        # Load configuration files for the default server block.
        include /etc/nginx/default.d/*.conf;

        error_page 404 /404.html;
        location = /404.html {
        }

        error_page 500 502 503 504 /50x.html;
        location = /50x.html {
        }
    }
``` 
```powershell
[tp2_linux@localhost ~]$ cat /etc/nginx/nginx.conf | grep include
include /usr/share/nginx/modules/*.conf;
    include             /etc/nginx/mime.types;
    include /etc/nginx/conf.d/*.conf;
        include /etc/nginx/default.d/*.conf;
```
## 3. Déployer un nouveau site web

🌞 **Créer un site web**

```powershell
[tp2_linux@localhost tp2_linux]$ pwd
/var/www/tp2_linux
[tp2_linux@localhost tp2_linux]$ sudo touch index.html
[tp2_linux@localhost tp2_linux]$ sudo nano index.html
<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>MEOW</title>
  <link rel="stylesheet" href="style.css">
  <script src="script.js"></script>
</head>
<body>
  <h1>MEOW mon premier serveur web</h1>ct
</body>
</html>

```

🌞 **Adapter la conf NGINX**

```powershell
[tp2_linux@localhost conf.d]$ sudo nano page.conf
server {
  # le port choisi devra être obtenu avec un 'echo $RANDOM' là encore
  listen 12528;

  root /var/www/tp2_linux;
}
```
```powershell
[tp2_linux@localhost nginx]$ sudo rm nginx.conf.default
[tp2_linux@localhost nginx]$ sudo systemctl restart nginx
[tp2_linux@localhost nginx]$ sudo firewall-cmd --add-port=12528/tcp --permanent
success
```

🌞 **Visitez votre super site web**
```bash
Bayle@Ynov-Matheo MINGW64 ~ (master)
$
% Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   158  100   158    0     0  11550      0 --:--:-- --:--:-- --:--:-- 12153<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>MEOW</title>
</head>
<body>
  <h1>MEOW mon premier serveur web</h1>
</body>
</html>
```

# III. Your own services


🌞 **Afficher le fichier de service SSH**

```powershell
[tp2_linux@localhost ~]$ cat /usr/lib/systemd/system/sshd.service | grep ExecStart=
ExecStart=/usr/sbin/sshd -D $OPTIONS
```

🌞 **Afficher le fichier de service NGINX**

```powershell
[tp2_linux@localhost ~]$ cat /usr/lib/systemd/system/nginx.service | grep ExecStart=
ExecStart=/usr/sbin/nginx
```

## 3. Création de service

🌞 **Créez le fichier `/etc/systemd/system/tp2_nc.service`**

```
[tp2_linux@localhost ~]$ cat /etc/systemd/system/tp2_nc.service
[Unit]
Description=Super netcat tout fou

[Service]
ExecStart=/usr/bin/nc -l 26002
```

> Vous remplacerez `<PORT>` par un numéro de port random obtenu avec la même méthode que précédemment.

🌞 **Indiquer au système qu'on a modifié les fichiers de service**
```powershell
[tp2_linux@localhost ~]$ sudo systemctl daemon-reload
```
🌞 **Démarrer notre service de ouf**

```powershell
[tp2_linux@localhost ~]$ sudo systemctl start tp2_nc
```

🌞 **Vérifier que ça fonctionne**

```powershell
[tp2_linux@localhost ~]$ sudo systemctl status tp2_nc
● tp2_nc.service - Super netcat tout fou
     Loaded: loaded (/etc/systemd/system/tp2_nc.service; static)
     Active: active (running) since Thu 2022-12-08 23:17:16 CET; 1min 17s ago
   Main PID: 1306 (nc)
      Tasks: 1 (limit: 11116)
     Memory: 1.1M
        CPU: 12ms
     CGroup: /system.slice/tp2_nc.service
             └─1306 /usr/bin/nc -l 666

Dec 08 23:17:16 localhost.localdomain systemd[1]: Started Super netcat tout fou.
```

```powershell
[tp2_linux@localhost ~]$ ss -laptn | grep 26002
LISTEN 0      10           0.0.0.0:26002      0.0.0.0:*
LISTEN 0      10              [::]:26002         [::]:*
```

🌞 **Les logs de votre service**

```
sudo journalctl -xe -u tp2_nc | grep start
 A start job for unit tp2_nc.service has finished successfully.

```
```
[tp2_linux@localhost ~]$ sudo journalctl -xe -u tp2_nc | grep "cc"
Dec 08 23:27:53 tp2_linux nc[2518]: cc

```
```
sudo journalctl -xe -u tp2_nc | grep exit
Dec 08 23:29:41 tp2_linux systemd[1]: tp2_nc.service: Failed with result 'exit-code'.

```




🌞 **Affiner la définition du service**

```powershell
[tp2_linux@localhost ~]$ sudo systemctl daemon-reload
```
```powershell
Dec 08 23:35:56 tp2_linux systemd[1]: tp2_nc.service: Failed with result 'exit-code'.
░░ Subject: Unit failed
░░ Defined-By: systemd
░░ Support: https://access.redhat.com/support
░░
░░ The unit tp2_nc.service has entered the 'failed' state with result 'exit-code'.
Dec 08 23:35:56 tp2_linux systemd[1]: tp2_nc.service: Scheduled restart job, restart counter is at 2.
░░ Subject: Automatic restarting of a unit has been scheduled
░░ Defined-By: systemd
░░ Support: https://access.redhat.com/support
░░
░░ Automatic restarting of the unit tp2_nc.service has been scheduled, as the result for
░░ the configured Restart= setting for the unit

```
