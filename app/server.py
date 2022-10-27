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
import WazeRouteCalculator
import uvicorn
import json


class Server:
    def __init__(self,config):
        self.config = config
        self.tags_metadata = [
            {
                "name": "Routes",
                "description": "Get routes info",
            },

        ]
        self.region = config.get('WAZE','route.region')
        self.avoid_toll_roads = config.get('WAZE','avoid_toll_roads')
        self.avoid_subscription_roads = config.get('WAZE','avoid_subscription_roads')
        self.app = FastAPI(title="Wazy", description="Monitor your routes and get notified when it flows", version='1.0.0', openapi_tags=self.tags_metadata, contact={"name": "Tomer Klein", "email": "tomer.klein@gmail.com", "url": "https://github.com/t0mer/Wazy"})


        @self.app.get('/route/get',tags=['Routes'], summary="Get route by addresses")
        def get_route(from_address: str, to_address: str, avoid_toll_roads: bool=False, avoid_subscription_roads:bool=False):
            try:
                route = WazeRouteCalculator.WazeRouteCalculator(from_address, to_address, region=self.region,avoid_toll_roads=avoid_toll_roads,avoid_subscription_roads=avoid_subscription_roads)
                route_time, route_distance = route.calc_route_info()
                # route_time = '{:02d}:{:02d}'.format(*divmod(int(str(route_time)), 60))
                route_time_seconds = (int(route_time)*60)
                message = '{"time":"' + str(self.convert_to_preferred_format(route_time_seconds)) + '","distance":"' + str(route_distance) + ' km","nav_url":"' + self.create_nav_url(route.end_coords['lat'],route.end_coords['lon']) +'"}'
                return JSONResponse(content = json.loads(message)) 
            except Exception as e:
                logger.error(str(e))
                return JSONResponse(content = '{"message":"' +str(e)+ '","success":false}')


        @self.app.get('/route/default',tags=['Routes'], summary="Get default route")
        def get_default_route():
            try:
                from_address = config.get('WAZE','route.start_address')
                to_address = config.get('WAZE','route.end_address')
                avoid_toll_roads = config.get('WAZE','route.avoid_toll_roads')
                avoid_subscription_roads = config.get('WAZE','route.avoid_subscription_roads')
                route = WazeRouteCalculator.WazeRouteCalculator(from_address, to_address, region=self.region,avoid_toll_roads=avoid_toll_roads,avoid_subscription_roads=avoid_subscription_roads)
                route_time, route_distance = route.calc_route_info()
                route_time_seconds = (int(route_time)*60)
                message = '{"time":"' + str(self.convert_to_preferred_format(route_time_seconds)) + '","distance":"' + str(route_distance) + ' km","nav_url":"' + self.create_nav_url(route.end_coords['lat'],route.end_coords['lon']) +'"}'
                return JSONResponse(content = json.loads(message)) 
            except Exception as e:
                logger.error(str(e))
                return JSONResponse(content = '{"message":"' +str(e)+ '","success":false}')

        @self.app.get('/route/byname',tags=['Routes'], summary="Get route by name")
        def get_route_by_name(name: str):
            try:
                from_address = config.get(name,'route.start_address')
                to_address = config.get(name,'route.end_address')
                avoid_toll_roads = config.get(name,'route.avoid_toll_roads')
                avoid_subscription_roads = config.get(name,'route.avoid_subscription_roads')
                route = WazeRouteCalculator.WazeRouteCalculator(from_address, to_address, region=self.region,avoid_toll_roads=avoid_toll_roads,avoid_subscription_roads=avoid_subscription_roads)
                route_time, route_distance = route.calc_route_info()
                route_time_seconds = (int(route_time)*60)
                message = '{"time":"' + str(self.convert_to_preferred_format(route_time_seconds)) + '","distance":"' + str(route_distance) + ' km","nav_url":"' + self.create_nav_url(route.end_coords['lat'],route.end_coords['lon']) +'"}'
                return JSONResponse(content = json.loads(message)) 
            except Exception as e:
                logger.error(str(e))
                return JSONResponse(content = '{"message":"' +str(e)+ '","success":false}')

        @self.app.get('/route/default',tags=['Routes'], summary="Get default route")
        def get_default_route():
            try:
                from_address = config.get('WAZE','route.start_address')
                to_address = config.get('WAZE','route.end_address')
                avoid_toll_roads = config.get('WAZE','route.avoid_toll_roads')
                avoid_subscription_roads = config.get('WAZE','route.avoid_subscription_roads')
                route = WazeRouteCalculator.WazeRouteCalculator(from_address, to_address, region=self.region,avoid_toll_roads=avoid_toll_roads,avoid_subscription_roads=avoid_subscription_roads)
                route_time, route_distance = route.calc_route_info()
                route_time_seconds = (int(route_time)*60)
                message = '{"time":"' + str(self.convert_to_preferred_format(route_time_seconds)) + '","distance":"' + str(route_distance) + ' km","nav_url":"' + self.create_nav_url(route.end_coords['lat'],route.end_coords['lon']) +'"}'
                return JSONResponse(content = json.loads(message)) 
            except Exception as e:
                logger.error(str(e))
                return JSONResponse(content = '{"message":"' +str(e)+ '","success":false}')

        @self.app.get('/route/locations',tags=['Routes'], summary="Get route by location name name")
        def get_route_by_name(start: str, end: str):
            try:
                from_address = config.get("ADRESSES",'address.' + start)
                to_address = config.get("ADRESSES",'address.' + end)
                avoid_toll_roads = self.avoid_toll_roads
                avoid_subscription_roads = self.avoid_subscription_roads
                route = WazeRouteCalculator.WazeRouteCalculator(from_address, to_address, region=self.region,avoid_toll_roads=avoid_toll_roads,avoid_subscription_roads=avoid_subscription_roads)
                route_time, route_distance = route.calc_route_info()
                route_time_seconds = (int(route_time)*60)
                message = '{"time":"' + str(self.convert_to_preferred_format(route_time_seconds)) + '","distance":"' + str(route_distance) + ' km","nav_url":"' + self.create_nav_url(route.end_coords['lat'],route.end_coords['lon']) +'"}'
                return JSONResponse(content = json.loads(message)) 
            except Exception as e:
                logger.error(str(e))
                return JSONResponse(content = '{"message":"' +str(e)+ '","success":false}')




    def convert_to_preferred_format(self,sec):
        sec = sec % (24 * 3600)
        hour = sec // 3600
        sec %= 3600
        min = sec // 60
        sec %= 60
        return "%02d:%02d:%02d" % (hour, min, sec) 


    def start(self):
        logger.debug("Starting web server")
        uvicorn.run(self.app, host="0.0.0.0", port=8081)

    def create_nav_url(self, lat, lon):
        return "https://waze.to?ll={lat},{lon}&navigate=yes".format(lat=lat, lon=lon)