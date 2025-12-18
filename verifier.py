def appartient_grammaire_reguliere(mot, regles_production, axiome):
    """
    Version optimisée avec mémoïsation pour éviter les calculs redondants
    """
    memo = {}

    
    def deriver(symboles_courants, index):
        cle = (tuple(symboles_courants), index)
        
        if cle in memo:
            return memo[cle]
        
        # Si plus de symboles à dériver et on est à la fin du mot
        if not symboles_courants and index == len(mot):
            memo[cle] = True
            return True
        
        # Si plus de symboles mais il reste du mot, ou vice versa
        if not symboles_courants or index > len(mot):
            memo[cle] = False
            return False
        
        symbole_courant = symboles_courants[0]
        symboles_suivants = symboles_courants[1:]
        
        # Si le symbole courant est un terminal
        if symbole_courant not in regles_production:
            if index < len(mot) and symbole_courant == mot[index]:
                resultat = deriver(symboles_suivants, index + 1)
                memo[cle] = resultat
                return resultat
            else:
                memo[cle] = False
                return False
        
        # Si le symbole courant est une variable
        for production in regles_production[symbole_courant]:
            # Production vide
            if production == 'ε' or production == 'epsilon':
                if deriver(symboles_suivants, index):
                    memo[cle] = True
                    return True
            
            # Production vers un terminal
            elif len(production) == 1 and production not in regles_production:
                if index < len(mot) and production == mot[index]:
                    if deriver(symboles_suivants, index + 1):
                        memo[cle] = True
                        return True
            
            # Production vers terminal + variable
            elif len(production) == 2:
                terminal, variable = production[0], production[1]
                if index < len(mot) and terminal == mot[index]:
                    nouveaux_symboles = [variable] + symboles_suivants
                    if deriver(nouveaux_symboles, index + 1):
                        memo[cle] = True
                        return True
            
            # Production vers une variable seule
            elif len(production) == 1 and production in regles_production:
                nouveaux_symboles = [production] + symboles_suivants
                if deriver(nouveaux_symboles, index):
                    memo[cle] = True
                    return True
        
        memo[cle] = False
        return False
    
    return deriver([axiome], 0)