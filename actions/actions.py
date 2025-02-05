from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd

class ActionQuerySalesPerformance(Action):
    def name(self):
        return "action_query_sales_performance"

    def run(self, dispatcher, tracker, domain):
        df = pd.read_csv("NRM_DataSet_Training - All_Data.csv")
        df["Date"] = pd.to_datetime(df["Date"])
        latest_message = tracker.latest_message.get("text")

        if "Q4" in latest_message:
            # Q4 vs Q3 comparison
            sales_q4 = df[df["Date"].dt.quarter == 4]["Sales_Revenue"].sum()
            sales_q3 = df[df["Date"].dt.quarter == 3]["Sales_Revenue"].sum()
            dispatcher.utter_message(text=f"The total sales in Q4 were {sales_q4}, compared to {sales_q3} in the previous quarter.")
        elif "growth" in latest_message:
            # Product categories with highest growth YoY
            growth = df.groupby("Product_Name")["Sales_Revenue"].sum().sort_values(ascending=False)
            top_category = growth.idxmax()
            dispatcher.utter_message(text=f"The product category with the highest growth YoY is {top_category}.")
        elif "top 5 SKUs" in latest_message:
            # Top 5 SKUs contributing to 80% of revenue
            df["Contribution"] = df["Sales_Revenue"] / df["Sales_Revenue"].sum()
            top_skus = df.sort_values(by="Contribution", ascending=False).head(5)
            sku_list = ", ".join(top_skus["Product_Name"].tolist())
            dispatcher.utter_message(text=f"The top 5 SKUs contributing to 80% of revenue are: {sku_list}.")
        elif "average sales per store" in latest_message:
            # Average sales per store for top-performing products
            avg_sales = df.groupby("Product_Name")["Sales_Revenue"].mean().sort_values(ascending=False)
            top_product = avg_sales.idxmax()
            dispatcher.utter_message(text=f"The average sales per store for {top_product} is {avg_sales.max()}.")
        elif "Brand A vs. Brand B" in latest_message:
            # Compare sales performance of Brand A vs. Brand B in the South region
            brand_a_sales = df[(df["Product_Name"] == "Brand A") & (df["Region"] == "South")]["Sales_Revenue"].sum()
            brand_b_sales = df[(df["Product_Name"] == "Brand B") & (df["Region"] == "South")]["Sales_Revenue"].sum()
            dispatcher.utter_message(text=f"In the South region, Brand A sales were {brand_a_sales}, and Brand B sales were {brand_b_sales}.")
        return []

class ActionQueryPromotionEffectiveness(Action):
    def name(self):
        return "action_query_promotion_effectiveness"

    def run(self, dispatcher, tracker, domain):
        df = pd.read_csv("NRM_DataSet_Training - All_Data.csv")
        latest_message = tracker.latest_message.get("text")

        if "highest ROI" in latest_message:
            # Promotional scheme with the highest ROI
            highest_roi = df.loc[df["Discount (%)"].idxmax()]
            promotion_name = highest_roi["Product_Name"]
            roi_value = highest_roi["Gross_Profit_Margin (%)"]
            dispatcher.utter_message(text=f"The promotional scheme with the highest ROI last quarter was {promotion_name} with an ROI of {roi_value}%.")
        elif "incremental sales" in latest_message:
            # Breakdown of incremental sales driven by discounts vs. bundling offers
            discount_sales = df[df["Discount (%)"] > 0]["Sales_Revenue"].sum()
            bundling_sales = df[df["Product_Name"].str.contains("Bundle")]["Sales_Revenue"].sum()
            dispatcher.utter_message(text=f"Incremental sales driven by discounts: {discount_sales}. Bundling offers: {bundling_sales}.")
        elif "customer retention" in latest_message:
            # Promotions with the highest customer retention
            retention = df.groupby("Product_Name")["Purchase_Frequency"].mean().sort_values(ascending=False)
            top_promotion = retention.idxmax()
            dispatcher.utter_message(text=f"The promotion with the highest customer retention is {top_promotion}.")
        elif "cannibalization" in latest_message:
            # Percentage of promotions leading to cannibalization
            cannibalization = df[df["Discount (%)"] > 0]["Returns_Units"].sum() / df["Returns_Units"].sum()
            dispatcher.utter_message(text=f"{cannibalization:.2%} of promotions led to cannibalization of other SKUs.")
        elif "Diwali campaign" in latest_message:
            # Sales performance before, during, and after Diwali campaign
            diwali_sales = df[df["Date"].str.contains("2024-10")]["Sales_Revenue"].sum()
            dispatcher.utter_message(text=f"Sales during the Diwali campaign were {diwali_sales}.")
        return []

class ActionQueryRetailInsights(Action):
    def name(self):
        return "action_query_retail_insights"

    def run(self, dispatcher, tracker, domain):
        df = pd.read_csv("NRM_DataSet_Training - All_Data.csv")
        latest_message = tracker.latest_message.get("text")

        if "stockouts" in latest_message:
            # Regions/stores with the highest stockouts
            stockouts = df.groupby("Region")["Returns_Units"].sum().idxmax()
            dispatcher.utter_message(text=f"The region with the highest stockouts last month was {stockouts}.")
        elif "heatmap" in latest_message:
            # Heatmap of sales by city for the last six months
            sales_by_city = df.groupby("Region")["Sales_Revenue"].sum()
            dispatcher.utter_message(text=f"Sales by city for the last six months: {sales_by_city.to_dict()}.")
        elif "e-commerce vs. physical stores" in latest_message:
            # Percentage of sales from e-commerce vs. physical stores
            ecommerce_sales = df[df["Channel"] == "E-commerce"]["Sales_Revenue"].sum()
            retail_sales = df[df["Channel"] == "Retail"]["Sales_Revenue"].sum()
            total_sales = ecommerce_sales + retail_sales
            ecommerce_percentage = (ecommerce_sales / total_sales) * 100
            retail_percentage = (retail_sales / total_sales) * 100
            dispatcher.utter_message(text=f"E-commerce sales: {ecommerce_percentage:.2f}%, Physical store sales: {retail_percentage:.2f}%.")
        elif "distributor" in latest_message:
            # Distributor with the highest sales volume in the last 3 months
            distributor_sales = df.groupby("Channel")["Sales_Revenue"].sum().idxmax()
            dispatcher.utter_message(text=f"The distributor with the highest sales volume in the last 3 months is {distributor_sales}.")
        elif "declining sales" in latest_message:
            # Stores with consistently declining sales over the last three quarters
            declining_stores = df.groupby("Region")["Sales_Revenue"].sum().sort_values().head(1)
            dispatcher.utter_message(text=f"The store with consistently declining sales is {declining_stores.idxmax()}.")
        return []

class ActionQueryCustomerPricingInsights(Action):
    def name(self):
        return "action_query_customer_pricing_insights"

    def run(self, dispatcher, tracker, domain):
        df = pd.read_csv("NRM_DataSet_Training - All_Data.csv")
        latest_message = tracker.latest_message.get("text")

        if "5% price increase" in latest_message:
            # Impact of a 5% price increase on sales volume
            price_increase = 1.05  # 5% increase
            df["New_Price"] = df["Retail_Price"] * price_increase
            df["New_Sales_Revenue"] = df["New_Price"] * df["Sales_Units"]
            total_revenue = df["New_Sales_Revenue"].sum()
            dispatcher.utter_message(text=f"A 5% price increase would result in total revenue of {total_revenue}.")
        elif "price-sensitive products" in latest_message:
            # Top 3 most price-sensitive products
            price_sensitivity = df.groupby("Product_Name")["Discount (%)"].mean().sort_values().head(3)
            dispatcher.utter_message(text=f"The top 3 most price-sensitive products are: {price_sensitivity.index.tolist()}.")
        elif "cross-sell potential" in latest_message:
            # SKUs with the highest cross-sell potential
            cross_sell = df.groupby("Product_Name")["Sales_Units"].sum().sort_values(ascending=False).head(3)
            dispatcher.utter_message(text=f"The SKUs with the highest cross-sell potential are: {cross_sell.index.tolist()}.")
        elif "discounts vs. cashback" in latest_message:
            # Consumer preferences for discounts vs. cashback
            discount_preference = df[df["Discount (%)"] > 0]["Sales_Revenue"].sum()
            cashback_preference = df[df["Product_Name"].str.contains("Cashback")]["Sales_Revenue"].sum()
            dispatcher.utter_message(text=f"Consumer preference for discounts: {discount_preference}, Cashback: {cashback_preference}.")
        elif "elasticity of demand" in latest_message:
            # Elasticity of demand for premium product line
            premium_products = df[df["Product_Name"].str.contains("Premium")]
            elasticity = (premium_products["Sales_Units"].sum() / premium_products["Retail_Price"].sum())
            dispatcher.utter_message(text=f"The elasticity of demand for our premium product line is {elasticity:.2f}.")
        return []

class ActionRunABTestingSimulation(Action):
    def name(self):
        return "action_run_ab_testing_simulation"

    def run(self, dispatcher, tracker, domain):
        df = pd.read_csv("NRM_DataSet_Training - All_Data.csv")
        latest_message = tracker.latest_message.get("text")

        if "reduce the price of Product X by 10%" in latest_message:
            # Simulate a 10% price reduction for Product X
            product_x = df[df["Product_Name"] == "Product X"]
            price_reduction = 0.9  # 10% reduction
            new_revenue = (product_x["Retail_Price"] * price_reduction * product_x["Sales_Units"]).sum()
            dispatcher.utter_message(text=f"A 10% price reduction for Product X would result in revenue of {new_revenue}.")
        elif "allocate 20% more budget to digital promotions" in latest_message:
            # Simulate a 20% budget increase for digital promotions
            digital_sales = df[df["Channel"] == "E-commerce"]["Sales_Revenue"].sum()
            new_sales = digital_sales * 1.2
            dispatcher.utter_message(text=f"Allocating 20% more budget to digital promotions would result in sales of {new_sales}.")
        elif "A/B test for two discount strategies" in latest_message:
            # Simulate A/B test for discount strategies
            flat_discount = df[df["Discount (%)"] == 10]["Sales_Revenue"].sum()
            buy_one_get_one = df[df["Product_Name"].str.contains("Buy 1 Get 1")]["Sales_Revenue"].sum()
            dispatcher.utter_message(text=f"Flat 10% off: {flat_discount}, Buy 1 Get 1: {buy_one_get_one}.")
        elif "next month’s sales for our best-selling SKU" in latest_message:
            # Predict next month’s sales for the best-selling SKU
            best_sku = df.groupby("Product_Name")["Sales_Revenue"].sum().idxmax()
            predicted_sales = df[df["Product_Name"] == best_sku]["Sales_Units"].mean() * 30  # Assuming 30 days
            dispatcher.utter_message(text=f"Predicted sales for {best_sku} next month: {predicted_sales}.")
        elif "removing a low-performing SKU" in latest_message:
            # Simulate the impact of removing a low-performing SKU
            low_performing_sku = df.groupby("Product_Name")["Sales_Revenue"].sum().idxmin()
            remaining_sales = df[df["Product_Name"] != low_performing_sku]["Sales_Revenue"].sum()
            dispatcher.utter_message(text=f"Removing {low_performing_sku} would result in total sales of {remaining_sales}.")
        return []

class ActionSimulateMarketDisruptions(Action):
    def name(self):
        return "action_simulate_market_disruptions"

    def run(self, dispatcher, tracker, domain):
        df = pd.read_csv("NRM_DataSet_Training - All_Data.csv")
        latest_message = tracker.latest_message.get("text")

        if "competitor launches a similar product with a 15% lower price" in latest_message:
            # Simulate competitor's price reduction impact
            competitor_price_reduction = 0.85  # 15% reduction
            df["New_Price"] = df["Retail_Price"] * competitor_price_reduction
            new_revenue = (df["New_Price"] * df["Sales_Units"]).sum()
            dispatcher.utter_message(text=f"If a competitor reduces prices by 15%, our total revenue would be {new_revenue}.")
        elif "30-day supply chain disruption" in latest_message:
            # Simulate supply chain disruption impact
            disrupted_sales = df["Sales_Revenue"].sum() * 0.7  # Assume 30% drop
            dispatcher.utter_message(text=f"A 30-day supply chain disruption would result in sales of {disrupted_sales}.")
        elif "move 10% of our offline sales budget to e-commerce" in latest_message:
            # Simulate budget reallocation impact
            offline_sales = df[df["Channel"] == "Retail"]["Sales_Revenue"].sum()
            ecommerce_sales = df[df["Channel"] == "E-commerce"]["Sales_Revenue"].sum()
            new_ecommerce_sales = ecommerce_sales * 1.1
            new_offline_sales = offline_sales * 0.9
            total_sales = new_ecommerce_sales + new_offline_sales
            dispatcher.utter_message(text=f"Moving 10% of the offline sales budget to e-commerce would result in total sales of {total_sales}.")
        elif "increase trade margins by 5%" in latest_message:
            # Simulate trade margin increase impact
            df["New_Wholesale_Price"] = df["Wholesale_Price"] * 1.05
            new_revenue = (df["New_Wholesale_Price"] * df["Sales_Units"]).sum()
            dispatcher.utter_message(text=f"Increasing trade margins by 5% would result in revenue of {new_revenue}.")
        elif "new competitor entering the market" in latest_message:
            # Simulate new competitor impact
            new_competitor_sales = df["Sales_Revenue"].sum() * 0.8  # Assume 20% drop
            dispatcher.utter_message(text=f"A new competitor entering the market would result in sales of {new_competitor_sales}.")
        return []