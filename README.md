README.txt
==========

MyAlbumRater - A Music Album Rating and Commenting Platform
------------------------------------------------------------

Overview
--------
MyAlbumRater is a Django-based web application that allows music enthusiasts to discover, rate, and comment on their favorite music albums. Built with modern web technologies, the platform offers a dynamic and responsive user experience where users can upload albums, provide ratings and detailed reviews, and interact with a vibrant community of fellow music lovers.

Features
--------
• **User Registration & Authentication:**  
  - Secure user signup and login functionality using Django’s built-in authentication system.
  - Profile management with editable bio, profile picture, and the ability to follow other users.
  - Options for password change and account deletion.

• **Album Management:**  
  - Upload new albums with cover art, title, genre, and description.
  - Automatic slug generation for SEO-friendly URLs.
  - Album editing and deletion for the original uploader.

• **Ratings & Comments:**  
  - Users can rate albums on a scale of 1 to 10.
  - Add, edit, or delete comments with support for up to 1500 characters per comment.
  - “Read more” functionality for lengthy comments, ensuring concise displays with expandable content.

• **Search & Filtering:**  
  - Comprehensive search functionality to filter albums and users by keywords.
  - Additional filtering by genre and sorting options (e.g., highest views, most recent uploads).

• **Dynamic Content Loading (AJAX):**  
  - AJAX-powered pagination for smooth and efficient browsing of albums and comments.
  - Asynchronous comment submission and updates, minimizing page reloads.

• **Responsive Design & Modern UI:**  
  - Responsive layout built with Bootstrap 5.
  - Custom CSS styles ensure a clean and user-friendly interface.
  - Interactive features such as automatic textarea resizing, character counting, and a “back to top” button.

• **Database Population Script:**  
  - A dedicated script (`population_script.py`) is provided to populate the database with sample users, albums, and comments for development and testing purposes.

Technologies and Frameworks
---------------------------
• **Django:**  
  - Backend framework providing a robust ORM, templating engine, and comprehensive user authentication.
  
• **SQLite:**  
  - Lightweight database engine used for development.
  
• **Bootstrap 5:**  
  - Frontend framework for responsive design and prebuilt UI components.

• **Pillow:**  
  - For processing uploaded images
  
• **JavaScript & AJAX:**  
  - Custom JS files for asynchronous comment submission (`ajax_comment.js`), AJAX pagination (`ajax_pagination.js`), auto-resizing textareas (`auto_resize.js`), “back to top” functionality (`back_to_top.js`), and “read more” functionality (`readmore.js`).
  
• **HTML & CSS:**  
  - Django templating language combined with custom CSS (`static/css/main.css`) for styling and layout.
