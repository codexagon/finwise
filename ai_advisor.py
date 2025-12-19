import os

from PySide6 import QtCore, QtUiTools
from PySide6.QtWidgets import QMessageBox, QSizePolicy
from PySide6.QtCore import QThread, Signal

from google import genai
from pathlib import Path
from dotenv import load_dotenv

from datetime import datetime
from collections import defaultdict

import database, account

class AIWorker(QThread):
    finished = Signal(str)
    error = Signal(str)
    
    def __init__(self, prompt):
        super().__init__()
        self.prompt = prompt
    
    def run(self):
        try:
            api_key = os.environ.get('GEMINI_API_KEY')
            if not api_key:
                self.error.emit("API key not found. Please set GEMINI_API_KEY environment variable.")
                return
            
            client = genai.Client(api_key=api_key)
            
            response = client.models.generate_content(
                model="models/gemini-2.5-flash",
                contents=self.prompt
            )

            self.finished.emit(response.text)
        except Exception as e:
            self.error.emit(str(e))

class AIAdvisorWindow:
    def __init__(self):
        self.worker = None
        load_dotenv(Path(__file__).resolve().parent / ".env")

        loader = QtUiTools.QUiLoader()
        ui_file = QtCore.QFile("ui/ai_advisor_window.ui")
        ui_file.open(QtCore.QFile.ReadOnly)
        self.ui = loader.load(ui_file)

        self.ui.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.ui.setFixedSize(self.ui.size())
        self.ui.setMaximumSize(self.ui.size())
        self.ui.setMinimumSize(self.ui.size())

        if not os.environ.get("GEMINI_API_KEY"):
            QMessageBox.critical(
                self.ui,
                "API Key Missing",
                "Please set the GEMINI_API_KEY environment variable.\n\n"
                "Get your API key from https://aistudio.google.com/app/apikey"
            )
            self.ui.close()

        self.ui.responseArea.setPlaceholderText(
            "Click on any button above to get personalized financial advice based on your transactions.\n"
            "General Analysis: overall financial health assessment\n"
            "Saving Tips: Practical ways to spend more money\n"
        )

        self.ui.generalAnalysisButton.clicked.connect(lambda: self.get_response("general"))
        self.ui.savingTipsButton.clicked.connect(lambda: self.get_response("savings"))
        self.ui.closeButton.clicked.connect(self.ui.close)

        ui_file.close()
    
    def get_response(self, advice_type):
        self.set_buttons_enabled(False)

        loading_messages = {
            "general": "Analyzing your overall financial health...",
            "savings": "Finding ways to help you save more..."
        }

        self.ui.responseArea.setPlainText(loading_messages.get(advice_type, "Loading...") + "\n\nPlease wait, this may take a few seconds...")

        transactions = database.get_all_transactions()
        account_info = account.get_account_info()
        summary = self.prepare_financial_summary(transactions, account_info)

        prompt = self.create_prompt(advice_type, summary)

        self.worker = AIWorker(prompt)
        self.worker.finished.connect(self.on_advice_received)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def create_prompt(self, advice_type, summary):
        base_prompt = f"""You are a helpful personal financial advisor. Speak directly to the user in second person (you/your). Never use third-person terms like they/their. Based on this financial data:

{summary}

"""
    
        prompts = {
        "general": base_prompt + """Provide a concise financial health assessment including:
1. Your overall financial health score (Good/Fair/Needs Improvement)
2. Key strengths in your financial habits
3. Top 3 areas you can improve
4. Insights into your spending patterns
5. 3-5 specific, actionable recommendations you can apply

Tone: encouraging, practical.
No unnecessary paragraphs.
Output only plain text.
No markdown, headings, or bold.
Number items simply as 1. 2. 3.""",
        
        "savings": base_prompt + """Focus on savings strategies including:
1. Your current savings rate analysis
2. Identify unnecessary expenses based on your spending patterns
3. Suggest 5 specific ways you can save more money based on your spending categories
4. Set a realistic monthly savings goal for you
5. Quick wins you can implement immediately

Tone: specific and action-focused.
Reference your actual spending categories.
No unnecessary paragraphs.
Output only plain text.
No markdown, headings, or bold.
Number items simply as 1. 2. 3.
Do not use third-person language.
Always write for "you".""",
        }
    
        return prompts.get(advice_type, base_prompt)

    
    def prepare_financial_summary(self, transactions, account_info):
        balance = account_info['current_balance']
        total_transactions = account_info['transaction_count']
        
        total_income = 0
        total_expenses = 0
        category_spending = defaultdict(float)
        
        today = datetime.now()
        current_month = today.strftime("%Y-%m")
        monthly_income = 0
        monthly_expenses = 0
        
        for trans in transactions:
            amount = trans[3]
            trans_type = trans[4]
            category = trans[5]
            date = trans[1]
            
            if trans_type == "Income":
                total_income += amount
                if date.startswith(current_month):
                    monthly_income += amount
            else:
                total_expenses += amount
                category_spending[category] += amount
                if date.startswith(current_month):
                    monthly_expenses += amount
        
        top_categories = sorted(category_spending.items(), key=lambda x: x[1], reverse=True)[:5]
        
        summary = f"""Current Balance: ₹{balance:.2f}
Total Transactions: {total_transactions}

All-Time Overview:
- Total Income: ₹{total_income:.2f}
- Total Expenses: ₹{total_expenses:.2f}
- Net Savings: ₹{total_income - total_expenses:.2f}
- Savings Rate: {((total_income - total_expenses) / total_income * 100) if total_income > 0 else 0:.1f}%

This Month ({current_month}):
- Income: ₹{monthly_income:.2f}
- Expenses: ₹{monthly_expenses:.2f}
- Net: ₹{monthly_income - monthly_expenses:.2f}

Top Spending Categories (All Time):
"""
        for i, (category, amount) in enumerate(top_categories, 1):
            percentage = (amount / total_expenses * 100) if total_expenses > 0 else 0
            summary += f"{i}. {category}: ₹{amount:.2f} ({percentage:.1f}% of total expenses)\n"
        
        return summary
    
    def on_advice_received(self, advice):
        self.ui.responseArea.setText(advice)
        self.set_buttons_enabled(True)
    
    def on_error(self, error_msg):
        self.ui.responseArea.clear()

        QMessageBox.critical(
            self.ui,
            "AI Advisor Error",
            f"Error: {error_msg}\n\n"
            "Please check:\n"
            "• GEMINI_API_KEY environment variable is set\n"
            "• Internet connection is active\n"
            "• API key is valid\n"
            "• API quota is not exceeded\n\n"
            "Get your API key from https://aistudio.google.com/app/apikey"
        )

        self.set_buttons_enabled(True)
    
    def set_buttons_enabled(self, enabled):
        self.ui.generalAnalysisButton.setEnabled(enabled)
        self.ui.savingTipsButton.setEnabled(enabled)