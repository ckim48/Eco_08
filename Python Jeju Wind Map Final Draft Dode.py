# install konlpy, pandas, dash_bootstrap_components
from collections import Counter
from konlpy.tag import Okt
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
# from wordcloud import WordCloud
# from plotly_wordcloud import plotly_wordcloud as pwc
# from plotly.offline import plot
# from PIL import Image
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.font_manager as fm #setting the font of the graph
# import matplotlib


# Dash main code
# html.Div: one block, section
app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP, '"https://fonts.googleapis.com/css2?family=Mulish:wght@200&display=swap" rel="stylesheet"']) # (just a style systemic setting for this one)
app.layout = html.Div(children=[
    # making menu bar
    dbc.Navbar(
        [
            #A means hyperlink
            html.A( 
                # 톱니바퀴
                html.I(className="bi bi-clipboard-data-fill me-2 ms-4", style = {"font-size":"30px"}),
                href="/",
            ),
            dbc.NavbarBrand("Sentimental Dashboard", className="ms-2")
        ],
    ),
    dbc.Container(
        dbc.Card(
            dbc.CardBody(
                [
                html.H3(
                    children = "About our data",
                    style = {"textAlign":"center"}
                ),
                html.P(
                    children = "This is the data set we used, which contains all the information of 60 eco-friendly places in Jeju, from name to its location",
                    style = {"textAlign":"center"}
                ),
                html.A(
                    children = "Check the Data",
                    href="https://docs.google.com/spreadsheets/d/1brry4omurC3LIm46YVw6Qgihu4_uT6kgYlNMh_4lnIE/edit#gid=0",
                    style = {"textAlign":"enter"}
                )
                ],
                style={"background-color":"rgba(151,232,235,0.5)"}
            ),
            style =  {"margin-top":"20px"}
        ),
    ),

    # making a search bar
    html.Div(children=[
        html.Label("Enter a eco-friendly place in Jeju: ", style={"font-weight":"bold","margin-left":"20px","color":"#3D91E5","font-family": 'Mulish, sans-serif'}),
        dcc.Input(id="place", value="전체", type="text", style={"padding":"10px","margin-top":"15px","margin-bottom":"15px","margin-left":"15px", "border":"1.5px solid #000000", "border-radius":"5px"}) #"id" means variable(name) in html, and "value" fills out the blank
    ]
    ),

    # making bar graph description (heading, paragraph)
    html.Div([
        html.H3(
            children=[html.I(className="bi bi-binoculars-fill me-2 ms-4", style = {"font-size":"30px"}), "The Most Frequent Words"],
            style={"textAlign":"center"}
        ),
        html.P(
            children="As the data set above shows, we first extracted 60 keywords/places from the Jeju Wind Map, which shows eco-friendly places in Jeju. Then, we scrapped the contents in 10 Naver blogs for each keyword using Naver API. After that, we only extracted the nouns that are consist of 2 or more letters. The 600 Naver API blogs are stored in the data set below:",
            style={"textAlign":"center"}
        ),
        html.A(
            children = "Check the Data",
            href="https://docs.google.com/spreadsheets/d/1E-B9_pzy0iv77zxN25t88yS7GE-K_AbYVF1vWQVomHw/edit#gid=306813603",
            style = {"textAlign":"center", "display":"block"}
        ),
    ]),
    # making bar graph
    html.Div(id="frequent"),

    # making pie chart description (heading, paragraph)
    html.Div([
        html.H3(
            children=[html.I(className="bi bi-star-fill me-2 ms-4", style = {"font-size":"30px"}), "The Rating of the Place"],
            style={"textAlign":"center"}
        ),
        html.P(
            children="We collected sentimental ratings of the place from Naver blog and created a pie chart using the ratings. The sections are: negative, neutral, and positive",
            style={"textAlign":"center"}
        ),
    ]),
    # making pie chart that shows sentiment
    html.Div(id="sentiment"),

    # making pie chart description (heading, paragraph)
    html.Div([
        html.H3(
            children=[html.I(className="bi bi-chat-heart-fill me-2 ms-4", style = {"font-size":"30px"}), "The Frequency of the Neutral, Positive Sentiment"],
            style={"textAlign":"center"}
        ),
        html.P(
            children="We calculated the number of neutral and positive comments for each places by filtering the sentiment of each blog post",
            style={"textAlign":"center"}
        ),
    ]),
    # the frequency of positive and non-positive comments, dbc.Row: seperating columns
    dbc.Row(
        children=[
            dbc.Col( # left column
            html.Div(id="sentiment_frequent_neutral"),
            ),
            dbc.Col( # right column
            html.Div(id="sentiment_frequent"),
            )
        ]
    )
])


# function: Shows graph that is typed in the search bar
# When the value(search bar's value) changes, app.callback 실행, then the function below executes
@app.callback(
    Output("frequent","children"), #the result of the function below is returned in "frequent" Div as a children
    Input("place","value"), #id = place (search bar)
)
def show_graph(value):
    data = pd.read_csv("final_labelled.csv")
    # data grouping (by 10 --> by place names)
    place_lst = data["Place"].tolist()
    # the graph that user typed
    graph_p = "모든 장소" #for title in the bottom
    if value in place_lst:
        data = data[data["Place"]==value]
        graph_p = value
    else:
        for place in place_lst:
            if place.find(value) != -1:
                data = data[data["Place"]==place]
                graph_p = place
                break
    # Data organizing, filtering invalid data
    only_str = [document for document in data["Blog"] if type(document) is str] # Blog is the column name
    # list to one string
    oneStr = " ".join(only_str)
    okt = Okt()
    nouns = okt.nouns(oneStr)
    #remove one letter word
    for i in nouns:
        if len(i) < 2:
            nouns.remove(i)
    # counting top 20
    count = Counter(nouns)
    most_frequent = count.most_common(20) # Top 20
    # list
    x = []
    y = []
    for i in most_frequent:
        x.append(i[0])
        y.append(i[1])
    # making two colums for bar graph
    data = pd.DataFrame(
    {
        "Word":x,
        "Frequency":y
    }
    )
    # Bar Graph
    title = "Place: " + graph_p
    fig = px.bar(data, x="Word",y="Frequency", title=title) # axis assign
    # graph returned to the "frequent" Div in app layout
    result = dcc.Graph(figure=fig)
    return result


# function: Shows the sentiment(rating) of the graph
@app.callback(
    Output("sentiment","children"),
    Input("place","value"),
)
def show_graph(value):
    data = pd.read_csv("final_labelled.csv")
    # data grouping (by 10 --> by place names)
    place_lst = data["Place"].tolist()
    # the graph that user typed
    graph_p = "모든 장소" 
    if value in place_lst:
        data = data[data["Place"]==value]
        graph_p = value
    else:
        for place in place_lst:
            if place.find(value) != -1:
                data = data[data["Place"]==place]
                graph_p = place
                break
    # data["Sentiment"].value_counts() = {-1:3, 0:5, 1:2}
    data_sentiment = data["Sentiment"].value_counts().to_list() #[3,5,2]
    label = data["Sentiment"].value_counts().keys().to_list() #[-1,0,1]
    for i in range(len(label)):
        if label[i] == 1:
            label[i] = "Positive"
        elif label[i] == 0:
            label[i] = "Neutral"
        else:
            label[i] = "Negative"
    fig_pie = px.pie(values=data_sentiment, names=label) # making pie chart
    result = dcc.Graph(figure=fig_pie)
    return result


# The frequency of the words in positive comments
# Everything is the same as the "frequent" code except line 158
@app.callback(
    Output("sentiment_frequent","children"),
    Input("place","value"),
)
def show_grap2(value):
    data = pd.read_csv("final_labelled.csv")
    data = data[data["Sentiment"]==1]
    place_lst = data["Place"].tolist()
    # the graph that user typed
    graph_p = "모든 장소" #for title in the bottom
    if value in place_lst:
        data = data[data["Place"]==value]
        graph_p = value
    else:
        for place in place_lst:
            if place.find(value) != -1:
                data = data[data["Place"]==place]
                graph_p = place
                break
    # Data organizing, filtering invalid data
    only_str = [document for document in data["Blog"] if type(document) is str] # Blog is the column name
    # list to one string
    oneStr = " ".join(only_str)
    okt = Okt()
    nouns = okt.nouns(oneStr)
    #remove one letter word
    for i in nouns:
        if len(i) < 2:
            nouns.remove(i)
    # counting top 20
    count = Counter(nouns)
    most_frequent = count.most_common(20) # Top 20
    # list
    x = []
    y = []
    for i in most_frequent:
        x.append(i[0])
        y.append(i[1])
    # making two colums for bar graph
    data = pd.DataFrame(
    {
        "Word":x,
        "Frequency":y
    }
    )
    # Bar Graph
    title = "Place: " + graph_p
    fig = px.bar(data, x="Word",y="Frequency", title=title, color_discrete_sequence=["#7FFFD4"]) # axis assign, color change, if error: (pip uninstall black, pip uninstall click, pip install black, pip install click 차례대로)
    # graph returned to the "sentiment_frequent" Div in app layout
    result = dcc.Graph(figure=fig)
    return result


# The frequency of the words in neutral comments
# Everything is the same as the code above
@app.callback(
    Output("sentiment_frequent_neutral","children"),
    Input("place","value"),
)
def show_grap2(value):
    data = pd.read_csv("final_labelled.csv")
    data = data[data["Sentiment"]==0]
    place_lst = data["Place"].tolist()
    # the graph that user typed
    graph_p = "모든 장소" #for title in the bottom
    if value in place_lst:
        data = data[data["Place"]==value]
        graph_p = value
    else:
        for place in place_lst:
            if place.find(value) != -1:
                data = data[data["Place"]==place]
                graph_p = place
                break
    # Data organizing, filtering invalid data
    only_str = [document for document in data["Blog"] if type(document) is str] # Blog is the column name
    # list to one string
    oneStr = " ".join(only_str)
    okt = Okt()
    nouns = okt.nouns(oneStr)
    #remove one letter word
    for i in nouns:
        if len(i) < 2:
            nouns.remove(i)
    # counting top 20
    count = Counter(nouns)
    most_frequent = count.most_common(20) # Top 20
    # list
    x = []
    y = []
    for i in most_frequent:
        x.append(i[0])
        y.append(i[1])
    # making two colums for bar graph
    data = pd.DataFrame(
    {
        "Word":x,
        "Frequency":y
    }
    )
    # Bar Graph
    title = "Place: " + graph_p
    fig = px.bar(data, x="Word",y="Frequency", title=title, color_discrete_sequence=["#3D91E5"]) # axis assign, color change, if error: (pip uninstall black, pip uninstall click, pip install black, pip install click 차례대로)
    # graph returned to the "sentiment_frequent" Div in app layout
    result = dcc.Graph(figure=fig)
    return result


# running the whole code (main dash code, app)
if __name__ == "__main__":
    app.run_server(debug = True)
    

# World Cloud
# img = np.array(Image.open("Jeju Island Image.jpg"))
# oneStr = " ".join(nouns)
# wordcloud = WordCloud("/content/NanumGothic.ttf", mask=img, background_color = "white").generate(oneStr)
# plt.imshow(wordcloud)
# plt.axis("off")
