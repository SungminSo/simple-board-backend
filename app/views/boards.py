from flask import request, Blueprint, g

from . import json_response
from ..models.boards import Board
from ..models.articles import Article
from ..shared.auth import Auth

board_api = Blueprint('board', __name__)


@board_api.route('/board/<int:limit>/boards/<int:page>', methods=['GET'])
@Auth.token_required
def get_boards(limit: int, page: int):
    boards = Board.get_all_boards()
    ret_boards = []

    for board in boards[limit * (page-1):limit * page]:
        ret_boards.append({
            'uuid': board.uuid,
            'name': board.name,
            'created_at': board.created_at,
            'updated_at': board.updated_at
        })

    return json_response({'total': len(boards), 'boards': ret_boards}, 200)


@board_api.route('/board', methods=['POST'])
@Auth.token_required
def create_board():
    try:
        req_data = request.get_json()
        name = req_data['name']
    except TypeError:
        return json_response({'errorMsg': 'please send request data'}, 400)
    except KeyError:
        return json_response({'errorMsg': 'please check your request data'}, 400)

    if len(name) == 0:
        return json_response({'errorMsg': 'please check board name'}, 400)

    board_already_exists = Board.find_board_by_name(name)
    if board_already_exists:
        return json_response({'errorMsg': 'board already exists'}, 409)

    user_id = g.user['id']

    board = Board(
        name=name,
        user_id=user_id
    )
    board_uuid = board.save()

    return json_response({'uuid': board_uuid}, 201)


@board_api.route('/board', methods=['PATCH'])
@Auth.token_required
def update_board():
    try:
        req_data = request.get_json()
        uuid = req_data['uuid']
        new_name = req_data['new_name']
    except TypeError:
        return json_response({'errorMsg': 'please send request data'}, 400)
    except KeyError:
        return json_response({'errorMsg': 'please check your request data'}, 400)

    if len(new_name) == 0:
        return json_response({'errorMsg': 'please check board name'}, 400)

    board = Board.find_board_by_uuid(uuid)
    if not board:
        return json_response({'errorMsg': 'board does not exist'}, 404)

    user_id = g.user['id']
    if board.user_id != user_id:
        return json_response({'errorMsg': 'permission denied'}, 403)

    board_uuid = board.update(new_name)
    return json_response({'uuid': board_uuid}, 200)


@board_api.route('/board/<string:uuid>', methods=['DELETE'])
@Auth.token_required
def delete_board(uuid: str):
    board = Board.find_board_by_uuid(uuid)
    if not board:
        return json_response({'errorMsg': 'board does not exist'}, 404)

    user_id = g.user['id']
    if board.user_id != user_id:
        return json_response({'errorMsg': 'permission denied'}, 403)

    articles = Article.get_articles_by_board(board.id)
    for article in articles:
        article.delete()
    board.delete()
    return json_response({}, 204)


@board_api.route('/dashboard/<int:article_num>', methods=['GET'])
@Auth.token_required
def get_dashboard(article_num: int):
    boards = Board.get_all_boards()
    ret_boards = []

    for board in boards:
        articles = Article.get_recent_articles_by_board(board.id, article_num)
        ret_article = []

        for article in articles:
            ret_article.append({
                'uuid': article.uuid,
                'title': article.title,
                'content': article.content,
                'created_at': article.created_at,
                'updated_at': article.updated_at
            })

        ret_boards.append({
            'uuid': board.uuid,
            'name': board.name,
            'created_at': board.created_at,
            'updated_at': board.updated_at,
            'articles': ret_article
        })

    return json_response({'boards': ret_boards}, 200)
