#SIPP V GIA Calculator, Tax, Total return is assumed net of inflation#

import streamlit as st

st.title("S.I.P.P versus Direct Investment Calculator- UK")
st.subheader("Evaluating the merits of the SIPP")
# -----------------------------
# USER INPUTS
# -----------------------------
st.header("Inputs")

NumberOfYears = st.number_input("Years to retirement", min_value=1, max_value=60, value=37)
GrowthRate = st.number_input("Expected investment rate (%)", min_value=0.0, max_value=20.0, value=7.0) / 100
LifeExpectancy = st.number_input("Life expectancy", min_value=60, max_value=120, value=80)
RetirementAge = st.number_input("Retirement age", min_value=50, max_value=75, value=67)

# Contribution choice
st.subheader("SIPP Contribution Settings")
use_default = st.radio(
    "Choose contribution mode:",
    ("Use preset £1,901/year", "Enter my own yearly SIPP contribution")
)

if use_default == "Use preset £1,901/year":
    YearlyContSIPPTotal = 1901
else:
    YearlyContSIPPTotal = st.number_input(
        "Enter your yearly SIPP contribution (£)",
        min_value=1,
        max_value=200000,
        value=1901
    )

# GIA contribution rule
YearlyContGIATotal = YearlyContSIPPTotal * 0.625

# -----------------------------
# CALCULATE BUTTON
# -----------------------------
if st.button("Calculate"):

    # -----------------------------
    # CORE CALCULATIONS
    # -----------------------------
    GrowthRatePeriod = 1 + GrowthRate
    GrowthIndex = GrowthRatePeriod ** NumberOfYears
    T = 1 - GrowthIndex
    L = 1 - GrowthRatePeriod

    # Pots at retirement
    SIPPTotal = YearlyContSIPPTotal * (T / L)
    GIATotal = YearlyContGIATotal * (T / L)

    st.header("Results")

    st.subheader("Pot at Retirement")
    st.write(f"SIPP pot at retirement: £{SIPPTotal:,.0f}")
    st.write(f"GIA pot at retirement: £{GIATotal:,.0f}")

    # Withdrawals (5% p.a. = 1/20 yearly)
    SIPPIncome = SIPPTotal / 20
    GIAIncome = GIATotal / 20

    st.subheader("Yearly Income at Retirement")
    st.write(f"SIPP yearly income: £{SIPPIncome:,.2f}")
    st.write(f"GIA yearly income: £{GIAIncome:,.2f}")

    # Value at death
    YearsRetired = LifeExpectancy - RetirementAge
    CrudeGrowth = (1.07) ** YearsRetired

    # SIPP FV
    SIPPFV1 = SIPPTotal * CrudeGrowth
    SIPPFV2 = ((CrudeGrowth - 1) / GrowthRate) * (SIPPIncome)
    SIPPFV = SIPPFV1 - SIPPFV2

    # GIA FV
    GIAFV1 = GIATotal * CrudeGrowth
    GIAFV2 = ((CrudeGrowth - 1) / GrowthRate) * (GIAIncome)
    GIAFV = GIAFV1 - GIAFV2

    st.subheader("Value of Pots at Death")
    st.write(f"SIPP value at death: £{SIPPFV:,.0f}")
    st.write(f"GIA value at death: £{GIAFV:,.0f}")

    # Lifetime tax
    SIPPLifetax = (SIPPFV * 0.01) * YearsRetired
    GIALifetax = ((GIAFV * 0.0072) - 540) * YearsRetired

    st.subheader("Lifetime Tax During Retirement")
    st.write(f"SIPP lifetime tax: £{SIPPLifetax:,.0f}")
    if GIALifetax>0:
        st.write(f"GIA lifetime tax: £{GIALifetax:,.0f}")
    else:
        st.write(f"No GIA lifetime tax")
    # Estate tax
    GIAIHT = GIAFV * 0.13
    SIPPIHT = SIPPFV * 0.43

    st.subheader("Estate Tax at Death")
    st.write(f"SIPP estate tax: £{SIPPIHT:,.0f}")
    st.write(f"GIA estate tax: £{GIAIHT:,.0f}")

    # Inheritance
    SIPPInheritance = SIPPFV - SIPPIHT
    GIAInheritance = GIAFV - GIAIHT

    st.subheader("Net Inheritance")
    st.write(f"Net inheritance from SIPP: £{SIPPInheritance:,.0f}")
    st.write(f"Net inheritance from GIA: £{GIAInheritance:,.0f}")

    # Total tax extracted
    SIPPTaxTot = SIPPIHT + SIPPLifetax
    GIATaxTot = GIAIHT + GIALifetax

    st.subheader("Total Tax Extracted")
    st.write(f"Total tax extracted from SIPP: £{SIPPTaxTot:,.0f}")
    st.write(f"Total tax extracted from GIA: £{GIATaxTot:,.0f}")
