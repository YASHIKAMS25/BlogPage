Blog Page – Wagtail & Django
This project is a fully functional blog page built using Wagtail and Django, designed to manage and display blog posts efficiently. It includes a dynamic frontend, a robust backend, and SEO-friendly implementations to enhance visibility.


Features

🌐 Frontend (User Interface)

Designed with HTML, CSS, and JavaScript for a responsive and engaging UI.
Blog posts are displayed dynamically on the blog index page (blogpage_index.html).
Each blog has a dedicated detail page (blogpage.html).
Includes like and comment functionalities, enhancing user interaction.
Implemented share functionality, allowing users to easily copy and share blog links.

⚙️ Backend (Wagtail & Django)

Built using Django and Wagtail CMS for efficient blog management.
Models defined in models.py to handle blog posts, likes, and comments.
Supports dynamic blog creation, editing, and deletion through the Wagtail admin panel.
Uses Django ORM for database management and efficient query handling.
Like and comment functionalities are updated dynamically without page reload.

🔍 SEO Optimization

Integrated meta tags for better search engine visibility.
Implemented clean URL structures to improve rankings.
Added Open Graph (OG) tags for optimized social media sharing.
Installation & Setup

1️⃣ Clone the Repository
sh
Copy
Edit
git clone https://github.com/yourusername/blog-page.git
cd blog-page

2️⃣ Create a Virtual Environment
sh
Copy
Edit
python -m venv venv  
source venv/bin/activate  # On Windows: venv\Scripts\activate

3️⃣ Install Dependencies
sh
Copy
Edit
pip install -r requirements.txt

4️⃣ Apply Migrations
sh
Copy
Edit
python manage.py migrate

5️⃣ Run the Development Server
sh
Copy
Edit
python manage.py runserver
Access the blog at http://127.0.0.1:8000/


Usage
Admin Panel: http://127.0.0.1:8000/admin/ (Login required)
Create & Manage Blogs via the Wagtail CMS panel.
Interact with Posts – Users can like, comment, and share blog posts.
Future Enhancements
Add category and tag filters for better content organization.
Implement a search functionality to find blog posts easily.
Improve SEO analytics tracking for better insights.
Contributing
Contributions are welcome! Feel free to fork the repository, raise issues, or submit pull requests.


License
This project is licensed under the MIT License.

