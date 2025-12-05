from PySide6.QtWidgets import QApplication, QTableWidgetItem
from PySide6.QtGui import QColor, QFont, QFontDatabase

import database, preferences

class Functions:
    @staticmethod
    def load_transactions(table, category, order):
        table.setRowCount(0)
        transactions = database.get_all_transactions(category, order)

        for pos, data in enumerate(transactions):
            table.insertRow(pos)

            for i in range(len(data)):
                table.setItem(pos, i, QTableWidgetItem(str(data[i])))

    @staticmethod
    def get_transaction_details(table):
        selected_row = table.currentRow()

        if selected_row < 0:
            return None
    
        id = table.item(selected_row, 0).text()
        date = table.item(selected_row, 1).text()
        name = table.item(selected_row, 2).text()
        amount = table.item(selected_row, 3).text()
        type = table.item(selected_row, 4).text()
        category = table.item(selected_row, 5).text()
        description = table.item(selected_row, 6).text()

        return {
            "id": id,
            "date": date,
            "name": name,
            "amount": amount,
            "type": type,
            "category": category,
            "description": description
        }

    @staticmethod
    def load_fonts():
        font_id = QFontDatabase.addApplicationFont("assets/inter-variable-font.ttf")
        font_family = QFontDatabase.applicationFontFamilies(font_id)

        if font_family:
            font = QFont(font_family[0], 10)
            QApplication.setFont(font)
        else:
            print("Font could not be loaded.")
        