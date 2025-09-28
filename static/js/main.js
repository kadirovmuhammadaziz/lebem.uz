// Main JavaScript file for Django Reviews App

// Utility Functions
function formatPrice(price) {
  return new Intl.NumberFormat("uz-UZ").format(price)
}

function formatDate(dateString) {
  const date = new Date(dateString)
  return date.toLocaleDateString("uz-UZ", {
    year: "numeric",
    month: "long",
    day: "numeric",
  })
}

function generateStars(rating) {
  const fullStars = Math.floor(rating)
  const hasHalfStar = rating % 1 !== 0
  const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0)

  let starsHtml = ""

  // Full stars
  for (let i = 0; i < fullStars; i++) {
    starsHtml += '<i class="fas fa-star"></i>'
  }

  // Half star
  if (hasHalfStar) {
    starsHtml += '<i class="fas fa-star-half-alt"></i>'
  }

  // Empty stars
  for (let i = 0; i < emptyStars; i++) {
    starsHtml += '<i class="far fa-star"></i>'
  }

  return starsHtml
}

function debounce(func, wait) {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

function getCookie(name) {
  let cookieValue = null
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";")
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}

function showAlert(message, type = "info") {
  // Remove existing alerts
  const existingAlerts = document.querySelectorAll(".custom-alert")
  existingAlerts.forEach((alert) => alert.remove())

  // Create new alert
  const alertDiv = document.createElement("div")
  alertDiv.className = `alert alert-${type} alert-dismissible fade show custom-alert position-fixed`
  alertDiv.style.cssText = "top: 20px; right: 20px; z-index: 9999; min-width: 300px;"
  alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `

  document.body.appendChild(alertDiv)

  // Auto remove after 5 seconds
  setTimeout(() => {
    if (alertDiv.parentNode) {
      alertDiv.remove()
    }
  }, 5000)
}

// Phone number formatting
function formatPhoneNumber(input) {
  let value = input.value.replace(/\D/g, "")

  if (value.startsWith("998")) {
    value = value.substring(3)
  }

  if (value.length >= 9) {
    value = value.substring(0, 9)
    value = `+998 ${value.substring(0, 2)} ${value.substring(2, 5)} ${value.substring(5, 7)} ${value.substring(7, 9)}`
  } else if (value.length >= 7) {
    value = `+998 ${value.substring(0, 2)} ${value.substring(2, 5)} ${value.substring(5, 7)}`
  } else if (value.length >= 5) {
    value = `+998 ${value.substring(0, 2)} ${value.substring(2, 5)}`
  } else if (value.length >= 2) {
    value = `+998 ${value.substring(0, 2)}`
  } else if (value.length > 0) {
    value = `+998 ${value}`
  }

  input.value = value
}

// Initialize phone formatting on all phone inputs
document.addEventListener("DOMContentLoaded", () => {
  const phoneInputs = document.querySelectorAll('input[type="tel"]')
  phoneInputs.forEach((input) => {
    input.addEventListener("input", function () {
      formatPhoneNumber(this)
    })

    input.addEventListener("focus", function () {
      if (!this.value) {
        this.value = "+998 "
      }
    })
  })

  // Initialize tooltips
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  tooltipTriggerList.map((tooltipTriggerEl) => new window.bootstrap.Tooltip(tooltipTriggerEl))

  // Add fade-in animation to cards
  const cards = document.querySelectorAll(".card")
  cards.forEach((card, index) => {
    setTimeout(() => {
      card.classList.add("fade-in")
    }, index * 100)
  })
})

// Form validation enhancement
;(() => {
  window.addEventListener(
    "load",
    () => {
      const forms = document.getElementsByClassName("needs-validation")
      Array.prototype.filter.call(forms, (form) => {
        form.addEventListener(
          "submit",
          (event) => {
            if (form.checkValidity() === false) {
              event.preventDefault()
              event.stopPropagation()

              // Focus on first invalid field
              const firstInvalid = form.querySelector(":invalid")
              if (firstInvalid) {
                firstInvalid.focus()
              }
            }
            form.classList.add("was-validated")
          },
          false,
        )
      })
    },
    false,
  )
})()

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    e.preventDefault()
    const target = document.querySelector(this.getAttribute("href"))
    if (target) {
      target.scrollIntoView({
        behavior: "smooth",
        block: "start",
      })
    }
  })
})

// Back to top button
const backToTopButton = document.createElement("button")
backToTopButton.innerHTML = '<i class="fas fa-arrow-up"></i>'
backToTopButton.className = "btn btn-primary position-fixed"
backToTopButton.style.cssText =
  "bottom: 20px; right: 20px; z-index: 999; border-radius: 50%; width: 50px; height: 50px; display: none;"
backToTopButton.setAttribute("title", "Yuqoriga")

document.body.appendChild(backToTopButton)

window.addEventListener("scroll", () => {
  if (window.pageYOffset > 300) {
    backToTopButton.style.display = "block"
  } else {
    backToTopButton.style.display = "none"
  }
})

backToTopButton.addEventListener("click", () => {
  window.scrollTo({
    top: 0,
    behavior: "smooth",
  })
})

// Loading states for buttons
function setButtonLoading(button, loading = true) {
  if (loading) {
    button.disabled = true
    button.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Yuklanmoqda...'
  } else {
    button.disabled = false
    // Restore original text (you might want to store this)
    button.innerHTML = button.getAttribute("data-original-text") || "Yuborish"
  }
}

// Image lazy loading fallback
document.addEventListener("DOMContentLoaded", () => {
  const images = document.querySelectorAll("img")
  images.forEach((img) => {
    img.addEventListener("error", function () {
      this.src = "/static/images/no-image.jpg"
    })
  })
})

// Search functionality (if needed)
function initializeSearch() {
  const searchInput = document.getElementById("search-input")
  if (searchInput) {
    searchInput.addEventListener(
      "input",
      debounce(function () {
        const query = this.value.trim()
        if (query.length >= 3) {
          performSearch(query)
        }
      }, 300),
    )
  }
}

async function performSearch(query) {
  try {
    const response = await fetch(`/api/products/products/search/?search=${encodeURIComponent(query)}`)
    const results = await response.json()
    displaySearchResults(results)
  } catch (error) {
    console.error("Qidiruv xatoligi:", error)
  }
}

function displaySearchResults(results) {
  // Implement search results display
  console.log("Search results:", results)
}

// API configuration and endpoints
const API_BASE_URL = "/api"
const API_ENDPOINTS = {
  categories: `${API_BASE_URL}/products/categories/`,
  products: `${API_BASE_URL}/products/products/`,
  featuredProducts: `${API_BASE_URL}/products/products/featured/`,
  productDetail: (slug) => `${API_BASE_URL}/products/products/${slug}/`,
  categoryProducts: (slug) => `${API_BASE_URL}/products/categories/${slug}/products/`,
  productReviews: (slug) => `${API_ENDPOINTS.products}${slug}/reviews/`,
  reviewStats: (slug) => `${API_ENDPOINTS.products}${slug}/reviews/stats/`,
  createReview: `${API_BASE_URL}/reviews/create/`,
  createContact: `${API_BASE_URL}/reviews/contact/`,
}

// Global state management
let currentPage = "home"
let currentProduct = null
let currentCategory = null

// API utility functions
async function apiCall(url, options = {}) {
  const defaultOptions = {
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
  }

  const config = { ...defaultOptions, ...options }

  try {
    const response = await fetch(url, config)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    return await response.json()
  } catch (error) {
    console.error("API call failed:", error)
    throw error
  }
}

// Page loading functions
async function loadHomePage() {
  currentPage = "home"
  showLoading()

  try {
    const mainContent = document.getElementById("main-content")
    mainContent.innerHTML = await fetch("/templates/index.html").then((r) => r.text())

    await loadCategories()
    await loadFeaturedProducts()

    hideLoading()
  } catch (error) {
    console.error("Error loading home page:", error)
    showAlert("Sahifani yuklashda xatolik yuz berdi", "danger")
    hideLoading()
  }
}

async function loadCategories() {
  try {
    const categories = await apiCall(API_ENDPOINTS.categories)
    displayCategories(categories)
  } catch (error) {
    console.error("Error loading categories:", error)
    showAlert("Kategoriyalarni yuklashda xatolik yuz berdi", "danger")
  }
}

function displayCategories(categories) {
  const container = document.getElementById("categories-container")
  if (!container) return

  if (categories.length === 0) {
    container.innerHTML = '<div class="col-12 text-center"><p class="text-muted">Kategoriyalar topilmadi</p></div>'
    return
  }

  container.innerHTML = categories
    .map(
      (category) => `
        <div class="col-lg-3 col-md-4 col-sm-6 mb-4">
            <div class="card hover-card category-card h-100" onclick="loadCategoryProducts('${category.slug}')">
                <div class="card-body text-center">
                    <div class="category-icon mb-3">
                        <i class="fas fa-box fa-3x text-primary"></i>
                    </div>
                    <h5 class="card-title">${category.name}</h5>
                    <p class="card-text text-muted">${category.description || "Kategoriya tavsifi"}</p>
                    <small class="text-muted">
                        <i class="fas fa-cube me-1"></i>
                        ${category.products_count || 0} ta mahsulot
                    </small>
                </div>
            </div>
        </div>
    `,
    )
    .join("")
}

async function loadFeaturedProducts() {
  try {
    const products = await apiCall(API_ENDPOINTS.featuredProducts)
    displayFeaturedProducts(products)
  } catch (error) {
    console.error("Error loading featured products:", error)
    showAlert("Tanlangan mahsulotlarni yuklashda xatolik yuz berdi", "danger")
  }
}

function displayFeaturedProducts(products) {
  const container = document.getElementById("featured-products-container")
  if (!container) return

  if (products.length === 0) {
    container.innerHTML =
      '<div class="col-12 text-center"><p class="text-muted">Tanlangan mahsulotlar topilmadi</p></div>'
    return
  }

  container.innerHTML = products
    .slice(0, 8)
    .map(
      (product) => `
        <div class="col-lg-3 col-md-4 col-sm-6 mb-4">
            <div class="card hover-card product-card h-100" onclick="loadProductDetail('${product.slug}')">
                <div class="card-img-container">
                    <img src="${product.image || "/static/images/no-image.jpg"}"
                         class="card-img-top" alt="${product.name}">
                </div>
                <div class="card-body">
                    <h6 class="card-title">${product.name}</h6>
                    <div class="rating mb-2">
                        ${generateStars(product.rating || 0)}
                        <small class="text-muted ms-1">(${product.reviews_count || 0})</small>
                    </div>
                    <div class="price-section">
                        <span class="price fw-bold">${formatPrice(product.price)} so'm</span>
                        ${
                          product.old_price && product.old_price > product.price
                            ? `<small class="old-price text-muted text-decoration-line-through ms-2">${formatPrice(product.old_price)} so'm</small>`
                            : ""
                        }
                    </div>
                </div>
            </div>
        </div>
    `,
    )
    .join("")
}

async function loadCategoryProducts(categorySlug) {
  currentPage = "category"
  currentCategory = categorySlug
  showLoading()

  try {
    const mainContent = document.getElementById("main-content")
    mainContent.innerHTML = await fetch("/templates/category_products.html").then((r) => r.text())

    const [categoryData, products] = await Promise.all([
      apiCall(`${API_ENDPOINTS.categories}${categorySlug}/`),
      apiCall(API_ENDPOINTS.categoryProducts(categorySlug)),
    ])

    displayCategoryInfo(categoryData)
    displayCategoryProducts(products)

    hideLoading()
  } catch (error) {
    console.error("Error loading category products:", error)
    showAlert("Kategoriya mahsulotlarini yuklashda xatolik yuz berdi", "danger")
    hideLoading()
  }
}

function displayCategoryInfo(category) {
  document.getElementById("category-name").textContent = category.name
  document.getElementById("category-title").textContent = `${category.name} Mahsulotlari`
  document.getElementById("category-description").textContent = category.description || "Kategoriya tavsifi"
}

function displayCategoryProducts(products) {
  const container = document.getElementById("products-container")
  const countElement = document.getElementById("products-count")
  const noProductsElement = document.getElementById("no-products")

  if (countElement) {
    countElement.textContent = `${products.length} ta mahsulot topildi`
  }

  if (products.length === 0) {
    container.innerHTML = ""
    if (noProductsElement) {
      noProductsElement.style.display = "block"
    }
    return
  }

  if (noProductsElement) {
    noProductsElement.style.display = "none"
  }

  container.innerHTML = products
    .map(
      (product) => `
        <div class="col-lg-4 col-md-6 mb-4">
            <div class="card hover-card product-card h-100" onclick="loadProductDetail('${product.slug}')">
                <div class="card-img-container">
                    <img src="${product.image || "/static/images/no-image.jpg"}"
                         class="card-img-top" alt="${product.name}">
                </div>
                <div class="card-body">
                    <h5 class="card-title">${product.name}</h5>
                    <p class="card-text text-muted">${product.short_description || product.description?.substring(0, 100) + "..." || ""}</p>
                    <div class="rating mb-2">
                        ${generateStars(product.rating || 0)}
                        <small class="text-muted ms-1">(${product.reviews_count || 0})</small>
                    </div>
                    <div class="price-section">
                        <span class="price fw-bold">${formatPrice(product.price)} so'm</span>
                        ${
                          product.old_price && product.old_price > product.price
                            ? `<small class="old-price text-muted text-decoration-line-through ms-2">${formatPrice(product.old_price)} so'm</small>`
                            : ""
                        }
                    </div>
                    <small class="text-muted">
                        <i class="fas fa-eye me-1"></i>${product.views_count || 0} marta ko'rilgan
                    </small>
                </div>
            </div>
        </div>
    `,
    )
    .join("")
}

async function loadProductDetail(productSlug) {
  currentPage = "product"
  currentProduct = productSlug
  showLoading()

  try {
    const mainContent = document.getElementById("main-content")
    mainContent.innerHTML = await fetch("/templates/product_detail.html").then((r) => r.text())

    const [product, reviews, stats] = await Promise.all([
      apiCall(API_ENDPOINTS.productDetail(productSlug)),
      apiCall(API_ENDPOINTS.productReviews(productSlug)),
      apiCall(API_ENDPOINTS.reviewStats(productSlug)),
    ])

    displayProductDetail(product)
    displayProductReviews(reviews, stats)
    initializeReviewForm(productSlug)

    hideLoading()
  } catch (error) {
    console.error("Error loading product detail:", error)
    showAlert("Mahsulot ma'lumotlarini yuklashda xatolik yuz berdi", "danger")
    hideLoading()
  }
}

function displayProductDetail(product) {
  document.getElementById("product-name").textContent = product.name
  document.getElementById("product-description").textContent = product.description || "Mahsulot tavsifi mavjud emas"
  document.getElementById("product-price").textContent = `${formatPrice(product.price)} so'm`
  document.getElementById("product-views").textContent = product.views_count || 0
  document.getElementById("product-image").src = product.image || "/static/images/no-image.jpg"
  document.getElementById("product-breadcrumb").textContent = product.name

  // Update breadcrumb
  const categoryBreadcrumb = document.getElementById("category-breadcrumb")
  if (categoryBreadcrumb && product.category) {
    categoryBreadcrumb.textContent = product.category.name
    categoryBreadcrumb.dataset.slug = product.category.slug
  }

  // Handle old price
  const oldPriceElement = document.getElementById("product-old-price")
  if (product.old_price && product.old_price > product.price) {
    oldPriceElement.textContent = `${formatPrice(product.old_price)} so'm`
    oldPriceElement.style.display = "inline"
  }

  // Update rating
  const ratingStars = document.getElementById("product-rating-stars")
  const ratingText = document.getElementById("product-rating-text")
  if (ratingStars && ratingText) {
    ratingStars.innerHTML = generateStars(product.rating || 0)
    ratingText.textContent = `(${product.reviews_count || 0} sharh)`
  }
}

function displayProductReviews(reviews, stats) {
  const container = document.getElementById("reviews-container")
  const countElement = document.getElementById("reviews-count")

  if (countElement) {
    countElement.textContent = stats.total_reviews || 0
  }

  if (reviews.length === 0) {
    container.innerHTML = `
            <div class="text-center py-4">
                <i class="fas fa-comments fa-3x text-muted mb-3"></i>
                <h5 class="text-muted">Hali sharhlar yo'q</h5>
                <p class="text-muted">Birinchi bo'lib sharh qoldiring!</p>
            </div>
        `
    return
  }

  container.innerHTML = reviews
    .map(
      (review) => `
        <div class="review-item bg-white p-4 rounded mb-3 shadow-sm">
            <div class="d-flex justify-content-between align-items-start mb-2">
                <div>
                    <h6 class="mb-1">${review.name}</h6>
                    <div class="rating">
                        ${generateStars(review.rating)}
                    </div>
                </div>
                <small class="text-muted">${formatDate(review.created_at)}</small>
            </div>
            <p class="mb-0">${review.comment}</p>
        </div>
    `,
    )
    .join("")
}

function initializeReviewForm(productSlug) {
  const form = document.getElementById("review-form")
  const ratingInput = document.getElementById("rating-input")
  const ratingValue = document.getElementById("review-rating")

  // Initialize rating input
  if (ratingInput) {
    const stars = ratingInput.querySelectorAll(".fa-star")
    stars.forEach((star, index) => {
      star.addEventListener("click", () => {
        const rating = index + 1
        ratingValue.value = rating
        updateRatingDisplay(stars, rating)
      })

      star.addEventListener("mouseenter", () => {
        updateRatingDisplay(stars, index + 1)
      })
    })

    ratingInput.addEventListener("mouseleave", () => {
      updateRatingDisplay(stars, Number.parseInt(ratingValue.value))
    })
  }

  // Handle form submission
  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault()
      await submitReview(productSlug)
    })
  }
}

function updateRatingDisplay(stars, rating) {
  stars.forEach((star, index) => {
    if (index < rating) {
      star.classList.remove("far")
      star.classList.add("fas")
      star.style.color = "#ffc107"
    } else {
      star.classList.remove("fas")
      star.classList.add("far")
      star.style.color = "#dee2e6"
    }
  })
}

async function submitReview(productSlug) {
  const form = document.getElementById("review-form")
  const submitBtn = form.querySelector('button[type="submit"]')

  // Store original button text
  submitBtn.setAttribute("data-original-text", submitBtn.innerHTML)
  setButtonLoading(submitBtn, true)

  try {
    const formData = {
      product_slug: productSlug,
      name: document.getElementById("review-name").value,
      phone: document.getElementById("review-phone").value,
      rating: Number.parseInt(document.getElementById("review-rating").value),
      comment: document.getElementById("review-comment").value,
    }

    await apiCall(API_ENDPOINTS.createReview, {
      method: "POST",
      body: JSON.stringify(formData),
    })

    showAlert("Sharhingiz muvaffaqiyatli yuborildi!", "success")
    form.reset()
    document.getElementById("review-rating").value = "5"
    updateRatingDisplay(document.querySelectorAll("#rating-input .fa-star"), 5)

    // Reload reviews
    const [reviews, stats] = await Promise.all([
      apiCall(API_ENDPOINTS.productReviews(productSlug)),
      apiCall(API_ENDPOINTS.reviewStats(productSlug)),
    ])
    displayProductReviews(reviews, stats)
  } catch (error) {
    console.error("Error submitting review:", error)
    showAlert("Sharh yuborishda xatolik yuz berdi", "danger")
  } finally {
    setButtonLoading(submitBtn, false)
  }
}

async function loadContactPage() {
  currentPage = "contact"
  showLoading()

  try {
    const mainContent = document.getElementById("main-content")
    mainContent.innerHTML = await fetch("/templates/contact.html").then((r) => r.text())

    initializeContactForm()
    hideLoading()
  } catch (error) {
    console.error("Error loading contact page:", error)
    showAlert("Aloqa sahifasini yuklashda xatolik yuz berdi", "danger")
    hideLoading()
  }
}

function initializeContactForm() {
  const form = document.getElementById("contact-form")
  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault()
      await submitContactForm()
    })
  }
}

async function submitContactForm() {
  const form = document.getElementById("contact-form")
  const submitBtn = form.querySelector('button[type="submit"]')

  submitBtn.setAttribute("data-original-text", submitBtn.innerHTML)
  setButtonLoading(submitBtn, true)

  try {
    const formData = {
      name: document.getElementById("contact-name").value,
      phone: document.getElementById("contact-phone").value,
      email: document.getElementById("contact-email").value,
      subject: document.getElementById("contact-subject").value,
      message: document.getElementById("contact-message").value,
    }

    await apiCall(API_ENDPOINTS.createContact, {
      method: "POST",
      body: JSON.stringify(formData),
    })

    showAlert("Xabaringiz muvaffaqiyatli yuborildi!", "success")
    form.reset()
  } catch (error) {
    console.error("Error submitting contact form:", error)
    showAlert("Xabar yuborishda xatolik yuz berdi", "danger")
  } finally {
    setButtonLoading(submitBtn, false)
  }
}

function sortProducts() {
  const sortValue = document.getElementById("sort-select").value
  if (currentCategory) {
    loadCategoryProductsSorted(currentCategory, sortValue)
  }
}

async function loadCategoryProductsSorted(categorySlug, ordering) {
  try {
    const url = `${API_ENDPOINTS.categoryProducts(categorySlug)}?ordering=${ordering}`
    const products = await apiCall(url)
    displayCategoryProducts(products)
  } catch (error) {
    console.error("Error loading sorted products:", error)
    showAlert("Mahsulotlarni saralashda xatolik yuz berdi", "danger")
  }
}

// Loading state functions
function showLoading() {
  const spinner = document.getElementById("loading-spinner")
  if (spinner) {
    spinner.style.display = "block"
  }
}

function hideLoading() {
  const spinner = document.getElementById("loading-spinner")
  if (spinner) {
    spinner.style.display = "none"
  }
}

document.addEventListener("DOMContentLoaded", () => {
  // Handle navigation clicks
  document.addEventListener("click", (e) => {
    const link = e.target.closest("a[data-page]")
    if (link) {
      e.preventDefault()
      const page = link.dataset.page

      switch (page) {
        case "home":
          loadHomePage()
          break
        case "contact":
          loadContactPage()
          break
      }
    }
  })

  // Load initial page
  if (window.location.pathname === "/" || window.location.pathname === "") {
    loadHomePage()
  }
})

// Export functions for use in other scripts
window.AppUtils = {
  formatPrice,
  formatDate,
  generateStars,
  debounce,
  getCookie,
  showAlert,
  setButtonLoading,
  loadHomePage,
  loadCategoryProducts,
  loadProductDetail,
  loadContactPage,
}
