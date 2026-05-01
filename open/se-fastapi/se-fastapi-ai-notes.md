# FastAPI 深入掌握 — AI 笔记

> 来源：
> - FastAPI 官方文档 - Dependencies: https://fastapi.tiangolo.com/tutorial/dependencies/
> - FastAPI 官方文档 - Dependencies with Yield: https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/
> - FastAPI 官方文档 - Classes as Dependencies: https://fastapi.tiangolo.com/tutorial/dependencies/classes-as-dependencies/
> - FastAPI 官方文档 - Middleware (Tutorial): https://fastapi.tiangolo.com/tutorial/middleware/
> - FastAPI 官方文档 - Advanced Middleware: https://fastapi.tiangolo.com/advanced/middleware/
> - FastAPI 官方文档 - Lifespan Events: https://fastapi.tiangolo.com/advanced/events/
> - FastAPI 官方文档 - Deployment Concepts: https://fastapi.tiangolo.com/deployment/concepts/
> 生成时间：2026-05-01
> 学习目标：FastAPI 核心机制系统学习

---

## 锚点

想象一条工厂流水线。请求是原材料，从入口进来，经过一道道工序：质检（中间件）→ 领取配件（依赖注入）→ 加工（路由函数）→ 包装（响应模型）→ 再过一遍质检（中间件返回）→ 出厂。流水线开工前要预热机器（startup），下班要关灯锁门（shutdown）。整条线的效率取决于每道工序是不是非阻塞的（async）。

FastAPI 的所有核心机制都在这条流水线上。后面每个概念，都是流水线上的一个环节。

## 核心问题

为什么 Flask 写一个接口很快，但项目大了以后到处都在重复"获取数据库连接→查用户→关连接"？因为 Flask 没有一个统一的"领配件"环节——每个路由函数得自己准备自己需要的东西。FastAPI 的依赖注入就是解决这个问题的：路由函数只管声明"我需要什么"，框架替你准备好。

## 核心概念

### 依赖注入（Dependency Injection）

路由函数声明自己需要什么，框架负责准备好、传进来。你不用自己创建数据库连接、不用自己解析 token——写上参数类型，FastAPI 自动搞定。

```python
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/{user_id}")
async def read_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(User).get(user_id)
```

`Depends(get_db)` 就是告诉 FastAPI："调用这个路由之前，先帮我执行 `get_db`，把结果给我。"

少了它会怎样？每个路由函数都要自己写 `db = SessionLocal()` 和 `db.close()`，十几个接口就重复十几次。而且一旦连接方式变了，你得改十几个地方。

### 依赖嵌套（Sub-dependencies）

依赖本身也能依赖别的东西。A 依赖 B，B 依赖 C，FastAPI 会自动按顺序解析，先执行 C，再 B，最后 A。就像流水线上，"安装引擎"这道工序需要"引擎"这个配件，而"引擎"又需要"螺丝"——框架自动把螺丝准备好、装好引擎、再给你。

```python
def get_token_header(x_token: str = Header()):
    if x_token != "fake-super-secret-token":
        raise HTTPException(400, "X-Token header invalid")
    return x_token

def get_query_param(q: str = Query()):
    return q

@app.get("/items/")
async def read_items(
    token: str = Depends(get_token_header),
    q: str = Depends(get_query_param),
):
    return {"token": token, "q": q}
```

`get_token_header` 还可以进一步依赖别的东西，形成任意深度的依赖树。FastAPI 自动处理拓扑排序。

### 类作为依赖（Classes as Dependencies）

不光函数能当依赖，类也行。只要类的 `__init__` 参数 FastAPI 能解析（比如 `int`、`str`、`Header()` 等），就能用 `Depends(MyClass)` 自动实例化。

```python
class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

@app.get("/items/")
async def items(commons: CommonQueryParams = Depends(CommonQueryParams)):
    return {"q": commons.q, "skip": commons.skip, "limit": commons.limit}
```

简写：`commons: CommonQueryParams = Depends()` — 省略括号里的类名，FastAPI 从类型注解推断。

为什么需要类？当多个参数总是一起出现时（比如分页的 skip/limit），用类打包比散着一堆参数干净。

### yield 依赖（资源清理）

用 `yield` 而不是 `return` 来提供依赖，`yield` 后面的代码在请求结束后执行，用来做清理工作。这就是"领配件→用完→还回去"的完整周期。

```python
async def get_db():
    db = SessionLocal()
    try:
        yield db    # 这里把连接给路由函数用
    finally:
        db.close()   # 请求结束后自动关闭连接
```

请求进来 → 执行到 `yield` → 把 `db` 传给路由函数 → 路由函数执行完 → 回来执行 `db.close()`。

少了它？你只能在路由函数末尾手动 `db.close()`，但一旦路由函数抛异常，`close()` 就跳过了。`yield + finally` 保证无论如何都会清理。

### 依赖的作用域（Scope）

同一个依赖被多个路由使用时，默认每次请求都重新执行。但你可以用 `use_cache=True`（默认值）让同一个请求内、同一个依赖只执行一次。

```python
# 同一个请求内，不管多少个依赖用了 get_db，只执行一次
db: Session = Depends(get_db)
```

还有一个更深层的概念：依赖的生命周期。函数级的依赖（默认）每次请求创建、请求结束销毁。如果你想要应用级的单例（比如数据库连接池），应该用 lifespan 或者模块级变量，不要用依赖注入。

### 中间件（Middleware）

请求进来后、到达路由函数之前，以及路由函数返回响应之后，中间件都要过一遍。像流水线上的质检站：原材料进来先过第一道质检，成品出来再过一遍。

```python
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)  # 放行，让请求继续往下走
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

关键在 `call_next(request)` — 这一行把请求传给下一个中间件（或最终的路由函数），拿到响应后再回来执行后面的代码。

### 中间件的执行顺序

最后注册的中间件，最先处理请求，最后处理响应。像洋葱：最外层先包，最后拆。

```python
@app.middleware("http")  # 第三层（最外层）
async def middleware_c(request, call_next):
    print("C: 请求进来")
    response = await call_next(request)
    print("C: 响应出去")
    return response

@app.middleware("http")  # 第二层
async def middleware_b(request, call_next):
    print("B: 请求进来")
    response = await call_next(request)
    print("B: 响应出去")
    return response

@app.middleware("http")  # 第一层（最内层）
async def middleware_a(request, call_next):
    print("A: 请求进来")
    response = await call_next(request)
    print("A: 响应出去")
    return response
```

请求经过顺序：C → B → A → 路由函数 → A → B → C。

为什么这么设计？因为 `@app.middleware` 是装饰器模式——每个中间件把下一个包在里面。最后添加的包在最外面，所以最先执行。

### 生命周期事件（Lifespan）

应用启动时做什么（加载模型、连数据库）、关闭时做什么（释放连接、清缓存）。用 `lifespan` 参数配合 `asynccontextmanager` 实现。

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时执行（yield 之前）
    model = load_ml_model()
    app.state.model = model
    print("模型加载完成")

    yield  # 应用运行中...

    # 关闭时执行（yield 之后）
    release_model(model)
    print("资源释放完成")

app = FastAPI(lifespan=lifespan)
```

老写法 `@app.on_event("startup")` 和 `@app.on_event("shutdown")` 已废弃，官方推荐 lifespan。

为什么 lifespan 更好？on_event 的 startup 和 shutdown 是分开的两个函数，没法共享局部变量。lifespan 用一个函数、一个 yield 就搞定了，上下文自然共享。而且 lifespan 是 ASGI 标准协议的一部分，不依赖 FastAPI 特有功能。

### 请求/响应模型（Pydantic）

用 Pydantic 的 `BaseModel` 定义数据结构，FastAPI 自动做三件事：验证请求数据、转换类型、生成 OpenAPI 文档。

```python
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    age: int | None = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

@app.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate):
    # user 已经被验证过、转换过类型了
    # response_model 自动过滤掉不在 UserResponse 里的字段
    return save_user(user)
```

`response_model` 的核心作用是**过滤输出**。数据库返回了 20 个字段，但 `response_model` 只定义了 3 个，API 就只返回这 3 个。密码字段？不存在的。

### 异步与性能

FastAPI 基于 Starlette（ASGI 框架）。ASGI 和 WSGI 的区别就一个字：**异步**。

同步框架（Flask/Django）处理请求时，一个请求占一个线程。数据库查询花了 50ms？线程就在那等 50ms，别的请求进不来（除非开新线程）。

异步框架（FastAPI）处理请求时，遇到 I/O 操作（数据库、网络、文件）就挂起当前协程，去处理别的请求。等 I/O 完了再回来继续。一个线程就能处理几百个并发。

但有个前提：你的数据库驱动、HTTP 客户端也得是异步的（比如用 `databases` 而不是 `sqlite3`，用 `httpx` 而不是 `requests`）。如果你在 async 函数里调用了同步阻塞代码（比如 `time.sleep()`），反而比同步框架更慢——因为你在异步事件循环里阻塞了所有人。

```python
# 对了
@app.get("/users")
async def get_users():
    users = await db.fetch_all("SELECT * FROM users")  # 异步 I/O
    return users

# 错了
@app.get("/users")
async def get_users():
    time.sleep(5)  # 阻塞！整个事件循环卡住
    return []
```

FastAPI 也支持同步路由函数（不加 `async`）。它会在线程池里执行，不会阻塞事件循环。所以如果你不确定，写普通 `def` 反而更安全。

## 关键代码模式

### 模式 1：可复用的依赖注入

```python
# dependencies.py
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = jwt.decode(token, SECRET_KEY)
    user = db.query(User).get(payload["sub"])
    if not user:
        raise HTTPException(401)
    return user

# router.py
@app.get("/me")
async def read_me(user: User = Depends(get_current_user)):
    return user
```

什么时候用：多个接口需要"当前登录用户"时。把认证逻辑集中到一个依赖里，路由函数只管用。

### 模式 2：依赖覆盖（测试用）

```python
def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
```

什么时候用：测试时替换真实数据库为测试数据库。不用改任何路由代码，只在测试 setup 里覆盖一次。

### 模式 3：中间件链

```python
@app.middleware("http")
async def catch_exceptions(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid4())
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response
```

执行顺序：catch_exceptions（外层）→ add_request_id（内层）→ 路由函数。异常捕获在最外层，保证所有错误都能兜住。

### 模式 4：Lifespan 资源管理

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    app.state.redis = await aioredis.from_url("redis://localhost")
    app.state.db_pool = await create_pool(DATABASE_URL)
    yield
    # shutdown
    await app.state.redis.close()
    await app.state.db_pool.close()

app = FastAPI(lifespan=lifespan)

# 在路由里访问
@app.get("/cache/{key}")
async def get_cache(key: str):
    val = await app.state.redis.get(key)
    return {"key": key, "value": val}
```

什么时候用：需要全局共享的资源（Redis 连接、数据库连接池、ML 模型）。

## 逐节详解

### Section 1: 依赖注入机制

碰到的问题：每个路由都要重复"获取资源→使用→释放"的逻辑。比如 10 个接口都要查数据库，就得写 10 次 `db = SessionLocal(); try: ...; finally: db.close()`。

自然的想法：把获取数据库连接抽成一个函数，每个路由调用它。但谁来保证 `close()` 一定执行？路由抛异常怎么办？

FastAPI 的做法：用 `Depends()` 声明依赖，框架负责执行和清理。用 `yield` 代替 `return`，`yield` 后面的代码在请求结束后必定执行（类似 try/finally）。

**依赖的四种写法**：

1. **函数依赖**：最常见，`Depends(get_something)`
2. **类依赖**：参数打包，`Depends(MyClass)` — FastAPI 自动调用 `__init__`
3. **嵌套依赖**：A 依赖 B，B 依赖 C，自动解析
4. **yield 依赖**：带清理逻辑，`yield` 前是准备，`yield` 后是清理

**缓存行为**：同一个请求内，同一个依赖函数默认只执行一次，结果被缓存。如果需要每次都执行，用 `Depends(get_something, use_cache=False)`。

**Annotated 类型别名**（推荐写法）：

```python
from typing import Annotated

DBSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]

@app.get("/me")
async def read_me(db: DBSession, user: CurrentUser):
    return user
```

好处：类型别名可以复用，不用在每个路由里重复写 `Depends()`。

### Section 2: 中间件执行顺序

碰到的问题：需要在每个请求前后加通用逻辑（日志、认证、CORS、压缩）。不想每个路由都写一遍。

自然的想法：写个装饰器包在每个路由上。但路由多了容易漏，而且装饰器之间有顺序依赖时容易搞混。

FastAPI 的做法：中间件是全局的，用 `@app.middleware("http")` 注册。执行顺序由注册顺序决定——最后注册的最先执行。

**关键细节**：

1. `@app.middleware("http")` 和 `app.add_middleware(SomeMiddleware)` 的区别：前者是函数式中间件，后者是类式中间件（如 `GZipMiddleware`、`CORSMiddleware`）。

2. `BaseHTTPMiddleware` 是 Starlette 提供的基类，适合写有状态或需要初始化参数的中间件。但有个坑：它会把响应体完全读入内存。如果响应很大（比如文件下载），用函数式中间件更安全。

3. `call_next(request)` 返回的是 `Response` 对象。如果你想修改响应体，需要先读取 `response.body`，修改后创建新的 `Response`。直接修改原 response 的 body 是无效的。

```python
@app.middleware("http")
async def modify_response(request: Request, call_next):
    response = await call_next(request)
    # 想修改 body？这样不对：response.body = b"new body"
    # 这样才对：
    body = b""
    async for chunk in response.body_iterator:
        body += chunk
    return JSONResponse(
        content={"modified": True, "original": body.decode()},
        status_code=response.status_code,
        headers=dict(response.headers),
    )
```

4. 中间件的注册顺序 = `app.add_middleware` 的调用顺序。FastAPI 内部会把它们存在一个列表里，请求来时从后往前执行。所以如果你先注册 CORS 再注册认证，请求进来时先过认证再过 CORS——这可能不是你想要的。通常 CORS 应该是最外层（最先注册）。

### Section 3: 生命周期事件

碰到的问题：应用启动时需要加载资源（ML 模型、数据库连接池），关闭时需要释放。这些操作只执行一次，不是每个请求都执行。

自然的想法：用全局变量。在模块加载时初始化，在 `atexit` 里清理。但 `atexit` 不保证执行时序，而且异步资源的清理 `atexit` 做不了（它不支持 async）。

FastAPI 的做法：`lifespan` 参数 + `@asynccontextmanager`。yield 前是 startup，yield 后是 shutdown。

**lifespan vs on_event**：

| 维度 | lifespan | on_event（已废弃） |
|------|---------|-------------------|
| 写法 | 一个函数，yield 分隔 | 两个装饰器，分开写 |
| 变量共享 | 天然共享（同一个函数作用域） | 需要用全局变量或 app.state |
| 标准化 | ASGI 协议标准 | FastAPI 特有 |
| 异常处理 | yield 后的代码保证执行 | shutdown 可能被跳过 |

**实际应用场景**：

- 加载 ML 模型到内存
- 创建数据库连接池
- 初始化 Redis 连接
- 启动后台任务（如定时清理）
- 关闭时释放所有资源

**多个 lifespan 的组合**：如果项目有多个模块各自需要 lifespan，可以用 `from contextlib import AsyncExitStack` 组合，或者把所有初始化逻辑集中到一个 lifespan 函数里。后者更简单、更常见。

### Section 4: 请求/响应模型设计

碰到的问题：前端传过来的数据格式不确定，可能是字符串可能是数字；后端返回的数据可能包含敏感字段（密码、内部 ID）。

自然的想法：手动验证每个字段，手动构造返回字典。但这很繁琐，而且容易漏。

FastAPI 的做法：Pydantic 模型自动验证、转换、过滤。

**请求模型（BaseModel 子类）**：

```python
class ItemCreate(BaseModel):
    name: str                    # 必填，必须是字符串
    price: float                 # 必填，自动转 float（"9.9" → 9.9）
    description: str | None = None  # 选填，默认 None
    tags: list[str] = []         # 选填，默认空列表
```

FastAPI 拿到这段代码后自动做的事：
- 请求体里没有 `name`？返回 422 + 具体错误信息
- `price` 传了 `"abc"`？返回 422 + "not a valid float"
- 多传了 `id` 字段？默认忽略（Pydantic v2 配置可改）

**响应模型（response_model 参数）**：

```python
class UserResponse(BaseModel):
    id: int
    name: str
    email: str

@app.get("/users/{id}", response_model=UserResponse)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).get(id)
    # user 对象可能有 password_hash, created_at, updated_at 等十几个字段
    # 但 response_model 只返回 id, name, email
    return user
```

`response_model` 的三大作用：
1. **过滤字段** — 只返回模型里定义的字段
2. **类型转换** — 返回值自动转成模型定义的类型
3. **文档生成** — OpenAPI 文档里自动出现对应的 schema

**response_model_exclude_unset**：只返回实际设置了值的字段，没设置的不返回。适合 PATCH 接口——客户端只传了 name，返回里就没有 description 字段（而不是 description: null）。

### Section 5: 性能优化

碰到的问题：高并发下接口变慢。原因可能有好几个：阻塞 I/O、序列化慢、连接没复用。

**异步 vs 同步路由**：

- `async def` 路由：在事件循环里执行。适合 I/O 密集型（数据库查询、调用外部 API）。前提是用的库也是异步的。
- `def` 路由（不加 async）：在线程池里执行。适合 CPU 密集型或必须用同步库的场景。不会阻塞事件循环。
- `async def` 里调用同步阻塞代码：**最差选择**。阻塞事件循环，所有请求都卡住。

**并发模型**：

FastAPI 背后是 Uvicorn（ASGI 服务器）。每个 worker 是一个进程，每个进程里有一个事件循环。主流部署方式：

```
nginx → uvicorn (多 worker) → FastAPI app
```

worker 数量一般设为 `2 * CPU核心数 + 1`。不是越多越好——worker 之间不共享内存，太多反而浪费资源。

**常见优化手段**：

1. **连接池**：数据库、Redis、HTTP 客户端都用连接池，不要每次请求新建连接
2. **GZipMiddleware**：压缩响应体，减少传输时间
3. **缓存**：对不变的数据加缓存（Redis 或内存缓存）
4. **response_model**：只返回需要的字段，减少序列化开销
5. **后台任务**：用 `BackgroundTasks` 把非关键操作（发邮件、写日志）挪到响应之后执行
6. **分页**：避免一次查全表，用 `skip` + `limit`

```python
from fastapi import BackgroundTasks

def send_email(to: str, subject: str):
    # 发邮件很慢，但不影响用户操作
    ...

@app.post("/register")
async def register(user: UserCreate, bg: BackgroundTasks):
    save_user(user)
    bg.add_task(send_email, user.email, "欢迎注册")  # 响应之后再发
    return {"msg": "注册成功"}
```

## 与其他框架的对比

Flask 和 Django 解决的是 Web 开发问题，FastAPI 也是。区别在于它们处理并发的方式不同，这不是同一个问题吗？是。但从 Flask/Django 变到 FastAPI，核心差异就一个：同步变异步。

| 维度 | FastAPI | Flask | Django |
|------|---------|-------|--------|
| 并发模型 | ASGI（异步） | WSGI（同步） | WSGI（同步），3.1+ 支持 ASGI |
| 类型系统 | Pydantic 自动验证 | 手动验证或用 Flask-Marshmallow | Form / Serializer |
| API 文档 | 自动生成 OpenAPI | 需要 Flask-RESTX / Flasgger | 需要 DRF + drf-spectacular |
| 依赖注入 | 内置 | 无（或用 Flask-Injector） | 无内置 |
| 异步支持 | 原生 | 不支持 | Django 3.1+ 支持异步视图 |
| 学习曲线 | 中等 | 低 | 高 |

FastAPI 不是银弹。如果你的项目以模板渲染为主（传统网站），Flask/Django 更合适。FastAPI 的强项是 API 服务——尤其是高并发、需要自动文档、强类型验证的场景。

## 面试高频考点

| 考点 | 他真正想知道的 | 回答要点 | 常见错误 |
|------|---------------|----------|----------|
| FastAPI 的依赖注入是什么 | 你知不知道怎么避免重复代码 | 声明式地告诉框架"我需要什么"，框架负责准备和清理。用 `Depends()` 实现。yield 依赖保证资源释放 | 把依赖注入和中间件搞混——中间件是全局的拦截器，依赖注入是路由级别的资源提供 |
| 中间件的执行顺序 | 你能不能正确组织多个中间件 | 最后注册的最先执行请求处理、最后执行响应处理（洋葱模型）。`call_next` 是分界点 | 以为先注册的先执行。实际上先注册的在内层 |
| async def 和 def 路由的区别 | 你懂不懂异步编程 | async 在事件循环里跑，def 在线程池里跑。async 里不能调阻塞代码 | 以为所有路由都应该加 async。在 async 里调同步阻塞代码会导致全站变慢 |
| lifespan 是干什么的 | 你知不知道应用级资源管理 | 替代废弃的 on_event，用 yield 分隔启动和清理逻辑，天然共享上下文变量 | 不知道 on_event 已废弃，或者不知道 lifespan 的优势 |
| Pydantic 在 FastAPI 里做什么 | 你理不理解自动验证和文档生成 | 请求体验证 + 类型转换 + 响应过滤 + OpenAPI 文档生成，四合一 | 只知道验证，不知道 response_model 的过滤作用 |
| FastAPI 为什么快 | 你能不能说清楚异步 I/O 的好处 | 异步 I/O 不阻塞线程，一个线程处理几百个并发。底层是 Starlette + Uvicorn | 以为"FastAPI"名字里的 Fast 是因为代码执行快。其实是 I/O 并发高 |
| 怎么做测试 | 你有没有实际项目经验 | 用 `TestClient`（基于 httpx）+ `dependency_overrides` 替换依赖 | 不知道 dependency_overrides，测试时连真实数据库 |
| CORS 怎么配 | 你做过前后端分离吗 | `app.add_middleware(CORSMiddleware, ...)`，设 allow_origins/methods/headers | 把 CORS 中间件注册在错误的位置，导致其他中间件先拦截了预检请求 |
