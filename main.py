import os, sys

from PySide6 import QtCore, QtUiTools
from PySide6.QtWidgets import (QApplication, QHeaderView, QAbstractItemView, QDialog, QMessageBox, QSizePolicy)

import database, account, preferences

import utils.xp_system as xp
from utils.functions import Functions

from log_transaction import LogTransactionDialog
from update_transaction import UpdateTransactionDialog

class FinanceTrackerApp:
    DATA_DIR = os.path.join(os.path.expanduser("~"), "finwise-data")

    def __init__(self):
        if not os.path.exists(self.DATA_DIR):
            os.mkdir(self.DATA_DIR)

        Functions.load_fonts()
        
        database.create_tables()

        if not os.path.exists(os.path.join(self.DATA_DIR, "account_data.dat")):
            account.create_account()
        
        if not os.path.exists(os.path.join(self.DATA_DIR, "preferences.dat")):
            preferences.set_defaults()

        loader = QtUiTools.QUiLoader()
        ui_file = QtCore.QFile("ui/main_window.ui")
        ui_file.open(QtCore.QFile.ReadOnly)
        self.ui = loader.load(ui_file)
        ui_file.close()

        self.setup_connections()

        self.ui.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.ui.setFixedSize(self.ui.size())
        self.ui.setMaximumSize(self.ui.size())
        self.ui.setMinimumSize(self.ui.size())
        
        category_sort = self.ui.sortByCategoryDropdown.currentText()
        sort_order = self.ui.sortingOrderDropdown.currentText()
        Functions.load_transactions(self.ui.transactionsTable, category_sort, sort_order)

        self.setup_tabs()
    
    def setup_connections(self):
        # Connections in Home tab
        self.ui.logTransactionButton.clicked.connect(self.open_transaction_dialog)

        # Connections in Transactions tab
        self.ui.updateTransactionButton.clicked.connect(self.open_update_dialog)
        self.ui.deleteTransactionButton.clicked.connect(self.handle_delete)

        self.ui.sortByCategoryDropdown.currentTextChanged.connect(self.setup_transactions_tab)
        self.ui.sortingOrderDropdown.currentTextChanged.connect(self.setup_transactions_tab)

        # Connections in Profile tab
        self.ui.saveSettingsButton.clicked.connect(self.save_settings)
    
    def setup_tabs(self):
        self.setup_home_tab()
        self.setup_profile_tab()
        self.setup_transactions_tab()
    
    def setup_home_tab(self):
        tabWidget = self.ui.tabWidget
        accountBalanceMainDisplay = self.ui.accountBalanceMain

        balance = account.get_account_info()["current_balance"]

        accountBalanceString = f"<html><head/><body><p><span style=\" font-size:20pt; font-weight:700;\">₹ {str(balance)}</span></p></body></html>"
        accountBalanceMainDisplay.setText(accountBalanceString)

        tabWidget.tabBar().setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
    
    def setup_transactions_tab(self):
        table = self.ui.transactionsTable

        table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        header = table.horizontalHeader()

        header.setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Stretch)

        table.setColumnWidth(1, 85)
        table.setColumnWidth(2, 150)
        table.setColumnWidth(3, 80)
        table.setColumnWidth(4, 65)
        table.setColumnWidth(5, 120)

        table.setColumnHidden(0, True)

        category_sort = self.ui.sortByCategoryDropdown.currentText()
        sort_order = self.ui.sortingOrderDropdown.currentText()
        Functions.load_transactions(self.ui.transactionsTable, category_sort, sort_order)
    
    def setup_profile_tab(self):
        accountNameDisplay = self.ui.accountName
        accountBalanceDisplay = self.ui.accountBalance
        accountTransactionsDisplay = self.ui.accountTransactions
        accountXpDisplay = self.ui.accountXp

        information = account.get_account_info()

        accountNameDisplay.setText(information["account_name"])
        accountBalanceDisplay.setText("₹" + str(information["current_balance"]))
        accountTransactionsDisplay.setText(str(information["transaction_count"]))
        accountXpDisplay.setText(str(information["xp"]))

        self.handle_settings()

    def handle_settings(self):
        setCategoriesInput = self.ui.categoriesInput
        setAccountNameInput = self.ui.accountNameInput

        existing_settings = preferences.get_preferences()
        information = account.get_account_info()

        setCategoriesInput.setText(",".join(existing_settings["categories"]))
        setAccountNameInput.setText(information["account_name"])
    
    def save_settings(self):
        setCategoriesInput = self.ui.categoriesInput
        setAccountNameInput = self.ui.accountNameInput
        new_categories = setCategoriesInput.text().strip().split(",")
        new_account_name = setAccountNameInput.text().strip()
        preferences.update_preferences("categories", new_categories)
        account.update_account("account_name", new_account_name)
        self.setup_profile_tab()
        QMessageBox.information(None, "Success", "Settings saved successfully.")
    
    def open_transaction_dialog(self):
        count = account.get_account_info()["transaction_count"]
        transactionDialog = LogTransactionDialog(count)
        transactionDialog.update_categories(preferences.get_preferences()["categories"])
        submitted = transactionDialog.ui.exec()

        if submitted == QDialog.Accepted:
            category_sort = self.ui.sortByCategoryDropdown.currentText()
            sort_order = self.ui.sortingOrderDropdown.currentText()
            Functions.load_transactions(self.ui.transactionsTable, category_sort, sort_order)
            self.setup_tabs()
    
    def open_update_dialog(self):
        transaction_details = Functions.get_transaction_details(self.ui.transactionsTable)
        
        if transaction_details is None:
            QMessageBox.warning(None, "No Selection", "No transaction selected. Please choose a transaction to update.")
            return None

        updateDialog = UpdateTransactionDialog(transaction_details)
        updateDialog.update_categories(preferences.get_preferences()["categories"])
        submitted = updateDialog.ui.exec()

        if submitted == QDialog.Accepted:
            category_sort = self.ui.sortByCategoryDropdown.currentText()
            sort_order = self.ui.sortingOrderDropdown.currentText()
            Functions.load_transactions(self.ui.transactionsTable, category_sort, sort_order)
            self.setup_tabs()

    def handle_delete(self):
        transaction_details = Functions.get_transaction_details(self.ui.transactionsTable)

        if transaction_details is None:
            QMessageBox.warning(None, "No Selection", "No transaction selected. Please choose a transaction to delete.")
            return None

        confirm = QMessageBox.question(None, "Confirm Delete", "Are you sure you want to delete this transaction?")

        if confirm == QMessageBox.StandardButton.Yes:
            delete_id = transaction_details["id"]
            delete_amount = float(transaction_details["amount"])
            if transaction_details["type"] == "Income":
                account.update_account("current_balance", -delete_amount)
            else:
                account.update_account("current_balance", delete_amount)

            account.update_account("transaction_count", -1)
            account.update_account("xp", xp.XP_REWARDS["transaction_deleted"])
            database.delete_transaction(delete_id)
            QMessageBox.information(None, "Success", "Transaction deleted successfully!")

            category_sort = self.ui.sortByCategoryDropdown.currentText()
            sort_order = self.ui.sortingOrderDropdown.currentText()
            Functions.load_transactions(self.ui.transactionsTable, category_sort, sort_order)

            self.setup_tabs()
        else:
            QMessageBox.information(None, "Cancelled", "Transaction deletion cancelled.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = FinanceTrackerApp()
    window.ui.show()
    sys.exit(app.exec())