document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("fb-form");
  const input = document.getElementById("comment-input");
  const submitBtn = document.getElementById("submit-btn");
  const errorMsg = document.getElementById("error-msg");

  // disable submit if input empty
  function checkInput() {
    const val = input.value.trim();
    submitBtn.disabled = val === "";
    errorMsg.style.display = val === "" ? "block" : "none";
  }

  // initial check
  checkInput();

  // listen for typing
  input.addEventListener("input", checkInput);

  // on submit, if somehow still empty, prevent
  form.addEventListener("submit", (e) => {
    if (input.value.trim() === "") {
      e.preventDefault();
      errorMsg.textContent = "please enter a comment before submitting";
      errorMsg.style.display = "block";
    }
  });
});
