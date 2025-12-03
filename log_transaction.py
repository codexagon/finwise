from PySide6 import QtCore, QtUiTools
from PySide6.QtWidgets import QMessageBox, QSizePolicy

import database, account, preferences

class LogTransactionDialog:
    def __init__(self):
        loader = QtUiTools.QUiLoader()
        ui_file = QtCore.QFile("ui/log_transaction_dialog.ui")
        ui_file.open(QtCore.QFile.ReadOnly)
        self.ui = loader.load(ui_file)

        self.ui.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.ui.setFixedSize(self.ui.size())
        self.ui.setMaximumSize(self.ui.size())
        self.ui.setMinimumSize(self.ui.size())
        
        dateInputBox = self.ui.selectDateInput

        dateInputBox.setDate(QtCore.QDate.currentDate())

        submitBtn = self.ui.submitButton
        cancelBtn = self.ui.cancelButton

        submitBtn.clicked.connect(self.add_transaction)
        cancelBtn.clicked.connect(self.ui.close)

        ui_file.close()
    
    def update_categories(self, categories):
        categoryInput = self.ui.selectCategoryInput
        categoryInput.addItems(categories)
    
    def add_transaction(self):
        name = self.ui.addNameInput.text()
        description = self.ui.addDescInput.toPlainText()
        amount = self.ui.addAmountInput.value()
        type = self.ui.selectTypeInput.currentText()
        category = self.ui.selectCategoryInput.currentText()
        date = self.ui.selectDateInput.date().toPython()

        if not name:
            QMessageBox.critical(None,"Error", "Name cannot be empty!")
        elif not amount:
            QMessageBox.critical(None,"Error", "Amount cannot be 0!")
        else:
            database.add_transaction(date, amount, name, description, type, category)
            account.update_account("transaction_count", 1)
            account.update_account("current_balance", amount if type == "Income" else -amount)
            account.update_account("xp", 5)
            self.ui.accept()
            QMessageBox.information(None, "Success", "Transaction added successfully!")
