document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("[data-booking-form]");

    if (!form) {
        return;
    }

    const checkInInput = document.getElementById("check-in-date");
    const checkOutInput = document.getElementById("check-out-date");
    const feedback = document.getElementById("date-range-feedback");
    const summary = document.getElementById("availability-summary");
    const roomResults = document.querySelector("[data-room-results]");

    const setFeedback = function (message, isValid) {
        if (!feedback) {
            return true;
        }

        feedback.textContent = message;
        feedback.classList.remove("is-valid", "is-invalid");

        if (message) {
            feedback.classList.add(isValid ? "is-valid" : "is-invalid");
        }

        return isValid;
    };

    const validateDates = function () {
        const checkInValue = checkInInput.value;
        const checkOutValue = checkOutInput.value;

        if (!checkInValue || !checkOutValue) {
            return setFeedback("Choose both dates to search for available rooms.", false);
        }

        if (checkOutValue <= checkInValue) {
            return setFeedback("Check-out must be after check-in.", false);
        }

        return setFeedback("Date range looks good. You can search for available rooms now.", true);
    };

    checkInInput.addEventListener("change", validateDates);
    checkOutInput.addEventListener("change", validateDates);

    form.addEventListener("submit", function (event) {
        if (!validateDates()) {
            event.preventDefault();
            checkOutInput.focus();
        }
    });

    if (summary && roomResults) {
        const roomCount = roomResults.children.length;
        summary.textContent = roomCount + " room" + (roomCount === 1 ? "" : "s") + " shown";
    }

    if (checkInInput.value || checkOutInput.value) {
        validateDates();
    }
});
