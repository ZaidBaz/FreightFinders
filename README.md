# FreightFinders (Schneider Team 1)
## Repository Link
https://github.com/ZaidBaz/FreightFinders
## Overview
### Goal
Our project aimed to optimize the Schneider FreightPower search engine to enhance its usability, improve its responsiveness, and address user frustrations. By addressing common challenges faced by independent truckers, Schneider-contracted truckers, and dispatchers using the platform, we successfully implemented several features to streamline the search experience.

### Users
The search engine is designed for:
- Independent truckers<br>
- Truckers contracted with Schneider<br>
- Dispatchers or companies looking to book transportation loads


## User Frustrations and Solutions
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
Frontend: React <br>
Backend: Django <br>
Mapping API: PC Miler  <br>

We chose React for the frontend due to its ability to create an interactive, user-friendly interface with responsive design principles. Django was selected for the backend framework because of its seamless integration with Python. For accurate geographic data, we utilized PC Miler.

#### Backend Code Highlights
 1. Single Search View: Enables retrieving details for a single location using PC Miler.
 2. Radius Search: 
Filters results based on a user-specified radius around a geographic location.
3. Date Filters: 
Allows filtering load postings by start and end dates.
4. Capacity Type Filters:
Supports multi-selection of transport modes to filter results.
5. Complex Query Handling: 
Combines location, date, and capacity filters efficiently using Python’s ThreadPoolExecutor.

## Setup  Steps

### 1. Clone the Repository:
`git clone https://github.com/ZaidBaz/FreightFinders.git` <br>
Navigate to the project directory: `cd FreightFinders`
### 2. Set Up Virtual Environment:
Split the terminal into two sessions. In both terminal sessions, activate the virtual environment after navigating to the main project directory with:
<br>`source venv/bin/activate` 
### 3. Frontend Setup:
- Navigate to the frontend directory:  `cd frontend` <br>
- Install dependencies: `npm install`
- Start the development server: `npm start`
### 4. Backend Setup:
- Navigate to the backend directory: `cd backend/FreightFinders`
- Install Python dependencies: `pip install -r requirements.txt`
- Apply database migrations: `python manage.py migrate`
- Start the backend server: `python manage.py runserver`

## What Works & What Doesn’t
### What Works
- Miles to be Traveled slider, allowing users to specify travel ranges.
- Improved search accessibility by moving recommendations to a dedicated section.
- Multi-selection of capacity types for a more streamlined search process.
- Filter optimizations for faster query execution using asynchronous programming.

### What Doesn’t Work
While all implemented features work as intended, there are additional enhancements that could improve the user experience in future iterations.

## What We’d Work on Next
- Mobile Optimization: Ensure the platform is fully optimized for mobile devices to cater to truckers on the go.
Advanced Filtering 
- Options: Add advanced filters, such as weight capacity.
- Radius sliders: For now, the radius for origin, destination and miles to be travelled allows the user to set a maximum distance. It would be helpful to enable them to set a minimum distance simultaneously.



## Contributors
Nikita, Pearl, Zaid and Zalissa.
