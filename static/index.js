const url = new URL(window.location.href);
if (url.searchParams.get("completed") === "true") {
    // 🎉 Fire confetti
    confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 }
    });

    // 🚫 Remove `?completed=true` from URL without reloading
    url.searchParams.delete("completed");
    window.history.replaceState({}, document.title, url.pathname);
}

flatpickr("#start_time", {
    enableTime: true,
    noCalendar: true,
    dateFormat: "H:i",
    time_24hr: true,
    onChange: function(selectedDates, dateStr, instance) {
      // Optional: Sync end_time minimum to start_time
      if (selectedDates.length) {
        endPicker.set('minTime', dateStr);
      }
    }
});

var endPicker = flatpickr("#end_time", {
    enableTime: true,
    noCalendar: true,
    dateFormat: "H:i",
    time_24hr: true,
});