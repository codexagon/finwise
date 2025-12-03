from PySide6.QtWidgets import QTableWidgetItem

import database, preferences

class Functions:
    @staticmethod
    def load_transactions(table):
        table.setRowCount(0)
        transactions = database.get_all_transactions()

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
        