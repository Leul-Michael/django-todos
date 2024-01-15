const forms = document.querySelectorAll("#form")
if (forms.length > 0) {
  forms.forEach((form) => {
    form.addEventListener("submit", () => {
      const submitButton = form.querySelector("button")
      submitButton && (submitButton.disabled = true)
    })
  })
}

const formButtons = document.querySelectorAll("#form-btn")

if (formButtons.length > 0) {
  formButtons.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.stopPropagation()
    })
  })
}

const closeBtns = document.querySelectorAll("#close-toast")
if (closeBtns.length > 0) {
  closeBtns.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      if (e.target.parentElement.parentElement)
        e.target.parentElement.parentElement.remove()
    })
  })
}

const activeList = document.querySelector("#active-list")
if (activeList) {
  activeList.scrollIntoView()
}
