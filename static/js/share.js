function shareButton() {
  navigator.clipboard
    .writeText(window.location.href)
    .then(() => {
      alert("URL copied to clipboard!");
    })
    .catch((err) => {
      alert("Error in copying URL: ", err);
    });
}
