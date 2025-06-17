# TODO

## ORCID API Token

I (_poorly_) set this up to get a search token for the ORCID Public API on every
request/page-load - rather than only interacting with the API, and obtaining a
search token when it _actually_ needs to search and read data from the ORCID API.

```py
# Connect to ORCID.org public API, and get a search token.
orcid_api = PublicAPI(
    institution_key=app.config["ORCID_API_CLIENT_ID"],
    institution_secret=app.config["ORCID_API_CLIENT_SECRET"]
)
orcid_token = orcid_api.get_search_token_from_orcid()
```

Ideally, `PublicAPI`, and `get_search_token_from_orcid` should not run until
absolutely needed to move forward with executing `read_record_public`:

```py
employments = orcid_api.read_record_public(
    orcid_id=orcid_id,
    request_type="employments",
    token=orcid_token
)
```

Finally, with the above changes - in combination with `Flask-Caching` storing
DOI and ORCID information - subsequent page reloads should not result in any
external connections to `doi.org` nor `orcid.org`.
