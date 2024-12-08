# FreightFinders (Schneider Team 1)
## Overview
### Goal
Our project aimed to optimize the Schneider FreightPower search engine to enhance its usability, improve its responsiveness, and address user frustrations. By addressing common challenges faced by independent truckers, Schneider-contracted truckers, and dispatchers using the platform, we successfully implemented several features to streamline the search experience.

### Users
The search engine is designed for:

<ul>
- Independent truckers<br>
- Truckers contracted with Schneider<br>
- Dispatchers or companies looking to book transportation loads
</ul>

## User frusturations and solutions
1. ###  Miles to be Traveled<br>
<b>Problem:</b> No option to input the desired travel distance for a single session.<br> 
<b>Solution: </b>Implemented a "Miles to be Traveled" slider, enabling users to specify their travel range, ranging from 25 to 1000 miles.<br>

2. ###  Inconspicuous Search Feature
<b>Problem:</b> Recommendations overshadow the search engine, requiring users to scroll unnecessarily.<br> 
<b>Solution: </b>Moved recommendations to a dedicated section to the right of the search engine for better visibility and direct access.<br>

3. ### Single Selection in Capacity Type
<b>Problem:</b> Only one capacity type could be selected, leading to repetitive searches.<br> 
<b>Solution: </b>Added multi-selection capability for Capacity Types (e.g., Power Only, Dry Van, Refrigerated) to streamline searches.<br>


## Features Implemented
### 1. Miles to be Traveled
<b>What’s New:</b> A slider allowing users to specify the distance they are willing to travel in a single session.<br> 
<b>Impact: </b>Simplifies search for truckers with specific travel preferences.

###  2. Improved Search Accessibility
</b>What’s New: </b>Recommendations no longer interfere with the search engine and are moved to a dedicated section.<br> 
<b>Impact: </b>Users can now directly access the search engine without unnecessary scrolling.

### 3. Multi-Capacity Type Selection
<b>What’s New:</b> Users can select multiple capacity types, such as Power Only, Dry Van, and Refrigerated, in a single search.<br> 
<b>Impact:</b> Reduces redundant searches, improving overall efficiency.

### 4. Search Filter Optimizations
<b>What’s New: </b>Leveraged asynchronous programming to handle API calls concurrently.<br> 
<b>Impact:</b> Reduced execution time for search results, providing a much faster experience.

## Tech Stack
Overall, in terms of the tech stack, we used React for the frontend as it enabled us to create an interactive, user-friendly interface with responsive design principles. We also used Django for the backend framework due to its seamless integration with Python, which was our preferred programming language. We also used PC Miler for fetching the location data accurately.

#### Backend Code HIghlights
 1. Single Search View: Enables retrieving details for a single location using PC Miler.
 2. Radius Search: 
Filters results based on a user-specified radius around a geographic location.
3. Date Filters: 
Allows filtering load postings by start and end dates.
4. Capacity Type Filters:
Supports multi-selection of transport modes to filter results.
5. Complex Query Handling: 
Combines location, date, and capacity filters efficiently using Python’s ThreadPoolExecutor.

## Running the project

Split terminal into 2 sessions. In the main directory and in both the terminals, run <br>
`source venv/bin/activate`
<br>

<b>Frontend Setup</b>: in terminal 1, navigate to the frontend directory and run `npm start`
<br>
<b>Backend Setup</b>: In terminal 2, navigate to the backend directory and run <br>
`pip install -r requirements.txt` <br>
`python manage.py migrate` <br>
`python manage.py runserver` <br>


## Contributors
Nikita, Pearl, Zaid and Zalissa.
