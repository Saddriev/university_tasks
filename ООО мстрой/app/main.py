"""
Точка входа FastAPI: TreeStore API — загрузка дерева из JSON, эндпоинты дерева и health.
"""
import json
import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, Request, status

from app.config import settings
from app.schemas import (
    ItemIdRequest,
    TreeStoreRequest,
    TreeStoreResponse,
)
from app.treestore import ItemNotFoundError, TreeStore

logger = logging.getLogger(__name__)


def load_items_from_json(path: Path) -> list[dict[str, Any]]:
    """
    Загружает массив элементов из JSON-файла.
    Raises:
        FileNotFoundError: если файл не найден.
        json.JSONDecodeError: если содержимое не валидный JSON.
    """
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_tree_store(request: Request) -> TreeStore:
    """Зависимость: возвращает TreeStore из app.state."""
    store = getattr(request.app.state, "tree_store", None)
    if store is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="TreeStore not initialized",
        )
    return store


def _create_tree_store(items: list[dict[str, Any]]) -> TreeStore:
    """Создаёт экземпляр TreeStore из списка элементов."""
    return TreeStore(items)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Загрузка дерева при старте, освобождение при остановке."""
    try:
        items = load_items_from_json(settings.data_file)
        app.state.tree_store = _create_tree_store(items)
        logger.info(
            "TreeStore initialized from %s (%s items)",
            settings.data_file,
            len(items),
        )
    except FileNotFoundError:
        logger.warning(
            "Data file not found: %s, starting with empty tree",
            settings.data_file,
        )
        app.state.tree_store = _create_tree_store([])
    except json.JSONDecodeError as e:
        logger.exception("Invalid JSON in data file: %s", settings.data_file)
        raise RuntimeError(
            f"Invalid data file {settings.data_file}: {e!s}"
        ) from e
    yield
    app.state.tree_store = None


app = FastAPI(title="TreeStore API", version="1.0.0", lifespan=lifespan)


@app.post(
    "/api/v1/tree/init",
    response_model=TreeStoreResponse,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal server error",
        },
    },
)
def init_tree(request: TreeStoreRequest, req: Request) -> TreeStoreResponse:
    """Инициализирует дерево переданным массивом элементов."""
    req.app.state.tree_store = TreeStore(request.items)
    return TreeStoreResponse(
        result={
            "status": "initialized",
            "items_count": len(request.items),
        }
    )


@app.get(
    "/api/v1/tree/getAll",
    response_model=TreeStoreResponse,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal server error",
        },
    },
)
def get_all(
    tree_store: TreeStore = Depends(get_tree_store),
) -> TreeStoreResponse:
    """Возвращает все элементы дерева."""
    result = tree_store.get_all()
    return TreeStoreResponse(result=result)


@app.post(
    "/api/v1/tree/getItem",
    response_model=TreeStoreResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Item not found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal server error",
        },
    },
)
def get_item(
    request: ItemIdRequest,
    tree_store: TreeStore = Depends(get_tree_store),
) -> TreeStoreResponse:
    """Возвращает элемент по id. 404, если элемент не найден."""
    try:
        result = tree_store.get_item(request.id)
        return TreeStoreResponse(result=result)
    except ItemNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@app.post(
    "/api/v1/tree/getChildren",
    response_model=TreeStoreResponse,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal server error",
        },
    },
)
def get_children(
    request: ItemIdRequest,
    tree_store: TreeStore = Depends(get_tree_store),
) -> TreeStoreResponse:
    """Возвращает дочерние элементы для указанного id."""
    result = tree_store.get_children(request.id)
    return TreeStoreResponse(result=result)


@app.post(
    "/api/v1/tree/getAllParents",
    response_model=TreeStoreResponse,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal server error",
        },
    },
)
def get_all_parents(
    request: ItemIdRequest,
    tree_store: TreeStore = Depends(get_tree_store),
) -> TreeStoreResponse:
    """Возвращает цепочку родителей от элемента до корня."""
    result = tree_store.get_all_parents(request.id)
    return TreeStoreResponse(result=result)


@app.get(
    "/api/v1/health",
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal server error",
        },
    },
)
def health() -> dict[str, str]:
    """Проверка работоспособности API."""
    return {"status": "ok"}
