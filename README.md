# Candidature Auto

Petit outil Python qui envoie une candidature spontanée personnalisée en quelques secondes.

## Le problème

Pendant ma recherche d'emploi, chaque candidature spontanée prenait plusieurs minutes : trouver l'adresse mail du recruteur, adapter le message, joindre le CV, vérifier qu'on ne s'est pas trompé de nom. Sur des dizaines d'entreprises, ce temps s'additionne vite.

## La solution

Une petite fenêtre où l'on saisit le prénom, le nom et l'entreprise du recruteur. Le script :

1. **devine l'adresse mail** à partir du format utilisé par l'entreprise (`prenom.nom@entreprise.com`, `pnom@entreprise.com`…), stocké dans `entreprises.xlsx` (100 entreprises) ;
2. **rédige le mail** à partir d'un modèle, avec la civilité, le nom et l'entreprise ;
3. **affiche un récapitulatif** (destinataire, objet, message) et attend une confirmation ;
4. **envoie le mail** avec le CV en pièce jointe.

Le nom des recruteurs est normalisé avant de construire l'adresse : `Éric Lefèvre` chez AXA devient `eric.lefevre@axa.com`.

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
- À utiliser avec modération : un mail ciblé et personnalisé, pas un envoi de masse.

## Tests

```bash
pip install pytest
pytest
```

## Stack

Python, pandas, Tkinter, smtplib, python-dotenv.
