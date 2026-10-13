# Candidature Auto

Petit outil Python pour envoyer un premier message de prise de contact à un recruteur, en quelques secondes.

## Le problème

Pendant ma recherche d'emploi, je voulais me faire connaître d'un grand nombre d'entreprises, sans y passer des heures. Le frein n'était pas le message lui-même mais tout ce qu'il y a autour : retrouver l'adresse du bon interlocuteur, adapter les salutations, joindre le CV, vérifier qu'on ne s'est pas trompé de nom.

## L'idée

Ce mail n'a pas vocation à décrocher un poste à lui seul. C'est une **première prise de contact** : un message court qui présente mon profil, avec le CV en pièce jointe. Si la personne est intéressée, l'échange continue, et la suite se fait au cas par cas, de façon personnalisée. L'outil automatise seulement l'étape la plus répétitive, pour garder du temps pour les conversations qui en valent la peine.

## Comment ça marche

Une petite fenêtre où l'on saisit le prénom, le nom et l'entreprise de l'interlocuteur. Le script :

1. **retrouve l'adresse mail** à partir du format utilisé par l'entreprise (`prenom.nom@entreprise.com`, `pnom@entreprise.com`…), stocké dans `entreprises.xlsx` (100 entreprises) ;
2. **rédige le message** à partir d'un modèle, avec la civilité, le nom et l'entreprise ;
3. **affiche un récapitulatif** (destinataire, objet, message) et attend une confirmation ;
4. **envoie le mail** avec le CV en pièce jointe.

Le nom de l'interlocuteur est normalisé avant de construire l'adresse : `Éric Lefèvre` chez AXA devient `eric.lefevre@axa.com`.

## Utilisation

```bash
pip install -r requirements.txt
cp .env.example .env      # puis remplis .env avec ton adresse, ton mot de passe d'application et le chemin de ton CV
python candidature_auto.py
```

- Pour ajouter une entreprise : une ligne dans `entreprises.xlsx`, avec son nom et son format d'adresse.
- Pour changer le message : modifie `modele_mail.txt` (la première ligne est l'objet).

## Sécurité

Aucun identifiant n'est écrit dans le code. L'adresse et le mot de passe sont lus depuis un fichier `.env` local, exclu du dépôt par le `.gitignore`. Avec Gmail, il faut utiliser un [mot de passe d'application](https://myaccount.google.com/apppasswords) plutôt que le mot de passe du compte.

## Limites

- Le format d'adresse est une déduction : si l'entreprise utilise une exception pour certains salariés, le mail n'arrivera pas.
- Un message court reste une porte d'entrée : il ouvre la conversation, il ne la remplace pas.
- Chaque envoi est confirmé à la main : l'outil n'envoie jamais en masse sans relecture.

## Tests

```bash
pip install pytest
pytest
```

## Stack

Python, pandas, Tkinter, smtplib, python-dotenv.
