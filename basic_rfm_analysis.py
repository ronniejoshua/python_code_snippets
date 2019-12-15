import pandas as pd
import numpy as np
import datetime as dt

# importing data for RFM analysis
ord_df = pd.read_csv(
    "./rfm_analysis_data.csv", encoding="ISO-8859-1", parse_dates=["order_date"]
)

# Finding the date range of transactions
ord_dt_min = ord_df["order_date"].min()
ord_dt_max = ord_df["order_date"].max()


# creating a rfm dataframe using group by
rfm_df = ord_df.groupby(["customer"]).agg(
    {
        "order_date": lambda x: (ord_dt_max - x.max()).days,  # Recency
        "order_id": lambda x: len(x),  # Frequency
        "grand_total": lambda x: x.sum(),  # Monetary Value
    }
)

# converting the order_date to integer value
rfm_df["order_date"] = rfm_df["order_date"].astype(int)


# renaming the columns
rfm_df.rename(
    columns={
        "order_date": "recency",
        "order_id": "frequency",
        "grand_total": "monetary_value",
    },
    inplace=True,
)

# Validating the RFM Table:
aaron = ord_df[ord_df["customer"] == "Aaron Bergman"]
(ord_dt_max - dt.datetime(2013, 11, 11)).days == 415


# Creating Quantiles for segmentations [Q1, Q2, Q3]
quantiles = rfm_df.quantile(q=[0.25, 0.5, 0.75])
quantiles = quantiles.to_dict()
rfmseg_df = rfm_df

# Creating a Segmenter function:
def RSegmenter(x, str_rmf, qd):
    """
    x : the df column(recency)
    str_rmf: the column label 'recency'
    qd : the quantiles dictionary
    return : int the lower the better [1 brought recently]
    """
    if x <= qd[str_rmf][0.25]:
        return 1
    elif x <= qd[str_rmf][0.50]:
        return 2
    elif x <= qd[str_rmf][0.75]:
        return 3
    else:
        return 4


def FMSegmenter(x, str_rmf, qd):
    """
    x : the df column(frequency, monetary_value)
    str_rmf: the column label 'frequency' & 'monetary_value'
    qd : the quantiles dictionary
    return : int the higher the better [1 higher value | more frequent]
    """
    if x <= qd[str_rmf][0.25]:
        return 4
    elif x <= qd[str_rmf][0.50]:
        return 3
    elif x <= qd[str_rmf][0.75]:
        return 2
    else:
        return 1


# Applying the "Segmenter" functions
rfmseg_df["R_Quartile"] = rfmseg_df["recency"].apply(
    RSegmenter, args=("recency", quantiles)
)
rfmseg_df["F_Quartile"] = rfmseg_df["frequency"].apply(
    FMSegmenter, args=("frequency", quantiles)
)
rfmseg_df["M_Quartile"] = rfmseg_df["monetary_value"].apply(
    FMSegmenter, args=("monetary_value", quantiles)
)

# Creating the combined segmenter column
rfmseg_df["RFMSegments"] = (
    rfmseg_df.R_Quartile.map(str)
    + rfmseg_df.F_Quartile.map(str)
    + rfmseg_df.M_Quartile.map(str)
)

rfm_seg_m = rfmseg_df.groupby("RFMSegments").agg("monetary_value").mean().reset_index()
rfm_seg_e = rfmseg_df.groupby("RFMSegments").agg("recency").mean().reset_index()
rfm_seg_f = rfmseg_df.groupby("RFMSegments").agg("frequency").mean().reset_index()


# Creating agggregated segmenter column
rfmseg_df["RFMScore"] = rfmseg_df[["R_Quartile", "F_Quartile", "M_Quartile"]].sum(
    axis=1
)

rfm_ts_m = rfmseg_df.groupby("RFMScore").agg("monetary_value").mean().reset_index()
rfm_ts_e = rfmseg_df.groupby("RFMScore").agg("recency").mean().reset_index()
rfm_ts_f = rfmseg_df.groupby("RFMScore").agg("frequency").mean().reset_index()

# top customers in the premium segment [111]
rfmseg_df[rfmseg_df["RFMSegments"] == "111"].sort_values(
    ["RFMSegments", "monetary_value"], ascending=[True, False]
)


# Illustration 2:
# --------------

df = pd.read_csv("OnlineRetail.csv", encoding="ISO-8859-1", parse_dates=["InvoiceDate"])


df = df[df.Country == "United Kingdom"]
df = df[pd.notnull(df["CustomerID"])]
df["Revenue"] = df["UnitPrice"] * df["Quantity"]
df = df[(df["Quantity"] > 0)]
df = df[["CustomerID", "InvoiceDate", "InvoiceNo", "Quantity", "UnitPrice", "Revenue"]]

print("Min:{}; Max:{}".format(df["InvoiceDate"].min(), df["InvoiceDate"].max()))

snapshot_date = max(df.InvoiceDate) + dt.timedelta(days=1)

# Aggregate data on a customer level
rfm = df.groupby("CustomerID").agg(
    {
        "InvoiceDate": lambda date: (snapshot_date - date.max()).days,
        "InvoiceNo": lambda num: len(num),
        "Revenue": lambda price: price.sum(),
    }
)

# Alternatively:
# rfm = df.groupby(['CustomerID']).agg({
#     'InvoiceDate': lambda date: (snapshot_date - date.max()).days,
#     'InvoiceNo': 'count',
#     'TotalSum': 'sum'})

# Rename columns for easier interpretation
rfm.rename(
    columns={"InvoiceDate": "recency", "InvoiceNo": "frequency", "Revenue": "monetary"},
    inplace=True,
)

rfm["recency"] = rfm["recency"].astype(int)


# Creating rmf_segment:
def join_rfm(x):
    return str(x["r_quartile"]) + str(x["f_quartile"]) + str(x["m_quartile"])


rfm["rfm_segment"] = rfm.apply(join_rfm, axis=1)

# Creating rmf_score
rfm["rfm_score"] = rfm[["r_quartile", "f_quartile", "m_quartile"]].sum(axis=1)


# rfm_score insigts
rfm.groupby("rfm_score").agg(
    {"recency": "mean", "frequency": "mean", "monetary": ["mean", "count"]}
).round(1)


# Defining custom label for rfm_score segments
def rfm_score_segmenter(df):
    if df["rfm_score"] >= 9:
        return "bronze"
    elif (df["rfm_score"] >= 5) and (df["rfm_score"] < 9):
        return "silver"
    else:
        return "gold"


rfm["general_segments"] = rfm.apply(rfm_score_segmenter, axis=1)

rfm.groupby("general_segments").agg(
    {"recency": "mean", "frequency": "mean", "monetary": ["mean", "count"]}
).round(1)

