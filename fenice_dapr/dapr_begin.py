from fastapi.responses import JSONResponse
import dapr
from dapr.clients import DaprClient
from fastapi import FastAPI, status
import uvicorn

app = FastAPI()

# 使用 Dapr 端口创建 DaprClient
dapr_port = 3500
dapr_client = DaprClient()

# 声明一个状态存储的名称和密钥
state_store_name = "statestore"
state_key = "my_state_key"

# 使用 FastAPI 路由实现 GET 请求来获取状态存储的值
@app.get("/get_state")
async def get_state():
    try:
        # 通过 DaprClient 获取状态存储的值
        state = await dapr_client.get_state(state_store_name, state_key)
        return JSONResponse(content={"state": state.value})
    except dapr.errors.DaprError as e:
        return JSONResponse(content={"error": str(e)})

# 使用 FastAPI 路由实现 POST 请求来设置状态存储的值
@app.post("/set_state")
async def set_state(value: str):
    try:
        # 通过 DaprClient 设置状态存储的值
        await dapr_client.save_state(state_store_name, state_key, value)
        return JSONResponse(content={"success": True})
    except dapr.errors.DaprError as e:
        return JSONResponse(content={"error": str(e)})

# 运行 FastAPI 应用程序
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)