from flask import Blueprint, jsonify, request
import requests
import time

from unidecode import unidecode



api = Blueprint('api', __name__)


@api.route("/")
def hello_world():
    return jsonify(hello="world")


@api.route("/static/<path:filename>")
def staticfiles(filename):
    return send_from_directory(api.config["STATIC_FOLDER"], filename)


@api.route("/media/<path:filename>")
def mediafiles(filename):
    return send_from_directory(api.config["MEDIA_FOLDER"], filename)


@api.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        filename = secure_filename(file.filename)
        file.save(os.path.join(api.config["MEDIA_FOLDER"], filename))
    return """
    <!doctype html>
    <title>upload new File</title>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file><input type=submit value=Upload>
    </form>
    """


@api.route('/api/time')
def get_current_time():
        return jsonify({'time': time.time()})

@api.route('/api/gios-data')
def get_gios_data():
        try:
                response = requests.get('https://api.gios.gov.pl/pjp-api/rest/station/findAll')
                response.raise_for_status()
                data = response.json()
                return jsonify(data)
        except requests.RequestException as e:
                return jsonify({'error': str(e)}), 500

@api.route('/api/air-quality-index/<int:stationId>')
def get_air_quality_index(stationId):
        try:
                response = requests.get(f'https://api.gios.gov.pl/pjp-api/rest/aqindex/getIndex/{stationId}')
                response.raise_for_status()
                data = response.json()
                return jsonify(data)
        except requests.RequestException as e:
                return jsonify({'error': str(e)}), 500
        
@api.route('/api/gios-historic-data')
def get_gios_historic_data():
    try:
        # Retrieve query parameters
        indicator = request.args.get('indicator', default='')
        page = request.args.get('page', default='0')
        size = request.args.get('size', default='20')
        sort = request.args.get('sort', default='')
        wojewodztwo = request.args.get('wojewodztwo', default='')

        # Construct the GIOŚ API URL with query parameters
        api_url = f"https://api.gios.gov.pl/pjp-api/v1/rest/statistics/getStatisticsForPollutants?indicator={indicator}&page={page}&size={size}&sort={sort}&filter[wojewodztwo]={wojewodztwo}"

        # Make the request to the GIOŚ API
        response = requests.get(api_url)
        response.raise_for_status()  # This will raise an exception for HTTP errors
        data = response.json()
        lista_statystyk = data.get("Lista statystyk", [])
        for item in lista_statystyk:
            for key, value in item.items():
                if isinstance(value, str):
                    item[key] = unidecode(value)  # Replace non-ASCII characters
        
        data.historicDataProcessingPandas(jsonify(lista_statystyk))
        # Return the modified list as JSON
        return jsonify(lista_statystyk)

    except requests.RequestException as e:
        # Return error message if the request fails
        return jsonify({'error': str(e)}), 500
