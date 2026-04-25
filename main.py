import uvicorn
from fastapi import FastAPI, Request

import circles_generator_functions
import images_generator_functions

api_app = FastAPI()


@api_app.get("/health")
async def health():
    return {"status": "ok"}


@api_app.get("/trajectory_generator/get_trajectory_circles")
async def process_spu(goal_degrees: int):

    result = circles_generator_functions.generate_trajectory(goal_degrees)

    return result


@api_app.get("/trajectory_generator/get_trajectory_images_drag")
async def process_spu(start_block: int, finish_block: int):
    result = images_generator_functions.generate_trajectory(start_block, finish_block)

    return result


if __name__ == "__main__":
    uvicorn.run(api_app, host='0.0.0.0', port=5000)
