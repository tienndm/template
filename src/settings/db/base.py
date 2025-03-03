from ast import parse
from urllib.parse import ParseResult, parse_qs, urlencode, urlparse, urlunparse

def normalizeUri(databaseUri: str) -> str:
    parseUri = urlparse(databaseUri)
    queryParams = parse_qs(parseUri.query)
    if 'reinitialize' in queryParams:
        del queryParams['reinitialize']
    
    normalizeUri = parseUri._replace(query=urlencode(queryParams, doseq=True))
    normalizeUri = urlunparse(normalizeUri)

    return normalizeUri

def hasReinitialize(databaseUri: str) -> bool:
    parseUri = urlparse(databaseUri)
    queryParams = parse_qs(parseUri.query)
    reinitializeValues = queryParams.get("reinitialize", [])

    return False if not reinitializeValues else reinitializeValues[0].lower() == 'true'