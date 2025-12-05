
SET NAMES 'utf8mb4';
SET CHARACTER SET utf8mb4;

CREATE DATABASE IF NOT EXISTS sapienta_db;
USE sapienta_db;

CREATE TABLE refresh_token (
	jwt_id VARCHAR(255) PRIMARY KEY,
	user_sub VARCHAR(255) NOT NULL,
	token_hash VARCHAR(255) NOT NULL,
	expires_at BIGINT NOT NULL,
	created_at INT DEFAULT CURRENT_TIMESTAMP,
	is_revoked TINYINT(1) DEFAULT 0
);


-- Table: UTILISATEUR
CREATE TABLE utilisateur (
    utilisateur_id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    mot_de_passe VARCHAR(255) NOT NULL,
    status_actif BOOLEAN NOT NULL DEFAULT TRUE,
    type_compte SET('MENTOR', 'ADMIN', 'USER') NOT NULL
);

-- Table: CATÉGORIE
CREATE TABLE categorie (
    categorie_id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL
);

-- Table: RESSOURCE
CREATE TABLE ressource (
    ressource_id INT AUTO_INCREMENT PRIMARY KEY,
    titre VARCHAR(200) NOT NULL,
    description VARCHAR(500),
    url_ressource VARCHAR(500) NOT NULL,
    visibilite BOOLEAN NOT NULL DEFAULT TRUE,
    categorie_id INT,
    auteur_id INT,
    FOREIGN KEY (categorie_id) REFERENCES categorie(categorie_id) ON DELETE SET NULL,
    FOREIGN KEY (auteur_id) REFERENCES utilisateur(utilisateur_id) ON DELETE SET NULL
);

-- Table: COLLECTION
CREATE TABLE collection (
    collection_id INT AUTO_INCREMENT PRIMARY KEY,
    titre VARCHAR(200) NOT NULL,
    description VARCHAR(500),
    visibilite BOOLEAN NOT NULL DEFAULT TRUE,
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

