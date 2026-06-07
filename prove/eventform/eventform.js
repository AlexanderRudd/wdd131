
const form = document.querySelector("#eventForm");
const type = document.querySelector("#type");
const output = document.querySelector("#output");
const studentID = document.querySelector("#studentID")
const accessCode = document.querySelector("#accessCode")
const studentNum = document.querySelector("#studentNum")
const guestCode = document.querySelector("#guestCode")


// Ensure they choose a date later than the current date
function isPastDate(value) {
  const today = new Date();
  const chosen = new Date(value);
  return chosen < today;
}

function updateFormFields() {
  const selectedType = type.value;

  if (selectedType === "student") {
    studentID.hidden = false;
    studentNum.required = true;
    
    accessCode.hidden = true;
    guestCode.required = false;
  } else if (selectedType === "guest") {
    // Show guest, hide student
    accessCode.hidden = false;
    guestCode.required = true;
    
    studentID.hidden = true;
    studentNum.required = false;
  } else {
    studentID.hidden = true;
    studentNum.required = false;
    
    accessCode.hidden = true;
    guestCode.required = false;
  }
}

type.addEventListener("change", updateFormFields);

form.addEventListener("submit", function (event) {
  event.preventDefault();
  output.textContent = "";

  const firstName = form.firstName.value.trim();
  const lastName = form.lastName.value.trim();
  const email = form.email.value.trim();
  const typeValue = form.type.value;
  const availableDate = form.availableDate.value;

  
    if (isPastDate(availableDate)) {
    output.textContent = "Please choose a later date.";
    return;

    if (typeValue === "student") {
    const studentIdValue = studentNum.value.trim();
    const isOnlyNumbers = /^\d+$/.test(studentIdValue); 

    if (studentIdValue.length < 9 || !isOnlyNumbers) {
      output.textContent = "Student ID must be at least 9 numbers and contain no letters.";
      return;
    }
  }

  }
  
  output.innerHTML = `
  <h2>Preference Submitted</h2>
  <p>${firstName} ${lastName}</p>
  <p>Email: ${email}</p>
  <p>Event Date: ${availableDate}</p>
  <p>Type: ${typeValue}</p>
  `;

  form.reset();
});
          