import json
import plotly
import plotly.express as px
import plotly.graph_objs as go
from plotly.offline import plot

from toolbox.tools import measure

def add_figure(question, plot_type):
    '''
    Wrapper for plotting different types of figures.
    Types include:

    TYPE = (
    (0,"Linear"),
    (1,"Histogram")
    )
    '''
    if plot_type == 0:
        plot_div = add_figure_scatter(question)
    elif plot_type == 1:
        plot_div = add_plotly_fig(question)
    return plot_div

def add_figure_scatter(question):
            '''
             Plot poll results.
            '''
            choices = question.choice_set.all()
            x_data = []
            y_data = []
            for choice in choices:
                x_data += [choice.choice_text]
                y_data += [choice.votes]           
            plot_div = plot({"data": [go.Scatter(x=x_data, y=y_data, marker_color='#FFC37B',opacity=0.5)],
                            "layout" : go.Layout(title=question.question_text, 
                                                margin=dict(l=5, r=105, t=30, b=5),
                                                height=250,
                                                paper_bgcolor="#d1d1d1",
                                                plot_bgcolor="#f3f3f3"),                       
                            },
                    output_type='div', show_link=False, link_text="", include_plotlyjs=False) 
            return plot_div

@measure
def add_plotly_fig(question):
            '''
             Plot poll results.
            '''
            choices = question.choice_set.all()
            x_data = []
            y_data = []
            for choice in choices:
                x_data += [choice.choice_text]
                y_data += [choice.votes]

            total_votes = sum(y_data)
            if total_votes != 0:
                for i in range(len(y_data)): 
                    y_data[i] = y_data[i]/total_votes
                   

            data =    [go.Bar(x=x_data, y=y_data, marker_color=px.colors.qualitative.Dark24, 
                              opacity=0.75, marker_line_color='#3288bd', marker_line_width=1.5 )]
            layout =    go.Layout(title="", 
                                                #autosize=True,
                                                margin=dict(l=5, r=5, t=30, b=5),
                                                height=300,
                                               # width=785,
                                                #plot_bgcolor="#f3f3f3",
                                                #paper_bgcolor="#d1d1d1",
                                                )
            fig = go.Figure(data=data, layout=layout)
            fig.update_layout(template="plotly_white")
            fig.to_plotly_json()

            return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)