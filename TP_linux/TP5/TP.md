# Partie 1 : Mise en place et maîtrise du serveur Web

## 1. Installation

🌞 **Installer le serveur Apache**

- paquet `httpd`

````
[matheo@tp5linux ~]$ sudo dnf install httpd
````

🌞 **Démarrer le service Apache**

- démarrez-le
````
[matheo@tp5linux conf]$ sudo systemctl start httpd
````
````
[matheo@tp5linux conf]$ sudo systemctl status httpd
● httpd.service - The Apache HTTP Server
     Loaded: loaded (/usr/lib/systemd/system/httpd.service; disabled; vendor preset: disabled)
     Active: active (running) since Fri 2023-01-06 13:06:32 CET; 7s ago
````

 - faites en sorte qu'Apache démarre automatiquement au démarrage de la machine
````
[matheo@tp5linux conf]$ sudo systemctl enable httpd
Created symlink /etc/systemd/system/multi-user.target.wants/httpd.service → /usr/lib/systemd/system/httpd.service.
````

 - ouvrez le port firewall nécessaire
````
[matheo@tp5linux conf]$ sudo firewall-cmd --add-port=80/tcp --permanent
[sudo] password for matheo:
success
````

 - utiliser une commande `ss` pour savoir sur quel port tourne actuellement Apache
````
  [matheo@tp5linux conf]$ sudo ss -lapnt | grep httpd
LISTEN 0      511                *:80              *:*    users:(("httpd",pid=1388,fd=4),("httpd",pid=1387,fd=4),("httpd",pid=1386,fd=4),("httpd",pid=1384,fd=4))
````

🌞 **TEST**

- vérifier que le service est démarré
````
[matheo@tp5linux conf]$ sudo journalctl -xe -u httpd

Jan 06 13:06:32 web.linux.tp5 httpd[1384]: Server configured, listening on: port 80
````
- vérifier qu'il est configuré pour démarrer automatiquement
````
[matheo@tp5linux conf]$ sudo systemctl status httpd | grep enabled
     Loaded: loaded (/usr/lib/systemd/system/httpd.service; enabled; vendor preset: disabled)
````
- vérifier avec une commande `curl localhost` que vous joignez votre serveur web localement
````
[matheo@tp5linux conf]$ curl localhost | head -n 5
<!doctype html>
<html>
  <head>
    <meta charset='utf-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1'>
````

- vérifier depuis votre PC que vous accéder à la page par défaut
  - avec une commande `curl` depuis un terminal de votre PC (je veux ça dans le compte-rendu, pas de screen)
````
Bayle@Ynov-Matheo MINGW64 ~ (master)
$ curl 10.105.1.11
<!doctype html>
<html>
  <head>
    <meta charset='utf-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <title>HTTP Server Test Page powered by: Rocky Linux</title>
    <style type="text/css">
````

## 2. Avancer vers la maîtrise du service

🌞 **Le service Apache...**

- affichez le contenu du fichier `httpd.service` qui contient la définition du service Apache
````
[matheo@tp5linux system]$ cat /usr/lib/systemd/system/httpd.service
````

🌞 **Déterminer sous quel utilisateur tourne le processus Apache**

- mettez en évidence la ligne dans le fichier de conf principal d'Apache (`httpd.conf`) qui définit quel user est utilisé
````
[matheo@tp5linux conf]$ cat httpd.conf | grep -i user
User apache
````

- utilisez la commande `ps -ef` pour visualiser les processus en cours d'exécution et confirmer que apache tourne bien sous l'utilisateur mentionné dans le fichier de conf
````
[matheo@tp5linux conf]$ ps -ef | grep apache
apache      1385    1384  0 13:06 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND
apache      1386    1384  0 13:06 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND
apache      1387    1384  0 13:06 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND
apache      1388    1384  0 13:06 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND
apache      1722    1384  0 13:32 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND
matheo      1836     863  0 13:43 pts/0    00:00:00 grep --color=auto apache
````

- la page d'accueil d'Apache se trouve dans `/usr/share/testpage/`
  - vérifiez avec un `ls -al` que tout son contenu est **accessible en lecture** à l'utilisateur mentionné dans le fichier de conf
````
[matheo@tp5linux share]$ ls -la | grep testpage
drwxr-xr-x.   2 root root    06 Jan 01 16:49 testpage
````

🌞 **Changer l'utilisateur utilisé par Apache**

- créez un nouvel utilisateur
  - pour les options de création, inspirez-vous de l'utilisateur Apache existant
````
[matheo@tp5linux etc]$ sudo adduser user1 -d /usr/share/httpd -s /sbin/nologin
[sudo] password for matheo:
adduser: warning: the home directory /usr/share/httpd already exists.
adduser: Not copying any file from skel directory into it.
Creating mailbox file: File exists
````

````
[matheo@tp5linux httpd]$ cat /etc/passwd | grep user1
user1:x:1001:1001::/usr/share/httpd:/sbin/nologin
````

- modifiez la configuration d'Apache pour qu'il utilise ce nouvel utilisateur
````
[matheo@tp5linux conf]$ cat httpd.conf | grep user1
User user1
````

- utilisez une commande `ps` pour vérifier que le changement a pris effet
````
[matheo@tp5linux conf]$ ps -ef | grep httpd
root        1931       1  0 17:34 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND
user1       1932    1931  0 17:34 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND
user1       1933    1931  0 17:34 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND
user1       1934    1931  0 17:34 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND
user1       1935    1931  0 17:34 ?        00:00:00 /usr/sbin/httpd -DFOREGROUND
````

🌞 **Faites en sorte que Apache tourne sur un autre port**

- modifiez la configuration d'Apache pour lui demander d'écouter sur un autre port de votre choix
````
[matheo@tp5linux conf]$ cat httpd.conf | grep -i listen
Listen 12345
````
- prouvez avec une commande `ss` que Apache tourne bien sur le nouveau port choisi
````
[matheo@tp5linux conf]$ sudo ss -laptn | grep httpd
LISTEN 0      511                *:12345            *:*    users:(("httpd",pid=2404,fd=4),("httpd",pid=2403,fd=4),("httpd",pid=2402,fd=4),("httpd",pid=2399,fd=4))
````

- vérifiez avec `curl` en local que vous pouvez joindre Apache sur le nouveau port
````
[matheo@tp5linux conf]$ curl localhost:12345 | head -5
<!doctype html>
<html>
  <head>
    <meta charset='utf-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1'>
````

- vérifiez avec votre navigateur que vous pouvez joindre le serveur sur le nouveau port
````
Bayle@Ynov-Matheo MINGW64 ~ (master)
$curl 10.105.1.11:12345 | head -5
<!doctype html>
<html>
  <head>
    <meta charset='utf-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1'>
````
# Partie 2 : Mise en place et maîtrise du serveur de base de données

🌞 **Install de MariaDB sur `db.tp5.linux`**

- je veux dans le rendu **toutes** les commandes réalisées
````
[matheo@db ~]$ sudo dnf install mariadb-server
````
````
[matheo@db ~]$ sudo mysql_secure_installation
````

- faites en sorte que le service de base de données démarre quand la machine s'allume
````
[matheo@db ~]$ sudo systemctl enable mariadb
Created symlink /etc/systemd/system/mysql.service → /usr/lib/systemd/system/mariadb.service.
Created symlink /etc/systemd/system/mysqld.service → /usr/lib/systemd/system/mariadb.service.
Created symlink /etc/systemd/system/multi-user.target.wants/mariadb.service → /usr/lib/systemd/system/mariadb.service.
````

````
[matheo@db ~]$ sudo systemctl start mariadb
````

🌞 **Port utilisé par MariaDB**

- vous repérerez le port utilisé par MariaDB avec une commande `ss` exécutée sur `db.tp5.linux`
````
[matheo@db ~]$ sudo ss -altnp | grep mariadb
LISTEN 0      80                 *:3306            *:*    users:(("mariadbd",pid=3799,fd=19))
````
- il sera nécessaire de l'ouvrir dans le firewall
````
[matheo@db ~]$ sudo firewall-cmd --add-port=3306/tcp --permanent
success
````

🌞 **Processus liés à MariaDB**

- repérez les processus lancés lorsque vous lancez le service MariaDB
- utilisz une commande `ps`
````
[matheo@db ~]$ ps -ef | grep mariadb
mysql       3799       1  0 14:28 ?        00:00:00 /usr/libexec/mariadbd --basedir=/usr
matheo     4084     877  0 15:04 pts/0    00:00:00 grep --color=auto mariadb
````

# Partie 3 : Configuration et mise en place de NextCloud

## 1. Base de données

🌞 **Préparation de la base pour NextCloud**

- une fois en place, il va falloir préparer une base de données pour NextCloud :
  - connectez-vous à la base de données à l'aide de la commande `sudo mysql -u root -p`
  - exécutez les commandes SQL suivantes :

````sql
MariaDB [(none)]> CREATE USER 'nextcloud'@'10.105.1.11' IDENTIFIED BY 'matheo';
Query OK, 0 rows affected (0.003 sec)
````
````sql
MariaDB [(none)]> CREATE DATABASE IF NOT EXISTS nextcloud CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
Query OK, 1 row affected (0.000 sec)
````
````sql
MariaDB [(none)]> GRANT ALL PRIVILEGES ON nextcloud.* TO 'nextcloud'@'10.105.1.11';
Query OK, 0 rows affected (0.003 sec)
````
````sql
MariaDB [(none)]> FLUSH PRIVILEGES;
Query OK, 0 rows affected (0.000 sec)
````

🌞 **Exploration de la base de données**

- afin de tester le bon fonctionnement de la base de données, vous allez essayer de vous connecter
  - depuis la machine `web.tp5.linux` vers l'IP de `db.tp5.linux`
  - utilisez la commande `mysql` pour vous connecter à une base de données depuis la ligne de commande
````
[matheo@web ~]$ mysql -u nextcloud -h 10.105.1.12 -p
Enter password:
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 23
````

    - si vous ne l'avez pas, installez-là
````
[matheo@web ~]$ sudo dnf install mysql-8.0.30-3.el9_0.x86_64
````
- **donc vous devez effectuer une commande `mysql` sur `web.tp5.linux`**
- une fois connecté à la base, utilisez les commandes SQL fournies ci-dessous pour explorer la base

````sql
mysql> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| nextcloud          |
+--------------------+
2 rows in set (0.00 sec)
````

🌞 **Trouver une commande SQL qui permet de lister tous les utilisateurs de la base de données**

````sql
MariaDB [(none)]> SELECT User FROM mysql.user;
+-------------+
| User        |
+-------------+
| nextcloud   |
| mariadb.sys |
| mysql       |
| root        |
+-------------+
4 rows in set (0.001 sec)
````

## 2. Serveur Web et NextCloud

🌞 **Install de PHP**

````
[matheo@web conf]$ sudo dnf config-manager --set-enabled crb

[matheo@web conf]$ sudo dnf install dnf-utils http://rpms.remirepo.net/enterprise/remi-release-9.rpm -y

[matheo@web conf]$ dnf module list php

[matheo@web conf]$ sudo dnf module enable php:remi-8.1 -y

[matheo@web conf]$ sudo dnf install -y php81-php
```

🌞 **Install de tous les modules PHP nécessaires pour NextCloud**

```
[matheo@web conf]$ sudo dnf install -y libxml2 openssl php81-php php81-php-ctype php81-php-curl php81-php-gd php81-php-iconv php81-php-json php81-php-libxml php81-php-mbstring php81-php-openssl php81-php-posix php81-php-session php81-php-xml php81-php-zip php81-php-zlib php81-php-pdo php81-php-mysqlnd php81-php-intl php81-php-bcmath php81-php-gmp
```

🌞 **Récupérer NextCloud**

- récupérer le fichier suivant avec une commande `curl` ou `wget` ````
[matheo@web www]$ sudo curl https://download.nextcloud.com/server/prereleases/nextcloud-25.0.0rc3.zip -O
````
````
[matheo@web www]$ ls /var/www/tp5_nextcloud/
3rdparty  config       core      index.html  occ           ocs-provider  resources   themes
apps      console.php  cron.php  index.php   ocm-provider  public.php    robots.txt  updater
AUTHORS   COPYING      dist      lib         ocs           remote.php    status.php  version.php
````

- **assurez-vous que le dossier `/var/www/tp5_nextcloud/` et tout son contenu appartient à l'utilisateur qui exécute le service Apache**
  - utilisez une commande `chown` si nécessaire
````
[matheo@web tp5_nextcloud]$ sudo chown apache:apache /var/www/tp5_nextcloud/ -R
````

🌞 **Adapter la configuration d'Apache**

````apache
[matheo@web conf]$ sudo cat httpd.conf | tail -n 18
IncludeOptional conf.d/*.conf

<VirtualHost *:80>
  # on indique le chemin de notre webroot
  DocumentRoot /var/www/tp5_nextcloud/
  # on précise le nom que saisissent les clients pour accéder au service
  ServerName  web.tp5.linux

  # on définit des règles d'accès sur notre webroot
  <Directory /var/www/tp5_nextcloud/>
    Require all granted
    AllowOverride All
    Options FollowSymLinks MultiViews
    <IfModule mod_dav.c>
      Dav off
    </IfModule>
  </Directory>
</VirtualHost>
````

🌞 **Redémarrer le service Apache** pour qu'il prenne en compte le nouveau fichier de conf

````
[matheo@web conf]$ sudo systemctl restart httpd
````

🌞 **Exploration de la base de données**

```sql
mysql> SELECT Count(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE';
+----------+
| Count(*) |
+----------+
|       95 |
+----------+
1 row in set (0.00 sec)
```
