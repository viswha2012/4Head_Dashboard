# Police Dashboard

## Overview

We have developed a comprehensive police dashboard aimed at providing visual insights into various metrics relevant to different levels of authority within the police hierarchy. The dashboard is designed to be dynamic, allowing users to customize and view data according to their specific needs.

## Features

- **Central Dashboard**: The central dashboard provides a customizable interface displaying visual data derived from the provided metric data. Users can select and view different graphs based on their preferences, with the ability to save customized layouts to their profiles.

- **Layered Access Levels**:
  - **Level 1 (ACP/DySP)**: This level enables users to track personal performance metrics, providing aggregated data and insights to reflect leadership impacts.
  - **Level 2 (Inspector)**: Inspectors can supervise sub-inspectors and monitor their own metrics for efficient management.
  - **Level 3 (Precinct)**: Users at this level can view required metrics of officers within a specific precinct, with data consolidated for upper layers.

- **Enhanced Data Visualization with Apache Superset**: We have integrated Apache Superset (Preset.io) to enhance police data visualization. Apache Superset offers real-time insights and dynamic graph generation, empowering users with user-friendly tools for manipulating visual data.

## Technologies Used

- **HTML**: Used for creating the website interface and embedding Apache Superset.
- **CSS**: Utilized for styling the dashboard for a visually appealing experience.
- **JavaScript**: Implemented for dynamic interactions and functionalities on the client-side.
- **Flask**: Used as the backend framework for server-side operations and handling database interactions.
- **Apache Superset (Preset.io)**: Integrated for advanced data visualization and analytics capabilities.

## Usage

To use the police dashboard, follow these steps:

1. Clone the repository to your local machine.
2. Install the necessary dependencies specified in the `requirements.txt` file.
3. Configure the Flask application to connect to your database and set up user profiles and access levels.
4. Run the Flask application to start the server.
5. Access the dashboard through a web browser by navigating to the appropriate URL.
6. Depending on your access level, customize the dashboard layout and view metrics relevant to your role.

## Contributors

- Sibi Rassal
- Viswha Vijay
- Vishal Mahendran
- Ram Prajeeth
