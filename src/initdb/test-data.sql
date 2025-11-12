SET NAMES 'utf8mb4';
SET CHARACTER SET utf8mb4;

USE sapienta_db;

-- Insertion des utilisateurs
INSERT INTO utilisateur (nom, prenom, email, mot_de_passe, status_actif, type_compte) VALUES
('Dupont', 'Alice', 'alice.dupont@example.com', 'hashed_password1', TRUE, 'MENTOR'),
('Martin', 'Bob', 'bob.martin@example.com', 'hashed_password2', TRUE, 'ADMIN'),
('Durand', 'Charlie', 'charlie.durand@example.com', 'hashed_password3', TRUE, 'USER'),
('Lemoine', 'David', 'david.lemoine@example.com', 'hashed_password4', TRUE, 'USER'),
('Moreau', 'Émilie', 'emilie.moreau@example.com', 'hashed_password5', FALSE, 'MENTOR'),
('Blanc', 'Claire', 'claire.blanc@example.com', 'hashed_password6', TRUE, 'MENTOR'),
('Petit', 'Éric', 'eric.petit@example.com', 'hashed_password7', TRUE, 'ADMIN'),
('Bertrand', 'Sophie', 'sophie.bertrand@example.com', 'hashed_password8', TRUE, 'USER');

-- Insertion des catégories
INSERT INTO categorie (nom) VALUES
('Programmation'),
('Mathématiques'),
('Physique'),
('Littérature'),
('Histoire'),
('Design');

-- Insertion des ressources

-- Ressources auteur MENTOR (Alice Dupont)
INSERT INTO ressource (titre, description, url_ressource, visibilite, categorie_id, auteur_id) VALUES
('Tutoriel Python', 'Introduction à Python', 'http://exemple.com/python', TRUE, 1, 1),
('Algèbre Linéaire', 'Cours d’algèbre linéaire', 'http://exemple.com/algebre', TRUE, 2, 1);

-- Ressources auteur ADMIN (Bob Martin)
INSERT INTO ressource (titre, description, url_ressource, visibilite, categorie_id, auteur_id) VALUES
('Physique Quantique', 'Concepts de base', 'http://exemple.com/physique', FALSE, 3, 2),
('Analyse Littéraire', 'Techniques d’analyse', 'http://exemple.com/litterature', TRUE, 4, 2);

-- Ressources auteur ÉTUDIANT (Charlie Durand, id=3)
INSERT INTO ressource (titre, description, url_ressource, visibilite, categorie_id, auteur_id) VALUES
('Projet Python Étudiant', 'Script pour projet', 'http://exemple.com/projet_py', FALSE, 1, 3),
('Notes de mathématiques', 'Résumé du cours', 'http://exemple.com/notes_math', FALSE, 2, 3);

-- Ressources auteur ÉTUDIANT (David Lemoine, id=4)
INSERT INTO ressource (titre, description, url_ressource, visibilite, categorie_id, auteur_id) VALUES
('Expériences Physiques', 'Rapport de laboratoire', 'http://exemple.com/phys_exp', FALSE, 3, 4);

-- Ressources auteur MENTOR inactif (Émilie Moreau, id=5)
INSERT INTO ressource (titre, description, url_ressource, visibilite, categorie_id, auteur_id) VALUES
('Cours avancé de Python', 'Pour développeurs', 'http://exemple.com/py_avance', TRUE, 1, 5);

-- Ressources auteur MENTOR (Claire Blanc, id=6)
INSERT INTO ressource (titre, description, url_ressource, visibilite, categorie_id, auteur_id) VALUES
('Histoire de France', 'Résumé chronologique', 'http://exemple.com/histoire_fr', TRUE, 5, 6),
('Design UX', 'Introduction au design centré utilisateur', 'http://exemple.com/design_ux', FALSE, 6, 6);

-- Ressources auteur ADMIN (Éric Petit, id=7)
INSERT INTO ressource (titre, description, url_ressource, visibilite, categorie_id, auteur_id) VALUES
('Équations différentielles', 'Cours complet', 'http://exemple.com/eq_diff', TRUE, 2, 7),
('Figures de style', 'Ressource pour le bac', 'http://exemple.com/styles', FALSE, 4, 7);

-- Ressources auteur ÉTUDIANT (Sophie Bertrand, id=8)
INSERT INTO ressource (titre, description, url_ressource, visibilite, categorie_id, auteur_id) VALUES
('Projet Java Étudiant', 'TP Java', 'http://exemple.com/projet_java', FALSE, 1, 8),
('Exposé Histoire', 'Napoléon Bonaparte', 'http://exemple.com/napoleon', FALSE, 5, 8);

-- Insertion des collections
INSERT INTO collection (titre, description, visibilite, auteur_id) VALUES
('Ressources Python', 'Collection pour apprendre Python', TRUE, 1),
('Cours de physique', 'Cours divers sur la physique', FALSE, 2),
('Culture Générale', 'Ressources variées pour concours', TRUE, 6),
('Maths avancées', 'Ressources avancées en mathématiques', TRUE, 7);

-- Insertion des liens collection_ressource

-- Collection 1: 'Ressources Python' (id=1)
INSERT INTO collection_ressource (collection_id, ressource_id) VALUES
(1, 1), -- Tutoriel Python
(1, 6); -- Cours avancé de Python

-- Collection 2: 'Cours de physique' (id=2)
INSERT INTO collection_ressource (collection_id, ressource_id) VALUES
(2, 3), -- Physique Quantique
(2, 5); -- Expériences Physiques

-- Collection 3: 'Culture Générale' (id=3)
INSERT INTO collection_ressource (collection_id, ressource_id) VALUES
(3, 7), -- Histoire de France
(3, 10); -- Figures de style

-- Collection 4: 'Maths avancées' (id=4)
INSERT INTO collection_ressource (collection_id, ressource_id) VALUES
(4, 8), -- Équations différentielles
(4, 2); -- Algèbre Linéaire

