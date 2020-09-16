# web-scraping-challenge

Step 1 - Scraping<br>
<ul>
  <li>Scrap images, text, and table from 5 different resources/website about mars.</li>
  <li>file: scrape_mars.py</li>
</ul>

Step 2 - MongoDB and Flask Application<br>
<ul>
  <li>Using flask_pymongo (PyMongo) to first connect to MongoDB</li>
  <li>When clicking "Get New Data" bottom, it will scrape the websites and update/insert data into the database. Then redirect to the HOME page</li>
  <li>Once getting back to the homepage, it will extract the results from the updated collection (table) and show on the homepage</li>
  <li>Using render_template to pass the fields/columns from the database the HTML file</li>
  <li>file: app.py</li>
 </ul>
