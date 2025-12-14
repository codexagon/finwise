from PySide6 import QtCore, QtUiTools
from PySide6.QtWidgets import QMessageBox, QSizePolicy

import database, account
import utils.xp_system as xp

class LogTransactionDialog:
    def __init__(self, transaction_count):
        loader = QtUiTools.QUiLoader()
        ui_file = QtCore.QFile("ui/log_transaction_dialog.ui")
        ui_file.open(QtCore.QFile.ReadOnly)
        self.ui = loader.load(ui_file)

        self.ui.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.ui.setFixedSize(self.ui.size())
        self.ui.setMaximumSize(self.ui.size())
        self.ui.setMinimumSize(self.ui.size())

        self.transaction_count = transaction_count
        
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
            current_info = account.get_account_info()
            old_xp = current_info["xp"]
            old_level = xp.calculate_level(old_xp)

            database.add_transaction(date, amount, name, description, type, category)
            account.update_account("transaction_count", 1)
            account.update_account("current_balance", amount if type == "Income" else -amount)

            xp_earned = xp.calculate_transaction_xp(amount, type, self.transaction_count + 1)
            account.update_account("xp", xp_earned)

            new_xp = old_xp + xp_earned
            new_level = xp.calculate_level(new_xp)

            self.ui.accept()

            if new_level > old_level:
                QMessageBox.information(
                    None,
                    "Level Up",
                    f"Congratulations! You've reached level {new_level}!\n"
                    f"XP earned: +{xp_earned}"
                )
            else:
                progress = xp.xp_progress_in_level(new_xp)
                QMessageBox.information(
                    None,
                    "Success",
                    "Transaction added successfully!\n"
                    f"XP earned: {xp_earned}\n"
                    f"Progress: {progress['xp_in_level']}/{progress['xp_gap']} XP to Level {new_level + 1}"
                )
