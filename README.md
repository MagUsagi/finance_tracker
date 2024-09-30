# Finance Tracker

## Overview

This **Finance Tracker** was created out of a personal need to track income and expenses more efficiently. After being unsatisfied with existing apps and services, I developed this project to tailor the features to my specific requirements. One key feature I focused on is the **visualization of income and expense balances**, which is presented through easy-to-understand graphs. Additionally, I aimed to implement an **Excel import feature**, which is currently under development.

The secondary purpose of this project is to serve as a portfolio piece for my job applications in the IT industry, particularly in **data science**. This project demonstrates my ability to manage financial data, perform data queries, and visualize the results, showcasing my skills in **database management** and **data visualization**.

## Features

### Monthly Dashboard
- Displays a **list of total amounts by category** for the month.
- Features a **pie chart** representing the categorical distribution and a **bar graph** showing daily expenses.
- The summary of each month can be easily viewed at a glance. The pie chart's colors are customized using the **Seaborn** color palette instead of the default.

### Transition
- Shows a combined graph with **monthly income and expense trends**.
- **Income is represented by a bar graph**, while **expenses are shown as a line graph**, providing a clear visual of the balance between the two.

### Expense List
- Displays a list with the following fields: **Date**, **Category**, **Amount**, **Description**, and **Edit** options.
- Edit options include **Update** and **Delete** functionalities.
- **Advanced search** capabilities:
  - Filter by **year** and **month**.
  - Filter by **amount range** (e.g., CHF 100 - CHF 500).
  - **Keyword search** within the description.
  - Filter by **category** using designated buttons.
- Includes an **Add New Expense** button for adding new records to the database.
- Pagination: results are shown in groups of 10, with the total number of results (e.g., "10 results") displayed at the top.

### Income List
- Similar to the Expense List but focused on **income records**.
- Features an **Add New Income** button and search functionality for filtering by **year** and **month**.

### Upcoming Features
- **Assets Page**: A list for tracking assets, similar to the Income List.
- **Category Page**: A page for **adding and editing categories**, which is currently only available through the admin page.

## Technologies Used
- **Programming Language**: Python
- **Framework**: Django
- **Visualization**: Plotly for generating interactive graphs
- **Frontend**: HTML, CSS

## Purpose
This project is part of my portfolio as I pursue a career in **data science**. It highlights:
- **Database management skills** through efficient handling of financial records.
- **Data visualization** using Plotly, a key component in analyzing and presenting financial data clearly.
- **User interface design** with a focus on usability, providing clear insights into personal finances.

The Excel import feature is a work-in-progress, and I plan to expand functionality to include asset management and category customization in future updates.
