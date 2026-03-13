from borrowed_code.reader import query

EXPECTED_START = """<link href="oaldpe.css" rel="stylesheet" type="text/css">\
<script src="oaldpe-jquery-3.6.0.min.js">"""


def test_query_startswith():
    result = query("oaldpe.mdx", "english")
    print(result)
    print(EXPECTED_START)
    assert result.startswith(EXPECTED_START)
