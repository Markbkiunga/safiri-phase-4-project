import React, { useState, useEffect } from 'react';
import NavBar from '../NavBar/NavBar';
import './Review.css';
import logo from '../pictures/SAFIRI LOGO.png';
import Footer from '../Footer/Footer';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';

const Review = () => {
  const [reviews, setReviews] = useState([]);

  // 1. Fetch existing reviews from the Flask server on component mount
  useEffect(() => {
    const fetchReviews = async () => {
      try {
        const response = await fetch('/reviews'); 
        if (!response.ok) throw new Error('Failed to fetch reviews');
        const data = await response.json();
        setReviews(data);
      } catch (error) {
        console.error('Error fetching reviews:', error);
      }
    };
    fetchReviews();
  }, []);

  // 2. Define Yup validation schema with required fields and data type validation
  const validationSchema = Yup.object().shape({
    name: Yup.string().required('Name is required'),
    place: Yup.string().required('Place visited is required'),
    reviewText: Yup.string().required('Review is required'),
    image: Yup.string().url('Must be a valid URL'),
    rating: Yup.number()
      .min(1, 'Rating must be at least 1')
      .max(10, 'Rating must not exceed 10')
      .required('Rating is required'), 
    source: Yup.string().required('Source is required'),
  });

  // Handle form submission and POST the data to the Flask server
  const handleSubmit = async (values, { resetForm, setSubmitting }) => {
    try {
      // Send the form data as JSON to the server
      const response = await fetch('/reviews', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(values), 
      });

      if (!response.ok) throw new Error('Failed to submit review');

      // If submission is successful, update the reviews state
      const newReview = await response.json();
      setReviews((prevReviews) => [...prevReviews, newReview]);

      // Reset the form after successful submission
      resetForm();
      alert('Review submitted successfully!'); 
    } catch (error) {
      console.error('Error submitting review:', error);
      alert('There was an error submitting your review. Please try again.');
    } finally {
      setSubmitting(false); 
    }
  };

  return (
    <div id="review-page">
      <NavBar />
      <img src={logo} alt="safiri-logo" id="safiri-logo" />
      <h1>Review</h1>

      <div className="review-container">
        <div className="form-container">
          <h2>Submit Your Review</h2>

          {/*Formik to manage the form */}
          <Formik
            initialValues={{
              name: '',
              place: '',
              reviewText: '',
              image: '',
              rating: '',
              source: '',
            }}
            validationSchema={validationSchema}
            onSubmit={handleSubmit}
          >
            {({ values, setFieldValue, isSubmitting }) => (
              <Form>
                {/* Name Field */}
                <div className="form-group">
                  <label htmlFor="name">Name:</label>
                  <Field type="text" id="name" name="name" />
                  <ErrorMessage name="name" component="div" className="error" />
                </div>

                {/* Place Field */}
                <div className="form-group">
                  <label htmlFor="place">Place Visited:</label>
                  <Field type="text" id="place" name="place" />
                  <ErrorMessage name="place" component="div" className="error" />
                </div>

                {/* Review Text */}
                <div className="form-group">
                  <label htmlFor="reviewText">Review:</label>
                  <Field as="textarea" id="reviewText" name="reviewText" />
                  <ErrorMessage name="reviewText" component="div" className="error" />
                </div>

                {/* Image URL Field */}
                <div className="form-group">
                  <label htmlFor="image">Image:</label>
                  <Field
                    type="text"
                    id="image"
                    name="image"
                    placeholder="Enter image URL (optional)"
                  />
                  <ErrorMessage name="image" component="div" className="error" />
                </div>

                {/* Rating Field */}
                <div className="form-group">
                  <label>How was your experience using our website?</label>
                  <div className="rating">
                    {Array.from({ length: 10 }, (_, i) => (
                      <span
                        key={i + 1}
                        className={`circle ${values.rating === i + 1 ? 'selected' : ''}`}
                        onClick={() => setFieldValue('rating', i + 1)}
                      >
                        {i + 1}
                      </span>
                    ))}
                  </div>
                  <ErrorMessage name="rating" component="div" className="error" />
                </div>

                {/* Source Dropdown */}
                <div className="form-group">
                  <label htmlFor="source">How did you hear about us?</label>
                  <Field as="select" id="source" name="source">
                    <option value="" label="Select an option" />
                    <option value="friends">From Friends</option>
                    <option value="family">From Family</option>
                    <option value="advertisement">From an Advertisement</option>
                    <option value="social-media">From Social Media</option>
                  </Field>
                  <ErrorMessage name="source" component="div" className="error" />
                </div>

                {/* Submit Button */}
                <button type="submit" disabled={isSubmitting} id="submit-review-button">
                  {isSubmitting ? 'Submitting...' : 'Submit Review'}
                </button>
              </Form>
            )}
          </Formik>
        </div>

        {/* Existing Reviews Display */}
        <div className="existing-reviews new-reviews">
          <h2>Reviews from Other Tourists</h2>
          {reviews.length > 0 ? (
            <ul>
              {reviews.map((review) => (
                <li key={review.id} className="review-item">
                  {review.image && (
                    <img src={review.image} alt={`${review.name}'s review`} className="review-picture" />
                  )}
                  <h3>{review.name}</h3>
                  <p><strong>Place Visited:</strong> {review.place}</p>
                  <p><strong>Review:</strong> {review.reviewText}</p>
                  <p><strong>Rating:</strong> {review.rating}</p>
                  <p><strong>Source:</strong> {review.source}</p>
                </li>
              ))}
            </ul>
          ) : (
            <p>Loading...</p>
          )}
        </div>
      </div>

      <Footer />
    </div>
  );
};

export default Review;
