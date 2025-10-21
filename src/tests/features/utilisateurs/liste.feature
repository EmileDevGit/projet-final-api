Feature: /utilisateurs - Liste des utilisateurs

	Scenario: L'administrateur accède à la liste complète 
		Given un administrateur existant
		When je fais un fetch sur l'endpoint /utilisateurs
		Then je recoit un code 200
		Then je recoit un tableau json


