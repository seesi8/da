import matplotlib.pyplot as plt
import networkx as nx

# Detailed schema data with parameters for each mutation
detailed_schema_data = {
    "shareUnitWithClass": [("classIds", "Int"), ("id", "String")],
    "shareResourceWithClass": [("assignees", "IsaAssignee"), ("classIds", "Int"), ("dueAt", "DateTime"), ("educationPeriod", "Int"), ("id", "String"), ("ids", "String"), ("resourceType", "String"), ("startsAt", "DateTime")],
    "unshareResources": [("ids", "String"), ("subjectId", "Int")],
    "studentFeedback": [("assignmentId", "Int"), ("content", "JSONString"), ("studentId", "Int")],
    "startAssignment": [("assignmentId", "Int"), ("isImpersonating", "Boolean")],
    "submitAssignment": [("assignmentId", "String")],
    "setQuestion": [("question", "String")],
    "setRubric": [("categoryItems", "String"), ("categoryQuestions", "String"), ("itemReference", "String")],
    "updateScores": [("assignmentId", "String"), ("scores", "String"), ("scoringCompleted", "Boolean"), ("studentId", "String")],
    "saveSessions": [("assignmentId", "String"), ("scoringSessionTemplate", "String"), ("sessions", "List"), ("template", "String")]
}
# Further adjusting the graph with specified layout improvements and line color

# Create a directed graph with updated properties for better layout
G = nx.DiGraph()

# Add nodes and edges based on the schema
for mutation, types in detailed_schema_data.items():
    G.add_node(mutation, color='lightblue', style='filled', node_type='Mutation')  # Mutation node
    for dtype in types:
        G.add_node(dtype, color='lightgreen', style='filled', node_type='Data Type')  # Data type node
        G.add_edge(mutation, dtype)

# Adjusting the layout to make the graph more spread out particularly at the center and bring nodes towards the center
pos = nx.spring_layout(G, k=0.75, scale=3, seed=42)

# Drawing the graph with enhanced layout and style
fig, ax = plt.subplots(figsize=(18, 14))
nx.draw_networkx_edges(G, pos, alpha=1.0, edge_color='black', width=2)

# Draw nodes with custom style for better visualization
for node, data in G.nodes(data=True):
    node_color = data['color']
    node_type = data['node_type']
    x, y = pos[node]
    bbox = dict(boxstyle="round,pad=0.1", ec=node_color, lw=2, fc="white")
    ax.text(x, y, node, ha='center', va='center', fontsize=10, fontweight='bold', bbox=bbox, family='monospace')

# Adding a color key for clarity
colors = {'Mutation': 'lightblue', 'Data Type': 'lightgreen'}
labels = list(colors.keys())
handles = [plt.Line2D([0], [0], marker='s', color='white', markerfacecolor='white', markeredgecolor=colors[label], markersize=10, label=label, markeredgewidth=2) for label in labels]
plt.legend(handles=handles, title="Node Types", fontsize=12, loc='upper left')

plt.title("Enhanced GraphQL Schema Relationships", fontsize=15)
plt.axis('off')  # Turn off the axis
plt.grid(False)
plt.savefig("./graph")
plt.show()
