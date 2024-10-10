import json
from flask import Flask, request, jsonify, render_template
import plotly.graph_objects as go
import pandas as pd
import os


app = Flask(__name__)


DATA_FILE ='data_points.json'


def load_data():
    """Load data points from a JSON file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return []


def save_data(data):
    """Save data points to a JSON file."""
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent= 4)


data_points = load_data()


@app.route('/')
def reportEvent():
    return render_template('reportEvent.html')  


@app.route('/support')
def support():
    return render_template('support.html')


@app.route('/index')
def index():
    #Plotly plot
    eventTypeColors = {
        'naturalDisaster': 'green',
        'political': 'blue',
        'popCulture' : 'pink',
        'War' : 'red',
        'other' : 'yellow'
    }
    markerColors = [eventTypeColors[point['typeOfEvent']] for point in data_points]

    fig = go.Figure(go.Scattermapbox(

        text=[f"{point['evn']} <br>\nDescription: {point['des']}<br>" for point in data_points],
        lat=[point['lat'] for point in data_points],
        lon=[point['lon'] for point in data_points],
        mode='markers',
        hoverinfo='text',
        marker=go.scattermapbox.Marker(
            size=9,
            color= markerColors
            ),
     ))

    

    fig.update_layout(
        mapbox=dict(
            style="carto-darkmatter", #carto-positron carto-darkmatter
            center={"lat": data_points[0]['lat'] if data_points else 0, "lon": data_points[0]['lon'] if data_points else 0},
            zoom=1,
        ),
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        font=dict(color='white'),
    )


   
    plot_html = fig.to_html(full_html=False)


    return render_template('index.html', plot=plot_html)


@app.route('/submit-data', methods=['POST'])
def submit_data():
    try:
        data = request.get_json()
        print(f"Received data: {data}")


        evn = data['evn']
        typeOfEvent = data['typeOfEvent']
        des = data['des']
        lat = float(data['lat'])
        lon = float(data['lon'])
        resource = data['resource']


        newEvent ={
            'evn': evn,
            'typeOfEvent': typeOfEvent,
            'des': des,
            'lat': lat,
            'lon': lon,
            'resource': resource
        }
       
       
        data_points.append(newEvent)
        save_data(data_points)


        return jsonify({'message': 'Data received successfully'})
    except Exception as e:
       
        print(f"Error: {e}")  
        return jsonify({'error': 'Failed to process data'}), 500
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': f'Missking key: {str(e)}'}), 400


@app.route('/plot')
def plot():
    # scatter mapbox plot
    fig = go.Figure(go.Scattermapbox(
        lat=[point['lat'] for point in data_points],
        lon=[point['lon'] for point in data_points],
        mode='markers',
        marker=go.scattermapbox.Marker(size=9, color='rgba(255, 0, 0, 0.8)'),
        text=[f"Event: {point['des']}<br>Resource: {point['resource']}" for point in data_points],
    ))


   
    fig.update_layout(
        template='plotly_dark',
        mapbox=dict(
            style="open-street-map",
            center={"lat": data_points[0]['lat'] if data_points else 0, "lon": data_points[0]['lon'] if data_points else 0},
            zoom=3,
        ),
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        font=dict(color='white')
    )
   
   
    return fig.to_html()




if __name__ == '__main__':
    app.run(debug=True)


