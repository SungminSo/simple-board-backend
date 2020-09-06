from flask import request, Blueprint, g

from . import json_response
from ..models.boards import Board
from ..models.articles import Article
from ..shared.auth import Auth

article_api = Blueprint('article', __name__)


@article_api.route("/article", methods=['GET', 'POST'])
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
