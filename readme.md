
# getActive
getActive is a website designed to help individuals find and enroll in various fitness activities within their community. Users are also able to create and publish their own activities for other users to take part in.

## Installation
-   Install project dependencies by running  `pip install -r requirements.txt`
-   Make and apply migrations by running  `python manage.py makemigrations`  and  `python manage.py migrate`

## Files Details
`getActive`  - app for finding and creating fitness activities
-   `models.py`  - Contains User and Activity models that contain information on users and fitness activities
	- Users model
	- Activity model that contains all details of an activity (with a serializer). 
		- Defines several fields with choices, such as `location_choices`, `category_choices`, and `duration_choices` that allows users to select from a predefined set of values when creating an activity instance.
		- The `attendants` field is also defined as a ManyToManyField to the `User` model, which allows for many users to attend a single activity and vice versa.
		- The `Activity` model defines several methods that return the predefined choices for certain fields which are helpful for generating forms or other UI elements that allow users to select from these choices.
		- The `serialize` method defined on the `Activity` model returns a dictionary representation of an activity instance, which is useful when working with JSON or other serialized data formats.
-   `urls.py`  - Contains all url paths for getActive, such as list of activities, creating new activities and viewing user's enrolled activities
-   `views.py`  - Contains all functions such as list of activities, filtering activities and creating new activities
	- `activities` renders the `getActive/activities.html` template and takes an optional `searchActivityForm` form that it passes to the template context when the request method is `GET`.
	- `newActivityForm` contains all the fields for creating a new activity
	- `new_activity` saves the new activity created and its related information, limits users to only creating 1 activity per day to prevent spamming of activities by a particular user, given that it is a community platform. Requires user to be authenticated.
	- `get_by_title` returns activities that contains the words in their title or description
	- `activity` to retrieve information of a specific activity
	- `searchActivityForm` to filter activities by extracting the search query and search for activities whose name or description contains the query using a Django QuerySet filter
	- `enroll` for authenticated users to enroll into an activity
	- `get_enrolled_talks` to retrieve the activities that users have enrolled in
	- Register, Login and Logout functions as like past projects
-   `static`  - Holds all static files
	   -   `styles.css`  - Contain all css used for styling the website. 
		   - @media used to ensure responsiveness of website
		   - responsive navbar design
		   - classes and ID tags for styling of the different components on the website
	   -   `js`  - Contains all JavaScript files for manipulating the DOM with ajax functionalities.
		   - `activities.js` to filter activities, display the activities, as well as an autocomplete function that provides suggestions when users search for an activity. 
			   - `DOMContentLoaded`event listener that waits for page to load before calling `get_all_data()` to retrieve data and populate the webpage. It also modifies the webpage by changing the title and displaying/hiding filters based on user input.
			   - `get_all_data` fetches data from a server, then calls the `show_activities()` function to display the data on the webpage.
			   - `show_activities` creates HTML elements for each activity and adds them to the webpage. It also attaches an event listener to each activity that directs the user to a separate page for that activity.
			   - Other functions include `show_autocomplete` which displays a list of suggested search terms based on user input and `get_data_by_title()` which fetches data from the server based on user input and displays the results on the webpage.
		   - `myActivities.js` to retrieve activities users have enrolled in and display them in the DOM. Allows users to easily access and find what they have enrolled in.
			   - adds an event listener to the DOMContentLoaded event which will execute the function `load_activities()` when the DOM has finished loading.
			   - `load_activities` sends a POST request to the server to retrieve enrolled activities, then creates a card for each activity, and adds an event listener to each card to redirect the user to a specific activity's page when clicked.
			   - `show_activities`  creates HTML elements with information about the activities fetched from the server, and appends them to a parent HTML element on the web page. It also adds a click event listener to each activity card that redirects the user to a new page with detailed information about the selected activity.
-   `Templates`  - Holds all html files for the pages explained in `views.py`
- `Media` folder that stores images uploaded to the website


## Distinctiveness and Complexity
This website is not similar to the past projects. It is a website for community-based fitness activities, focusing on creating a community around fitness activities, allowing users to create and enroll in various activities within their community. This feature is unique and adds a social aspect to fitness, which is not present in other CS50x projects.

Its complexity is described as follows:
* Multiple models with complex functions
* Linking multiple HTML files to Javascript files
* Uses ajax functionality to filter activities and display results without reloading the site. This feature adds a level of interactivity and responsiveness that is not present in other CS50x projects.
* Multiple filters can be selected at once
* Fully mobile-responsive, which adds an additional layer of complexity and user-friendliness.
