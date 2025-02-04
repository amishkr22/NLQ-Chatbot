import pandas as pd
from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

# Load dataset (ensure the correct file path)
DATA_PATH = "NRM_DataSet_Training - All_Data.csv"

# Load the dataset once (improves performance)
df = pd.read_csv(DATA_PATH)


class ActionGetSalesPerformance(Action):
    def name(self):
        return "action_get_sales_performance"

    def run(self, dispatcher, tracker, domain):
        try:
            # Load CSV file
            df = pd.read_csv(DATA_PATH)

            # Convert 'Date' column to datetime
            df["Date"] = pd.to_datetime(df["Date"], errors='coerce')

            # Extract Quarter from the Date
            df["Quarter"] = df["Date"].dt.to_period("Q")

            # Get last two quarters dynamically
            latest_quarter = df["Quarter"].max()
            previous_quarter = df["Quarter"].sort_values().unique()[-2]

            # Calculate sales for both quarters
            latest_sales = df[df["Quarter"] == latest_quarter]["Sales_Revenue"].sum()
            previous_sales = df[df["Quarter"] == previous_quarter]["Sales_Revenue"].sum()

            # Generate response
            response = (f"Total sales in {latest_quarter} were ${latest_sales:,.2f}, "
                        f"compared to ${previous_sales:,.2f} in {previous_quarter}.")
            
            dispatcher.utter_message(text=response)

        except Exception as e:
            dispatcher.utter_message(text=f"Error processing request: {str(e)}")
        return []

class ActionGetPromotionEffectiveness(Action):
    def name(self):
        return "action_get_promotion_effectiveness"

    def run(self, dispatcher, tracker, domain):
        # Example: Fetch promotion with the highest ROI
        best_promo = df[df["ROI"] == df["ROI"].max()]["Promotion"].values[0]
        response = f"The highest ROI promotion last quarter was '{best_promo}'."
        dispatcher.utter_message(text=response)
        return []


class ActionGetRetailChannelInsights(Action):
    def name(self):
        return "action_get_retail_channel_insights"

    def run(self, dispatcher, tracker, domain):
        # Example: Get region with the highest stockouts
        region_stockouts = df[df["Stockouts"] == df["Stockouts"].max()]["Region"].values[0]
        response = f"The region with the highest stockouts last month was {region_stockouts}."
        dispatcher.utter_message(text=response)
        return []


class ActionGetCustomerPricingInsights(Action):
    def name(self):
        return "action_get_customer_pricing_insights"

    def run(self, dispatcher, tracker, domain):
        # Example: Get most price-sensitive products
        price_sensitive_products = df.nlargest(3, "Price Sensitivity")["Product"].tolist()
        response = f"The top 3 most price-sensitive products are {', '.join(price_sensitive_products)}."
        dispatcher.utter_message(text=response)
        return []


class ActionRunABTestingSimulation(Action):
    def name(self):
        return "action_run_ab_testing_simulation"

    def run(self, dispatcher, tracker, domain):
        # Example: Simulate impact of Flat 10% off vs. Buy 1 Get 1 Free
        discount_impact = df[df["Discount Type"] == "Flat 10%"]["Projected Sales"].sum()
        bogo_impact = df[df["Discount Type"] == "BOGO"]["Projected Sales"].sum()

        response = (f"Projected sales impact:\n"
                    f"- **Flat 10% Off**: ${discount_impact:,}\n"
                    f"- **Buy 1 Get 1 Free**: ${bogo_impact:,}")
        
        dispatcher.utter_message(text=response)
        return []


class ActionSimulateMarketDisruptions(Action):
    def name(self):
        return "action_simulate_market_disruptions"

    def run(self, dispatcher, tracker, domain):
        # Example: Simulate competitor launching a cheaper product
        competitor_impact = df["Market Share Loss"].mean()  # Example: Average market share loss
        response = f"If a competitor launches a similar product at a 15% lower price, we estimate a market share decline of {competitor_impact:.2f}%."
        dispatcher.utter_message(text=response)
        return []
