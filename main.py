import os
import json
from flask import Flask, Response, g, jsonify, request
from database.models import db_session, select, Project
from util.middleware import authenticate
from util.request_handler import RequestHandler

app = Flask(__name__)
req_handler = RequestHandler()


@app.errorhandler(400)
def bad_request_error(error):
    response = jsonify({
        'error': 'Bad Request'
    })
    return response


@app.errorhandler(500)
def internal_server_error(error):
    response = jsonify({
        'error': 'Internal Server Error'
    })
    return response


@app.errorhandler(401)
def unauthorized_error(error):
    response = jsonify({
        'error': 'Unauthorized User Access'
    })
    return response


@app.route('/xrs/request_project', methods=['POST'])
def request_project():
    project = req_handler.get_project()

    app.logger.info('Project Requested: {}'.format(project))

    return jsonify(project)


@app.route('/all_projects', methods=['GET'])
def all_projects():
    if not os.environ.get('DEBUG', False):
        return Response({}, 401)

    results = []
    try:
        with db_session:
            query = select(p for p in Project)

            results = [{
                'name': p.name,
                # 'api_key': p.api_key,
                'api_token_count': p.api_token_count,
                'used_api_tokens': p.used_api_tokens,
                'expires': str(p.expires),
                'active': p.active,
            } for p in query]
    except Exception as e:
        app.logger.info(e)

    return jsonify(results)


@app.route('/xrs/eth_passthrough/<project_id>', methods=['POST'])
@authenticate
def handle_request(project_id):
    headers = {
        'PROJECT-ID': project_id,
        'API-TOKENS': g.project.api_token_count,
        'API-TOKENS-USED': g.project.used_api_tokens,
        'API-TOKENS-REMAINING': g.project.api_token_count - g.project.used_api_tokens
    }

    data = request.get_json(force=True)
    method = data['method']
    params = data['params']

    app.logger.info('Received Method: {}, Params: {}'.format(method, params))

    response = req_handler.post_eth_proxy(method=method, params=params)

    return Response(headers=headers, response=json.dumps(response))


def main():
    app.run(host='0.0.0.0', port=8080)


if __name__ == '__main__':
    main()
