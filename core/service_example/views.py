from fastapi import HTTPException, FastAPI, Depends

from .models import Hero, Team
from .schemes import HeroCreate, HeroUpdate, HeroRead

app = FastAPI()


async def get_filters(offset: int = 0, limit: int = 100, order_by: str = None):
    """ Dependencies with the common parameters for look for in a list """
    return {
        "offset": offset,
        "limit": limit,
        "order_by":  order_by
    }


@app.get("/hero", response_model=list[HeroRead])
async def get_all(filters=Depends(get_filters)):
    # TODO: Limit, offset, ...
    return Hero.get_all(Hero, **filters)


@app.get("/hero/{id}", response_model=HeroRead)
async def get_one(id: int):
    return Hero.get_one(Hero, id)


@app.post("/hero", response_model=HeroRead, status_code=201)
async def create(create_form: HeroCreate):
    # TODO: Include auth
    secret_password = create_form.password + "hash_super_secret"
    create_form = create_form.dict()
    create_form['secret_password'] = secret_password
    del create_form['password']
    return Hero(**create_form).create()


@app.delete("/hero/{id}")
async def delete(id: int) -> bool:
    try:
        hero = Hero.get_one(Hero, id)
    except:
        raise HTTPException(404, "This hero was not found")
    return hero.delete()


@app.put("/hero/{id}", response_model=HeroRead)
async def update(id: int, update_form: HeroUpdate):
    try:
        hero = Hero.get_one(Hero, id)
    except:
        raise HTTPException(404, "This hero was not found")

    return hero.update(update_form.dict())
