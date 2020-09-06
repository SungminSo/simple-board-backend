from flask import request, Blueprint, g

from . import json_response
from ..models.boards import Board
from ..models.articles import Article
from ..shared.auth import Auth

article_api = Blueprint('article', __name__)


@article_api.route("/article", methods=['GET', 'POST', 'PATCH', 'DELETE'])
@Auth.token_required
def article_views():
    if request.method == 'GET':
        try:
            board_uuid = request.args.get('board')
        except TypeError:
            return json_response({'errorMsg': 'please send request data'}, 400)
        except KeyError:
            return json_response({'errorMsg': 'please check your request data'}, 400)

        board = Board.find_board_by_uuid(board_uuid)
        if not board:
            return json_response({'errorMsg': 'board does not exist'}, 404)

        articles = Article.get_articles_by_board(board.id)
        ret_articles = {}

        for article in articles:
            ret_articles[article.title] = {
                "uuid": article.uuid,
                "title": article.title,
                "content": article.content,
                "created_at": article.created_at,
                "updated_at": article.updated_at
            }

        return json_response({'articles': ret_articles}, 200)

    elif request.method == 'POST':
        try:
            req_data = request.get_json()
            title = req_data['title']
            content = req_data['content']
            board_uuid = req_data['board_uuid']
        except TypeError:
            return json_response({'errorMsg': 'please send request data'}, 400)
        except KeyError:
            return json_response({'errorMsg': 'please check your request data'}, 400)

        board = Board.find_board_by_uuid(board_uuid)
        if not board:
            return json_response({'errorMsg': 'board does not exist'})

        user_id = g.user['id']

        article = Article(
            title=title,
            content=content,
            board_id=board.id,
            user_id=user_id
        )
        article_uuid = article.save()
        board.update_latest_article(article_uuid)

        return json_response({'uuid': article_uuid}, 201)

    elif request.method == 'PATCH':
        try:
            req_data = request.get_json()
            uuid = req_data['uuid']
            new_title = req_data['new_title']
            new_content = req_data['new_content']
        except TypeError:
            return json_response({'errorMsg': 'please send request data'}, 400)
        except KeyError:
            return json_response({'errorMsg': 'please check your request data'}, 400)

        article = Article.find_article_by_uuid(uuid)
        if not article:
            return json_response({'errorMsg': 'article does not exist'}, 404)

        user_id = g.user['id']
        if article.user_id != user_id:
            return json_response({'errorMsg': 'permission denied'}, 403)

        article_uuid = article.update(new_title, new_content)
        return json_response({'uuid': article_uuid}, 200)

    elif request.method == 'DELETE':
        try:
            uuid = request.args.get('uuid')
        except TypeError:
            return json_response({'errorMsg': 'please send request data'}, 400)
        except KeyError:
            return json_response({'errorMsg': 'please check your request data'}, 400)

        article = Article.find_article_by_uuid(uuid)
        if not article:
            return json_response({'errorMsg': 'article does not exsit'}, 404)

        user_id = g.user['id']
        if article.user_id != user_id:
            return json_response({'errorMsg': 'permission denied'}, 403)

        article.delete()
        return json_response({}, 204)
