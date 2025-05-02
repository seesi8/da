from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import json

# Create a GraphQL client using the exact headers from the curl request
transport = RequestsHTTPTransport(
    url='https://dgtkl2ep7natjmkbefhxflglie.appsync-api.us-east-1.amazonaws.com/graphql',
    use_json=True,
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:137.0) Gecko/20100101 Firefox/137.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Origin': 'https://apstudents.collegeboard.org',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'cross-site',
        'TE': 'trailers',
        'content-type': 'application/json; charset=UTF-8',
        'x-cb-catapult-authorization-token': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDQwNzIyNzUsImNiIjp7ImVudiI6InBpbmUiLCJucyI6InN0IiwibHR0IjoiQ0JMb2dpbiIsInVuIjoiWjlaOTk1Nzk5OTE0IiwiZW0iOiJqb2huLnNtaXRoMTIzNEBlbWFpbGh1Yi5rciIsInBpZCI6IjE0NzgyNjMwNSIsImFpZCI6Ijk1Nzk5OTE0Iiwib2t0YUFjY291bnRJZCI6IjAwdW82c3liOXhZaTFsYUYzNWQ3IiwiYXV0aG5MZXZlbCI6IjIwIiwiZHAiOnsiZmlyc3ROYW1lIjoiSm9obiIsIm1pZGRsZUluaXRpYWwiOm51bGwsInByZWZlcnJlZEZpcnN0Tm0iOm51bGwsImdyYWR1YXRpb25EYXRlIjoxNzgwMjcyMDAwMDAwLCJnZW5kZXIiOiJNQUxFIiwiYWRkcmVzcyI6eyJzdHJlZXQxIjoiNjcyNCBMYSBHcmFuZ2UgRHIiLCJzdHJlZXQyIjpudWxsLCJzdHJlZXQzIjpudWxsLCJjaXR5IjoiRGFsbGFzIiwic3RhdGVDb2RlIjoiVFgiLCJ6aXA0IjoiNjcxMSIsInppcDUiOiI3NTI0MSIsInByb3ZpbmNlIjpudWxsLCJjb3VudHJ5Q29kZSI6IlVTIiwiaW50ZXJuYXRpb25hbFBvc3RhbENvZGUiOm51bGwsImFkZHJlc3NUeXBlIjoiRE9NRVNUSUMifSwic3R1ZGVudFNlYXJjaFNlcnZpY2VPcHRJbiI6IlUiLCJzdHVkZW50U2VhcmNoU2VydmljZU9wdERhdGUiOm51bGwsImFmZmlsaWF0ZWRPcmdJZCI6bnVsbCwiYWZmaWxpYXRlZE9yZ05hbWUiOm51bGwsImFpQ29kZSI6bnVsbCwiYWlTcmNDb2RlIjpudWxsLCJjb2hvcnQiOiIyMDI2In19LCJpYXQiOjE3NDQwNzEzNzUsImlzcyI6ImNhdGFwdWx0LmNvbGxlZ2Vib2FyZC5vcmciLCJzdWIiOiJ1cy1lYXN0LTE6ODFiZjQ3MTQtOTk2My1jMjcxLTk1OGQtZWI1ZGVlNGYxMDBhIn0.u8FKq7VnKLd23kB_xGVKeSvSlWVaFXoV7Fvk9nD7UECVsgI4YRpsqObiFaQ5nvLWbh0LE4cfMwHoTEd6yrJ-DSQ4P9HdRbBKAAYJYfMsO9EV-HD-Vcl2oMzJjuxPa-1vaZ9uZNJ1CI5VG2hMN9CDDuiqnu23KVmCU20HgOy9GvhHcC3ANllqLntFvhW6NqjQg_JGJ28b-Uyhsv56H57_lBui720nsjb94fVOumZU-WewIDHz_Cs6fp7QAl1XfOhcgaR_rFX81Eary8ZvCBCgUbbUAmeKjMWUNl1_9Q-xRbGAWYVp7NiYqFF7_U169dASul0ASPgxVqiTvif2LdtAfQ',
        'x-amz-date': '20250408T002201Z',
        'x-amz-security-token': 'IQoJb3JpZ2luX2VjEPH//////////wEaCXVzLWVhc3QtMSJGMEQCICAKGm5M3rz6W//pnFiGnx1X6gYi9/K6973xwVurKK/oAiA7CRBMKgpIEowxKNJ+tDPZ+WI2p5YFrbibioGJkaPYRCrsAwhpEAQaDDU1ODQ3MDU5OTY4NiIMFFTf8uV9SO5R10p5KskD9PLz9+/3vS/nJTm7FHTWP4S+3AA1VDxyS+INjJ6fEdv6bSq1avDv/PxBqbd64ZOhWIXbvd3khbdfchztILM1LQUuNo/dc0Ba4sQpKLaIine1gIXTrGoL4dL5jstAjqbE5bQqQDKUSHXVlukLMVn2mCqP8EXe21v63JDT5rFis5UCjD3kWdnS0KNYSIBm45x5Jgtna2QlnOGJeQc3FYx9PupLgrrtob+QLbGSPaItCCK0VQE+EMk8yegOI6wYXuV3VtftgBp6wqtl7wswBuGsZgiMrGPXMeELdhs11U71INq905fEL8HMef7Kzivo3bQKya0iyCUjsX7MlaGVmocR8cKhY9zxQZUJvtAKTEwQiHwU/bQs32bnzUiitIOe2LiLxtEtouLFrSH4IfDJrL4LDbj5X4k76YaUaYQ0f56GllMy2C8b9vpqBX3e3MA/1lbWGqoDCM6vqAFz1DkznyXDbQkhbJtXyd7JxVG9ZSGT6vvnzmogFSSYxwgdOiINVU9U4J+8i12gKvNLxj6vAiMeqpGTojTIs5A1NmO2IzxVhoXqhSE4x/3dFguPwo3ZH1Y5HTWTKKV4ctuUmQxOrXGu+LDpuC1FBZokezDP1dG/BjqFAlNuWdQT1FZM+A4QZcCgc46H7IfZfr5SktyPVVxzdn7+yGevaI7on7CdcqFTkeeoqaffG6rnsw40Bfpv89EwnCJuIsmDdrw/HfjAX6ZUhZdB36kdyMCgvPZOyDB+dc1ZTkKksDtu/42H55orcQsGbbANX5dkLX1sfNBhHYl5v0NuosB3of4qrRspET+OBRbgZY2UI4hpc7JLq8Yf+X1+xUGpoEacW9ITHjS+XmxICvORZqdiRelcdp1R9tuMfJhgvlHgK43mVP9WqUCS+KTpc00qINZ5nhaYBC3kgXT66QlxetuPAM8+kXnFjq4ncSEAtJDyiPU5H3AIR4tpvYQOc5IgfNQ3Gw==',  # Replace with your actual token
        'authorization': 'AWS4-HMAC-SHA256 Credential=ASIAYEB3RCQDB5JPNG46/20250408/us-east-1/appsync/aws4_request, SignedHeaders=accept;content-type;host;x-amz-date;x-amz-security-token, Signature=291b720b4d72ecd3c9fde22a6b7a6acf3cc4058a510c5676885ec9da0461eebc'
    },
    verify=True,
    retries=3
)

client = Client(transport=transport, fetch_schema_from_transport=False)

# GraphQL query that mirrors the operation from the curl request
query = gql("""
query getUserPreferences($educationPeriod: Int!) {
  getUserPreferences(educationPeriod: $educationPeriod) {
    deletedNotifications
    __typename
  }
}
""")

# Execute the query using the exact parameters from the curl request
result = client.execute(query, variable_values={'educationPeriod': 26})

# Print the results
print(json.dumps(result, indent=2))
