
E-Voting System

A simple and secure Electronic Voting System built using Flask and HTML/CSS.
This application allows users to log in, cast their vote, and view election results.


Features:

    User login system
    Vote casting for candidates
    Prevent multiple voting
    Real-time election results
    Logout functionality
    Clean and responsive UI


Project Structure:

    E-voting-system/
    │
    ├── app.py
    ├── templates/
    │   ├── login.html
    │   ├── vote.html
         └── results.html

         

Technologies Used:

    Frontend:
        HTML
        CSS
    Backend:
        Python
        Flask



How It Works:

    User logs in using email and password.
    After login, user is redirected to the voting page.
    User selects a candidate and casts vote.
    System ensures one user = one vote.
    Results page displays total votes.



Future Improvements:

    Add database integration (SQLite/MySQL).
    Implement secure authentication (JWT / hashing     passwords).
    Admin dashboard.
    Live vote charts/graphs.
    Deploy online (Render / Heroku).


Important Notes:

    This is a basic project for learning purposes.
    Authentication is simple (not production-level secure).
    Data storage method depends on backend implementation.
    Can be enhanced with databases like SQLite/MySQL.
