# SAFIRI

## Brief Description

Safiri is a travel app designed to help users explore various destinations, submit reviews, and view a slideshow of attractive travel locations.

## Features

- Home : Displays a welcome message and a slideshow of travel destinations.

- Discover Page: Shows a list of popular travel places with their details.

- About Us Page: Provides information about the application and its team.

- Review Page: Allows users to submit reviews and view existing reviews from other tourists.

- Contact Us Page: Provides contact information and location details.

- Login Page: Allows users to log in to the application.

- Signup Page: Allows users to sign up for the application.

## Technologies used

- React
- React Router
- CSS
- React Slick for slideshow

## Setting Up

### 1. Cloning the Repository

Clone the repository using the following command:

```bash
git clone git@github.com:Markbkiunga/safiri-phase-4-project.git
```

### 2. Installing Dependencies

Navigate to the project directory and install the required dependencies:

```bash
npm install
```

### 3. Starting the Application

To start the application, run the following command:

```bash
npm start
```

## Components

1. App.jsx

This is the main component that sets up the routing for the application.

- Routes:

/ - Home
<br>
/discover - Discover
<br>
/about - About Us
<br>
/review - Review
<br>
/contactus - Contact Us

2. Home.jsx
   Displays the home page with a welcome message and a slideshow of travel destinations. Dependencies: NavBar, Slideshow

3. Slideshow.jsx
   A carousel component that shows various travel destination images and text.

Dependency: react-slick

4. Discover.jsx
   Lists popular travel places with their images, descriptions, activities, and transport options.

5. Footer.jsx
   Displays the footer with contact information, including email, phone number, and location.

- Dependency: react-icons

6. NavBar.jsx
   Navigation bar with links to different pages of the app. Includes a scroll effect for the navbar.

7. Review.jsx
   Allows users to submit reviews and view existing reviews. Reviews include a name, place visited, review text, image, rating, and source.

8. ContactUs.jsx
   Displays contact information for the application.

9. AboutUs.jsx
   Displays information about the application.

10. Login.jsx
    Allows users to log in to the application.

11. Signup.jsx
    Allows users to sign up for the application.

## Links

### Vercel link

[Vercel Link](https://safiri-phase-4-project.vercel.app/)

### Git hub link

[Github link ](https://github.com/Markbkiunga/safiri-phase-4-project)

## Author

Mark Brian and Megan Kwamboka

## Date

16th August 2024

## Conclusion

The project was worked on by Mark Brian , Kevin Kamau, Aron Kipkorir, Meghan Kwamboka and Anthony Onyango.
