
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio

pio.templates.default = "plotly_white"

control_data = pd.read_csv("control_group.csv", sep= ";")
test_data = pd.read_csv("test_group.csv", sep= ";")

control_data.columns = ["Campaign Name", "Date", "Spend", "Impressions", "Reach", "Website Clicks", "Searches", "Content Viewed", "Added to Cart", "Purchases"]
test_data.columns = ["Campaign Name", "Date", "Spend", "Impressions", "Reach", "Website Clicks", "Searches", "Content Viewed", "Added to Cart", "Purchases"]

# Impressions, Reach, Website Clicks, Searches, Content Viewed, Added to Cart, Purchases = 1 Null value Fill it with mean, control_data

null_dataColumns = ["Impressions", "Reach", "Website Clicks", "Searches", "Content Viewed", "Added to Cart", "Purchases"]

# Using a loop with an array (above) would make things more modular and readable
for data in null_dataColumns:
    control_data[data].fillna(value=control_data[data].mean().astype(int), inplace=True)

ab_data = control_data.merge(test_data, how= "outer")
ab_data = ab_data.sort_values(["Date"])
ab_data = ab_data.reset_index(drop=True)

def createScatterFigure(_x, _y, _size,_source):
    fig = px.scatter(data_frame = ab_data, 
                    x=_x,
                    y=_y, 
                    size=_size, 
                    color= _source, 
                    trendline="ols")
    
    return fig

def createPieFigure(_title, _labels, _values):
    fig = go.Figure(go.Pie(labels=_labels, values=_values))
    fig.update_layout(title_text=_title)

    fig.update_traces(textfont_size=30, 
                        marker=dict(colors= ["Yellow", "Cyan"], 
                        line=dict(color="black", width=2)))
    return fig

#Spend Ratio
label = ["Total Spend from Control Campaign", "Total Spend from Test Campaign"]
value = [sum(control_data["Spend"]), sum(test_data["Spend"])]
fig_totalSpend = createPieFigure("Total Spend Control vs Test", label, value)
fig_totalSpend.show()

#Purchase Ratio
label = ["Total Purchases from Control Campaign", "Total Purchases from Test Campaign"]
value = [sum(control_data["Purchases"]), sum(test_data["Purchases"])]
fig_totalPurchases = createPieFigure("Total Purchases Control vs Test", label, value)
fig_totalPurchases.show()

fig_addedToCart_purchases = createScatterFigure("Added to Cart", "Purchases", "Purchases", "Campaign Name")
fig_addedToCart_purchases.show()