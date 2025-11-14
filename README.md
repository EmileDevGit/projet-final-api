# API de bibliothèque de savoir SapientAPI

## Problématique
La gestion et le partage de ressources pédagogiques peuvent rapidement devenir compliqués lorsqu’on souhaite centraliser son savoir. SapientAPI vise à répondre à ce besoin en offrant une API capable de centraliser, organiser et partager des ressources. Facilitant ainsi la gestion de savoir numérique.


## Description
Cette api permet de déployer une bibliothèque de savoir. Elle comprends des collections, différents types de documents ainsi que la gestion des membres et des ressources. Les utilisateurs ont accès à la plateforme afin de consommer les ressources publiées par les mentors, mais peuvent tout de même enregistrer leurs propes notes personelles. Les mentors peuvent gérer la visibilité de leurs ressources et organiser celles-ci en collections.


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
| **Catégories** | | | |
| Créer | ❌ | ❌ | ✅ |
| Lire | ✅ | ✅ | ✅ |
| Modifier | ❌ | ❌ | ✅ |
| Supprimer | ❌ | ❌ | ✅ |
| **Collections** | | | |
| Créer | ✅ Propres - Privées | ✅ Propres - Publiques | ✅ Toutes |
| Lire | ✅ Publiques - Propres | ✅ Publiques - Propres | ✅ Toutes |
| Modifier | ✅ Propres | ✅ Propes | ✅ Toutes |
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

## Installation
Le projet est déployé à travers Docker compose. Celui-ci automatique le déploiement de l'API, les tests unitaires ainsi qu'une base de données MySQL. À noter qu'en date d'aujourd'hui, le projet n'est seulement compatible qu'avec une base de données relationelle MySQL.

## Contributeurs
- Émile Girard
- Émile Larochelle-Langevin


## Liscence
API de bibliothèque de savoir © 2025 by Émile Girard & Émile Larochelle-Langevin est distribué sous licence CC BY-NC-SA 4.0. 
Pour consulter les détails de la licence, visitez https://creativecommons.org/licenses/by-nc-sa/4.0/

## État du projet et plans futurs
Sprint 1 - Analyse du projet et ébauche du mock de l'API

Sprint 2 - Mise en place structure du projet et de la couche Interface

Sprint 3 - Implémentation des routes utilisateurs
