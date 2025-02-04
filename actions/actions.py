from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd

class ActionQuerySalesPerformance(Action):
    def name(self):
        return "action_query_sales_performance"

    def run(self, dispatcher, tracker, domain):
        df = pd.read_csv("NRM_DataSet_Training - All_Data.csv")
        df["Date"] = pd.to_datetime(df["Date"])
        sales_q4 = df[df["Date"].dt.quarter == 4]["Sales_Revenue"].sum()
        sales_q3 = df[df["Date"].dt.quarter == 3]["Sales_Revenue"].sum()
        dispatcher.utter_message(text=f"The total sales in Q4 were {sales_q4}, compared to {sales_q3} in the previous quarter.")
        return []

class ActionQueryPromotionEffectiveness(Action):
    def name(self):
        return "action_query_promotion_effectiveness"

    def run(self, dispatcher, tracker, domain):
        df = pd.read_csv("NRM_DataSet_Training - All_Data.csv")
        highest_roi = df.loc[df["Discount (%)"].idxmax()]
        promotion_name = highest_roi["Product_Name"]
        roi_value = highest_roi["Gross_Profit_Margin (%)"]
        dispatcher.utter_message(text=f"The promotional scheme with the highest ROI last quarter was {promotion_name} with an ROI of {roi_value}%.")
        return []

class ActionQueryRetailInsights(Action):
    def name(self):
        return "action_query_retail_insights"

    def run(self, dispatcher, tracker, domain):
        df = pd.read_csv("NRM_DataSet_Training - All_Data.csv")
        stockouts = df.groupby("Region")["Returns_Units"].sum().idxmax()
        dispatcher.utter_message(text=f"The region with the highest stockouts last month was {stockouts}.")
        return []

class ActionQueryCustomerPricingInsights(Action):
    def name(self):
        return "action_query_customer_pricing_insights"

    def run(self, dispatcher, tracker, domain):
        df = pd.read_csv("NRM_DataSet_Training - All_Data.csv")
        price_increase = 1.05  # 5% increase
        df["New_Price"] = df["Retail_Price"] * price_increase
        df["New_Sales_Revenue"] = df["New_Price"] * df["Sales_Units"]
        total_revenue = df["New_Sales_Revenue"].sum()
        dispatcher.utter_message(text=f"A 5% price increase would result in total revenue of {total_revenue}.")
        return []

class ActionRunABTestingSimulation(Action):
    def name(self):
        return "action_run_ab_testing_simulation"

    def run(self, dispatcher, tracker, domain):
        df = pd.read_csv("NRM_DataSet_Training - All_Data.csv")
        price_reduction = 0.9  # 10% reduction
        df["New_Price"] = df["Retail_Price"] * price_reduction
        df["New_Sales_Revenue"] = df["New_Price"] * df["Sales_Units"]
        total_revenue = df["New_Sales_Revenue"].sum()
        dispatcher.utter_message(text=f"A 10% price reduction would result in total revenue of {total_revenue}.")
        return []

class ActionSimulateMarketDisruptions(Action):
    def name(self):
        return "action_simulate_market_disruptions"

    def run(self, dispatcher, tracker, domain):
        df = pd.read_csv("NRM_DataSet_Training - All_Data.csv")
        competitor_price_reduction = 0.85  # 15% reduction
        df["New_Price"] = df["Retail_Price"] * competitor_price_reduction
        df["New_Sales_Revenue"] = df["New_Price"] * df["Sales_Units"]
        total_revenue = df["New_Sales_Revenue"].sum()
        dispatcher.utter_message(text=f"If a competitor reduces prices by 15%, our total revenue would be {total_revenue}.")
        return []