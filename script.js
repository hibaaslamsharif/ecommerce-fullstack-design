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