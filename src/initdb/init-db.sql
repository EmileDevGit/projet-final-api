
SET NAMES 'utf8mb4';
SET CHARACTER SET utf8mb4;

CREATE DATABASE IF NOT EXISTS sapienta_db;
USE sapienta_db;


-- Table: UTILISATEUR
CREATE TABLE utilisateur (
    utilisateur_id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prénom VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    mot_de_passe VARCHAR(255) NOT NULL,
    status_actif BOOLEAN NOT NULL DEFAULT TRUE,
    type_compte ENUM('MENTOR', 'ADMIN', 'ÉTUDIANT') NOT NULL
);

-- Table: CATÉGORIE
CREATE TABLE categorie (
    catégorie_id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL
);

-- Table: RESSOURCE
CREATE TABLE ressource (
    ressource_id INT AUTO_INCREMENT PRIMARY KEY,
    titre VARCHAR(200) NOT NULL,
    description VARCHAR(500),
    url_ressource VARCHAR(500) NOT NULL,
    visibilité BOOLEAN NOT NULL DEFAULT TRUE,
    catégorie_id INT,
    auteur_id INT,
    FOREIGN KEY (catégorie_id) REFERENCES categorie(catégorie_id) ON DELETE SET NULL,
    FOREIGN KEY (auteur_id) REFERENCES utilisateur(utilisateur_id) ON DELETE SET NULL
);

-- Table: COLLECTION
CREATE TABLE collection (
    collection_id INT AUTO_INCREMENT PRIMARY KEY,
    titre VARCHAR(200) NOT NULL,
    description VARCHAR(500),
    visibilité BOOLEAN NOT NULL DEFAULT TRUE,
    auteur_id INT,
    FOREIGN KEY (auteur_id) REFERENCES utilisateur(utilisateur_id) ON DELETE SET NULL
);

-- Table: COLLECTION_RESSOURCE
CREATE TABLE collection_ressource (
    collection_id INT,
    ressource_id INT,
    PRIMARY KEY (collection_id, ressource_id),
    FOREIGN KEY (collection_id) REFERENCES collection(collection_id) ON DELETE CASCADE,
    FOREIGN KEY (ressource_id) REFERENCES ressource(ressource_id) ON DELETE CASCADE
);

