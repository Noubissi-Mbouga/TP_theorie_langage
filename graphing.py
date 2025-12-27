# mycompiler/graphing.py
def setup_graphviz():
    if getattr(sys, 'frozen', False):
        # mode exécutable
        base_path = os.path.dirname(sys.executable)
    else:
        # mode script python
        base_path = os.path.abspath(".")

    graphviz_bin = os.path.join(base_path, "graphviz", "bin")
    os.environ["PATH"] += os.pathsep + graphviz_bin

setup_graphviz()

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



