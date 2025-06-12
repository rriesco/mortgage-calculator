import streamlit as st
import yaml
from functools import partial
from MortgageClass import MortgageCalculator

############################
###       Palette        ###
############################

color_side = "#212121"
color_bg = "#616161"
color_box = "#e0e0e0"
color_line = "#FFFFFF"
color_text = "#FFFFFF"

# color_bar_price_1 = "#f1c40f"
# color_bar_price_2 = "#e67e22"
# color_bar_price_3 = "#e74c3c"

# color_bar_interest_1 = "#3ec6c2"
# color_bar_interest_2 = "#1e7574"
# color_bar_interest_3 = "#1c5a5b"


# color_bar_price_1 = "#50E3C2"
# color_bar_price_2 = "#7399C5"
# color_bar_price_3 = "#E3C2FF"

# color_bar_interest_1 = "#D0021B"
# color_bar_interest_2 = "#F8E71C"
# color_bar_interest_3 = "#F5A623"

color_bar_price_1 = "#D1E3F8"
color_bar_price_2 = "#7AA9F7"
color_bar_price_3 = "#2E5CB8"

color_bar_interest_1 = "#f8d1d1"
color_bar_interest_2 = "#f89696"
color_bar_interest_3 = "#fa4f4f"

############################
###       Sidebar        ###
############################


st.title("Mortgage Calculator Dashboard")

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

house_price = st.session_state.get("house_price", 300000)
down_payment = st.session_state.get("down_payment", 60000)
interest_rate = st.session_state.get("interest_rate", 3.5)
loan_term_years = st.session_state.get("years", 30)
cost = st.session_state.get("cost", 0)
taxes = st.session_state.get("taxes", 0)

mortgage = MortgageCalculator(house_price, down_payment, interest_rate, loan_term_years, cost, taxes)
mortgage.run()
mortgage.get_amortization_schedule()

# ############################
# ###       1st Box        ###
# ############################

# color_bg = "#262730"
# color_line = "#FFFFFF"
# box_width = "400px"

# st.markdown("""
#     <style>
#     .main .block-container {
#         padding-left: 3rem;
#         padding-right: 3rem;
#         max-width: 80vw;

#     }
#     .no-borders-table, .no-borders-table tr, .no-borders-table td {
#         border: none !important;
#         background: #262730 !important;
#     }
#     </style>
# """, unsafe_allow_html=True)

# # markdown_1 = [
# #     f"""
# #     <div style='
# #         border:3px solid {color_line};
# #         border-radius:8px;
# #         padding:16px;
# #         background-color:{color_bg};
# #         width:{box_width};
# #         margin-left: 0;
# #         margin-right: auto;
# #     '>
# #     <table class='no-borders-table' style='width:100%; border-collapse:separate; border-spacing:0;'>
# #     """
# # ]

# # for key in params_keys:
# #     markdown_1.append(
# #         f"<tr>"
# #         f"<td style='text-align:left; padding: 4px 8px;'><b>{params[key]['title']}:</b></td>"
# #         f"<td style='text-align:right; padding: 4px 8px;'>{st.session_state[key]} {params[key]['unit']}</td>"
# #         f"</tr>"
# #     )
# # markdown_1.append("</table></div>")
# #
# # st.markdown("\n".join(markdown_1), unsafe_allow_html=True)

# ############################
# ###       2nd Box        ###
# ############################

# total_mortgage = mortgage.house_price + mortgage.taxes + mortgage.cost - mortgage.down_payment
# ratio_financing = mortgage.down_payment / mortgage.house_price * 100
# house_price = mortgage.house_price
# taxes_cost = mortgage.taxes_cost
# down_payment = mortgage.down_payment
# monthly_payment = mortgage.monthly_payment
# total_interest_paid = mortgage.total_interest_paid
# total_paid = mortgage.total_paid

# st.markdown("""
#     <style>
#     .main .block-container {
#         padding-left: 3rem;
#         padding-right: 3rem;
#         max-width: 80vw;

#     }
#     .no-borders-table, .no-borders-table tr, .no-borders-table td {
#         border: none !important;
#         background: #262730 !important;
#     }
#     </style>
# """, unsafe_allow_html=True)

# markdown_2 = [
#     f"""
#     <div style='
#         border:3px solid {color_line};
#         border-radius:8px;
#         padding:16px;
#         background-color:{color_bg};
#         width:{box_width};
#         margin-left: 0;
#         margin-right: auto;
#     '>
#     <table class='no-borders-table' style='width:100%; border-collapse:separate; border-spacing:0;'>
#     """
# ]


# markdown_2.append(
#     f"<tr>"
#     f"<td style='text-align:left; padding: 4px 8px;'><b>Monthly Payment:</b></td>"
#     f"<td style='text-align:right; padding: 4px 8px;'>{mortgage.monthly_payment:.2f} EUR/month</td>"
#     f"</tr>"
#     f"<tr>"
#     f"<td style='text-align:left; padding: 4px 8px;'><b>Mortgage Quantity:</b></td>"
#     f"<td style='text-align:right; padding: 4px 8px;'>{mortgage.total_mortgage:.0f} EUR</td>"
#     f"</tr>"
#     f"<tr>"
#     f"<td style='text-align:left; padding: 4px 8px;'><b>House Price:</b></td>"
#     f"<td style='text-align:right; padding: 4px 8px;'>{mortgage.house_price:.0f} EUR</td>"
#     f"</tr>"
#     f"<tr>"
#     f"<td style='text-align:left; padding: 4px 8px;'><b>Taxes & Additional Costs:</b></td>"
#     f"<td style='text-align:right; padding: 4px 8px;'>{mortgage.taxes_cost:.0f} EUR</td>"
#     f"</tr>"
#     f"<tr>"
#     f"<td style='text-align:left; padding: 4px 8px;'><b>Total Interest Paid:</b></td>"
#     f"<td style='text-align:right; padding: 4px 8px;'>{mortgage.total_interest_paid:.0f} EUR</td>"
#     f"</tr>"
# )
# markdown_2.append("</table></div>")



# st.markdown("\n".join(markdown_2), unsafe_allow_html=True)

# Format helper
def format_thousands_dot(number):
    return f"{number:,.0f}".replace(",", ".")

# Values
property_cost = mortgage.house_price + mortgage.taxes_cost
down_payment = mortgage.down_payment
mortgage_amount = mortgage.total_mortgage
interest_paid = mortgage.total_interest_paid
principal_paid = down_payment + mortgage_amount
total_cost_with_mortgage = principal_paid + interest_paid

# Bar 1 (top): width is as long as principal_paid (down_payment + mortgage), segments are house and taxes
bar1_width = principal_paid / total_cost_with_mortgage * 100
bar1_house = mortgage.house_price / total_cost_with_mortgage * 100
bar1_taxes = mortgage.taxes_cost / total_cost_with_mortgage * 100

# Bar 2 (bottom): full width, segments are down payment, mortgage, interest
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

box_width = "400px"
box_gap = "32px"

# --- Display the bars and summary ---

st.markdown("""
    <style>
    .main .block-container {
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

st.markdown(f"""
    <div style="border:3px solid {color_line};
        border-radius:8px;
        padding:16px;
        background-color:{color_bg};
        width:{box_width};
        margin-left: 0;
        margin-right: auto;
        margin-bottom: {box_gap};
">
    <div style="font-size:20px; font-weight:bold; text-align:center; margin-bottom:8px;">Monthly Payment</div>
    <div style="font-size:32px; font-weight:bold; color: {color_text}; text-align:center; margin-bottom:12px;">{mortgage.monthly_payment:.2f} €</div>
    <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
        <span>Mortgage Amount</span>
        <span style="font-weight:bold;">{total_mortgage} €</span>
    </div>
    <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
        <span>Financing Percentage</span>
        <span style="font-weight:bold;">{mortgage.financing_percentage:.0f} %</span>
    </div>""", unsafe_allow_html=True)

st.markdown(f"""
<div style="border:3px solid {color_line};
            border-radius:8px;
            padding:16px;
            background-color:{color_bg};
            width:{box_width};
            margin-left: 0;
            margin-right: auto;">
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

