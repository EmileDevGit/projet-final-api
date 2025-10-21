Feature: /utilisateurs - Liste des utilisateurs

	Scenario: L'administrateur accède à la liste complète 
		Given un administrateur existant
		When je fais un fetch sur l'endpoint /utilisateurs
		Then je recoit un code 200
		Then je recoit un tableau json nommé utilisateurs

	Scenario: L'administrateur accède à la liste des utilisateurs avec un filtre
		Given un administrateur existant
		When je fais un fetch sur l'endpoint /utilisateurs?mot-cle=marie
		Then je reçoit un code 200
		And je reçoit un tableau json nommé utilisateurs
		And les utilisateurs dans le tableau ont la chaîne marie dans leurs propriétées

