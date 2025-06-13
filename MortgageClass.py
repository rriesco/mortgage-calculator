import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import numpy_financial  as npf
import os

class MortgageCalculator:
    def __init__(self, house_price, down_payment, interest_rate, loan_term_years, cost, taxes, amortization_schedule_path=None, amortization_schedule_df=None):
        self.house_price = house_price
        self.down_payment = down_payment
        self.interest_rate = interest_rate / 100
        self.monthly_rate = self.interest_rate / 12
        self.loan_term_years = loan_term_years
        self.loan_term_months = self.loan_term_years * 12
        self.cost = cost
        self.taxes = taxes
        self.taxes_cost = (self.taxes / 100) * self.house_price + self.cost
        self.debt = self.taxes_cost + self.house_price - self.down_payment + self.cost
        self.amortization_schedule_path = amortization_schedule_path
        self.amortization_schedule_df = amortization_schedule_df
        self.initial_monthly_payment = self.calculate_mortgage_payment()
        
        if self.down_payment > self.house_price:
            raise ValueError("Down payment cannot be greater than house price.")
        
    def calculate_mortgage_payment(self):
        self.monthly_payment = -npf.pmt(self.monthly_rate, self.loan_term_months, self.debt)
        return self.monthly_payment

    def create_extra_amortization_schedule(self):
        if self.amortization_schedule_path is not None and os.path.exists(self.amortization_schedule_path):
            self.amortization_schedule = pd.read_csv(self.amortization_schedule_path, delimiter=';')
        elif self.amortization_schedule_df is not None and isinstance(self.amortization_schedule_df, pd.DataFrame):
            self.amortization_schedule = self.amortization_schedule_df
        else:
            self.amortization_schedule = None
    
    def create_amortization_schedule(self):
        """Create a mathematically correct amortization schedule."""
        self.remaining_months = self.loan_term_months
        self.monthly_payment = -npf.pmt(self.monthly_rate, self.remaining_months, self.debt)
        self.schedule_data = []
        self.remaining_balance = self.debt
        self.total_interest_paid = 0
    
        for month in range(1, self.loan_term_months + 1):
            extra_payment = 0
            amort_type = None

            if self.amortization_schedule is not None:
                amort_type = self.amortization_schedule.loc[month - 1, 'Type']
                extra_payment = self.amortization_schedule.loc[month - 1, 'Amortization']

            self.interest_payment = self.remaining_balance * self.monthly_rate
            self.regular_debt = self.monthly_payment - self.interest_payment
            self.debt_payment = self.monthly_payment - self.interest_payment + extra_payment
            
            # Prevent over payment (if the remaining balance is less than the debt payment)
            if self.remaining_balance - self.debt_payment < 0.01:
                self.debt_payment = self.remaining_balance
                actual_payment = self.debt_payment + self.interest_payment
            else:
                actual_payment = self.monthly_payment

            self.total_interest_paid += self.interest_payment
            self.remaining_balance -= self.debt_payment
            self.remaining_balance = max(0, self.remaining_balance)

            if extra_payment != 0:
                if amort_type == 'Term':
                    self.remaining_months = int(npf.nper(self.monthly_rate, -self.monthly_payment, self.remaining_balance) + 0.5)

                elif amort_type == 'Fee':
                    self.remaining_months -= 1
                    self.monthly_payment = -npf.pmt(self.monthly_rate, self.remaining_months, self.remaining_balance)
            else:
                self.remaining_months -= 1

            self.schedule_data.append({
                'Payment Number': month,
                'Monthly Payment': round(self.monthly_payment, 2),
                'Total Payment': round(actual_payment + extra_payment, 2),
                'Regular Amortization': round(self.regular_debt, 2),
                'Additional Amortization': round(extra_payment, 2),
                'Total Amortization': round(self.debt_payment, 2),
                'Amortization Type': amort_type,
                'Interest': round(self.interest_payment, 2),
                'Remaining Balance': round(max(0, self.remaining_balance), 2),
                
                'Accrued Interest': round(self.total_interest_paid, 2),
                'Remaining Months': self.remaining_months,
                'Remaining Balance (after payment)': round(max(0, self.remaining_balance), 2),
                'Amortization Type': extra_payment
            })

            if self.remaining_balance <= 0.01 or self.remaining_months <= 0:
                break
            
    def get_amortization_schedule(self):
        """Return the amortization schedule as a DataFrame."""
        if not hasattr(self, 'schedule_data'):
            raise ValueError("Amortization schedule has not been created yet.")
        return pd.DataFrame(self.schedule_data)
            
    def run(self):
        self.calculate_mortgage_payment()
        self.create_extra_amortization_schedule()
        self.create_amortization_schedule()
        self.total_mortgage = self.house_price + self.taxes + self.cost - self.down_payment
        self.total_cost = self.house_price + self.taxes_cost
        self.total_paid = self.debt + self.down_payment
        self.financing_percentage = self.total_mortgage / self.total_cost * 100
        # self.amortization_schedule = pd.DataFrame(self.schedule_data)
        # self.amortization_schedule.to_csv(self.amortization_schedule_path, index=False)

if __name__ == "__main__":
    params = {
        "house_price": 300000,
        "down_payment": 60000,
        "interest_rate": 0.04,
        "loan_term_years": 30,
        "cost": 5000,
        "taxes": 1.25
    }

    try:
        mortgage = MortgageCalculator(**params)
        results = mortgage.run()
        print(results.head(10)) 
    except Exception as e:
        print(f"Error: {e}")