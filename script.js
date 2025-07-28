function startCountdown(durationInSeconds) {
    let timer = durationInSeconds;
  
    const interval = setInterval(() => {
      const days = Math.floor(timer / (3600 * 24));
      const hours = Math.floor((timer % (3600 * 24)) / 3600);
      const minutes = Math.floor((timer % 3600) / 60);
      const seconds = Math.floor(timer % 60);
  
      document.getElementById("days").textContent = days;
      document.getElementById("hours").textContent = hours;
      document.getElementById("minutes").textContent = minutes;
      document.getElementById("seconds").textContent = seconds;
  
      if (--timer < 0) clearInterval(interval);
    }, 1000);
  }
  
  startCountdown(345600); // 4 days in seconds
  