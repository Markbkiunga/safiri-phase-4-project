import React, { useState, useEffect } from 'react';
import NavBar from '../NavBar/NavBar';
import './Review.css';
import logo from '../pictures/SAFIRI LOGO.png';
import Footer from '../Footer/Footer';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';

const Review = () => {
  const [reviews, setReviews] = useState([]);

  // Fetch existing reviews from the Flask server
  useEffect(() => {
    const fetchReviews = async () => {
      try {
        const response = await fetch('/reviews');
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setReviews(data);
      } catch (error) {
        console.error('Error fetching reviews:', error);
        setReviews([]);
      }
    };

    fetchReviews();
  }, []);

  // Form validation schema using Yup
  const validationSchema = Yup.object().shape({
    name: Yup.string().required('Name is required'),
    place: Yup.string().required('Place visited is required'),
    reviewText: Yup.string().required('Review is required'),
    image: Yup.string().url('Must be a valid URL').optional(),
    rating: Yup.number()
      .min(1, 'Rating must be between 1 and 10')
      .max(10, 'Rating must be between 1 and 10')
      .required('Rating is required'),
    source: Yup.string().required('Source is required'),
  });

  // Handle form submission and send data to the server
  const handleSubmit = async (values, { resetForm }) => {
    try {
      const response = await fetch('/reviews', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(values),
      });

      if (!response.ok) {
        throw new Error('Failed to submit review');
      }

      const newReview = await response.json();
      setReviews([...reviews, newReview]);
      resetForm();
    } catch (error) {
      console.error('Error submitting review:', error);
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
            {({ values, setFieldValue }) => (
              <Form>
                <div className="form-group">
                  <label htmlFor="name">Name:</label>
                  <Field type="text" id="name" name="name" />
                  <ErrorMessage name="name" component="div" className="error" />
                </div>

                <div className="form-group">
                  <label htmlFor="place">Place Visited:</label>
                  <Field type="text" id="place" name="place" />
                  <ErrorMessage name="place" component="div" className="error" />
                </div>

                <div className="form-group">
                  <label htmlFor="reviewText">Review:</label>
                  <Field as="textarea" id="reviewText" name="reviewText" />
                  <ErrorMessage
                    name="reviewText"
                    component="div"
                    className="error"
                  />
                </div>

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

                <div className="form-group">
                  <label>How was your experience using our website?</label>
                  <div className="rating">
                    {Array.from({ length: 10 }, (_, i) => (
                      <span
                        key={i + 1}
                        className={`circle ${
                          values.rating === i + 1 ? 'selected' : ''
                        }`}
                        onClick={() => setFieldValue('rating', i + 1)}
                      >
                        {i + 1}
                      </span>
                    ))}
                  </div>
                  <ErrorMessage name="rating" component="div" className="error" />
                </div>

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

                <button type="submit" id="submit-review-button">
                  Submit Review
                </button>
              </Form>
            )}
          </Formik>
        </div>

        <div className="existing-reviews new-reviews">
          <h2>Reviews from Other Tourists</h2>
          {reviews.length > 0 ? (
            <ul>
              {reviews.map((review) => (
                <li key={review.id} className="review-item">
                  {review.image && (
                    <img
                      src={review.image}
                      alt={`${review.name}'s review`}
                      className="review-picture"
                    />
                  )}
                  <h3>{review.name}</h3>
                  <p>
                    <strong>Place Visited:</strong> {review.place}
                  </p>
                  <p>
                    <strong>Review:</strong> {review.reviewText}
                  </p>
                  <p>
                    <strong>Rating:</strong> {review.rating}
                  </p>
                  <p>
                    <strong>Source:</strong> {review.source}
                  </p>
                </li>
              ))}
            </ul>
          ) : (
            <p>Loading...</p>
          )}
        </div>
      </div>

      <div id="review-page-footer">
        <Footer />
      </div>
    </div>
  );
};

export default Review;
