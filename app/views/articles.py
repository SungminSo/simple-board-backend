from flask import request, Blueprint, g

from . import json_response
from ..models import db
from ..models.boards import Board
from ..models.articles import Article
from ..shared.auth import Auth

article_api = Blueprint('article', __name__)


@article_api.route('/article/<string:board>/<int:limit>/articles/<int:page>', methods=['GET'])
@Auth.token_required
def get_articles(board: str, limit: int, page: int):
    board = Board.find_board_by_uuid(board)
    if not board:
        return json_response({'errorMsg': 'board does not exist'}, 404)

    articles = Article.get_articles_by_board(board.id)
    ret_articles = []

    for article in articles[limit * (page - 1):limit * page]:
        ret_articles.append({
            'uuid': article.uuid,
            'title': article.title,
            'content': article.content,
            'created_at': article.created_at,
            'updated_at': article.updated_at
        })

    return json_response({'total': len(articles), 'articles': ret_articles}, 200)


@article_api.route('/article', methods=['POST'])
@Auth.token_required
def create_article():
    try:
        req_data = request.get_json()
        title = req_data['title']
        content = req_data['content']
        board_uuid = req_data['board_uuid']
    except TypeError:
        return json_response({'errorMsg': 'please send request data'}, 400)
    except KeyError:
        return json_response({'errorMsg': 'please check your request data'}, 400)

    try:
        if len(title) == 0 or len(content) == 0:
            return json_response({'errorMsg': 'please check title and content'}, 400)
    except TypeError:
        return json_response({'errorMsg': 'please check you title, content, board_uuid data type'}, 400)
    board = Board.find_board_by_uuid(board_uuid)
    if not board:
        return json_response({'errorMsg': 'board does not exist'}, 404)

    user_id = g.user['id']

    article = Article(
        title=title,
        content=content,
        board_id=board.id,
        user_id=user_id
    )
    article_uuid = article.save()
    db.session.commit()

    return json_response({'uuid': article_uuid}, 201)


@article_api.route('/article', methods=['PATCH'])
@Auth.token_required
def update_article():
    try:
        req_data = request.get_json()
        uuid = req_data['uuid']
        new_title = req_data['new_title']
        new_content = req_data['new_content']
    except TypeError:
        return json_response({'errorMsg': 'please send request data'}, 400)
    except KeyError:
        return json_response({'errorMsg': 'please check your request data'}, 400)

    try:
        if len(new_title) == 0 or len(new_content) == 0:
            return json_response({'errorMsg': 'please check title and content'}, 400)
    except TypeError:
        return json_response({'errorMsg': 'please check you title and content data type'}, 400)
    article = Article.find_article_by_uuid(uuid)
    if not article:
        return json_response({'errorMsg': 'article does not exist'}, 404)

    user_id = g.user['id']
    if article.user_id != user_id:
        return json_response({'errorMsg': 'permission denied'}, 403)

    article_uuid = article.update(new_title, new_content)
    db.session.commit()

    return json_response({'uuid': article_uuid}, 200)


@article_api.route('/article/<string:uuid>', methods=['DELETE'])
@Auth.token_required
def delete_article(uuid: str):
    article = Article.find_article_by_uuid(uuid)
    if not article:
        return json_response({'errorMsg': 'article does not exist'}, 404)

    user_id = g.user['id']
    if article.user_id != user_id:
        return json_response({'errorMsg': 'permission denied'}, 403)

    article.delete()
    db.session.commit()

    return json_response({}, 204)
