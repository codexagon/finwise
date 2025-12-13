from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from collections import defaultdict

import database

class StatisticsWidget(QWidget):    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        self.figure = Figure(figsize=(8, 6), facecolor='#131b26')
        self.canvas = FigureCanvas(self.figure)
        
        layout.addWidget(self.canvas)
        self.setLayout(layout)
    
    def plot_spending_by_category(self):
        transactions = database.get_all_transactions()
        category_totals = defaultdict(float)
        for t in transactions:
            if t[4] == "Expense":
                category = t[5]
                amount = t[3]
                category_totals[category] += amount
        
        categories = list(category_totals.keys())
        amounts = list(category_totals.values())
        
        self.figure.clear()
        
        ax = self.figure.add_subplot(111)
        ax.set_facecolor('#0f111a')
        
        colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4']
        
        if amounts:
            ax.pie(
                amounts,
                labels=categories,
                autopct='%1.1f%%',
                colors=colors,
                textprops={'color': 'white'}
            )
            
            ax.set_title('Spending by Category', color='white', fontsize=16)
        else:
            ax.text(0.5, 0.5, 'No data available', 
                   ha='center', va='center', 
                   color='white', fontsize=14,
                   transform=ax.transAxes)
            ax.axis('off')
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def plot_income_by_category(self):
        transactions = database.get_all_transactions()
        category_totals = defaultdict(float)
        for t in transactions:
            if t[4] == "Income":
                category = t[5]
                amount = t[3]
                category_totals[category] += amount
        
        categories = list(category_totals.keys())
        amounts = list(category_totals.values())
        
        self.figure.clear()
        
        ax = self.figure.add_subplot(111)
        ax.set_facecolor('#0f111a')
        
        colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4']
        
        if amounts:
            ax.pie(
                amounts,
                labels=categories,
                autopct='%1.1f%%',
                colors=colors,
                textprops={'color': 'white'}
            )
            
            ax.set_title('Income by Category', color='white', fontsize=16)
        else:
            ax.text(0.5, 0.5, 'No data available', 
                   ha='center', va='center', 
                   color='white', fontsize=14,
                   transform=ax.transAxes)
            ax.axis('off')
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def plot_income_vs_expenses(self):
        transactions = database.get_all_transactions()

        total_income, total_expenses = 0, 0

        for t in transactions:
            amount = t[3]
            type = t[4]

            if type == "Income":
                total_income += amount
            else:
                total_expenses += amount
        
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor("#0f111a")
        self.figure.patch.set_facecolor("#131b26")

        if total_income == 0 and total_expenses == 0:
            ax.text(0.5, 0.5, 'No data available', 
               ha='center', va='center', 
               color='white', fontsize=14,
               transform=ax.transAxes)
            ax.axis('off')
        else:
            categories = ['Income', 'Expenses']
            amounts = [total_income, total_expenses]
            colors = ['#10b981', '#ef4444']

            bars = ax.bar(categories, amounts, color=colors, width=0.5, edgecolor='white', linewidth=2)

            for bar, amount in zip(bars, amounts):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'₹{amount:.0f}',
                       ha='center', va='bottom', color='white', 
                       fontsize=12)

            ax.set_ylabel('Amount (₹)', color='white', fontsize=12)
            ax.set_title('Total Income vs Expenses', color='white', fontsize=16)
            ax.tick_params(colors='white', labelsize=11)
            ax.grid(True, alpha=0.2, axis='y', color='#475569', linestyle='--')

            self.figure.tight_layout()
    
        self.canvas.draw()
    
    def plot_monthly_trend(self):
        from datetime import datetime

        transactions = database.get_all_transactions()

        monthly_income = defaultdict(float)
        monthly_expenses = defaultdict(float)

        for t in transactions:
            date_str = t[1]
            amount = t[3]
            trans_type = t[4]

            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            month_key = date_obj.strftime("%Y-%m")

            if trans_type == "Income":
                monthly_income[month_key] += amount
            else:
                monthly_expenses[month_key] += amount

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor('#0f111a')
        self.figure.patch.set_facecolor('#131b26')

        if not monthly_income and not monthly_expenses:
            ax.text(0.5, 0.5, 'No data available', 
                   ha='center', va='center', 
                   color='white', fontsize=14,
                   transform=ax.transAxes)
            ax.axis('off')
        else:
            all_months = sorted(set(list(monthly_income.keys()) + 
                                   list(monthly_expenses.keys())))

            income_values = [monthly_income[month] for month in all_months]
            expense_values = [monthly_expenses[month] for month in all_months]

            x = range(len(all_months))

            ax.plot(x, income_values, color='#10b981', linewidth=2.5, 
                   marker='o', markersize=8, label='Income', linestyle='-')
            ax.plot(x, expense_values, color='#ef4444', linewidth=2.5, 
                   marker='s', markersize=8, label='Expenses', linestyle='-')

            ax.set_xlabel('Month', color='white', fontsize=12)
            ax.set_ylabel('Amount (₹)', color='white', fontsize=12)
            ax.set_title('Monthly Income vs Expenses Trend', color='white', 
                        fontsize=16)

            ax.set_xticks(x)
            month_labels = [datetime.strptime(m, "%Y-%m").strftime("%b %Y") 
                           for m in all_months]
            ax.set_xticklabels(month_labels, rotation=45, ha='right')

            ax.tick_params(colors='white', labelsize=10)
            ax.grid(True, alpha=0.2, color='#475569', linestyle='--')
            ax.legend(facecolor='#1a1d29', edgecolor='#3b82f6', 
                     labelcolor='white', fontsize=11)

            self.figure.tight_layout()

        self.canvas.draw()