# API de bibliothèque de savoir SapientAPI

## Problématique
La gestion et le partage de ressources pédagogiques peuvent rapidement devenir compliqués lorsqu’on souhaite centraliser son savoir. SapientAPI vise à répondre à ce besoin en offrant une API capable de centraliser, organiser et partager des ressources. Facilitant ainsi la gestion de savoir numérique.


## Description
Cette api permet de déployer une bibliothèque de savoir. Elle comprends différents types de documents ainsi que la gestion des membres et des ressources. Les utilisateurs ont accès à la plateforme afin de consommer les ressources publiées par les mentors, mais peuvent tout de même enregistrer leurs propes notes personelles. Les mentors peuvent gérer la visibilité de leurs ressources.


## Technologies utilisées

| Technologie |  Utilité |
|-------------|----------------|
|![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) | Langage backend |
|![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white) | Framework REST rapide |
|![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white) | Conteneurisation |
|![SQL](https://img.shields.io/badge/SQL-4479A1?style=flat&logo=mysql&logoColor=white) | Base de données |
|![Git](https://img.shields.io/badge/Git-F05032?style=flat&logo=git&logoColor=white) | Gestion de version |
|![Pytest](https://img.shields.io/badge/Pytest-008080?style=flat&logo=pytest&logoColor=white) | Tests unitaires |
|![Gherkin](https://img.shields.io/badge/Gherkin-5C4F3C?style=flat&logo=cucumber&logoColor=white) | Tests comportementaux |
|![Pydantic](https://img.shields.io/badge/Pydantic-0673E6?style=flat&logo=pydantic&logoColor=white) | Validation des données et modèles|



## Authentification et droits d'accès
Le persona cherchant à se connecter à la plateforme devra s'authentifier avec un courriel et un mot de passe, si les informations sont correctes, un token d'authentification sera attribué pour une durée de 90 minutes.

# Matrice des droits d'accès - SapientAPI

| Action | Utilisateur | Mentor | Admin |
|--------|-------------|--------|-------|
| **Ressources** | | | |
| Créer | ✅Privée | ✅Privée - Publiques | ✅  |
| Lire | ✅ Publiques - Propres | ✅ Publiques - Propres | ✅ Toutes |
| Modifier | ✅ Propres | ✅ Propres | ✅ Toutes |
| Supprimer | ✅ Propres | ✅ Propres | ✅ Toutes |
| **Utilisateurs** | | | |
| Créer | ✅ Auto-inscription | ❌ | ✅ |
| Lire | ✅ Propre - Mentor | ✅ Propre - Mentor | ✅ Tous |
| Modifier | ✅ Propre | ✅ Propre | ✅ Tous |
| Supprimer | ✅ Propre | ✅ Propre | ✅ Tous |
| Gérer les rôles | ❌ | ❌ | ✅ |

*Les droits de l'utilisateurs sont limités à sa propre entité

## Récits utilisateurs
[Récits utilisateurs](docs/user-stories/user-stories.md)


## Cas d'utilisations
[Cas d'utilisations](docs/diagrammes/usecases.puml)

## Diagramme de classes UML
[Diagramme de classes](docs/diagrammes/classes.puml)

## Diagramme des composants de l’architecture
[Diagramme des composants de l’architecture](docs/diagrammes/DiagrammeDesComposantsDeArchitecture.png)

## Dépendances
Le déploiement des services demande les dépendances suivantes:
- Docker / Docker-Compose

C'est tout! Les services gèrent eux-même leurs dépendances au sein des conteneurs par les différents fichiers sous `/requirements`

## Installation
Simplement cloner ce dépôt dans un répertoire dédié à l'application sur le serveur de votre choix.

Pour assurer un déploiement fonctionnel, veuillez créer un fichier `.env` à la racine de ce répertoire.
Le fichier `.env.example` est distribué à titre d'exemple afin que vous ayez toutes les variables d'environnement
nécessaires au bon fonctionnement de l'application. Les valeurs qu'il contient devraient être changées afin d'assurer
la sécurité du service.

(Optionnel) Afin de valider l'intégrité du projet, vous pouvez lancer les tests unitaires avec:

`docker compose up sapienta_unit_tests`

Ensuite, déployez simplement l'application avec la commande suivante:

`docker compose up -d sapienta_api`

Docker compose assure un déploiement combiné du serveur de base de données MySQL, du serveur de l'API elle même
ainsi que le serveur d'authentification dédié.

Après quelques minutes, vérifez que vos conteneurs sont bel et bien déployés avec:

`docker ps | grep sapienta`

Pour toutes questions / bug trouvé, veuillez remplir un ticket et il sera évalué par notre équipe.
Vous trouverez ci-dessous la liste des bugs connus ainsi que le ticket associé.

## Bugs connus
- [\[ Ticket #107 \]](https://git.dti.crosemont.quebec/2252359/projetfinalapi/-/issues/107): la création de nouvelles ressources comporte un bug apparant lors de la requêtes de toutes les ressources.

## Contributeurs
- Émile Girard
- Émile Larochelle-Langevin


## Liscence
API de bibliothèque de savoir © 2025 by Émile Girard & Émile Larochelle-Langevin est distribué sous licence CC BY-NC-SA 4.0. 
Pour consulter les détails de la licence, visitez https://creativecommons.org/licenses/by-nc-sa/4.0/

## État du projet et plans futurs
✅ Sprint 1 - Analyse du projet et ébauche du mock de l'API

✅ Sprint 2 - Mise en place structure du projet et de la couche Interface

✅ Sprint 3 - Implémentation des routes utilisateurs

✅ Sprint 4 - Implémentation du service d'authentification

✅ Déploiement v0.9 - Cleanup du projet et présentation finale
