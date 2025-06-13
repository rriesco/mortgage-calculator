import streamlit as st
import yaml
from functools import partial
from MortgageClass import MortgageCalculator
import pandas as pd
import numpy as np  

############################
###        Params        ###
############################

color_side = "#212121"
color_bg = "#616161"
color_box = "#999999"
color_line = "#FFFFFF"
color_text = "#FFFFFF"
color_text_second = "#999999"
color_text_third = "#202020"

color_bar_price_1 = "#D1E3F8"
color_bar_price_2 = "#7AA9F7"
color_bar_price_3 = "#2E5CB8"

color_bar_interest_1 = "#f8d1d1"
color_bar_interest_2 = "#f89696"
color_bar_interest_3 = "#fa4f4f"

box_width = "400px"
box_gap = "32px"

# Set initial values and limits
with open("streamlit_params.yaml", "r") as file:
    params = yaml.safe_load(file)

params_keys = ["house_price", "down_payment", "years", "cost", "interest_rate", "taxes"]

for key in params_keys:
    text_key = f"{key}_text"
    slider_key = f"{key}_slider"
    if key not in st.session_state:
        st.session_state[key] = params[key]["default"]
    if text_key not in st.session_state:
        st.session_state[text_key] = str(params[key]["default"])
    if slider_key not in st.session_state:
        st.session_state[slider_key] = params[key]["default"]
        
############################
###  Auxiliar Functions  ###
############################      

def on_text_change(key):
    text_key = f"{key}_text"
    slider_key = f"{key}_slider"
    data_type = params[key]["data_type"]
    min_val = params[key]["min"]
    max_val = params[key]["max"]
    try:
        value = float(st.session_state[text_key]) if data_type == "float" else int(st.session_state[text_key])
        value = max(min(value, max_val), min_val)
        st.session_state[key] = value
        st.session_state[slider_key] = value
    except ValueError:
        pass

def on_slider_change(key):
    slider_key = f"{key}_slider"
    text_key = f"{key}_text"
    data_type = params[key]["data_type"]
    
    try:
        value = st.session_state[slider_key]
        st.session_state[key] = value
        st.session_state[text_key] = f"{value:.2f}" if data_type == "float" else str(value)
    except ValueError:
        pass

def format_thousands_dot(number):
    return f"{number:,.0f}".replace(",", ".")

############################
###       Sidebar        ###
############################

st.title("Mortgage Calculator")

st.markdown(f"""
    <style>
        [data-testid="stSidebar"] {{
            background-color: {color_side};
        }}
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("Mortgage Input")
    for key in params_keys:
        st.write(f"{params[key]['title']} ({params[key]['unit']})")
        
        cols = st.columns([5, 2])  # Adjust ratio as needed (slider, text)
        
        with cols[0]:
            st.slider(
                label=f'{params[key]["title"]} Slider ({params[key]["unit"]})',
                min_value=params[key]["min"],
                max_value=params[key]["max"],
                step=params[key]["step"],
                value=st.session_state[key],
                key=f"{key}_slider",
                on_change=partial(on_slider_change, key),
                label_visibility="collapsed"
            )
        with cols[1]:
            st.text_input(
                label=f'{params[key]["title"]} Slider ({params[key]["unit"]})',
                value=st.session_state[f"{key}_text"],
                key=f"{key}_text",
                on_change=partial(on_text_change, key),
                label_visibility="collapsed"
            )

############################
###       Backend        ###
############################

house_price = st.session_state.get("house_price", 425000)
down_payment = st.session_state.get("down_payment", 70000)
interest_rate = st.session_state.get("interest_rate", 1.8)
loan_term_years = st.session_state.get("years", 30)
cost = st.session_state.get("cost", 2000)
taxes = st.session_state.get("taxes", 6)

mortgage = MortgageCalculator(house_price, down_payment, interest_rate, loan_term_years, cost, taxes)
mortgage.run()
mortgage.get_amortization_schedule()

# Values
property_cost = mortgage.house_price + mortgage.taxes_cost
down_payment = mortgage.down_payment
mortgage_amount = mortgage.total_mortgage
interest_paid = mortgage.total_interest_paid
principal_paid = down_payment + mortgage_amount
total_cost_with_mortgage = principal_paid + interest_paid

# Bar 1 (Price): width is as long as principal_paid (down_payment + mortgage), segments are house and taxes
bar1_width = principal_paid / total_cost_with_mortgage * 100
bar1_house = mortgage.house_price / total_cost_with_mortgage * 100
bar1_taxes = mortgage.taxes_cost / total_cost_with_mortgage * 100

# Bar 2 (Interest): full width, segments are down payment, mortgage, interest
bar2_down = down_payment / total_cost_with_mortgage * 100
bar2_mortgage = mortgage_amount / total_cost_with_mortgage * 100
bar2_interest = interest_paid / total_cost_with_mortgage * 100

# Format values for display
price = format_thousands_dot(mortgage.house_price)
taxes = format_thousands_dot(mortgage.taxes_cost)
total_cost = format_thousands_dot(mortgage.total_cost)
down_payment_fmt = format_thousands_dot(mortgage.down_payment)
total_mortgage = format_thousands_dot(mortgage.total_mortgage)
total_interest_paid = format_thousands_dot(mortgage.total_interest_paid)
total = format_thousands_dot(mortgage.total_paid + mortgage.down_payment)

#############################
####       1st Box        ###
#############################

st.markdown("""
    <style>
    .main .block-container {
        padding-top: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
        max-width: 80vw;

    }
    .no-borders-table, .no-borders-table tr, .no-borders-table td {
        border: none !important;
        background: #262730 !important;
    }
    </style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 2, 3.5])  # Adjust ratios as needed (center box is wider)

with col1:
    st.markdown(f"""
        <div style="border:3px solid {color_line};
            border-radius:8px;
            padding:16px;
            background-color:{color_bg};
            margin-bottom: {box_gap};
    ">
        <div style="font-size:20px; font-weight:bold; text-align:center; margin-bottom:8px;">Monthly Payment</div>
        <div style="font-size:32px; font-weight:bold; color: {color_text}; text-align:center; margin-bottom:12px;">{mortgage.monthly_payment:.2f} €</div>
        <div style="display:flex; justify-content:space-between; margin-bottom:4px; font-weight:bold;">
            <span>Mortgage Amount</span>
            <span style="font-weight:bold;">{total_mortgage} €</span>
        </div>
        <div style="display:flex; justify-content:space-between; margin-bottom:4px; font-weight:bold;">
            <span>Financing Percentage</span>
            <span style="font-weight:bold;">{mortgage.financing_percentage:.0f} %</span>
        </div>""", unsafe_allow_html=True)

#############################
####       2nd Box        ###
#############################

    st.markdown(f"""
    <div style="border:3px solid {color_line};
                border-radius:8px;
                padding:16px;
                background-color:{color_bg};
                ">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="color:{color_bar_price_1}; font-weight:bold;">House Price</span>
            <span style="font-weight:bold;">{price} €</span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="color:{color_bar_price_2}; font-weight:bold;">Taxes and Additional Costs</span>
            <span>{taxes} €</span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; font-weight:bold; margin-bottom:8px;">
            <span>Total Cost of Property</span>
            <span>{total_cost} €</span>
        </div>                    
        <!-- Top bar: House Price + Additional Costs (aligned with principal paid) -->
        <div style="height:18px; width:{bar1_width}%; background:{color_bar_price_2}; border-radius:6px; position:relative; margin:16px 0 8px 0; overflow:hidden;">
            <div style="height:100%; width:{bar1_house}%; background:{color_bar_price_1}; border-radius:6px 0 0 6px; display:inline-block; float:left;"></div>
            <div style="height:100%; width:{bar1_taxes}%; background:{color_bar_price_2}; border-radius:0 6px 6px 0; display:inline-block; float:left;"></div>
        </div>
        <!-- Bottom bar: Down Payment + Mortgage + Interest -->
        <div style="height:18px; width:100%; background:{color_bg}; border-radius:6px; position:relative; margin-bottom:8px; overflow:hidden;">
            <div style="height:100%; width:{bar2_down}%; background:{color_bar_interest_1}; border-radius:6px 0 0 6px; display:inline-block; float:left;"></div>
            <div style="height:100%; width:{bar2_mortgage}%; background:{color_bar_interest_2}; display:inline-block; float:left;"></div>
            <div style="height:100%; width:{bar2_interest}%; background:{color_bar_interest_3}; border-radius:0 6px 6px 0; display:inline-block; float:left;"></div>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="color:{color_bar_interest_1};font-weight:bold;">Down Payment</span>
            <span>{down_payment_fmt} €</span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="color:{color_bar_interest_2};font-weight:bold;">Mortgage Amount</span>
            <span>{total_mortgage} €</span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="color:{color_bar_interest_3};font-weight:bold;">Mortgage Interest</span>
            <span>{total_interest_paid} €</span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; font-weight:bold; margin-top:8px;">
            <span>Total Cost with Mortgage</span>
            <span>{total} €</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Drop your amortization CSV file here", type=["csv"])

    if uploaded_file is not None:
        amortization_df = pd.read_csv(uploaded_file, delimiter=";")
        st.write('Calculating amortization with provided data...')
    else:
        amortization_df = pd.DataFrame({
                                    "Month": list(np.arange(1, loan_term_years*12 + 1)),
                                    "Amortization": [0] * (loan_term_years * 12),
                                    "Type": [np.nan] * (loan_term_years * 12)
                                })
        st.write('No data provided, using zero additional amortization.')
        
############################
###       Backend        ###
############################

mortgage_enhanced_amortization = MortgageCalculator(house_price, down_payment, interest_rate, loan_term_years, cost, taxes, amortization_schedule_df=amortization_df)
mortgage_enhanced_amortization.run()
mortgage_enhanced_amortization.get_amortization_schedule()

# Values
property_cost_enhanced_amortization = mortgage_enhanced_amortization.house_price + mortgage_enhanced_amortization.taxes_cost
down_payment_enhanced_amortization = mortgage_enhanced_amortization.down_payment
mortgage_amount_enhanced_amortization = mortgage_enhanced_amortization.total_mortgage
interest_paid_enhanced_amortization = mortgage_enhanced_amortization.total_interest_paid
principal_paid_enhanced_amortization = down_payment_enhanced_amortization + mortgage_amount_enhanced_amortization
total_cost_with_mortgage_enhanced_amortization = principal_paid_enhanced_amortization + interest_paid_enhanced_amortization

# Bar 1 (Price): width is as long as principal_paid (down_payment + mortgage), segments are house and taxes
bar1_width_enhanced_amortization = principal_paid_enhanced_amortization / total_cost_with_mortgage_enhanced_amortization * 100
bar1_house_enhanced_amortization = mortgage_enhanced_amortization.house_price / total_cost_with_mortgage_enhanced_amortization * 100
bar1_taxes_enhanced_amortization = mortgage_enhanced_amortization.taxes_cost / total_cost_with_mortgage_enhanced_amortization * 100

# Bar 2 (Interest): full width, segments are down payment, mortgage, interest
bar2_down_enhanced_amortization = down_payment_enhanced_amortization / total_cost_with_mortgage_enhanced_amortization * 100
bar2_mortgage_enhanced_amortization = mortgage_amount_enhanced_amortization / total_cost_with_mortgage_enhanced_amortization * 100
bar2_interest_enhanced_amortization = interest_paid_enhanced_amortization / total_cost_with_mortgage_enhanced_amortization * 100

# Format values for display
price_enhanced_amortization = format_thousands_dot(mortgage_enhanced_amortization.house_price)
taxes_enhanced_amortization = format_thousands_dot(mortgage_enhanced_amortization.taxes_cost)
total_cost_enhanced_amortization = format_thousands_dot(mortgage_enhanced_amortization.total_cost)
down_payment_fmt_enhanced_amortization = format_thousands_dot(mortgage_enhanced_amortization.down_payment)
total_mortgage_enhanced_amortization = format_thousands_dot(mortgage_enhanced_amortization.total_mortgage)
total_interest_paid_enhanced_amortization = format_thousands_dot(mortgage_enhanced_amortization.total_interest_paid)
total_enhanced_amortization = format_thousands_dot(mortgage_enhanced_amortization.total_paid + mortgage_enhanced_amortization.down_payment)

with col2:
        
    st.markdown(f"""
        <div style="border:3px solid {color_line};
            border-radius:8px;
            padding:16px;
            background-color:{color_bg};
            margin-bottom: {box_gap};
    ">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
        <div>
            <div style="font-size:20px; font-weight:bold; color: {color_text_second}; text-align:left; margin-bottom:8px;">Initial Payment</div>
            <div style="font-size:32px; font-weight:bold; color: {color_text_second}; text-align:left;">{mortgage_enhanced_amortization.initial_monthly_payment:.2f} €</div>
        </div>
        <div>
            <div style="font-size:20px; font-weight:bold; text-align:right; margin-bottom:8px;">Final Payment</div>
            <div style="font-size:32px; font-weight:bold; color: {color_text}; text-align:right;">{mortgage_enhanced_amortization.monthly_payment:.2f} €</div>
        </div>
        </div>
        <div style="display:flex; justify-content:space-between; margin-bottom:4px; font-weight:bold;">
            <span>Mortgage Amount</span>
            <span style="font-weight:bold;">{total_mortgage_enhanced_amortization} €</span>
        </div>
        <div style="display:flex; justify-content:space-between; margin-bottom:4px; font-weight:bold;">
            <span>Financing Percentage</span>
            <span style="font-weight:bold;">{mortgage_enhanced_amortization.financing_percentage:.0f} %</span>
        </div>""", unsafe_allow_html=True)
    
#############################
####       2nd Box        ###
#############################

    st.markdown(f"""
    <div style="border:3px solid {color_line};
                border-radius:8px;
                padding:16px;
                background-color:{color_bg};
                ">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="color:{color_bar_price_1}; font-weight:bold;">House Price</span>
            <span style="font-weight:bold;">{price_enhanced_amortization} €</span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="color:{color_bar_price_2}; font-weight:bold;">Taxes and Additional Costs</span>
            <span>{taxes_enhanced_amortization} €</span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; font-weight:bold; margin-bottom:8px;">
            <span>Total Cost of Property</span>
            <span>{total_cost_enhanced_amortization} €</span>
        </div>                    
        <!-- Top bar: House Price + Additional Costs (aligned with principal paid) -->
        <div style="height:18px; width:{bar1_width_enhanced_amortization}%; background:{color_bar_price_2}; border-radius:6px; position:relative; margin:16px 0 8px 0; overflow:hidden;">
            <div style="height:100%; width:{bar1_house_enhanced_amortization}%; background:{color_bar_price_1}; border-radius:6px 0 0 6px; display:inline-block; float:left;"></div>
            <div style="height:100%; width:{bar1_taxes_enhanced_amortization}%; background:{color_bar_price_2}; border-radius:0 6px 6px 0; display:inline-block; float:left;"></div>
        </div>
        <!-- Bottom bar: Down Payment + Mortgage + Interest -->
        <div style="height:18px; width:100%; background:{color_bg}; border-radius:6px; position:relative; margin-bottom:8px; overflow:hidden;">
            <div style="height:100%; width:{bar2_down_enhanced_amortization}%; background:{color_bar_interest_1}; border-radius:6px 0 0 6px; display:inline-block; float:left;"></div>
            <div style="height:100%; width:{bar2_mortgage_enhanced_amortization}%; background:{color_bar_interest_2}; display:inline-block; float:left;"></div>
            <div style="height:100%; width:{bar2_interest_enhanced_amortization}%; background:{color_bar_interest_3}; border-radius:0 6px 6px 0; display:inline-block; float:left;"></div>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="color:{color_bar_interest_1};font-weight:bold;">Down Payment</span>
            <span>{down_payment_fmt_enhanced_amortization} €</span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="color:{color_bar_interest_2};font-weight:bold;">Mortgage Amount</span>
            <span>{total_mortgage_enhanced_amortization} €</span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="color:{color_bar_interest_3};font-weight:bold;">Mortgage Interest</span>
            <span>{total_interest_paid_enhanced_amortization} €</span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; font-weight:bold; margin-top:8px;">
            <span>Total Cost with Mortgage</span>
            <span>{total_enhanced_amortization} €</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
#############################
####       Graphs         ###
#############################

from GraphicClass import GraphicClass
from GraphicClass import GraphicClass

params = {
    'color_side': "#212121",
    'color_bg': "#616161",
    'color_box': "#e0e0e0",
    'color_line': "#FFFFFF",
    'color_text': "#FFFFFF",
    'color_text_second': "#707070",
    'color_text_third': "#202020",
    'color_bar_price_1': "#D1E3F8",
    'color_bar_price_2': "#7AA9F7",
    'color_bar_price_3': "#2E5CB8",
    'color_bar_interest_1': "#f8d1d1",
    'color_bar_interest_2': "#f89696",
    'color_bar_interest_3': "#fa4f4f",
    'box_width': "400px",
    'box_gap': "32px"
}

graphics = GraphicClass(mortgage, mortgage_enhanced_amortization, params)
bars = graphics.monthly_payment_graph()
bars.show()

with col3:
    st.plotly_chart(bars, use_container_width=True)
