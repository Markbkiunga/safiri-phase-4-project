import React, { useState, useEffect } from 'react';
import NavBar from '../NavBar/NavBar';
import './Review.css';
import logo from '../pictures/SAFIRI LOGO.png';
import Footer from '../Footer/Footer';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';

const Review = () => {
  const [reviews, setReviews] = useState([]);

  useEffect(() => {
    const fetchReviews = async () => {
      try {
        const response = await fetch('/reviews');
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        if (Array.isArray(data)) {
          setReviews(data);
          console.log(data);
        } else {
          console.error('Unexpected data structure:', data);
          setReviews([]);
        }
      } catch (error) {
        console.error('Error fetching reviews:', error);
        setReviews([]);
      }
    };

    fetchReviews();
  }, []);

  const validationSchema = Yup.object().shape({
    name: Yup.string().required('Required'),
    place: Yup.string().required('Required'),
    reviewText: Yup.string().required('Required'),
    source: Yup.string().required('Required'),
  });

  const handleSubmit = (values, { resetForm }) => {
    const newReview = {
      id: Date.now(),
      name: values.name,
      place: values.place,
      review: values.reviewText,
      image: values.image,
      rating: values.rating,
      source: values.source,
    };

    console.log(newReview);
    setReviews([...reviews, newReview]);
    resetForm();
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
              rating: null,
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
                  <ErrorMessage
                    name="place"
                    component="div"
                    className="error"
                  />
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
                  <ErrorMessage
                    name="source"
                    component="div"
                    className="error"
                  />
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
                  {review.user.profile.image && (
                    <img
                      src={review.user.profile.image}
                      alt={`${review.user.username}'s review`}
                      className="review-picture"
                    />
                  )}
                  <h3>{review.user.username}</h3>
                  {review.site.description && (
                    <p>
                      <strong>Place Visited:</strong> {review.site.description}
                    </p>
                  )}
                  {review.description && (
                    <p>
                      <strong>Review:</strong> {review.description}
                    </p>
                  )}
                  {review.rating && (
                    <p>
                      <strong>Rating:</strong> {review.rating}
                    </p>
                  )}
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
