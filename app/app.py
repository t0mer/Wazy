import WazeRouteCalculator
from server import Server
from confighandler import ConfigHandler
from loguru import logger
import io

config = ConfigHandler().config
server = Server(config)

# from_address = "הגליל 48 רעננה, ישראל"
# to_address = "המלאכה 18 נתניה, ישראל"
# region = 'IL'
# route = WazeRouteCalculator.WazeRouteCalculator(from_address, to_address, region)
# route_time, route_distance = route.calc_route_info()
# logger.info('Time %.2f minutes, distance %.2f km.' % (route_time, route_distance))
# logger.info(str(route.end_coords['lat']) + "," + str(route.end_coords['lon']))
# logger.info(str(route.start_coords['lat']) + "," + str(route.end_coords['lon']))


server.start()
