# mycompiler/graphing.py


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
    path = dot.render(filename, cleanup=True)
    return path

    
def draw_dfa(dfa, filename="dfa"):
    dot = Digraph(comment="DFA", format="png")
    dot.attr(rankdir='LR')
    for s in dfa.states:
        shape = 'doublecircle' if s in dfa.final_states else 'circle'
        dot.node(s, shape=shape)
    dot.node('__start__', shape='point')
    dot.edge('__start__', dfa.start_state, label='')
    for s, trans in dfa.transitions.items():
        for sym, tgt in trans.items():
            dot.edge(s, tgt, label=sym)
    path = dot.render(filename, cleanup=True)
    return path

