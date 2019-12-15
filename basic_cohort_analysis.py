#!/usr/bin/env python
import pandas as pd
import datetime as dt
import seaborn as sns
import matplotlib.pyplot as plt

# Data Source: https://archive.ics.uci.edu/ml/machine-learning-databases/00502/online_retail_II.xlsx
df = pd.read_csv("OnlineRetail.csv", encoding="ISO-8859-1", parse_dates=["InvoiceDate"])

df.dropna(axis="index", subset=["CustomerID"], inplace=True)
df["InvoiceMonth"] = df["InvoiceDate"].map(lambda x: dt.datetime(x.year, x.month, 1))
df["CohortMonth"] = df.groupby("CustomerID")["InvoiceMonth"].transform("min")


def cohort_index_input(df, column):
    year = df[column].dt.year
    month = df[column].dt.month
    day = df[column].dt.day
    return year, month, day


invoice_year, invoice_month, _ = cohort_index_input(df, "InvoiceMonth")
cohort_year, cohort_month, _ = cohort_index_input(df, "CohortMonth")
years_diff = invoice_year - cohort_year
months_diff = invoice_month - cohort_month
df["CohortIndex"] = years_diff * 12 + months_diff + 1


# Count monthly active customers from each cohort
df_chrtcid = (
    df.groupby(["CohortMonth", "CohortIndex"])["CustomerID"].nunique().reset_index()
)
chrt_cid = df_chrtcid.pivot(
    index="CohortMonth", columns="CohortIndex", values="CustomerID"
)
chrt_sizes = chrt_cid.iloc[:, 0]
cid_retention = chrt_cid.divide(chrt_sizes, axis=0)
cid_retention.round(3) * 100
cid_retention.index = cid_retention.index.strftime("%m-%Y")


plt.figure(figsize=(10, 8))
plt.title("Retention rates")
sns.heatmap(data=cid_retention, annot=True, fmt=".0%", vmin=0.0, vmax=0.5, cmap="BuGn")
plt.show()


# Average Quantity Cohorts
df_chrtq = df.groupby(["CohortMonth", "CohortIndex"])["Quantity"].mean().reset_index()
chrtq = df_chrtq.pivot(index="CohortMonth", columns="CohortIndex", values="Quantity")
chrtq.index = chrtq.index.strftime("%m-%Y")

plt.figure(figsize=(10, 8))
plt.title("Average Quantity")
sns.heatmap(data=chrtq, annot=True, cmap="Blues")
plt.show()


# Average UnitPrice Cohorts
df_chrtup = df.groupby(["CohortMonth", "CohortIndex"])["UnitPrice"].mean().reset_index()
chrtup = df_chrtup.pivot(index="CohortMonth", columns="CohortIndex", values="UnitPrice")
chrtup.index = chrtup.index.strftime("%m-%Y")


plt.figure(figsize=(10, 8))
plt.title("Average Price")
sns.heatmap(data=chrtup, annot=True, cmap="Blues")
plt.show()

