# 使用Python的FastAPI和Dapr，您可以轻松地集中管理和调用第三方接口。以下是一些步骤，以便您开始使用它们：
"""

1. 安装FastAPI和Dapr
在终端或命令提示符中运行以下命令来安装FastAPI和Dapr：
```
pip install fastapi[all] dapr dapr-ext-fastapi
```

2. 编写代码
创建一个新文件，例如`app.py`，并添加以下代码：
```python
"""

from fastapi import FastAPI, HTTPException
from dapr.ext.fastapi import DaprActor, DaprActorMethod, actor_handlers

app = FastAPI()


# 创建一个Dapr Actor
class MyActor(DaprActor):
    def __init__(self):
        self.value = 0

    # 定义一个Actor方法
    @DaprActorMethod(name="add", entity="myactor")
    def add(self, value: int) -> int:
        self.value += value
        return self.value


# 将Actor添加到应用程序中
actor_handlers.append(MyActor)


# 定义另一个路由，该路由调用其他服务的API
@app.get("/api/call-other-service")
async def call_other_service():
    # 此处省略调用其他服务的代码
    # 如果调用失败，则抛出HTTPException
    raise HTTPException(status_code=500, detail="Error calling other service")

# 启动应用程序
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""

3. 运行应用程序
在终端或命令提示符中运行以下命令来启动应用程序：
```
dapr run --app-id myapp --app-port 8000 python app.py
```

4. 测试应用程序
使用任何HTTP客户端（例如Postman或cURL）向`http://localhost:3500/v1.0/invoke/myapp/method/add`发出POST请求，其中包含以下JSON有效负载：
```json
{
    "value": 10
}
```
此请求将调用`MyActor`的`add`方法，并将值10传递给它。该请求的响应应为20。

5. 调用其他服务的API
使用任何HTTP客户端（例如Postman或cURL）向`http://localhost:8000/api/call-other-service`发出GET请求，以调用其他服务的API。如果该请求失败，则应返回HTTP状态码500和错误详细信息。

以上是一个简单的示例，说明如何使用FastAPI和Dapr集中管理和调用第三方接口。您可以根据自己的需求进行修改和扩展。
"""