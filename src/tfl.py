import http_client.core as http_client
import http_client.json_middleware as json_middleware
import logging
from CONFIG import (
    BUS_ROUTE_75,
    BURGHILL_ROAD_STOP_L,
    BEACONSFIELD_ROAD_STOP_D,
    TFL_API_APP,
    TFL_API_KEY,
)


async def route_to_brit() -> list[dict[str, str]]:
    # 2. [EXTENSION] Check if 75 is actually the best way to go?
    #    https://api.tfl.gov.uk/journey/journeyresults/{{home}}/to/{{brit school}}?app_id={{app_id}}&app_key={{app_key}}

    deps_arrs, disruptions = await get_bus_journey(
        BUS_ROUTE_75, BURGHILL_ROAD_STOP_L, BEACONSFIELD_ROAD_STOP_D
    )

    return {
        "route": "75",
        "from": "Burghill Road Stop L",
        "to": "Beaconsfield Road",
        "departures_and_arrivals": deps_arrs,  # time format: "2024-02-15T21:35:18Z"
        "disruptions": disruptions,
    }


async def get_bus_journey(route: str, origin: str, dest: str) -> list[tuple[str, str]]:

    arrivals = await call_tfl_service(f"Line/{route}/Arrivals/{origin}")
    vehicles = [a["vehicleId"] for a in arrivals]  # registration plates!

    ret = []
    for (
        vehicle
    ) in (
        vehicles
    ):  # need to do one call per vehicle because batch response is too large
        path = await call_tfl_service(f"Vehicle/{vehicle}/Arrivals")
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

    disruptions = await call_tfl_service(f"/Line/{route}/Status")
    disruptions = disruptions[0]["lineStatuses"][0]
    disruptionText = disruptions["statusSeverityDescription"]
    if disruptions["statusSeverity"] < 10:
        disruptionText += ": " + disruptions["reason"]

    return ret, disruptionText


async def call_tfl_service(service: str, query: str = None):
    query = query + "&" if query else ""
    url = f"https://api.tfl.gov.uk/{service}?{query}app_id={TFL_API_APP}&app_key={TFL_API_KEY}"
    resp = None
    try:
        r = await json_middleware.wrap(http_client.request)
        resp = await r({"url": url, "headers": {"Accept": "application/json"}})
        json = resp["body"]
        logging.debug(f"TFL API: {service}?{query} [{len(json)} elements]")
        return json
    except Exception as e:
        logging.error(f"Error {e} accessing {url}, got {resp}")
        raise e


async def route_to_kings() -> list[dict[str, str]]:
    pass


async def route_to_rathbone() -> list[dict[str, str]]:
    pass
