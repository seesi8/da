import aiohttp
import asyncio
import json
import requests
from markdownify import markdownify as md
import os

if not os.path.exists("./token.txt"):
    raise FileNotFoundError("\n token.txt does not exist \n Please create a new file named \"token.txt\" with your token (ex. Bearer XXXXX) inside")


with open("./token.txt") as file:
    BEARERTOKEN = file.read()


STUDENTID = input("Enter your student ID: ")

# Function to extract IDs from a JSON string
def extract_ids(json_str):
    data = json.loads(json_str)
    first_key = next(iter(data))
    ids = [key for key, _ in data[first_key].items() if key != "questions"]
    return ids

# Function to replace items in the query string with new IDs
def replace_items(query, new_ids):
    items_start = query.find("\"items\":")
    if items_start == -1:
        return query

    pre_items = query[:items_start + 8]
    post_items = query[items_start:].split(']', 1)[1]

    new_items = [{'id': f'{id}---1', 'reference': id} for id in new_ids]
    new_items_str = json.dumps(new_items)

    return f'{pre_items}{new_items_str}{post_items}'

# Async function to fetch items using aiohttp
async def fetch_items(data):
    url = "https://items-va.learnosity.com/v2023.2.LTS/items"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:137.0) Gecko/20100101 Firefox/137.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=data) as response:
            return await response.text()


# Function to extract questions and convert HTML to Markdown, then save to a Markdown file
def extract_questions_answers(data):
    with open('output.md', 'w') as md_file:
        items = data['data']['items']  # Navigate to the 'items' list in the data
        for item in items:
            for question in item['questions']:
                question_text = md(question['stimulus'])
                correct_value = question['validation']['valid_response']['value'][0]  # Assumes single correct answer
                correct_answer = None
                
                # Find the correct answer label
                for option in question['options']:
                    if option['value'] == correct_value:
                        correct_answer = md(option['label'])
                        break
                
                conversion = {"i1" : "A", "i2" : "B", "i3" : "C", "i4": "D", "i5": "E"}
                test = conversion.get(correct_value, "?" )
                
                # Write the question and correct answer to Markdown file
                md_file.write(f"### Question:\n{question_text}\n")
                md_file.write(f"**Correct Answer ({test}): ** {correct_answer}\n\n")

# Main execution logic
async def main():
    assignmentId = input("Assignment ID: ")
    url = "https://apc-api-production.collegeboard.org/fym/graphql"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:137.0) Gecko/20100101 Firefox/137.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "application/json; charset=utf-8",
        
        "Authorization": BEARERTOKEN,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Priority": "u=4"
    }
    data = {
        "query": """query getSignedAssignmentResultRequest($assignmentId: String, $studentId: String, $includePriorStudents: String, $educationPeriod: String, $masterSubjectId: String, $scrambledStudentId: String) {
    quizIsPpc(assignmentId: $assignmentId, educationPeriod: $educationPeriod)
    assignment(assignmentId: $assignmentId, educationPeriod: $educationPeriod) {
        id
        status
        scoreDisplay
        hasImmediateFeedback
        studentResponses(studentId: $studentId)
        scoringRubricResponses(studentId: $studentId, scorerType: "teacher")
        results(studentId: $studentId, includePriorStudents: $includePriorStudents)
        resultsByItem(
        studentId: $studentId
        includePriorStudents: $includePriorStudents
        )
        scoringRubricResults(
        studentId: $studentId
        includePriorStudents: $includePriorStudents
        )
        responseAnalysis(studentId: $studentId)
        scoringRubricResponseAnalysis(studentId: $studentId)
        studentScoringRubricResults: scoringRubricResults(
        studentId: $studentId
        scorerType: "student"
        )
        teacherScoringRubricResults: scoringRubricResults(scorerType: "teacher")
        title
        startsAt
        dueAt
        timer
        sectionName
        sectionId
        isSecure
        studentScoring
        hasStudentScores
        isIndividualAssignment
        studentScoring
        printToggle
        students {
        id: initId
        firstName
        lastName
        apuid
        email
        __typename
        }
        progress(userId: $studentId) {
        submitted
        scoring
        scored
        studentScored
        teacherAndStudentScored
        __typename
        }
        studentSessions {
        userId
        submittedAt
        scoringCompletedAt
        createdBy
        __typename
        }
        feedback(studentId: $studentId) {
        content
        studentId
        __typename
        }
        timeTaken(studentId: $studentId) {
        studentId
        seconds
        __typename
        }
        timezone
        assessment {
        id: itemId
        title
        libraryType
        isPracticeExam
        isLearningCheckpoint
        isPerformanceTask
        associatedResources {
            resourceUrl
            resourceType
            __typename
        }
        isCbPracticeQuiz
        isSampleQuiz
        isSpp
        isPpc
        is_learning_checkpoint: isLearningCheckpoint
        __typename
        }
        customAssignmentSettings {
        startsAt
        dueAt
        timer
        userId
        __typename
        }
        questions(studentId: $scrambledStudentId) {
        ... on MultipleChoiceQuestion {
            id: itemId
            ownerId
            title
            isSecure
            isTopicQuestion
            isRetired
            isTeacherAuthored
            learnosityItemReference
            itemShareChain
            relatedSkills(educationPeriod: $educationPeriod) {
            tagCategoryId
            title
            children {
                tagId
                label
                title
                description
                category
                __typename
            }
            __typename
            }
            relatedOtherTags(
            educationPeriod: $educationPeriod
            masterSubjectId: $masterSubjectId
            ) {
            id
            label
            title
            description
            category
            __typename
            }
            type: __typename
        }
        ... on FreeResponseQuestion {
            id: itemId
            ownerId
            title
            isSecure
            isTopicQuestion
            isRetired
            isTeacherAuthored
            learnosityItemReference
            itemShareChain
            relatedSkills(educationPeriod: $educationPeriod) {
            tagCategoryId
            title
            children {
                tagId
                label
                title
                description
                __typename
            }
            __typename
            }
            relatedOtherTags(
            educationPeriod: $educationPeriod
            masterSubjectId: $masterSubjectId
            ) {
            id
            label
            title
            description
            category
            __typename
            }
            children: scoringRubric {
            id
            title
            learnosityItemReference
            type: __typename
            }
            type: __typename
        }
        __typename
        }
        categories(masterSubjectId: $masterSubjectId)
        scrambleQuestionsPerStudent
        scoreDisplay
        __typename
    }
    }""",
        "variables": {
            "assignmentId": assignmentId,
            "studentId": STUDENTID,
            "includePriorStudents": None,
            "masterSubjectId": "1",
            "scrambledStudentId": STUDENTID
        },
        "operationName": "getSignedAssignmentResultRequest"
    }
    response = requests.post(url, json=data, headers=headers)
    data = response.json()

    studentResponses = data["data"]["assignment"]["studentResponses"]
    print(studentResponses)
    new_ids = extract_ids(studentResponses)
    
    query_string = "action=get&security={\"consumer_key\":\"gHpBBB2lEYn2EDoS\",\"domain\":\"apclassroom.collegeboard.org\",\"timestamp\":\"20250404-0245\",\"user_id\":\"228490232\",\"signature\":\"$02$300926dca276e6d2b35aa50d6c91940466ef47f5b61f46562674a7cb2a7f6f24\"}&request={\"user_id\":\"228490232\",\"session_id\":\"\",\"retrieve_tags\":true,\"organisation_id\":537,\"dynamic_items\":{\"data_table_seed\":\"seed\",\"seed_with_item_id\":true}}&usrequest={\"items\":[{\"id\":\"VH921024---1\",\"reference\":\"VH921024\"},{\"id\":\"VH921028---1\",\"reference\":\"VH921028\"},{\"id\":\"VH930290---1\",\"reference\":\"VH930290\"},{\"id\":\"VH930291---1\",\"reference\":\"VH930291\"},{\"id\":\"VH930259---1\",\"reference\":\"VH930259\"}]}"
    new_query_string = replace_items(query_string, new_ids)
    result = await fetch_items(new_query_string)
    extract_questions_answers(json.loads(result))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
