import httpagentparser


def parse_useragent(useragent: str) -> list:
    return list(httpagentparser.simple_detect(useragent))

