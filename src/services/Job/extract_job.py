
from bs4 import BeautifulSoup
import requests
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from fake_useragent import UserAgent
import os
import re
import json


def extract_job_info(job_url):
    """
    Extracts information from a LinkedIn job posting using requests and BeautifulSoup.
    """
    result = {
        "status": "error",
        "message": "",
        "data": {}
    }

    try:
        # Validate URL
        if not re.match(r"https://www\.linkedin\.com/jobs/view/\d+", job_url):
            result["message"] = "Invalid URL format"
            return result

        # Configure headers with random user agent
        ua = UserAgent()
        headers = {
            'User-Agent': ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

        # Make the request
        response = requests.get(job_url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract job data
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

        # Description
        description_elem = soup.find("div", class_="description__text")
        job_data["description"] = description_elem.get_text(strip=True) if description_elem else "Not found"

        # Store raw data
        result["data"] = job_data
        result["status"] = "success_raw"


        try:
            llm = ChatOpenAI(
                model_name="gpt-4o-mini",
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
            #print("Raw LLM Output:", structured_output)  # Debug print

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


    except requests.RequestException as e:
        result["message"] = f"Error fetching job information: {str(e)}"
    except Exception as e:
        result["message"] = f"Error processing job information: {str(e)}"


    return result

