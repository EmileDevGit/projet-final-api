Feature: Liste des utilisateurs

	Scenario: L'administrateur accède à la liste complète 
		Given un administrateur existant
		When il fais un fetch sur touts les utilisateurs
		Then il recoit un code 200
		Then il recoit un tableau json nommé utilisateurs

	Scenario: L'administrateur accède à la liste des utilisateurs avec un filtre
		Given un administrateur existant
		When il fais un fetch sur les utilisateurs avec le mot-cle marie en parametre
		Then il recoit un code 200
		And il recoit un tableau json nommé utilisateurs
		And les utilisateurs dans le tableau ont la chaîne marie dans leur contenu

	Scenario: Un utilisateur afficher la liste des utilisateurs
		Given un utilisateur existant avec le rôle user
		When il fais un fetch sur les utilisateurs
		Then il recoit un code 200
		And il recoit un tableau json nommé utilisateurs
		And les utilisateurs dans le tableau ont le rôle mentor

