# mycompiler/graphing.py
from graphviz import Digraph
class Automate:
    def __init__(self):
        self.states = set()
        self.start_state = None
        self.final_states = set()
        self.transitions = {}


def grammaire_vers_automate(regle, axiome):
    auto = Automate()
    auto.start_state = axiome

    # Ajouter les états
    for A in regle:
        auto.states.add(A)

    # Ajouter un état final unique F
    auto.states.add("F")
    auto.final_states.add("F")

    for A, productions in regle.items():
        for prod in productions:

            if prod in ("epsilon", "ε"):
                # A est un état final
                auto.final_states.add(A)
                continue
            
            if len(prod) == 1:
                # A -> a
                sym = prod
                auto.transitions.setdefault(A, {})
                auto.transitions[A][sym] = "F"

            elif len(prod) == 2:
                # A -> aB
                sym = prod[0]
                B = prod[1]
                auto.transitions.setdefault(A, {})
                auto.transitions[A][sym] = B

    return auto


def draw_nfa(nfa, filename="nfa"):
    dot = Digraph(comment="NFA", format="png")
    dot.attr(rankdir='LR')
    # nodes
    for s in nfa.states:
        shape = 'doublecircle' if s in nfa.final_states else 'circle'
        dot.node(s, shape=shape)
    # start arrow
    dot.node('__start__', shape='point')
    dot.edge('__start__', nfa.start_state, label='')
    # transitions
    for s in nfa.states:
        for sym, dests in nfa.transitions.get(s, {}).items():
            for d in sorted(dests):
                dot.edge(s, d, label=sym)
    path = dot.render(filename, format="png", cleanup=True)
    print(path)
    return path

    
def draw_dfa(dfa, filename="automate"):
    """Génère un PNG à partir d'un objet automate sans utiliser le wrapper fragile."""
    
    # 1. Construction manuelle du code DOT (le langage de Graphviz)
    dot_source = 'digraph DFA {\n    rankdir=LR;\n    node [fontname="Arial"];\n'
    
    # Définition des états (cercles doubles pour les finaux)
    for s in dfa.states:
        shape = 'doublecircle' if s in dfa.final_states else 'circle'
        dot_source += f'    "{s}" [shape={shape}];\n'
    
    # Flèche d'entrée
    dot_source += '    __start [shape=point, style=invis];\n'
    dot_source += f'    __start -> "{dfa.start_state}";\n'
    
    # Transitions
    for s, trans in dfa.transitions.items():
        for sym, tgt in trans.items():
            dot_source += f'    "{s}" -> "{tgt}" [label="{sym}"];\n'
    
    dot_source += '}'

    # 2. Gestion des chemins de fichiers
    # On force l'écriture dans le dossier courant de l'utilisateur
    gv_file = os.path.abspath(f"{filename}.gv")
    png_file = os.path.abspath(f"{filename}.png")

    # Écriture du fichier source .gv
    with open(gv_file, 'w', encoding='utf-8') as f:
        f.write(dot_source)

    # 3. Appel de l'exécutable DOT
    try:
        # On cherche l'exécutable 'dot.exe'
        # Si on est dans l'EXE, le PATH configuré dans interface.py aidera à le trouver
        executable = "dot"
        
        # Commande : dot -Tpng fichier.gv -o fichier.png
        result = subprocess.run(
            [executable, '-Tpng', gv_file, '-o', png_file],
            capture_output=True,
            text=True,
            shell=True
        )

        if os.path.exists(png_file):
            # Optionnel : supprimer le fichier .gv après génération
            try: os.remove(gv_file) 
            except: pass
            return png_file
        else:
            print(f"Erreur Graphviz STDERR: {result.stderr}")
            return None

    except Exception as e:
        print(f"Erreur d'exécution subprocess: {e}")
        return None
