import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  Book,
  Plus,
  Star,
  MessageCircle,
  Search,
  Calendar,
  User,
  BookOpen,
  ChevronDown,
  ChevronUp,
} from "lucide-react";

// API Configuration
const API_BASE_URL = "http://127.0.0.1:8000";

// API Service
const api = {
  async getBooks(skip = 0, limit = 100) {
    const response = await fetch(
      `${API_BASE_URL}/books?skip=${skip}&limit=${limit}`,
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    if (!response.ok) throw new Error("Failed to fetch books");
    return response.json();
  },

  async createBook(bookData) {
    const response = await fetch(`${API_BASE_URL}/books`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(bookData),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Failed to create book");
    }

    return response.json();
  },

  async getBookReviews(bookId, skip = 0, limit = 100) {
    const response = await fetch(
      `${API_BASE_URL}/books/${bookId}/reviews?skip=${skip}&limit=${limit}`
    );
    if (!response.ok) throw new Error("Failed to fetch reviews");
    return response.json();
  },

  async createReview(bookId, reviewData) {
    const response = await fetch(`${API_BASE_URL}/books/${bookId}/reviews`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(reviewData),
    });
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Failed to create review");
    }
    return response.json();
  },
};

// Star Rating Component
const StarRating = ({
  rating,
  size = "sm",
  interactive = false,
  onRatingChange,
}) => {
  const [hoverRating, setHoverRating] = useState(0);
  const sizeClasses = {
    sm: "w-4 h-4",
    md: "w-5 h-5",
    lg: "w-6 h-6",
  };

  const handleClick = (value) => {
    if (interactive && onRatingChange) {
      onRatingChange(value);
    }
  };

  return (
    <div className="flex items-center space-x-1">
      {[1, 2, 3, 4, 5].map((star) => (
        <Star
          key={star}
          className={`${sizeClasses[size]} ${
            star <= (hoverRating || rating)
              ? "fill-yellow-400 text-yellow-400"
              : "text-gray-300"
          } ${
            interactive
              ? "cursor-pointer hover:scale-110 transition-transform"
              : ""
          }`}
          onClick={() => handleClick(star)}
          onMouseEnter={() => interactive && setHoverRating(star)}
          onMouseLeave={() => interactive && setHoverRating(0)}
        />
      ))}
      <span className="ml-2 text-sm text-gray-600">
        {rating ? rating.toFixed(1) : "0.0"}
      </span>
    </div>
  );
};

// Book Card Component
const BookCard = ({ book, onViewReviews, onAddReview }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className="bg-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-100 hover:border-blue-200">
      <div className="p-6">
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <h3 className="text-xl font-bold text-gray-900 mb-2 line-clamp-2">
              {book.title}
            </h3>
            <p className="text-gray-600 font-medium mb-1">by {book.author}</p>
            {book.published_year && (
              <div className="flex items-center text-sm text-gray-500 mb-2">
                <Calendar className="w-4 h-4 mr-1" />
                {book.published_year}
              </div>
            )}
            {book.isbn && (
              <p className="text-sm text-gray-500">ISBN: {book.isbn}</p>
            )}
          </div>
          <div className="bg-gradient-to-br from-blue-50 to-purple-50 p-3 rounded-lg">
            <BookOpen className="w-8 h-8 text-blue-600" />
          </div>
        </div>

        {book.description && (
          <div className="mb-4">
            <p
              className={`text-gray-700 leading-relaxed ${
                !isExpanded ? "line-clamp-3" : ""
              }`}
            >
              {book.description}
            </p>
            {book.description.length > 150 && (
              <button
                onClick={() => setIsExpanded(!isExpanded)}
                className="text-blue-600 hover:text-blue-800 text-sm mt-1 flex items-center"
              >
                {isExpanded ? (
                  <>
                    Show less <ChevronUp className="w-4 h-4 ml-1" />
                  </>
                ) : (
                  <>
                    Show more <ChevronDown className="w-4 h-4 ml-1" />
                  </>
                )}
              </button>
            )}
          </div>
        )}

        <div className="flex items-center justify-between pt-4 border-t border-gray-100">
          <button
            onClick={() => onViewReviews(book)}
            className="flex items-center space-x-2 px-4 py-2 text-blue-600 hover:text-blue-800 hover:bg-blue-50 rounded-lg transition-colors"
          >
            <MessageCircle className="w-4 h-4" />
            <span>View Reviews</span>
          </button>
          <button
            onClick={() => onAddReview(book)}
            className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white hover:bg-blue-700 rounded-lg transition-colors"
          >
            <Plus className="w-4 h-4" />
            <span>Add Review</span>
          </button>
        </div>
      </div>
    </div>
  );
};

// Review Card Component
const ReviewCard = ({ review }) => {
  return (
    <div className="bg-white rounded-lg border border-gray-200 p-4 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-gradient-to-br from-purple-400 to-pink-400 rounded-full flex items-center justify-center">
            <User className="w-5 h-5 text-white" />
          </div>
          <div>
            <h4 className="font-semibold text-gray-900">
              {review.reviewer_name}
            </h4>
            <p className="text-sm text-gray-500">
              {new Date(review.created_at).toLocaleDateString()}
            </p>
          </div>
        </div>
        <StarRating rating={review.rating} size="sm" />
      </div>
      {review.comment && (
        <p className="text-gray-700 leading-relaxed">{review.comment}</p>
      )}
    </div>
  );
};

// Add Book Modal
const AddBookModal = ({ isOpen, onClose, onSubmit, loading }) => {
  const [formData, setFormData] = useState({
    title: "",
    author: "",
    isbn: "",
    description: "",
    published_year: "",
  });
  const [errors, setErrors] = useState({});

  const handleSubmit = (e) => {
    e.preventDefault();
    const newErrors = {};

    if (!formData.title.trim()) newErrors.title = "Title is required";
    if (!formData.author.trim()) newErrors.author = "Author is required";
    if (
      formData.isbn &&
      !/^\d{10}(\d{3})?$/.test(formData.isbn.replace(/-/g, ""))
    ) {
      newErrors.isbn = "Invalid ISBN format";
    }
    if (
      formData.published_year &&
      (formData.published_year < 1000 ||
        formData.published_year > new Date().getFullYear())
    ) {
      newErrors.published_year = "Invalid year";
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    const submitData = { ...formData };
    if (submitData.published_year)
      submitData.published_year = parseInt(submitData.published_year);
    if (!submitData.isbn.trim()) delete submitData.isbn;
    if (!submitData.description.trim()) delete submitData.description;

    onSubmit(submitData);
  };

  const handleClose = () => {
    setFormData({
      title: "",
      author: "",
      isbn: "",
      description: "",
      published_year: "",
    });
    setErrors({});
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-xl max-w-md w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-900">Add New Book</h2>
            <button
              onClick={handleClose}
              className="text-gray-400 hover:text-gray-600 transition-colors"
            >
              ✕
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Title *
              </label>
              <input
                type="text"
                value={formData.title}
                onChange={(e) =>
                  setFormData({ ...formData, title: e.target.value })
                }
                className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                  errors.title ? "border-red-500" : "border-gray-300"
                }`}
                placeholder="Enter book title"
              />
              {errors.title && (
                <p className="text-red-500 text-sm mt-1">{errors.title}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Author *
              </label>
              <input
                type="text"
                value={formData.author}
                onChange={(e) =>
                  setFormData({ ...formData, author: e.target.value })
                }
                className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                  errors.author ? "border-red-500" : "border-gray-300"
                }`}
                placeholder="Enter author name"
              />
              {errors.author && (
                <p className="text-red-500 text-sm mt-1">{errors.author}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                ISBN
              </label>
              <input
                type="text"
                value={formData.isbn}
                onChange={(e) =>
                  setFormData({ ...formData, isbn: e.target.value })
                }
                className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                  errors.isbn ? "border-red-500" : "border-gray-300"
                }`}
                placeholder="Enter ISBN (optional)"
              />
              {errors.isbn && (
                <p className="text-red-500 text-sm mt-1">{errors.isbn}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Published Year
              </label>
              <input
                type="number"
                value={formData.published_year}
                onChange={(e) =>
                  setFormData({ ...formData, published_year: e.target.value })
                }
                className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                  errors.published_year ? "border-red-500" : "border-gray-300"
                }`}
                placeholder="Enter publication year (optional)"
              />
              {errors.published_year && (
                <p className="text-red-500 text-sm mt-1">
                  {errors.published_year}
                </p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Description
              </label>
              <textarea
                value={formData.description}
                onChange={(e) =>
                  setFormData({ ...formData, description: e.target.value })
                }
                rows={3}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter book description (optional)"
              />
            </div>

            <div className="flex space-x-3 pt-4">
              <button
                type="button"
                onClick={handleClose}
                className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={loading}
                className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
              >
                {loading ? "Adding..." : "Add Book"}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

// Add Review Modal
const AddReviewModal = ({ isOpen, onClose, onSubmit, book, loading }) => {
  const [formData, setFormData] = useState({
    reviewer_name: "",
    rating: 0,
    comment: "",
  });
  const [errors, setErrors] = useState({});

  const handleSubmit = (e) => {
    e.preventDefault();
    const newErrors = {};

    if (!formData.reviewer_name.trim())
      newErrors.reviewer_name = "Reviewer name is required";
    if (formData.rating < 1 || formData.rating > 5)
      newErrors.rating = "Rating must be between 1 and 5";

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    const submitData = { ...formData };
    if (!submitData.comment.trim()) delete submitData.comment;

    onSubmit(submitData);
  };

  const handleClose = () => {
    setFormData({ reviewer_name: "", rating: 0, comment: "" });
    setErrors({});
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-xl max-w-md w-full">
        <div className="p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-900">Add Review</h2>
            <button
              onClick={handleClose}
              className="text-gray-400 hover:text-gray-600 transition-colors"
            >
              ✕
            </button>
          </div>

          {book && (
            <div className="bg-gray-50 rounded-lg p-3 mb-6">
              <h3 className="font-semibold text-gray-900">{book.title}</h3>
              <p className="text-sm text-gray-600">by {book.author}</p>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Your Name *
              </label>
              <input
                type="text"
                value={formData.reviewer_name}
                onChange={(e) =>
                  setFormData({ ...formData, reviewer_name: e.target.value })
                }
                className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                  errors.reviewer_name ? "border-red-500" : "border-gray-300"
                }`}
                placeholder="Enter your name"
              />
              {errors.reviewer_name && (
                <p className="text-red-500 text-sm mt-1">
                  {errors.reviewer_name}
                </p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Rating *
              </label>
              <StarRating
                rating={formData.rating}
                size="lg"
                interactive={true}
                onRatingChange={(rating) =>
                  setFormData({ ...formData, rating })
                }
              />
              {errors.rating && (
                <p className="text-red-500 text-sm mt-1">{errors.rating}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Comment
              </label>
              <textarea
                value={formData.comment}
                onChange={(e) =>
                  setFormData({ ...formData, comment: e.target.value })
                }
                rows={4}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Share your thoughts about this book (optional)"
              />
            </div>

            <div className="flex space-x-3 pt-4">
              <button
                type="button"
                onClick={handleClose}
                className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={loading}
                className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
              >
                {loading ? "Submitting..." : "Submit Review"}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

// Reviews Modal
const ReviewsModal = ({
  isOpen,
  onClose,
  book,
  reviews,
  loading,
  onLoadMore,
  hasMore,
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-xl max-w-2xl w-full max-h-[80vh] flex flex-col">
        <div className="p-6 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold text-gray-900">
                {book?.title}
              </h2>
              <p className="text-gray-600">Reviews</p>
            </div>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 transition-colors"
            >
              ✕
            </button>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-6">
          {loading ? (
            <div className="flex items-center justify-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            </div>
          ) : reviews.length === 0 ? (
            <div className="text-center py-8">
              <MessageCircle className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <p className="text-gray-500">No reviews yet for this book.</p>
            </div>
          ) : (
            <div className="space-y-4">
              {reviews.map((review) => (
                <ReviewCard key={review.id} review={review} />
              ))}
              {hasMore && (
                <div className="text-center pt-4">
                  <button
                    onClick={onLoadMore}
                    className="px-4 py-2 text-blue-600 hover:text-blue-800 hover:bg-blue-50 rounded-lg transition-colors"
                  >
                    Load More Reviews
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

// Main App Component
const App = () => {
  console.log(
    "App component is rendering! Current path:",
    window.location.pathname
  );
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [showAddBookModal, setShowAddBookModal] = useState(false);
  const [showAddReviewModal, setShowAddReviewModal] = useState(false);
  const [showReviewsModal, setShowReviewsModal] = useState(false);
  const [selectedBook, setSelectedBook] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [reviewsLoading, setReviewsLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [user, setUser] = useState(() => {
    const token = localStorage.getItem("token");
    const userData = localStorage.getItem("user");
    console.log("localStorage user data:", userData);
    console.log("parsed user data:", userData ? JSON.parse(userData) : null);
    return token && userData ? JSON.parse(userData) : null;
  });

  const [success, setSuccess] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    console.log("Component mounted, loading books...");
    loadBooks();
  }, []);
  const loadBooks = async () => {
    try {
      setLoading(true);
      console.log("Starting to load books...");
      console.log("API URL:", `${API_BASE_URL}/books`);

      const response = await fetch(`${API_BASE_URL}/books`);
      console.log("Response status:", response.status);
      console.log("Response ok:", response.ok);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log("Books data:", data);
      setBooks(data);
      setError("");
    } catch (err) {
  console.error("Full error:", err);
  console.error("Error name:", err.name);
  console.error("Error message:", err.message);
  let errorMessage = "Failed to load books";
  if (err.message) {
    errorMessage = `Failed to load books: ${err.message}`;
  }
  setError(errorMessage);
} finally {
      setLoading(false);
    }
  };

  const handleAddBook = async (bookData) => {
    try {
      setSubmitting(true);
      const newBook = await api.createBook(bookData);
      setBooks([newBook, ...books]);
      setShowAddBookModal(false);
      setSuccess("Book added successfully!");
      setTimeout(() => setSuccess(""), 3000);
    } catch (err) {
  console.log("Setting error:", err);
  let errorMessage = "An error occurred";
  if (typeof err === 'string') {
    errorMessage = err;
  } else if (err.message) {
    errorMessage = err.message;
  } else if (err.detail) {
    errorMessage = err.detail;
  }
  setError(errorMessage);
  setTimeout(() => setError(""), 5000);
} finally {
  setSubmitting(false);
}
  };

  const handleViewReviews = async (book) => {
    setSelectedBook(book);
    setShowReviewsModal(true);
    setReviewsLoading(true);

    try {
      const reviewsData = await api.getBookReviews(book.id);
      setReviews(reviewsData);
    } catch (err) {
  setError("Failed to load reviews");
  setTimeout(() => setError(""), 3000);
} finally {
      setReviewsLoading(false);
    }
  };

  const handleAddReview = (book) => {
    setSelectedBook(book);
    setShowAddReviewModal(true);
  };

  const handleSubmitReview = async (reviewData) => {
    try {
      setSubmitting(true);
      await api.createReview(selectedBook.id, reviewData);
      setShowAddReviewModal(false);
      setSuccess("Review added successfully!");
      setTimeout(() => setSuccess(""), 3000);

      // Refresh reviews if reviews modal is open
      if (showReviewsModal) {
        const reviewsData = await api.getBookReviews(selectedBook.id);
        setReviews(reviewsData);
      }
    } catch (err) {
  let errorMessage = "Failed to submit review";
  if (typeof err === 'string') {
    errorMessage = err;
  } else if (err.message) {
    errorMessage = err.message;
  } else if (err.detail) {
    errorMessage = err.detail;
  }
  setError(errorMessage);
  setTimeout(() => setError(""), 5000);
} finally {
      setSubmitting(false);
    }
  };

  // Filter books based on search term
  const filteredBooks = books.filter(
    (book) =>
      book.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      book.author.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <div className="bg-gradient-to-br from-blue-600 to-purple-600 p-2 rounded-lg">
                <Book className="w-6 h-6 text-white" />
              </div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                BOOKIFY
              </h1>
            </div>

            {/* Authenticated Controls */}
            <div className="flex items-center space-x-4">
              {localStorage.getItem("token") ? (
                // Show logged in user controls
                <>
                  <span className="text-sm text-gray-700">
                    Welcome, {user?.username || "User"}
                  </span>
                  <button
                    onClick={() => setShowAddBookModal(true)}
                    className="inline-flex items-center space-x-2 px-4 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all duration-200 shadow-md hover:shadow-lg"
                  >
                    <Plus className="w-5 h-5" />
                    <span>Add Book</span>
                  </button>
                  <button
                    onClick={() => {
                      localStorage.removeItem("user");
                      localStorage.removeItem("token");
                      setUser(null);
                      window.location.reload(); // Force reload to update state
                    }}
                    className="inline-flex items-center space-x-2 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-100 transition"
                  >
                    <User className="w-4 h-4" />
                    <span>Logout</span>
                  </button>
                </>
              ) : (
                // Show login button
                <button onClick={() => navigate("/login")}>Login</button>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Notifications */}
      {error && (
  <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-4">
    <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
      {typeof error === 'string' ? error : 'An error occurred'}
    </div>
  </div>
)}

      {success && (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-4">
          <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg">
            {success}
          </div>
        </div>
      )}

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Search Bar */}
        <div className="mb-8">
          <div className="relative max-w-md">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Search books by title or author..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent shadow-sm"
            />
          </div>
        </div>

        {/* Books Grid */}
        {loading ? (
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            <span className="ml-3 text-gray-600">Loading books...</span>
          </div>
        ) : filteredBooks.length === 0 ? (
          <div className="text-center py-12">
            <BookOpen className="w-24 h-24 text-gray-300 mx-auto mb-6" />
            <h3 className="text-xl font-semibold text-gray-600 mb-2">
              {searchTerm ? "No books found" : "No books available"}
            </h3>
            <p className="text-gray-500 mb-6">
              {searchTerm
                ? "Try adjusting your search terms"
                : "Start building your library by adding the first book!"}
            </p>
            {!searchTerm && (
              <button
                onClick={() => setShowAddBookModal(true)}
                className="inline-flex items-center space-x-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                <Plus className="w-5 h-5" />
                <span>Add Your First Book</span>
              </button>
            )}
          </div>
        ) : (
          <>
            <div className="mb-6">
              <h2 className="text-lg font-semibold text-gray-900">
                {searchTerm
                  ? `Found ${filteredBooks.length} book(s)`
                  : `${filteredBooks.length} Book(s) in Library`}
              </h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredBooks.map((book) => (
                <BookCard
                  key={book.id}
                  book={book}
                  onViewReviews={handleViewReviews}
                  onAddReview={handleAddReview}
                />
              ))}
            </div>
          </>
        )}
      </main>

      {/* Modals */}
      <AddBookModal
        isOpen={showAddBookModal}
        onClose={() => setShowAddBookModal(false)}
        onSubmit={handleAddBook}
        loading={submitting}
      />

      <AddReviewModal
        isOpen={showAddReviewModal}
        onClose={() => setShowAddReviewModal(false)}
        onSubmit={handleSubmitReview}
        book={selectedBook}
        loading={submitting}
      />

      <ReviewsModal
        isOpen={showReviewsModal}
        onClose={() => setShowReviewsModal(false)}
        book={selectedBook}
        reviews={reviews}
        loading={reviewsLoading}
        onLoadMore={async () => {
          try {
            const nextReviews = await api.getBookReviews(
              selectedBook.id,
              reviews.length
            );
            setReviews([...reviews, ...nextReviews]);
          } catch (err) {
  let errorMessage = "Failed to load more reviews";
  if (typeof err === 'string') {
    errorMessage = err;
  } else if (err.message) {
    errorMessage = err.message;
  }
  console.log("Setting error:", errorMessage);
  setError(errorMessage);
  setTimeout(() => setError(""), 3000);
}
        }}
        hasMore={reviews.length % 100 === 0 && reviews.length !== 0}
      />
    </div>
  );
};

export default App;
