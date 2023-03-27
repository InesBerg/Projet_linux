### Script pour récupérer le prix dans un fichier csv
```
prix=$(curl -s https://www.tradingsat.com/lvmh-FR0000121014/ | grep '<span class="price">' | sed 's/.*>\([^<]*\)<.*/\1/>
date=$(date +%Y-%m-%d)
heure=$(date +%H:%M)
echo "$date,$heure,$prix" >> /home/ec2-user/projet_linux/prix_lvmh.csv
sed -i 's/€//g' prix_lvmh.csv
```
### Script pour se connecter à la session EC2
```
ssh -i /home/inesbergaut/Projet_linux.pem ec2-user@35.180.31.58
```

### Commande Crontab 
```
Commande crontab
*/5  9-18 * * 1-5 /home/ec2-user/scripts/prix_lvmh.sh
```
