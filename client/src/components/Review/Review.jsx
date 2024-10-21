import React, { useState, useEffect } from 'react';
import NavBar from '../NavBar/NavBar';
import './Review.css';
import logo from '../pictures/SAFIRI LOGO.png';
import Footer from '../Footer/Footer';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';

function Review({ user }) {
  const [reviews, setReviews] = useState([]);

  // 1. Fetch existing reviews from the Flask server on component mount
  useEffect(() => {
    const fetchReviews = async () => {
      try {
        const response = await fetch('/reviews');
        if (!response.ok) throw new Error('Failed to fetch reviews');
        const data = await response.json();
        setReviews(data);
        console.log(data);
        // console.log(user);
      } catch (error) {
        console.error('Error fetching reviews:', error);
      }
    };
    fetchReviews();
  }, [user]);

  // 2. Define Yup validation schema with required fields and data type validation
  const validationSchema = Yup.object().shape({
    userId: Yup.number().required('User ID is required'),
    siteId: Yup.number().required('Site ID is required'),
    reviewText: Yup.string().required('Review is required'),
    rating: Yup.number().required('Rating is required'),
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

      if (!response.ok) {
        throw new Error('Failed to submit review');
      }

      // If submission is successful, update the reviews state
      const newReview = await response.json();
      setReviews((prevReviews) => [...prevReviews, newReview]);

      // Reset the form after successful submission
      resetForm();
      alert('Review submitted successfully!');
    } catch (error) {
      console.error('Error submitting review:', error);
      alert('There was an error submitting your review.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div id="review-page">
      <NavBar user={user} />
      <img src={logo} alt="safiri-logo" id="safiri-logo" />
      <h1>Review</h1>
      <div className="review-container">
        <div className="form-container">
          <h2>Submit Your Review</h2>

          {/*Formik to manage the form */}
          <Formik
            initialValues={{
              siteId: '',
              review: '',
              rating: '',
            }}
            validationSchema={validationSchema}
            onSubmit={handleSubmit}
          >
            {({ values, setFieldValue, isSubmitting }) => (
              <Form>
                {/* User-ID Field */}
                <div className="form-group">
                  <label htmlFor="userId">User ID:</label>
                  <Field type="text" id="userId" name="userId" />
                  <ErrorMessage
                    name="userId"
                    component="div"
                    className="error"
                  />
                </div>

                {/* Place Field */}
                <div className="form-group">
                  <label htmlFor="siteId">Site ID:</label>
                  <Field type="text" id="siteId" name="siteId" />
                  <ErrorMessage
                    name="siteId"
                    component="div"
                    className="error"
                  />
                </div>

                {/* Review Text */}
                <div className="form-group">
                  <label htmlFor="reviewText">Review:</label>
                  <Field as="textarea" id="reviewText" name="reviewText" />
                  <ErrorMessage
                    name="reviewText"
                    component="div"
                    className="error"
                  />
                </div>

                {/* Rating Field */}
                <div className="form-group">
                  <label>How was your experience?</label>
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
                  <ErrorMessage
                    name="rating"
                    component="div"
                    className="error"
                  />
                </div>

                {/* Submit Button */}
                <button
                  type="submit"
                  disabled={isSubmitting}
                  id="submit-review-button"
                >
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
                  {review.user && (
                    <div className="review-user">
                      <img
                        src={
                          review.user.profile ? review.user.profile.image : ''
                        }
                        alt={`${review.user.username}'s review`}
                      />
                      <h3>Username: {review.user.username}</h3>
                      <h5>Created At: {review.created_at}</h5>
                      {review.updated_at !== review.created_at ? (
                        <h5>Updated At: {review.updated_at}</h5>
                      ) : (
                        <></>
                      )}
                    </div>
                  )}
                  <p>
                    <strong>Site: </strong> {review.site.name}
                  </p>
                  <p>{review.description}</p>
                  <p>{'☆'.repeat(review.rating)}</p>
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
}

export default Review;
