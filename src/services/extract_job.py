from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os
import re
import json

def extract_job_info(job_url):
    """
    Extracts information from a LinkedIn job posting using the provided URL.
    Args:
        job_url (str): URL of the job posting (e.g., https://www.linkedin.com/jobs/view/4208425886)
    Returns:
        dict: Dictionary with raw and structured job information or error message.
    """
    # Initialize the result
    result = {
        "status": "error",
        "message": "",
        "data": {}
    }

    try:
        # Validate URL
        if not re.match(r"https://www\.linkedin\.com/jobs/view/\d+", job_url):
            result["message"] = "Invalid URL. Must be in the format https://www.linkedin.com/jobs/view/<job_id>"
            return result

        # Scrape with Playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(job_url, timeout=60000)
            page.wait_for_timeout(5000)  # Wait for dynamic content to load
            html_content = page.content()
            browser.close()

        # Parse with BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")

        # Extract raw information
        job_data = {}

        # Job title
        title_elem = soup.find("h1", class_="top-card-layout__title")
        job_data["title"] = title_elem.get_text(strip=True) if title_elem else "Not found"

        # Company
        company_elem = soup.find("a", class_="topcard__org-name-link")
        job_data["company"] = company_elem.get_text(strip=True) if company_elem else "Not found"

        # Location
        location_elem = soup.find("span", class_="topcard__flavor--bullet")
        job_data["location"] = location_elem.get_text(strip=True) if location_elem else "Not found"

        # Full description (includes responsibilities, qualifications, etc.)
        description_elem = soup.find("div", class_="description__text")
        description_text = description_elem.get_text(strip=True) if description_elem else "Not found"
        job_data["description"] = description_text

        # Store raw data in result
        result["data"] = job_data
        result["status"] = "success_raw"
        print("Raw Scraped Data:", job_data)  # Debug print

        # Process with LangChain to structure the description
        try:
            llm = ChatOpenAI(
                model_name="gpt-4-mini",
                api_key=os.getenv("OPENAI_API_KEY"),
                temperature=0.3
            )
            prompt = PromptTemplate(
                input_variables=["text"],
                template="""
                Extract the following information from the provided job posting text:
                - Job title
                - Company
                - Location
                - General description
                - Main responsibilities
                - Required qualifications
                - Desired skills
                - Benefits (if mentioned)

                Format the output as a structured JSON:
                {
                    "title": "",
                    "company": "",
                    "location": "",
                    "description": "",
                    "responsibilities": [],
                    "qualifications": [],
                    "skills": [],
                    "benefits": []
                }
                Job posting text: {text}
                """
            )

            # Combine raw information for LLM
            raw_text = (
                f"Title: {job_data['title']}\n"
                f"Company: {job_data['company']}\n"
                f"Location: {job_data['location']}\n"
                f"Description: {job_data['description']}"
            )

            # Execute LLM
            response = llm.invoke(prompt.format(text=raw_text))
            structured_output = response.content  # ChatOpenAI returns a message object with content
            print("Raw LLM Output:", structured_output)  # Debug print

            # Clean and parse JSON
            json_match = re.search(r'\{.*\}', structured_output, re.DOTALL)
            if json_match:
                cleaned_output = json_match.group(0)
                structured_data = json.loads(cleaned_output)
                result["data"] = structured_data
                result["status"] = "success_structured"
            else:
                result["message"] = "No valid JSON found in LLM response"
                result["data"] = job_data  # Fall back to raw data

        except Exception as e:
            result["message"] = f"Error processing with LangChain: {str(e)}"
            result["data"] = job_data  # Fall back to raw data

    except Exception as e:
        result["message"] = f"Error extracting job information: {str(e)}"

    return result

