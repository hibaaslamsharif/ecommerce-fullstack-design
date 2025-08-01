// Countdown Timer
function startCountdown(durationInSeconds) {
  let timer = durationInSeconds;
  const interval = setInterval(() => {
    const days = Math.floor(timer / (3600 * 24));
    const hours = Math.floor((timer % (3600 * 24)) / 3600);
    const minutes = Math.floor((timer % 3600) / 60);
    const seconds = Math.floor(timer % 60);

    const daysEl = document.getElementById("days");
    const hoursEl = document.getElementById("hours");
    const minutesEl = document.getElementById("minutes");
    const secondsEl = document.getElementById("seconds");
    
    if (daysEl) daysEl.textContent = days;
    if (hoursEl) hoursEl.textContent = hours;
    if (minutesEl) minutesEl.textContent = minutes;
    if (secondsEl) secondsEl.textContent = seconds;

    if (--timer < 0) clearInterval(interval);
  }, 1000);
}

// Handle category display on product list page
function handleCategoryDisplay() {
  // Only run on product list page
  if (!document.getElementById('category-title')) return;

  // Get category from URL
  const urlParams = new URLSearchParams(window.location.search);
  const category = urlParams.get('category');

  // Category display names
  const categoryNames = {
    'automobiles': 'Automobiles',
    'clothes': 'Clothes and Wear',
    'home-interiors': 'Home Interiors',
    'computer-tech': 'Computer and Tech',
    'tools': 'Tools and Equipment',
    'sports': 'Sports and Outdoor',
    'pets': 'Animal and Pets',
    'machinery': 'Machinery Tools',
    'electronics': 'Electronics and Gadgets',
    'more': 'More Categories'
  };

  // Update page title and description if category exists
  if (category && categoryNames[category]) {
    document.getElementById('category-title').textContent = categoryNames[category];
    document.getElementById('category-description').textContent = `Showing products in ${categoryNames[category].toLowerCase()}`;
    document.title = `${categoryNames[category]} | Ecommerce Store`;
  }
}

// Product List Fetch
function fetchProducts() {
  fetch('http://localhost:8000/store/api/products/')
    .then(response => response.json())
    .then(data => {
      const productList = document.getElementById('product-list');
      productList.innerHTML = '';
      data.forEach(product => {
        const item = document.createElement('li');
        item.textContent = product.name + ' - ' + product.category;
        // Add Edit/Delete buttons
        item.innerHTML += ` <button onclick="deleteProduct(${product.id})">Delete</button>`;
        item.innerHTML += ` <button onclick="editProduct(${product.id}, '${product.name}', '${product.category}')">Edit</button>`;
        productList.appendChild(item);
      });
    });
}

fetchProducts();

document.getElementById('add-product-form').addEventListener('submit', function(e) {
  e.preventDefault();
  const name = document.getElementById('product-name').value;
  const category = document.getElementById('product-category').value;
  fetch('http://localhost:8000/store/api/products/', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({name, category})
  })
  .then(response => response.json())
  .then(data => {
    fetchProducts();
    document.getElementById('add-product-form').reset();
  });
});

function deleteProduct(id) {
  fetch(`http://localhost:8000/store/api/products/${id}/`, {
    method: 'DELETE'
  })
  .then(() => fetchProducts());
}

function editProduct(id, oldName, oldCategory) {
  const name = prompt('Edit name:', oldName);
  const category = prompt('Edit category:', oldCategory);
  if (name && category) {
    fetch(`http://localhost:8000/store/api/products/${id}/`, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({name, category})
    })
    .then(() => fetchProducts());
  }
}

// Initialize
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    startCountdown(345600); // 4 days in seconds
    handleCategoryDisplay();
  });
} else {
  startCountdown(345600);
  handleCategoryDisplay();
}