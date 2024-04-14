from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.uic import loadUi
from ana_lex import a_lexico
from ana_sintac import a_sintactico
from ana_seman import a_semantico


#MAIN
class MiVentana(QMainWindow):
    def __init__(self):
        super(MiVentana, self).__init__()
        loadUi('ventana.ui', self)
        
        self.pushButton.clicked.connect(self.verificar)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["Token", "Dato", "Posicion", "Status"])
        self.tableWidget.setColumnWidth(0, 220)
        self.tableWidget.setColumnWidth(1, 100)
        self.tableWidget.setColumnWidth(2, 80)
        self.tableWidget.setColumnWidth(3, 60)

    def verificar(self):
        self.CE.clear()  
        texto = self.textEdit.toPlainText()
        has_errors, tokens_lexico = a_lexico(texto)

        error_counter = 0
        self.tableWidget.setRowCount(0)

        for lexeme in tokens_lexico:
            parts = lexeme.split(maxsplit=2)
            tipo = parts[0]
            valor = parts[1]
            posicion = parts[2]
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(tipo))
            self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(valor))
            lexpos_value = posicion.split()[-1]
            self.tableWidget.setItem(rowPosition, 2, QTableWidgetItem(lexpos_value))

            if tipo == "ERROR":
                error_counter += 1
                self.tableWidget.setItem(rowPosition, 3, QTableWidgetItem("✕"))

        self.CE.addItem(str(error_counter))
        self.consola.clear()    
        self.sintactico.clear()       
        self.semantico.clear()                  
        if (error_counter == 0):
            print("Análisis léxico correcto")
            success, syntax_result = a_sintactico(texto)
            print("syntax_result value: "+syntax_result)
            if success:
                print("Análisis sintáctico correcto")
                self.sintactico.addItem("Status: Sintaxis Correcta")
                print (texto)
                
                semantic_result = a_semantico(texto)
                
                if "Console status:" in semantic_result:
                    print("semantic result "  + semantic_result)
                    self.semantico.addItem("Status: Semántica Correcta")
                    self.consola.addItem(semantic_result)
                else:
                    print("Error en el análisis semántico")
                    self.semantico.addItem("Status: Error en análisis semántico")
                    self.consola.addItem(semantic_result)
            else:
                print("Error de sintaxis")
                self.sintactico.addItem("Status: "+syntax_result)
                self.semantico.addItem("Status: Sintaxis invalida")
                
                        
        else:
            #self.consola.addItem("Análisis léxico con errores. Revise la tabla para más detalles.")
            self.sintactico.addItem("Status: Error de lexico. \n Análisis léxico con errores. Revise la tabla para más detalles.")
            self.semantico.addItem("Status: Sintaxis invalida")
            
if __name__ == '__main__':
    app = QApplication([])
    ventana = MiVentana()
    ventana.show()
    app.exec_()
