from plotly.offline import plot
import plotly.graph_objs as go
from bokeh.palettes import Spectral6
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components, json_item
from bokeh.models import ColumnDataSource
from bokeh.transform import factor_cmap
import json
import plotly
import plotly.express as px

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


def add_bokeh_figure(question):
            '''
             Plot poll results.
            '''
            
            choices = question.choice_set.all()
            x_data = []
            y_data = []
            for choice in choices:
                x_data += [choice.choice_text]
                y_data += [choice.votes]  
            source = ColumnDataSource(data=dict(x_data=x_data, y_data=y_data))
            p = figure(x_range=x_data,
                        tools="pan,box_zoom,reset,save",                        
                        x_axis_label='sections', y_axis_label='particles', sizing_mode = 'stretch_width', height=300,
                        )        
            p.vbar(x='x_data', top='y_data', width=0.9, source=source, fill_color=factor_cmap('x_data', palette=Spectral6, factors=x_data)) 
            id_num = 'graph'+str(question.id)
            graph = json.dumps(json_item(p, id_num))
            return graph

def add_figure_histogram(question):
            '''
             Plot poll results.
            '''
            choices = question.choice_set.all()
            x_data = []
            y_data = []
            for choice in choices:
                x_data += [choice.choice_text]
                y_data += [choice.votes]  
            source = ColumnDataSource(data=dict(x_data=x_data, y_data=y_data))
            p = figure(x_range=x_data,
                        tools="pan,box_zoom,reset,save",                        
                        x_axis_label='sections', y_axis_label='particles', sizing_mode = 'stretch_width', height=300,
                        )        
            p.vbar(x='x_data', top='y_data', width=0.9, source=source, fill_color=factor_cmap('x_data', palette=Spectral6, factors=x_data)) 

            script, div = components(p)
            return script, div

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

            data =    [go.Bar(x=x_data, y=y_data, marker_color=px.colors.qualitative.Dark24, opacity=0.75, marker_line_color='#3288bd', marker_line_width=1.5 )]
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


            # plot_div = plot({"data": [go.Scatter(x=x_data, y=y_data, marker_color='#FFC37B',opacity=0.5)],
            #                 "layout" : go.Layout(title=question.question_text, 
            #                                     margin=dict(l=5, r=105, t=30, b=5),
            #                                     height=250,
            #                                     paper_bgcolor="#d1d1d1",
            #                                     plot_bgcolor="#f3f3f3"),                       
            #                 },
            #         output_type='div', show_link=False, link_text="", include_plotlyjs=False) 
            return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)