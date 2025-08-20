from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel  # use for schema
from typing import Optional
from random import randrange

app = FastAPI()


# createpost schema
class post(BaseModel):
    title: str
    content: str
    is_published: bool = True  # default true
    rating: Optional[int] = None  # optional


my_posts = [{"title": "traveling", "content": "have a safe journey", "id": 4},
            {"title": "weather", "content": "it is fantastic cloudy day", "id": 6}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
        
        
def find_index_post(id):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return index
        
        
        
 




@app.get("/")
def root():
    return {"message": "Welcome to fastapis development"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts
            }


@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_post(post: post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0, 1000000000)  # assigning id key
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return {"post_detail": post}


@app.get("/posts/{id}")
def get_post(id: int):

    post = find_post(id)
    if post is not None:
        return {"post_detail": post}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
        


@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            del my_posts[index]
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")



@app.put("/posts/{id}")
def update_post(id: int, post: post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")
    print(post)
    post_dict = post.model_dump()
    post_dict["id"] = id
    my_posts[index] = post_dict
    return {"data": post_dict}
    