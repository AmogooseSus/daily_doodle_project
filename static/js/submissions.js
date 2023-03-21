function updateDisplayedImage(src, drawingId, upvotes) {
  document.getElementById('displayed-image').src = src;
  document.getElementById('details-link').href = "/dailydoodle/drawing/" + drawingId;
  document.getElementById('upvotes-count').textContent = upvotes;
}