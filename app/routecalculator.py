from confighandler import ConfigHandler
import WazeRouteCalculator
from loguru import logger



class RouteCalculator:


    def convert_to_preferred_format(self,minutes):
        sec = (int(minutes)*60)
        sec = sec % (24 * 3600)
        hour = sec // 3600
        sec %= 3600
        min = sec // 60
        sec %= 60
        return "%02d:%02d:%02d" % (hour, min, sec) 


    def create_nav_url(self, lat, lon):
        return "https://waze.to?ll={lat},{lon}&navigate=yes".format(lat=lat, lon=lon)


    def get_route(self,from_address, to_address,region, avoid_toll_roads, avoid_subscription_roads):
        route = WazeRouteCalculator.WazeRouteCalculator(from_address, to_address, region=region,avoid_toll_roads=avoid_toll_roads,avoid_subscription_roads=avoid_subscription_roads)
        route_time, route_distance = route.calc_route_info()
        return int(route_time), str(self.convert_to_preferred_format(int(route_time))), str(route_distance), self.create_nav_url(route.end_coords['lat'],route.end_coords['lon'])


                