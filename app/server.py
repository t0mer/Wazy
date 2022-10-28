from routecalculator import RouteCalculator
from fastapi import FastAPI, Request, File, Form, UploadFile, HTTPException
from fastapi.responses import UJSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from starlette.responses import FileResponse
from starlette.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from loguru import logger
from confighandler import ConfigHandler
import uvicorn
import json



class Server:
    def __init__(self):
        self.config = ConfigHandler().config
        self.tags_metadata = [
            {
                "name": "Routes",
                "description": "Get routes info",
            },

        ]
        self.region = self.config.get('WAZE','route.region')
        self.avoid_toll_roads = self.config.get('WAZE','route.avoid_toll_roads')
        self.avoid_subscription_roads = self.config.get('WAZE','route.avoid_subscription_roads')
        self.app = FastAPI(title="Wazy", description="Monitor your routes and get notified when it flows", version='1.0.0', openapi_tags=self.tags_metadata, contact={"name": "Tomer Klein", "email": "tomer.klein@gmail.com", "url": "https://github.com/t0mer/Wazy"})
        self.calculator = RouteCalculator()


        @self.app.get('/route/get',tags=['Routes'], summary="Get route by addresses")
        def get_route(from_address: str, to_address: str, avoid_toll_roads: bool=False, avoid_subscription_roads:bool=False):
            try:
                time_in_minutes,route_time,distance,nav_url = self.calculator.get_route(from_address=from_address,to_address=to_address,
                avoid_subscription_roads=avoid_subscription_roads,avoid_toll_roads=avoid_toll_roads,region=self.region)
                message = '{"time":"' + route_time + '","time_in_minutes":"' + str(time_in_minutes) +'","distance":"' + str(distance) + ' km","nav_url":"' + nav_url +'"}'
                return JSONResponse(content = json.loads(message)) 
            except Exception as e:
                logger.error(str(e))
                return JSONResponse(content = '{"error":"' +str(e)+ '","success":false}')


        @self.app.get('/route/default',tags=['Routes'], summary="Get default route")
        def get_default_route():
            try:
                from_address = self.config.get('WAZE','route.start_address')
                to_address = self.config.get('WAZE','route.end_address')
                avoid_toll_roads = self.config.get('WAZE','route.avoid_toll_roads')
                avoid_subscription_roads = self.config.get('WAZE','route.avoid_subscription_roads')
                
                time_in_minutes,route_time,distance,nav_url = self.calculator.get_route(from_address=from_address,to_address=to_address,
                avoid_subscription_roads=avoid_subscription_roads,avoid_toll_roads=avoid_toll_roads,region=self.region)
                message = '{"time":"' + route_time + '","time_in_minutes":"' + str(time_in_minutes) +'","distance":"' + str(distance) + ' km","nav_url":"' + nav_url +'"}'
                return JSONResponse(content = json.loads(message)) 
            except Exception as e:
                logger.error(str(e))
                return JSONResponse(content = '{"message":"' +str(e)+ '","success":false}')

        @self.app.get('/route/byname',tags=['Routes'], summary="Get route by name")
        def get_route_by_name(name: str):
            try:
                time_in_minutes,route_time,distance,nav_url = self.calculator.get_route_info_by_name(name=name)
                message = '{"time":"' + route_time + '","time_in_minutes":"' + str(time_in_minutes) +'","distance":"' + str(distance) + ' km","nav_url":"' + nav_url +'"}'
                return JSONResponse(content = json.loads(message)) 
            except Exception as e:
                logger.error(str(e))
                return JSONResponse(content = '{"message":"' +str(e)+ '","success":false}')

        

        @self.app.get('/route/locations',tags=['Routes'], summary="Get route by location name")
        def get_route_by_name(start: str, end: str):
            try:
                from_address = self.config.get("ADRESSES",'address.' + start)
                to_address = self.config.get("ADRESSES",'address.' + end)
                avoid_toll_roads = self.avoid_toll_roads
                avoid_subscription_roads = self.avoid_subscription_roads
                time_in_minutes,route_time,distance,nav_url = self.calculator.get_route(from_address=from_address,to_address=to_address,
                avoid_subscription_roads=avoid_subscription_roads,avoid_toll_roads=avoid_toll_roads,region=self.region)
                message = '{"time":"' + route_time + '","time_in_minutes":"' + str(time_in_minutes) +'","distance":"' + str(distance) + ' km","nav_url":"' + nav_url +'"}'
                return JSONResponse(content = json.loads(message)) 
            except Exception as e:
                logger.error(str(e))
                return JSONResponse(content = '{"message":"' +str(e)+ '","success":false}')


    def start(self):
        logger.debug("Starting web server")
        uvicorn.run(self.app, host="0.0.0.0", port=8081)

 