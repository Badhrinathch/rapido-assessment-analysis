"""
Rapido Data Science Assessment — reproducible analysis.
Run from the folder containing the seven raw CSVs:
    python analysis.py
Outputs key summary CSVs and prints headline findings.
"""
import pandas as pd, numpy as np
from pathlib import Path

DATA = Path(".")
files = ["captains.csv","doc_events.csv","approvals.csv","activation.csv",
         "nudges.csv","airport_hourly.csv","airport_trips.csv"]

dfs = {f: pd.read_csv(DATA/f) for f in files}
cap, docs, app, act, nud, ah, tr = [dfs[f] for f in files]

for df, c in [(cap,"signup_ts"),(docs,"event_ts"),(app,"decision_ts"),
              (act,"first_order_ts"),(nud,"sent_ts"),(ah,"hour_ts"),(tr,"request_ts")]:
    if c in df: df[c] = pd.to_datetime(df[c], errors="coerce")

# June is right-censored because the source extract ends 2026-06-30.
cohort = cap.merge(app, on="captain_id")
m = cohort[cohort.signup_ts.dt.month <= 5].copy()

def stage_mask(df, stage):
    if stage <= 3: return df.docs_cleared >= stage
    if stage == 4:
        return ((df.vehicle_type.isin(["Auto","Cab"])&(df.docs_cleared>=4)) |
                (df.vehicle_type.eq("ERickshaw")&(df.docs_cleared>=3)))
    if stage == 5:
        return ((df.vehicle_type.isin(["Auto","Cab"])&(df.docs_cleared>=5)) |
                (df.vehicle_type.eq("ERickshaw")&(df.docs_cleared>=4)))
    return ((df.vehicle_type.isin(["Auto","Cab"])&(df.docs_cleared>=6)) |
            (df.vehicle_type.eq("ERickshaw")&(df.docs_cleared>=5)))

labels=["DL","RC","AADHAAR",
        "PERMIT (Auto/Cab) / FITNESS (ERickshaw)",
        "FITNESS (Auto/Cab) / INSURANCE (ERickshaw)","INSURANCE"]
for i,label in enumerate(labels,1):
    n=stage_mask(m,i).sum()
    print(f"{label:45s} {n:6d}  {n/len(m):6.1%}")
print("APPROVED", (m.final_status=="approved").sum(),
      f"{(m.final_status=='approved').mean():.1%}")

# Segment cuts.
for col in ["city","vehicle_type","acquisition_channel","device_tier","app_language","age_band"]:
    g=m.groupby(col).agg(signups=("captain_id","size"),
                          approved=("final_status",lambda s:s.eq("approved").sum()))
    g["approval_rate"]=g.approved/g.signups
    print("\n",col,"\n",g.sort_values("approval_rate"))

# Airport terminal demand/supply.
apt=ah[ah.zone_type=="airport_terminal"].copy()
apt["hour"]=apt.hour_ts.dt.hour
h=apt.groupby("hour").agg(requests=("requests","sum"),
    fulfilled=("fulfilled_requests","sum"),unfulfilled=("unfulfilled_requests","sum"),
    captain_hours=("online_captains","sum"))
h["fill_rate"]=h.fulfilled/h.requests
h["rides_per_captain_hour"]=h.fulfilled/h.captain_hours
h["extra_online_captains"]=(h.unfulfilled/h.rides_per_captain_hour)/61
print("\nAirport total fill:",apt.fulfilled_requests.sum()/apt.requests.sum())
print("\nWorst hours:\n",h.sort_values("unfulfilled",ascending=False).head(6))
