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

    
import os
import subprocess

def draw_dfa(dfa, filename="dfa"):
    # 1. On crée manuellement le code source DOT
    dot_source = 'digraph DFA {\n    rankdir=LR;\n'
    for s in dfa.states:
        shape = 'doublecircle' if s in dfa.final_states else 'circle'
        dot_source += f'    "{s}" [shape={shape}];\n'
    
    dot_source += '    "__start__" [shape=point];\n'
    dot_source += f'    "__start__" -> "{dfa.start_state}";\n'
    
    for s, trans in dfa.transitions.items():
        for sym, tgt in trans.items():
            dot_source += f'    "{s}" -> "{tgt}" [label="{sym}"];\n'
    dot_source += '}'

    # 2. On écrit le fichier source .gv
    gv_file = f"{filename}.gv"
    png_file = f"{filename}.png"
    with open(gv_file, 'w', encoding='utf-8') as f:
        f.write(dot_source)

    # 3. On appelle dot.exe directement avec subprocess
    try:
        # On essaie d'appeler 'dot' qui doit être dans le PATH grâce à interface.py
        result = subprocess.run(
            ['dot', '-Tpng', gv_file, '-o', png_file],
            capture_output=True,
            text=True,
            shell=True # Important sous Windows
        )
        
        if os.path.exists(png_file):
            return os.path.abspath(png_file)
        else:
            print(f"Erreur rendu : {result.stderr}")
            return None
    except Exception as e:
        print(f"Erreur fatale : {e}")
        return None
