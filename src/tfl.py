from CONFIG import (
    BUS_ROUTE_75,
    BURGHILL_ROAD_STOP_L,
    BEACONSFIELD_ROAD_STOP_D,
    TFL_API_APP,
    TFL_API_KEY,
)
import json
from picodebug import logPrint
from urequest import urlopen


# TODO: convert to asyncio, coroutines:
# https://www.reddit.com/r/raspberrypipico/comments/yj46d2/pico_w_stops_running_randomly_after_a_while/


def route_to_brit() -> list[dict[str, str]]:
    # 2. [EXTENSION] Check if 75 is actually the best way to go?
    #    https://api.tfl.gov.uk/journey/journeyresults/{{home}}/to/{{brit school}}?app_id={{app_id}}&app_key={{app_key}}

    deps_arrs, disruptions = get_bus_journey(
        BUS_ROUTE_75, BURGHILL_ROAD_STOP_L, BEACONSFIELD_ROAD_STOP_D
    )

    return {
        "route": "75",
        "from": "Burghill Road Stop L",
        "to": "Beaconsfield Road",
        "departures_and_arrivals": deps_arrs,  # time format: "2024-02-15T21:35:18Z"
        "disruptions": disruptions,
    }


def get_bus_journey(route: str, origin: str, dest: str) -> list[tuple[str, str]]:

    arrivals = call_tfl_service(f"Line/{route}/Arrivals/{origin}")
    vehicles = [a["vehicleId"] for a in arrivals]  # registration plates!

    ret = []
    for (
        vehicle
    ) in (
        vehicles
    ):  # need to do one call per vehicle because batch response is too large
        path = call_tfl_service(f"Vehicle/{vehicle}/Arrivals")
        try:
            dep = next(filter(lambda s: s["naptanId"] == origin, path))[
                "expectedArrival"
            ]
        except StopIteration:
            dep = None
        try:
            arr = next(filter(lambda s: s["naptanId"] == dest, path))["expectedArrival"]
        except StopIteration:
            arr = None

        ret.append((dep, arr))

    disruptions = call_tfl_service(f"/Line/{route}/Status")[0]["lineStatuses"][0]
    disruptionText = disruptions["statusSeverityDescription"]
    if disruptions["statusSeverity"] < 10:
        disruptionText += ": " + disruptions["reason"]

    return ret, disruptionText


def call_tfl_service(service: str, query: str = None):
    query = query + "&" if query else ""
    url = f"https://api.tfl.gov.uk/{service}?{query}app_id={TFL_API_APP}&app_key={TFL_API_KEY}"
    try:
        sock = urlopen(url)
        bytes = (
            # closes socket
            # https://docs.micropython.org/en/latest/library/socket.html#socket.socket.read
            sock.read()
        )
        logPrint(f"TFL API: {service}?{query} [{len(bytes)} bytes]")
        return json.loads(bytes)
    except Exception as e:
        logPrint(f"Error {e} accessing {url}")
        raise e


def route_to_kings() -> list[dict[str, str]]:
    pass


def route_to_rathbone() -> list[dict[str, str]]:
    pass
