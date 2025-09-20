# app/main.py
import os
from typing import Any, Dict, List, Optional

from fastapi import Body, FastAPI, Header, Query, Response
from fastapi.middleware.cors import CORSMiddleware

API_PREFIX = "/v1"
DEFAULT_ORDER_VERSION = os.getenv("ORDER_VERSION", "1")
ALLOWED_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app = FastAPI(title="IdeaFlow API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in ALLOWED_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- LIST (x–y window) ----
@app.get(f"{API_PREFIX}/posts")
def list_posts(
    response: Response,
    order: str = Query("position", pattern="^(position|date)$"),
    start: int = Query(1, ge=1),
    count: int = Query(25, ge=1, le=100),
    q: Optional[str] = None,
    tags: Optional[str] = None,
    status: Optional[str] = None,
    from_: Optional[str] = Query(None, alias="from"),
    to: Optional[str] = None,
):
    # TODO: query DB using (order,start,count) with sparse keys (or date order)
    response.headers["X-Order-Version"] = DEFAULT_ORDER_VERSION
    # Return empty list for now; front-end can integrate without payload shape lock.
    return {"items": [], "next_start": start + count}

# ---- CREATE ----
@app.post(f"{API_PREFIX}/posts")
def create_post(
    data: Dict[str, Any] = Body(...),
    idempotency_key: Optional[str] = Header(None, alias="Idempotency-Key"),
):
    # TODO: upsert idempotency key, insert row, return created post
    return {"ok": True}

# ---- UPDATE (full) ----
@app.put(f"{API_PREFIX}/posts/{{post_id}}")
def update_post(post_id: str, data: Dict[str, Any] = Body(...)):
    # TODO: full update
    return {"ok": True, "id": post_id}

# ---- PATCH (quick edits) ----
@app.patch(f"{API_PREFIX}/posts/{{post_id}}")
def patch_post(post_id: str, data: Dict[str, Any] = Body(...)):
    # TODO: partial update (e.g., target_date)
    return {"ok": True, "id": post_id}

# ---- REORDER (apply Just Sort or drag result) ----
@app.post(f"{API_PREFIX}/posts/reorder")
def reorder_posts(
    response: Response,
    body: Dict[str, Any] = Body(...),
):
    # TODO: rewrite sparse keys (only changed rows)
    response.headers["X-Order-Version"] = str(int(DEFAULT_ORDER_VERSION))
    return {"ok": True}

# ---- OPTIONAL single-move endpoint (midpoint strategy) ----
@app.post(f"{API_PREFIX}/posts/move")
def move_post(body: Dict[str, Any] = Body(...)):
    # TODO: compute new position_key between neighbors
    return {"ok": True}

# ---- AI preview (proxy to HF Space later) ----
@app.post(f"{API_PREFIX}/ai/sort")
def ai_sort(posts: List[Dict[str, Any]] = Body(...), x_shared_secret: Optional[str] = Header(None, alias="X-Shared-Secret")):
    # TODO: call HF Space with gradio_client, pass X-Shared-Secret from env
    return {"order": [], "scores": [], "source": "heuristic"}

# ---- DELETE ----
@app.delete(f"{API_PREFIX}/posts/{{post_id}}")
def delete_post(post_id: str):
    # TODO: hard or soft delete
    return {"ok": True}

# ---- Client logs ----
@app.post(f"{API_PREFIX}/log")
def client_log(payload: Dict[str, Any] = Body(...)):
    # TODO: write to server logs / DB
    return {"ok": True}

# ---- Health ----
@app.get(f"{API_PREFIX}/healthz")
def healthz():
    return {"ok": True}
