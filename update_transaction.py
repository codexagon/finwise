from PySide6 import QtCore, QtUiTools
from PySide6.QtWidgets import QMessageBox, QSizePolicy

import database, account, preferences

class UpdateTransactionDialog:
    def __init__(self, transaction_details):
        loader = QtUiTools.QUiLoader()
        ui_file = QtCore.QFile("ui/update_transaction_dialog.ui")
        ui_file.open(QtCore.QFile.ReadOnly)
        self.ui = loader.load(ui_file)

        self.ui.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.ui.setFixedSize(self.ui.size())
        self.ui.setMaximumSize(self.ui.size())
        self.ui.setMinimumSize(self.ui.size())

        self.ui.updateNameInput.setText(transaction_details["name"])
        self.ui.updateDescInput.setPlainText(transaction_details["description"])
        self.ui.updateAmountInput.setValue(float(transaction_details["amount"]))
        self.ui.updateTypeInput.setCurrentText(transaction_details["type"])
        self.ui.updateCategoryInput.setCurrentText(transaction_details["category"])
        self.ui.updateDateInput.setDate(QtCore.QDate.fromString(transaction_details["date"], "yyyy-MM-dd"))

        updateSubmitBtn = self.ui.updateSubmitButton
        updateCancelBtn = self.ui.updateCancelButton

        updateSubmitBtn.clicked.connect(lambda: self.update_transaction(transaction_details))
        updateCancelBtn.clicked.connect(self.ui.close)

        ui_file.close()

    def update_categories(self, categories):
        categoryInput = self.ui.updateCategoryInput
        categoryInput.addItems(categories)
    
    def update_transaction(self, transaction_details):
        new_name = self.ui.updateNameInput.text()
        new_description = self.ui.updateDescInput.toPlainText()
        new_amount = self.ui.updateAmountInput.value()
        new_type = self.ui.updateTypeInput.currentText()
        new_category = self.ui.updateCategoryInput.currentText()
        new_date = self.ui.updateDateInput.date().toPython()

        if not new_name:
            QMessageBox.critical(None,"Error", "Name cannot be empty!")
        elif not new_amount:
            QMessageBox.critical(None,"Error", "Amount cannot be 0!")
        else:
            old_amount = float(transaction_details["amount"])
            old_type = transaction_details["type"]

            if old_type == "Income":
                account.update_account("current_balance", -old_amount)
            else:
                account.update_account("current_balance", old_amount)

            if new_type == "Income":
                account.update_account("current_balance", new_amount)
            else:
                account.update_account("current_balance", -new_amount)

            database.update_transaction(transaction_details["id"], new_date, new_amount, new_name, new_description, new_type, new_category)
            self.ui.accept()
            QMessageBox.information(None, "Success", "Transaction updated successfully!")