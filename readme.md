# Slide AI Generator

This project is an AI-powered presentation generator that creates PowerPoint slide decks based on a given topic. It leverages large language models (LLMs) for content synthesis and web search APIs to gather relevant information, producing structured and informative presentations with speaker notes and relevant images.

## Features

*   **AI-Powered Content Generation:** Synthesizes presentation content, including titles, subtitles, bullet points, and speaker notes, using an LLM.
*   **Optimized Web Search:** Generates an optimized search query for a given topic to fetch highly relevant information from the web.
*   **Dynamic Slide Layouts:** Automatically selects suitable slide layouts from a template, supporting titles, content, and images.
*   **Image Integration:** Fetches and integrates relevant images into slides based on slide titles.
*   **Speaker Notes:** Includes detailed speaker notes for each slide to assist presenters.
*   **Customizable Templates:** Uses a PowerPoint template for consistent styling.

## Setup

To set up and run this project, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/mayberohan/AI_Slides.git
    cd slide_ai
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure API Keys:**
    This project uses external APIs for web search (SerpAPI) and LLM access (e.g., Gemini). You need to set up your API keys.

    *   **SerpAPI:** Obtain an API key from [SerpAPI](https://serpapi.com/).
    *   **LLM Client:** Depending on the LLM client used (e.g., Gemini), you will need to configure its API key. For Gemini, this would be `GEMINI_API_KEY`.

    Create a `.env` file in the root directory of the project and add your API keys:
    ```
    SERPAPI_KEY="your_serpapi_api_key_here"
    GEMINI_API_KEY="your_gemini_api_key_here"
    # Add other LLM API keys as needed
    ```

## Usage

To generate a presentation, run the `main.py` script with the required arguments:

```bash
python -m src.main --topic "Your Presentation Topic" --output "output_filename.pptx" --template "templates/default.pptx"
```

**Example:**

```bash
python -m src.main --topic "The Impact of Artificial Intelligence on Healthcare" --output "AI_Healthcare_Presentation.pptx" --template "templates/default.pptx"
```

## Project Structure

*   `src/`: Contains the core Python scripts for the application.
    *   `main.py`: Entry point of the application, handles argument parsing, search query generation, content synthesis, and presentation creation.
    *   `search_client.py`: Handles web searches using SerpAPI.
    *   `synthesizer.py`: Orchestrates LLM calls for content generation and parses the structured output.
    *   `ppt_generator.py`: Manages the creation and population of PowerPoint slides using `python-pptx`.
    *   `llm_client.py`: Interface for interacting with the Large Language Model.
    *   `image_client.py`: Handles fetching relevant images.
    *   `config.py`: Stores configuration variables like `MAX_SEARCH_RESULTS`.
    *   `utils.py`: Utility functions.
    *   `cache.py`: Caching mechanisms.
    *   `web_search.py`: (Potentially for alternative web search implementations)
*   `prompts.md`: Stores the LLM prompts for slide generation and search query optimization.
*   `templates/`: Contains PowerPoint template files (e.g., `default.pptx`).
*   `images/`: Directory for storing fetched images.
*   `requirements.txt`: Lists all Python dependencies.

