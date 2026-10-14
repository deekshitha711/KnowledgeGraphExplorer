# Knowledge Graph Explorer

An interactive data science application that collects information from Wikipedia and Wikidata, builds knowledge graphs, and visualizes relationships between concepts. It also provides graph statistics and interactive charts to help users explore and analyze connected information.

## Features

- **Topic Search:** Search for a topic and explore related concepts.
- **Multiple Data Sources:** Choose between Wikipedia and Wikidata.
- **Knowledge Graph Visualization:** View concepts as nodes and their connections as directed edges.
- **Concepts & Relations:** Explore concepts, descriptions, relationship labels, and source links in a table.
- **Graph Analysis:** View metrics such as nodes, edges, graph density, connected components, average degree, and degree centrality.
- **Interactive Charts:** Explore the most connected concepts using a bar chart and examine node connection counts using a histogram.
- **Data Cleaning:** Remove duplicate and irrelevant entries before graph construction.
- **Caching:** Reduce repeated processing and API requests using Streamlit caching.

## Technologies Used

- **Python** – Main programming language
- **Streamlit** – Interactive web dashboard
- **Wikipedia MediaWiki API** – Article summaries and related article links
- **Wikidata API** – Structured entity information and claims
- **Requests** – API communication
- **NetworkX** – Graph construction and analysis
- **PyVis** – Interactive network visualization
- **Pandas** – Tabular data handling
- **Plotly Express** – Data visualization

## Project Structure

```text
KnowledgeGraphExplorer/
│
├── app.py
├── requirements.txt
│
├── src/
│   ├── __init__.py
│   ├── wikipedia_api.py
│   ├── wikidata_api.py
│   ├── data_cleaner.py
│   └── graph_builder.py
│
└── .streamlit/
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/deekshitha711/KnowledgeGraphExplorer.git
cd KnowledgeGraphExplorer
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\activate
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Run the application

```bash
python -m streamlit run app.py
```

## How to Use

1. Open the application in your browser.
2. Enter a topic or select one of the suggested topics.
3. Choose Wikipedia or Wikidata as the data source.
4. Adjust the node limit as required.
5. Explore the **Knowledge Graph** view to see concepts and connections.
6. Open **Concepts & Relations** to review the collected information and source links.
7. Open **Data Analysis** to examine graph metrics, the central-concepts bar chart, and the degree-distribution histogram.

## How It Works

1. **Data Collection:** Retrieves article information or structured entity data from the selected API.
2. **Data Preprocessing:** Cleans titles, summaries, and related entries.
3. **Graph Construction:** Uses NetworkX to represent concepts as nodes and relationships as directed edges.
4. **Visualization:** Uses PyVis to display the interactive knowledge graph.
5. **Analysis:** Calculates graph statistics and uses Plotly Express to generate charts.
6. **Dashboard:** Displays the graph, concept table, and analysis through Streamlit.

## Graph Analysis

The application uses graph metrics to understand the structure of the retrieved network:

- **Nodes:** Number of concepts or entities.
- **Edges:** Number of directed connections.
- **Graph Density:** Proportion of possible connections that exist.
- **Connected Components:** Groups of connected nodes, depending on the component definition used.
- **Average Degree:** Average number of connections per node.
- **Degree Centrality:** Measures the direct connectivity of each node.

## Requirements

- Python installed on your computer
- Git for cloning the repository
- Internet connection to retrieve data from Wikipedia or Wikidata
- Python dependencies listed in `requirements.txt`

## Applications

- Exploring relationships between concepts
- Discovering related topics
- Understanding structured knowledge
- Analyzing network connectivity
- Learning graph theory and data visualization

## Future Enhancements

- Display specific Wikidata property names on graph edges.
- Add advanced graph algorithms and community detection.
- Provide additional graph filtering options.
- Support exporting graph data and analysis results.
- Improve visualization for larger networks.
