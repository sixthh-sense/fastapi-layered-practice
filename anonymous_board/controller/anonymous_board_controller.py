# Spring Boot / Spring Reactive
# @RestController / @Controller
# FastAPI의 경우 API Router라는 녀석이 위의 역할을 수행합니다.
from typing import List

from fastapi import APIRouter, HTTPException

from anonymous_board.controller.request.create_anonymous_board_request import CreateAnonymousBoardRequest
from anonymous_board.controller.response.anonymous_board_response import AnonymousBoardResponse
from anonymous_board.service.anonymous_board_service_impl import AnonymousBoardServiceImpl

from typing import List

# @RequestMapping("/board")
# Controller, Service, Repository 객체 모두 싱글톤 구성
# 안타깝게도 python은 특성상 이러한 IoC, DI 메커니즘이 취약함.
# 다만 Controller 역할을 하는 Router의 경우 알아서 싱글톤 구성을 가지게 됩니다.
anonymous_board_controller = APIRouter(prefix="/board")
board_service = AnonymousBoardServiceImpl.getInstance()

# 자동 완성 기능
# 맥북 - 옵션 + 앤터
# 리눅스 / 윈도우 - 알트 + 앤터

# @PostMapping("/create")
@anonymous_board_controller.post("/create",
                                 response_model=AnonymousBoardResponse)
def create_anonymous_board(request: CreateAnonymousBoardRequest):
    # 실제로 역할과 책임 관점에서 객체를 분리시키는 것이 더 좋은데
    # request로 퉁치는 것 보다 request_form과 request를 분리시키는 것이 더 좋음
    # 보편적으로 웹 페이지에서 요청하는 정보들은 여러가지 도메인 정보를 전부 가지고 있음
    # 그리고 여러 도메인 정보들이 특정 도메인에 기록되는 구성을 가지고 있음.
    # 실제로 위와 같은 형식으로 구성하면 request form이 바뀌더라도
    # 실제 controller, service 내부 코드는 바뀌지 않음
    # 왜냐하면 그 역할과 책임 자체가 request 객체에 있기 때문
    createdBoard = board_service.create(request.title, request.content)

    return AnonymousBoardResponse(
        id=createdBoard.id,
        title=createdBoard.title,
        content=createdBoard.content,
        created_at=createdBoard.created_at
    )

@anonymous_board_controller.get("/list",
                                response_model=List[AnonymousBoardResponse])
def list_anonymous_boards():
    boardList = board_service.list()

    return [
        AnonymousBoardResponse(
            id=anonymous_board.id,
            title=anonymous_board.title,
            content=anonymous_board.content,
            created_at=anonymous_board.created_at.isoformat()
        ) for anonymous_board in boardList
    ]

@anonymous_board_controller.get("/{board_id}",
    response_model=AnonymousBoardResponse)
def get_anonymous_board(board_id: str):
    try:
        anonymous_board = board_service.read(board_id)

    except ValueError:
        raise HTTPException(status_code=404, detail="Board not found")

    return AnonymousBoardResponse(
        id=anonymous_board.id,
        title=anonymous_board.title,
        content=anonymous_board.content,
        created_at=anonymous_board.created_at.isoformat()
    )