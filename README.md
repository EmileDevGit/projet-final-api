# API de bibliothèque de savoir SapientAPI

## Description
Cette api permet de déployer une bibliothèque de savoir. Elle comprends des collections, différents types de documents ainsi que la gestion des membres et des ressources. Les utilisateurs ont accès à la plateforme afin de consommer les ressources publiées par les mentors, mais peuvent tout de même enregistrer leurs propes notes personelles. Les mentors peuvent gérer la visibilité de leurs ressources et organiser celles-ci en collections.


## Authentification et droits d'accès
Le persona cherchant à se connecter à la plateforme devra s'authentifier avec un courriel et un mot de passe, si les informations sont correctes, un token d'authentification sera attribué pour une durée de 90 minutes.

Le tableau suivant montre les droits d'accès de bases en prenant acquis une session valide.

| Acteur / Droits | Utilisateur | Mentor | Admin |
| --------------- | ----------- | ------ | ----- |
| CRUD ressources | ✅ *        | ✅     | ✅    |
| CRUD catégories | ❌          | ❌     | ✅    |
| CRUD collections| ✅ *        | ✅     | ✅    |
| CRUD utilisateur| ✅ *        | ❌     | ✅    |

*Les droits de l'utilisateurs sont limités à sa propre entité

## Récits utilisateurs
[Récits utilisateurs](docs/user-stories/user-stories.md)


## Cas d'utilisations
[Cas d'utilisations](docs/diagrammes/usecases.puml)

## Diagramme de classes UML
[Diagramme de classes](docs/diagrammes/classes.puml)

## Installation
À venir!

## Usage
À venir!

## Contributeurs
- Émile Girard
- Émile Larochelle-Langevin


## Liscence
API de bibliothèque de savoir © 2025 by Émile Girard & Émile Larochelle-Langevin est distribué sous licence CC BY-NC-SA 4.0. 
Pour consulter les détails de la licence, visitez https://creativecommons.org/licenses/by-nc-sa/4.0/

## État du projet et plans futurs
Sprint 1 en cours - Analyse du projet et ébauche du mock de l'API
