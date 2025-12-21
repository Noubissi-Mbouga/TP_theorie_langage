#!/usr/bin/python3
import sys
from PyQt6.QtWidgets import (QApplication,QMainWindow,QWidget,QVBoxLayout,QHBoxLayout,QLabel,QLineEdit,
    QTextEdit,QPushButton,QGroupBox,QMessageBox,QTabWidget)
from PyQt6.QtCore import Qt
from verifier import appartient_grammaire_reguliere
import os

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



from graphing import *


global regle 
global ax_depart

def formatter_regle(Rule):
    regle={}
    rule = Rule.split()
    new,n= [],[]
    for i in range(len(rule)):
        new=rule[i].split('->')
        n = new[1].split('|')
        regle[new[0]] = n
    return regle

class GrammarCheckerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Verificateur de grammaire")
        self.setGeometry(100,100,800,600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        tabs = QTabWidget()
        layout.addWidget(tabs)

        grammar_tab = self.create_grammar_tab()
        tabs.addTab(grammar_tab, "Renseignement de la Grammaire")

        check_tab = self.create_check_tab()
        tabs.addTab(check_tab, "Verification du mot et visualisation")

    def create_check_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        grammar_group = QGroupBox("Grammaire Definie")
        grammar_layout = QVBoxLayout()
        
        self.grammar_display = QTextEdit()
        self.grammar_display.setReadOnly(True)
        self.grammar_display.setMaximumHeight(250)
        self.grammar_display.setPlainText("Aucune grammaire definie")
        grammar_layout.addWidget(self.grammar_display)

        grammar_group.setLayout(grammar_layout)
        layout.addWidget(grammar_group)

        # Groupe pour la verification
        check_group = QGroupBox("verifier un mot")
        check_layout = QHBoxLayout()

        # Renseigner le mot a verifier 
        word_layout = QHBoxLayout()
        word_layout.addWidget(QLabel("mot a verifier: "))
        self.word_input = QLineEdit()
        self.word_input.setPlaceholderText("entrer un mot .......")
        word_layout.addWidget(self.word_input)
        check_layout.addLayout(word_layout)

        # Bouton pour tester le ;ot
        self.check_button = QPushButton("Verifier le mot")
        self.check_button.clicked.connect(self.check_word)
        check_layout.addWidget(self.check_button)

        # resultat
        self.result_label = QLabel("Resultat apparaitra ici.........")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setStyleSheet("padding:20px; font-size: 14px; border: 1px solid gray;")
        check_layout.addWidget(self.result_label)

        check_group.setLayout(check_layout)
        layout.addWidget(check_group)
        widget.setLayout(layout)

        return widget

    def create_grammar_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        variables_group = QGroupBox("Variables (Symboles non terminaux)")
        variables_layout = QVBoxLayout()

        self.variables_input = QLineEdit()
        self.variables_input.setPlaceholderText("Ex: S,Q,B")
        variables_layout.addWidget(self.variables_input)

        variables_group.setLayout(variables_layout)
        layout.addWidget(variables_group)

        alphabet_group = QGroupBox("Alphabet (symboles terminaux)")
        alphabet_layout = QVBoxLayout()

        self.alphabet_input = QLineEdit()
        self.alphabet_input.setPlaceholderText("Ex: S,Q,B")
        alphabet_layout.addWidget(self.alphabet_input)

        alphabet_group.setLayout(alphabet_layout)
        layout.addWidget(alphabet_group)

        #axiomes
        axiom_group = QGroupBox("Axiome(symbole de depart)")
        axiom_layout = QVBoxLayout()

        self.axiom_input = QLineEdit()
        self.axiom_input.setPlaceholderText("Ex: A")
        axiom_layout.addWidget(self.axiom_input)

        axiom_group.setLayout(axiom_layout)
        layout.addWidget(axiom_group)

        #Regles de production
        rules_group = QGroupBox("Regles de production")
        rules_layout = QVBoxLayout()

        rules_help = QLabel("EXEMPLE: S -> aS | bA \n A -> Sb \n NB:le mot vide est note 'epsilon' ou 'ε' \n une regle par ligne" )
        rules_help.setStyleSheet("color: gray; font-size:14px;")
        rules_layout.addWidget(rules_help)

        self.rules_input = QTextEdit()
        self.rules_input.setPlaceholderText("S -> aS |bA \n A -> bS ")
        rules_layout.addWidget(self.rules_input)

        rules_group.setLayout(rules_layout)
        layout.addWidget(rules_group)

        #boutons
        buttons_layout = QHBoxLayout()

        self.save_grammar_button = QPushButton("Sauvegarder grammaire")
        self.save_grammar_button.clicked.connect(self.save_grammar)
        buttons_layout.addWidget(self.save_grammar_button)

        self.clear_button = QPushButton("Effacer")
        self.clear_button.clicked.connect(self.clear_grammar)
        buttons_layout.addWidget(self.clear_button)

        layout.addLayout(buttons_layout)

        widget.setLayout(layout)

        return widget

    def clear_grammar(self):
        self.variables_input.clear()
        self.alphabet_input.clear()
        self.rules_input.clear()
        self.axiom_input.clear()
        self.grammar_display.setPlaceholderText("Aucune grammaire definie")

    def save_grammar(self):
        try:
            variables = self.variables_input.text().strip()
            alphabet = self.alphabet_input.text().strip()
            axiom = self.axiom_input.text().strip()
            rules_text = self.rules_input.toPlainText().strip()

            if not all([variables, alphabet, rules_text,axiom]):
                QMessageBox.warning(self, "Erreur", "Tous les champs doivent etre remplis")
                return
            
            # stockage de grammaire
            self.grammar = {
                'variables' : variables,
                'alphabet' : alphabet,
                'rules' : rules_text,
                'axiom' : axiom
            }

            regle = formatter_regle(rules_text)
            ax_depart = axiom
            print(regle)
            automate = grammaire_vers_automate(regle, ax_depart)
            image_path = draw_dfa(automate, filename="automate")
            print("Image générée :", image_path)


            print(appartient_grammaire_reguliere("ababab",regle,ax_depart))  # True
            print(appartient_grammaire_reguliere("abbaabba",regle,ax_depart))  # False

            #mise a jour de l'affichage
            self.grammar_display.setHtml(f'<img src="{image_path}">')
            #display_text = f"variables: {variables}\n"
            #display_text += f"alphabet: {alphabet}\n"
            #display_text += f"Axiome: {axiom}\n"
            #self.grammar_display.setPlainText(display_text)
            QMessageBox.information(self,"Succes", "Grammaire sauvegarde")
        except Exception as e:
            QMessageBox.critical(self,"Erreur",f"Erreur lors de la sauvegarde: {str(e)}")


    def check_word(self):
        if not hasattr(self, 'grammar'):
            QMessageBox.warning(self, "Erreur", "Veuillez d'abord definir une grammaire")
            return
       
        word = self.word_input.text().strip()
        if not word:
            QMessageBox.warning(self,"Erreur","veuillez entrer un mot a verifier")
            return
        # code concernant la logique pour tester si un mot appartient a la grammaire
        regle = formatter_regle(self.rules_input.toPlainText().strip())
        ax_depart = self.axiom_input.text().strip()
        result = appartient_grammaire_reguliere(word,regle,ax_depart)
        # le resultat sera affiche de la maniere suivante self.result_label.setText()
        if result:
            self.result_label.setText("Ce mot appartient a la grammaire")
        else:
            self.result_label.setText("Ce mot n'appartient pas a la grammaire")
        # on pourra aussi set un stylesheet



def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = GrammarCheckerGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
