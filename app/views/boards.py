from flask import request, Blueprint, g

from . import json_response
from ..models.boards import Board, BoardSchema
from ..shared.auth import Auth

board_api = Blueprint('board', __name__)
board_schema = BoardSchema


@board_api.route("/board", methods=['GET', 'POST'])
@Auth.token_required
def board_views():
    if request.method == 'GET':
        boards = Board.get_all_boards()
        ret_boards = {}

        for board in boards:
            ret_boards[board.name] = {
                "uuid": board.uuid,
                "name": board.name,
                "created_at": board.created_at
            }

        return json_response({'boards': ret_boards}, 200)
    elif request.method == 'POST':
        try:
            req_data = request.get_json()
            name = req_data['name']
        except TypeError:
            return json_response({'errorMsg': 'please send request data'}, 400)
        except KeyError:
            return json_response({'errorMsg': 'please check your request data'}, 400)

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



