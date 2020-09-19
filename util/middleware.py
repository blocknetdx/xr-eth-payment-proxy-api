import datetime
from functools import wraps
from flask import g, request, jsonify
from database.models import db_session, Project


def check_keys_exist(req):
    print(req.headers.get('Api-Key'), req.view_args['project_id'])
    if 'Api-Key' not in req.headers or 'project_id' not in req.view_args:
        return False

    return True


def missing_keys():
    response = jsonify({
        'message': "API_KEY header missing or project-id missing from path!",
        'error': 1
    })

    return response, 401


def project_not_exists():
    response = jsonify({
        'message': "API_KEY is incorrect or project-id does not exist!",
        'error': 2
    })

    return response, 401


def project_expired():
    response = jsonify({
        'message': "Project has expired!",
        'error': 3
    })

    return response, 401


def api_tokens_exceeded():
    response = jsonify({
        'message': "API Tokens Exceeded!",
        'error': 4
    })

    return response, 401


def authenticate(f):
    @wraps(f)
    @db_session
    def wrapper(*args, **kwargs):
        if not check_keys_exist(request):
            return missing_keys()

        project_id = request.view_args['project_id']
        api_key = request.headers.get('Api-Key')

        project = Project.get(name=project_id, api_key=api_key, active=True)
        if project is None:
            return project_not_exists()

        if datetime.datetime.now() > project.expires:
            return project_not_exists()

        if project.used_api_tokens is None:
            project.used_api_tokens = 0

        if project.used_api_tokens >= project.api_token_count:
            project.active = False
            return api_tokens_exceeded()

        project.used_api_tokens += 1

        g.project = project

        return f(*args, **kwargs)
    return wrapper
