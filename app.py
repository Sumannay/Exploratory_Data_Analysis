"""InsightLab: Customer Retail Analytics Platform.

Three executive dashboards:
  1. Customer Analysis
  2. Customer Segmentation RFM
  3. Segmentation Analytical Insight
"""

from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="InsightLab | Customer Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
[data-testid="stSidebar"] { background: #1a2332; }
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
.kpi-card {
    background: linear-gradient(135deg, #1e40af 0%, #1d4ed8 100%);
    border-radius: 12px; padding: 18px 22px; color: #fff;
    margin-bottom: 8px; box-shadow: 0 4px 15px rgba(30,64,175,0.35);
}
.kpi-card.teal  { background: linear-gradient(135deg, #0d9488, #0f766e); }
.kpi-card.green { background: linear-gradient(135deg, #059669, #047857); }
.kpi-card.amber { background: linear-gradient(135deg, #d97706, #b45309); }
.kpi-val { font-size:1.7rem; font-weight:700; }
.kpi-sub { font-size:0.75rem; opacity:0.8; margin-top:2px; }
.sec-title { font-size:1rem; font-weight:600; color:#1e293b;
             margin-bottom:6px; padding-bottom:4px;
             border-bottom:2px solid #e2e8f0; }
.main-hdr { font-size:1.7rem; font-weight:700; color:#1e293b; }
.insight-box { background:#f8fafc; border:1px solid #e2e8f0;
               border-radius:10px; padding:14px 16px; margin-top:8px; }
.insight-title { font-size:0.75rem; font-weight:700; color:#1e40af;
                 text-transform:uppercase; letter-spacing:0.6px; }
.insight-val { font-size:1.3rem; font-weight:700; color:#1e293b; }
.insight-sub { font-size:0.75rem; color:#64748b; }
.warn-box { background:#fef9c3; border:1px solid #fbbf24;
            border-radius:10px; padding:12px 14px; margin-top:10px; }
.warn-val { font-size:1.1rem; font-weight:700; color:#92400e; }
.warn-sub { font-size:0.75rem; color:#78350f; }
</style>
""", unsafe_allow_html=True)

# ── Data Paths ──
BASE_DIR = Path(__file__).resolve().parent
TX_FILE  = BASE_DIR / "data" / "processed" / "retail_customer_analytics.csv"
RFM_FILE = BASE_DIR / "data" / "processed" / "customer_rfm_summary.csv"

if not TX_FILE.exists():
    st.error("Dataset not found. Run:  `python src/retail_analytics.py`")
    st.stop()

@st.cache_data(show_spinner=False)
def load_data():
    tx  = pd.read_csv(TX_FILE, parse_dates=["order_date"])
    rfm = pd.read_csv(RFM_FILE)
    return tx, rfm

tx_raw, rfm_raw = load_data()

# ── Sidebar ──
st.sidebar.markdown("## 📊 InsightLab")
st.sidebar.caption("Customer Retail Analytics Platform")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Dashboard",
    ["📈 Customer Analysis",
     "🎯 Customer Segmentation RFM",
     "🔍 Segmentation Analytical Insight"],
    label_visibility="collapsed"
)
st.sidebar.markdown("---")

categories = sorted(tx_raw["category"].dropna().unique().tolist())
sel_cat = st.sidebar.selectbox("Select Category", ["All"] + categories)

months = sorted(tx_raw["year_month"].unique().tolist())
if len(months) >= 2:
    st.sidebar.markdown("**Date Range**")
    m_start, m_end = st.sidebar.select_slider(
        "date_range", options=months,
        value=(months[0], months[-1]),
        label_visibility="collapsed"
    )
else:
    m_start, m_end = months[0], months[-1]

tx = tx_raw.copy()
rfm = rfm_raw.copy()
if sel_cat != "All":
    tx = tx[tx["category"] == sel_cat]
tx = tx[(tx["year_month"] >= m_start) & (tx["year_month"] <= m_end)]

st.sidebar.markdown("---")
st.sidebar.info(f"""
**Dataset Summary**
- Transactions: {len(tx):,}
- Customers: {tx['customer_name'].nunique():,}
- Total Revenue: ${tx['sales_amount'].sum():,.0f}
""")

SEG_COLORS = {
    "Champion": "#2563eb", "Loyal Customer": "#0d9488",
    "Potential Loyalist": "#f59e0b", "At Risk": "#ef4444",
    "Others": "#6b7280", "Lost Customers": "#94a3b8"
}

PLOT_CFG = dict(use_container_width=True)

# ══════════════════════════════════════════════
# DASHBOARD 1 – CUSTOMER ANALYSIS
# ══════════════════════════════════════════════
if page == "📈 Customer Analysis":
    total_rev = tx["sales_amount"].sum()

    hc1, hc2, hc3 = st.columns([2, 2, 1.5])
    with hc1:
        st.markdown('<div class="main-hdr">Customer Analysis</div>', unsafe_allow_html=True)
    with hc2:
        st.markdown(f"**Category:** `{sel_cat}`")
    with hc3:
        st.markdown(f"""<div style='text-align:right'>
            <div style='font-size:0.75rem;color:#64748b'>Total Revenue</div>
            <div style='font-size:1.5rem;font-weight:700;color:#1e293b'>${total_rev:,.0f}</div>
        </div>""", unsafe_allow_html=True)
    st.markdown("---")

    # Row 1
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown('<div class="sec-title">Month-Wise Revenue</div>', unsafe_allow_html=True)
        mo = (tx.groupby("year_month")["sales_amount"].sum()
                .reset_index().sort_values("year_month"))
        mo.columns = ["Month", "Revenue"]
        fig = px.bar(mo, x="Month", y="Revenue",
                     color_discrete_sequence=["#3b82f6"],
                     text=mo["Revenue"].apply(
                         lambda v: f"${v/1e6:.1f}M" if v >= 1e6 else f"${v/1e3:.0f}K"))
        fig.update_traces(textposition="outside", textfont_size=8)
        fig.update_layout(height=260, margin=dict(t=10,b=50,l=0,r=0),
                          plot_bgcolor="white",
                          xaxis=dict(tickangle=45, tickfont=dict(size=8)),
                          yaxis=dict(showgrid=True, gridcolor="#f1f5f9", title=""),
                          showlegend=False)
        st.plotly_chart(fig, key="ch_mo", **PLOT_CFG)

    with c2:
        st.markdown('<div class="sec-title">Revenue per State</div>', unsafe_allow_html=True)
        sr = tx.groupby("state")["sales_amount"].sum().reset_index()
        sr.columns = ["state", "Revenue"]
        fig = px.choropleth(sr, locations="state", locationmode="USA-states",
                            color="Revenue",
                            color_continuous_scale=["#dbeafe", "#1d4ed8"],
                            scope="usa")
        fig.update_layout(height=260, margin=dict(t=0,b=0,l=0,r=0),
                          coloraxis_showscale=False,
                          geo=dict(bgcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig, key="ch_map", **PLOT_CFG)

    with c3:
        st.markdown('<div class="sec-title">Age-Wise Sales Analysis</div>', unsafe_allow_html=True)
        bins = [0,25,35,45,55,65,100]
        lbls = ["<25","25-34","35-44","45-54","55-64","65+"]
        tx2 = tx.copy()
        tx2["age_group"] = pd.cut(tx2["age"], bins=bins, labels=lbls, right=False)
        ar = tx2.groupby("age_group", observed=True)["sales_amount"].sum().reset_index()
        fig = px.bar(ar, x="sales_amount", y="age_group", orientation="h",
                     color_discrete_sequence=["#0d9488"],
                     text=ar["sales_amount"].apply(lambda v: f"${v/1e3:.0f}K"))
        fig.update_traces(textposition="outside", textfont_size=8)
        fig.update_layout(height=260, margin=dict(t=10,b=10,l=0,r=20),
                          plot_bgcolor="white",
                          xaxis=dict(showgrid=True, gridcolor="#f1f5f9", title=""),
                          yaxis=dict(title=""),
                          showlegend=False)
        st.plotly_chart(fig, key="ch_age", **PLOT_CFG)

    # Row 2
    c4, c5, c6 = st.columns(3)

    with c4:
        st.markdown('<div class="sec-title">Region-Wise Revenue Share (%)</div>', unsafe_allow_html=True)
        rr = tx.groupby("region")["sales_amount"].sum().reset_index()
        rc = {"West":"#3b82f6","Northeast":"#f59e0b","South":"#ef4444","Midwest":"#8b5cf6"}
        fig = px.pie(rr, values="sales_amount", names="region",
                     color="region", color_discrete_map=rc, hole=0.45)
        fig.update_traces(textinfo="percent+label", textfont_size=10)
        fig.update_layout(height=260, margin=dict(t=10,b=10,l=0,r=0), showlegend=False)
        st.plotly_chart(fig, key="ch_reg", **PLOT_CFG)

    with c5:
        st.markdown('<div class="sec-title">Gender-Wise Sales Analysis</div>', unsafe_allow_html=True)
        gc = (tx.groupby(["category","gender"])["sales_amount"].sum()
                .reset_index()
                .pivot(index="category", columns="gender", values="sales_amount")
                .fillna(0).reset_index())
        fig = go.Figure()
        for gender, color in [("Female","#ec4899"),("Male","#3b82f6")]:
            if gender in gc.columns:
                fig.add_trace(go.Bar(
                    y=gc["category"], x=gc[gender], name=f"{gender}",
                    orientation="h", marker_color=color,
                    text=gc[gender].apply(lambda v: f"${v/1e6:.2f}M"),
                    textposition="inside", textfont_size=7
                ))
        fig.update_layout(barmode="group", height=260,
                          margin=dict(t=10,b=20,l=0,r=0),
                          plot_bgcolor="white",
                          xaxis=dict(showgrid=True, gridcolor="#f1f5f9", title=""),
                          yaxis=dict(tickfont=dict(size=8), title=""),
                          legend=dict(orientation="h", y=-0.18, font=dict(size=8)))
        st.plotly_chart(fig, key="ch_gen", **PLOT_CFG)

    with c6:
        st.markdown('<div class="sec-title">Quantity–Discount Correlation</div>', unsafe_allow_html=True)
        smp = tx.sample(min(600, len(tx)), random_state=42)
        fig = px.scatter(smp, x="discount_percent", y="quantity",
                         color_discrete_sequence=["#3b82f6"],
                         opacity=0.5, trendline="ols",
                         trendline_color_override="#ef4444",
                         labels={"discount_percent":"Discount %","quantity":"Qty"})
        fig.update_layout(height=260, margin=dict(t=10,b=20,l=0,r=0),
                          plot_bgcolor="white",
                          xaxis=dict(showgrid=True, gridcolor="#f1f5f9"),
                          yaxis=dict(showgrid=True, gridcolor="#f1f5f9"))
        st.plotly_chart(fig, key="ch_disc", **PLOT_CFG)


# ══════════════════════════════════════════════
# DASHBOARD 2 – RFM SEGMENTATION
# ══════════════════════════════════════════════
elif page == "🎯 Customer Segmentation RFM":

    st.markdown("""
    <div style="background:linear-gradient(90deg,#1e40af,#1d4ed8);
                border-radius:10px;padding:16px 22px;margin-bottom:18px;">
      <div style="font-size:1.3rem;font-weight:700;color:#fff">
        📊 Customer Segmentation Analysis</div>
      <div style="font-size:0.78rem;color:#bfdbfe">RFM Analysis</div>
    </div>""", unsafe_allow_html=True)

    f1, f2, f3 = st.columns(3)
    with f1:
        seg_opts = ["All"] + sorted(rfm["Segment"].dropna().unique())
        sel_seg = st.selectbox("Segment", seg_opts, key="d2_seg")
    with f2:
        reg_opts = ["All"] + sorted(rfm["region"].dropna().unique())
        sel_reg = st.selectbox("Region", reg_opts, key="d2_reg")
    with f3:
        st.selectbox("Date Range", ["Last 12 Months"], key="d2_date")

    rfm_f = rfm.copy()
    if sel_seg != "All":
        rfm_f = rfm_f[rfm_f["Segment"] == sel_seg]
    if sel_reg != "All":
        rfm_f = rfm_f[rfm_f["region"] == sel_reg]

    # KPIs
    k1, k2, k3, k4 = st.columns(4)
    avg_rec  = rfm_f["Sum_of_Recency"].mean() if len(rfm_f) else 0
    avg_freq = rfm_f["Frequency"].mean() if len(rfm_f) else 0
    avg_mon  = rfm_f["Monetary"].mean() if len(rfm_f) else 0
    n_cust   = len(rfm_f)

    with k1:
        st.markdown(f"""<div class="kpi-card teal">
            <div style="font-size:1rem;font-weight:600">🕐 Recency</div>
            <div class="kpi-val">{avg_rec:.1f} Days Avg.</div>
            <div class="kpi-sub">Days since last purchase</div>
        </div>""", unsafe_allow_html=True)
    with k2:
        st.markdown(f"""<div class="kpi-card">
            <div style="font-size:1rem;font-weight:600">📅 Frequency</div>
            <div class="kpi-val">{avg_freq:.1f} Orders Avg.</div>
            <div class="kpi-sub">Avg orders per customer</div>
        </div>""", unsafe_allow_html=True)
    with k3:
        st.markdown(f"""<div class="kpi-card green">
            <div style="font-size:1rem;font-weight:600">💰 Monetary</div>
            <div class="kpi-val">${avg_mon:,.0f}</div>
            <div class="kpi-sub">Revenue Avg. per customer</div>
        </div>""", unsafe_allow_html=True)
    with k4:
        st.markdown(f"""<div class="kpi-card amber">
            <div style="font-size:1rem;font-weight:600">👥 Customers</div>
            <div class="kpi-val">{n_cust:,}</div>
            <div class="kpi-sub">Filtered total</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    lc, mc, rc = st.columns([1.2, 1.8, 1.1])

    with lc:
        st.markdown("**Customer Segments**")
        sc = rfm_f["Segment"].value_counts().reset_index()
        sc.columns = ["Segment", "Count"]
        fig = px.bar(sc, x="Segment", y="Count",
                     color="Segment", color_discrete_map=SEG_COLORS, text="Count")
        fig.update_traces(textposition="outside", textfont_size=9)
        fig.update_layout(height=250, margin=dict(t=5,b=60,l=0,r=0),
                          plot_bgcolor="white",
                          xaxis=dict(tickangle=30, tickfont=dict(size=8)),
                          yaxis=dict(showgrid=True, gridcolor="#f1f5f9", title=""),
                          showlegend=False)
        st.plotly_chart(fig, key="d2_seg_bar", **PLOT_CFG)

        st.markdown("**Segment Distribution**")
        fig = px.pie(sc, values="Count", names="Segment",
                     color="Segment", color_discrete_map=SEG_COLORS, hole=0.4)
        fig.update_traces(textinfo="percent+label", textfont_size=8)
        fig.update_layout(height=220, margin=dict(t=5,b=5,l=0,r=0), showlegend=False)
        st.plotly_chart(fig, key="d2_seg_pie", **PLOT_CFG)

    with mc:
        st.markdown("**RFM Score Heatmap**")
        rfm_f2 = rfm_f.copy()
        if len(rfm_f2) >= 10:
            try:
                rfm_f2["R_q"] = pd.qcut(rfm_f2["Sum_of_Recency"], 5,
                                         labels=[5,4,3,2,1], duplicates="drop").astype(int)
                rfm_f2["F_q"] = pd.qcut(rfm_f2["Frequency"].rank(method="first"), 5,
                                         labels=[1,2,3,4,5], duplicates="drop").astype(int)
            except Exception:
                rfm_f2["R_q"] = 3; rfm_f2["F_q"] = 3
        else:
            rfm_f2["R_q"] = 3; rfm_f2["F_q"] = 3

        hd = rfm_f2.groupby(["R_q","F_q"])["Monetary"].sum().reset_index()
        hp = hd.pivot(index="R_q", columns="F_q", values="Monetary").fillna(0)
        for i in range(1,6):
            if i not in hp.index:    hp.loc[i] = 0
            if i not in hp.columns: hp[i] = 0
        hp = hp.sort_index(ascending=False)[sorted(hp.columns)]

        seg_lbl = {
            (5,5):"Champions",(5,4):"Champions",(4,5):"Champions",
            (5,3):"Loyal Customers",(4,4):"Loyal Customers",(3,5):"Loyal Customers",
            (3,3):"Potential Loyalists",(4,2):"Potential Loyalists",
            (2,2):"At Risk",(2,3):"At Risk",(1,3):"At Risk",
            (1,1):"Lost Customers",(1,2):"Lost Customers",(2,1):"Lost Customers",
        }
        txt = []
        for r in sorted(hp.index, reverse=True):
            row = []
            for f in sorted(hp.columns):
                lbl = seg_lbl.get((r,f),"")
                row.append(f"● {lbl}" if lbl else "")
            txt.append(row)

        cscale = [[0,"#ef4444"],[0.25,"#f97316"],[0.5,"#fbbf24"],
                  [0.75,"#86efac"],[1,"#22c55e"]]
        fig = go.Figure(go.Heatmap(
            z=hp.values,
            x=[str(c) for c in sorted(hp.columns)],
            y=[str(r) for r in sorted(hp.index, reverse=True)],
            text=txt, texttemplate="%{text}",
            textfont=dict(size=8, color="white"),
            colorscale=cscale, showscale=False,
            xgap=3, ygap=3
        ))
        fig.update_layout(height=430, margin=dict(t=10,b=40,l=40,r=10),
                          xaxis=dict(title="Frequency Score (F)"),
                          yaxis=dict(title="Recency Score (R)"))
        st.plotly_chart(fig, key="d2_heat", **PLOT_CFG)

    with rc:
        st.markdown("**Insights**")
        champs   = rfm_f[rfm_f["Segment"]=="Champion"]
        at_risk  = rfm_f[rfm_f["Segment"]=="At Risk"]
        champ_rev = champs["Monetary"].sum()
        ar_cnt   = len(at_risk)
        loyal_pct = len(rfm_f[rfm_f["Segment"]=="Loyal Customer"]) / max(len(rfm_f),1) * 100

        st.markdown(f"""
        <div class="insight-box">
          <div class="insight-title">Top Revenue Segment</div>
          <div class="insight-val">Champions: ${champ_rev/1e3:.1f}K</div>
          <div class="insight-sub">Total Revenue</div>
        </div>
        <div class="warn-box">
          <div class="insight-title" style="color:#92400e">⚠️ At-Risk Customers</div>
          <div class="warn-val">{ar_cnt:,}</div>
          <div class="warn-sub">Customers with declining activity.<br>Consider re-engagement campaigns.</div>
        </div>
        <div class="insight-box" style="margin-top:10px">
          <div class="insight-title">Avg Order Value</div>
          <div class="insight-val">${rfm_f['Monetary'].mean()/max(rfm_f['Frequency'].mean(),1):.0f}</div>
          <div class="insight-sub">Revenue per transaction</div>
        </div>
        <div class="insight-box" style="margin-top:10px">
          <div class="insight-title">Loyal Customer %</div>
          <div class="insight-val">{loyal_pct:.1f}%</div>
          <div class="insight-sub">of filtered base</div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# DASHBOARD 3 – ANALYTICAL INSIGHT
# ══════════════════════════════════════════════
elif page == "🔍 Segmentation Analytical Insight":

    h1, h2 = st.columns([3, 1])
    with h1:
        st.markdown("""
        <div class="main-hdr">Customer Segmentation Analytical Insight</div>
        <div style="font-size:0.85rem;color:#64748b">Product Category: All &nbsp;|&nbsp; Full Dataset</div>
        """, unsafe_allow_html=True)
    with h2:
        st.markdown(f"<div style='text-align:right;padding-top:10px;font-size:0.8rem;color:#64748b'>{m_start} – {m_end}</div>",
                    unsafe_allow_html=True)
    st.markdown("---")

    # KPI row
    total_cust = len(rfm)
    loyal_n    = len(rfm[rfm["Segment"]=="Loyal Customer"])
    at_risk_n  = len(rfm[rfm["Segment"]=="At Risk"])
    avg_rfm    = rfm["Frequency"].mean()

    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric("Total Transactions", f"{len(tx_raw):,}")
    with m2: st.metric("Total Customers", f"{total_cust:,}")
    with m3: st.metric("Loyal Customer Fill", f"{loyal_n/total_cust*100:.2f}%")
    with m4: st.metric("At Risk %", f"{at_risk_n/total_cust*100:.2f}%")

    st.markdown("<br>", unsafe_allow_html=True)

    l, m, r = st.columns([1.3, 1.3, 1.5])

    with l:
        st.markdown('<div class="sec-title">Customer Distribution – By Segment</div>',
                    unsafe_allow_html=True)
        sd = rfm["Segment"].value_counts().reset_index()
        sd.columns = ["Segment","Count"]
        fig = px.pie(sd, values="Count", names="Segment",
                     color="Segment", color_discrete_map=SEG_COLORS, hole=0.45)
        fig.update_traces(textinfo="percent", textfont_size=8)
        fig.update_layout(height=210, margin=dict(t=5,b=5,l=0,r=0),
                          legend=dict(font=dict(size=8)))
        st.plotly_chart(fig, key="d3_seg_pie", **PLOT_CFG)

        st.markdown('<div class="sec-title">Customer Distribution – By City</div>',
                    unsafe_allow_html=True)
        cc = rfm["city"].value_counts().head(5).reset_index()
        cc.columns = ["City","Count"]
        fig = px.bar(cc, x="Count", y="City", orientation="h",
                     color_discrete_sequence=["#3b82f6"], text="Count")
        fig.update_traces(textposition="outside", textfont_size=9)
        fig.update_layout(height=175, margin=dict(t=5,b=5,l=0,r=20),
                          plot_bgcolor="white",
                          xaxis=dict(showgrid=True, gridcolor="#f1f5f9", title=""),
                          yaxis=dict(title=""))
        st.plotly_chart(fig, key="d3_city", **PLOT_CFG)

    with m:
        st.markdown('<div class="sec-title">Customer Distribution – By Customer Type</div>',
                    unsafe_allow_html=True)
        ct = rfm["customer_type"].value_counts().reset_index()
        ct.columns = ["Type","Count"]
        fig = px.pie(ct, values="Count", names="Type",
                     color_discrete_sequence=["#3b82f6","#f59e0b"], hole=0.45)
        fig.update_traces(textinfo="percent+label", textfont_size=10)
        fig.update_layout(height=210, margin=dict(t=5,b=5,l=0,r=0), showlegend=False)
        st.plotly_chart(fig, key="d3_ctype", **PLOT_CFG)

        st.markdown('<div class="sec-title">Distribution – Segment & Customer Type</div>',
                    unsafe_allow_html=True)
        sct = rfm.groupby(["Segment","customer_type"]).size().reset_index(name="Count")
        fig = px.bar(sct, x="Count", y="Segment", color="customer_type",
                     orientation="h", barmode="stack",
                     color_discrete_map={"New":"#3b82f6","Returning":"#f59e0b"},
                     text="Count")
        fig.update_traces(textposition="inside", textfont_size=7)
        fig.update_layout(height=175, margin=dict(t=5,b=5,l=0,r=10),
                          plot_bgcolor="white",
                          xaxis=dict(showgrid=True, gridcolor="#f1f5f9", title=""),
                          yaxis=dict(tickfont=dict(size=8), title=""),
                          legend=dict(font=dict(size=8), title=""))
        st.plotly_chart(fig, key="d3_sct", **PLOT_CFG)

    with r:
        st.markdown('<div class="sec-title">Top Customers – By Sales</div>',
                    unsafe_allow_html=True)
        tc = rfm.nlargest(10,"Monetary")[["customer_name","Monetary"]].reset_index(drop=True)
        tc.columns = ["Customer","Revenue"]
        fig = px.bar(tc, x="Revenue", y="Customer", orientation="h",
                     color_discrete_sequence=["#1d4ed8"],
                     text=tc["Revenue"].apply(lambda v: f"${v/1e3:.0f}K"))
        fig.update_traces(textposition="outside", textfont_size=8)
        fig.update_layout(height=275, margin=dict(t=5,b=5,l=0,r=30),
                          plot_bgcolor="white",
                          xaxis=dict(showgrid=True, gridcolor="#f1f5f9", title="Revenue"),
                          yaxis=dict(title="", autorange="reversed"))
        st.plotly_chart(fig, key="d3_top", **PLOT_CFG)

        st.markdown('<div class="sec-title">Sales Contribution – Treemap</div>',
                    unsafe_allow_html=True)
        sr2 = rfm.groupby("Segment")["Monetary"].sum().reset_index()
        fig = px.treemap(sr2, path=["Segment"], values="Monetary",
                         color="Segment", color_discrete_map=SEG_COLORS)
        fig.update_traces(textinfo="label+percent root")
        fig.update_layout(height=115, margin=dict(t=5,b=5,l=0,r=0))
        st.plotly_chart(fig, key="d3_tree", **PLOT_CFG)

    # RFM Table
    st.markdown("---")
    st.markdown('<div class="sec-title">Customer RFM Scores and Segments</div>',
                unsafe_allow_html=True)
    cols = ["customer_name","Monetary","Frequency","Sum_of_Recency","Segment"]
    disp = rfm[cols].copy()
    disp.columns = ["Customer Name","Monetary","Frequency","Sum of Recency","Segment"]
    disp["Monetary"] = disp["Monetary"].round(1)

    pal = {
        "Champion":"#dbeafe","Loyal Customer":"#d1fae5",
        "Potential Loyalist":"#fef9c3","At Risk":"#fee2e2",
        "Others":"#f1f5f9","Lost Customers":"#f1f5f9"
    }

    def color_row(row):
        c = pal.get(row["Segment"], "#ffffff")
        return [f"background-color:{c}"] * len(row)

    styled = (disp.head(50).style
              .apply(color_row, axis=1)
              .format({"Monetary": "{:,.1f}"}))
    st.dataframe(styled, use_container_width=True, height=320)
