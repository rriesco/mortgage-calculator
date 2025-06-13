import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class GraphicClass:
    def __init__(self, mortgage, mortgage_enhanced, params):
        self.mortgage = mortgage
        self.mortgage_enhanced = mortgage_enhanced
        self.params = params
        self.set_streamlit_theme()

    def set_streamlit_theme(self):
        pio.templates["Streamlit"] = go.layout.Template(
            layout=go.Layout(
                font=dict(size=16, color=self.params['color_text']),
                title_font=dict(size=22, color=self.params['color_text']),
                width=800,
                height=500,
                plot_bgcolor=self.params['color_bg'],
                paper_bgcolor=self.params['color_bg'],
                legend_title_text='',
                legend=dict(
                    font=dict(size=14, color=self.params['color_text_third']),
                    title_text='',
                    bgcolor=self.params['color_box'],
                    bordercolor=self.params['color_line'],
                    borderwidth=2,
                    xanchor="right",
                    yanchor="top",
                    orientation="v"
                ),
                xaxis=dict(
                    tickfont=dict(size=14),
                    title_font=dict(size=18),
                ),
                yaxis=dict(
                    tickfont=dict(size=14),
                    title_font=dict(size=18),
                    gridcolor=self.params['color_line'],
                ),
                # colorway=["#4A90E2", "#50E3C2", "#B82E2E"],  # Custom color palette
                colorway=["#4A90E2", "#3ECAAC", "#EC6161"],  # Custom color palette
                # colorway=[color_bar_interest_3, color_bar_price_2, "#50E3C2",],  # Custom color palette
            )
        )

        pio.templates.default = "Streamlit"

    def monthly_payment_graph(self):
        data = self.mortgage.get_amortization_schedule().iloc[::12]
        data_enhanced = self.mortgage_enhanced.get_amortization_schedule().iloc[::12]
        color_box = self.params['color_box']
        
        
        fig = make_subplots(rows=2, cols=1, 
                            shared_xaxes=True,
                            vertical_spacing=0.05,
                            )

        # Plot 1
        fig.add_trace(go.Bar(
            x=data['Payment Number'],
            y=data['Interest'],
            name='Interest',
            showlegend=True),
            row=1,
            col=1
            )

        fig.add_trace(go.Bar(
            x=data['Payment Number'],
            y=data['Regular Amortization'],
            name='Regular Amortization',
            showlegend=True),
            row=1,
            col=1
            )

        fig.add_trace(go.Bar(
            x=data['Payment Number'],
            y=data['Additional Amortization'],
            name='Additional Amortization',
            showlegend=True),
            row=1,
            col=1
        )

        # Plot 2
        fig.add_trace(go.Bar(
            x=data_enhanced['Payment Number'],
            y=data_enhanced['Interest'],
            name='Interest',
            showlegend=False),
            row=2,
            col=1
            )

        fig.add_trace(go.Bar(
            x=data_enhanced['Payment Number'],
            y=data_enhanced['Regular Amortization'],
            name='Regular Amortization',
            showlegend=False),
            row=2,
            col=1
            )

        fig.add_trace(go.Bar(
            x=data_enhanced['Payment Number'],
            y=data_enhanced['Additional Amortization'],
            name='Additional Amortization',
            showlegend=False),
            row=2,
            col=1
        )

        fig.update_layout(
            width=900,
            height=600,
            barmode='stack',
            xaxis_title='',
            yaxis_title='',
        )

        fig.update_layout(
            legend=dict(
                orientation='h',        # horizontal legend
                yanchor='bottom',
                y=1,                 # slightly above the plot
                xanchor='center',
                x=0.5,                  # centered horizontally
                title_text='',          # no legend title
                bgcolor=color_box,# transparent background (optional)
                font=dict(size=14, color='black')
            )
        )

        fig.add_annotation(
            xref='paper', yref='paper',
            x=-0.08, y=0.5,
            text='Payment (€)',  # Your global y-axis title
            showarrow=False,
            textangle=-90,
            font=dict(size=18),
            xanchor='center',
            yanchor='middle'
        )

        fig.update_xaxes(title_text='', range=[-10, self.mortgage.loan_term_years * 12], row=1, col=1)
        fig.update_yaxes(range=[-10, data_enhanced['Total Payment'].max() * 1.1], row=1, col=1)

        fig.update_xaxes(title_text='Month', range=[-10, self.mortgage.loan_term_years * 12], row=2, col=1)
        fig.update_yaxes(range=[-10, data_enhanced['Total Payment'].max() * 1.1], row=2, col=1)
        
        return fig
