from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import time
import json

with open("./token.txt") as file:
    BEARERTOKEN = file.read()
    
# Create a GraphQL client
transport = RequestsHTTPTransport(
    url='https://apc-api-production.collegeboard.org/fym/graphql',
    use_json=True,
    headers={
        'Authorization': BEARERTOKEN,
        'Content-Type': 'application/json'
    },
    verify=True,
    retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=False)

# GraphQL query template
query = gql("""
    
query IntrospectionQuery {
  __schema {
    mutationType {
      fields {
        name
        description
        args {
          name
          description
          type {
            kind
            name
            ofType {
              name
              kind
            }
          }
          defaultValue
        }
        type {
          name
          kind
        }
      }
    }
  }
}



""")

# List of different assignment IDs
assignment_ids = ["63276724"]
STUDENTID = "228490232"

# Execute the query for each assignment ID
for assignment_id in assignment_ids:
    start_time = time.time()

    params = {
    # 'id': '123',
    'assignmentId': '65806628',
    'scores': '{"228490232" : 36}',
    'scoringCompleted': False,
    "studentId": STUDENTID
    }
    result = client.execute(query, variable_values=params)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")
    with open("output.json", "w") as file:
        file.write(json.dumps(result, indent=2))
    print(result)  # Output the result of each query
