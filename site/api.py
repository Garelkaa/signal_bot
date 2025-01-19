from fastapi import FastAPI, HTTPException, Query
import uvicorn

from signature import BotSettings


app = FastAPI()
bot_settings = BotSettings()


@app.get("/postback")
async def handle_postback(user_id: int = Query(None)):
    if user_id is not None:
        try:
            print(f"User ID: {user_id}")
            await bot_settings.db.add_user_ref(uid=user_id)
            
            return {"message": "Postback успешно получен"}, 200
        except ValueError:
            print(f"Некорректный user_id: {user_id}")
            raise HTTPException(status_code=400, detail="Некорректный user_id")
    else:
        print("Параметр user_id отсутствует")
        raise HTTPException(status_code=400, detail="Параметр user_id отсутствует")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
