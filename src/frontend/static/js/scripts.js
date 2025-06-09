document.addEventListener("DOMContentLoaded", function() {

    // update thresholds values
    const warningForm = document.getElementById("lux-warning-form");
    if (warningForm) {
        warningForm.onsubmit = function(e) {
            e.preventDefault();
            const low_threshold = document.getElementById("lux-low-threshold").value;
            const high_threshold = document.getElementById("lux-high-threshold").value;
            const user_id = document.getElementById("user-id").value;

            fetch("/warnings/set_threshold", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    user_id: user_id,
                    low_threshold: low_threshold === "" ? null : Number(low_threshold),
                    high_threshold: high_threshold === "" ? null : Number(high_threshold)
                })
            })
            .then(r => r.json())
            .then(data => {
                document.getElementById("lux-warning-result").innerText = data.message || data.error;
            });
        };
    }


    let measuring = false;
    let startTime = null;
    let endTime = null;
    let timerInterval = null;
    const avgBtn = document.getElementById("average-lux-toggle");
    const avgResult = document.getElementById("average-lux-result");
    const user_id = document.getElementById("user-id").value;

    // calculate average
    avgBtn.addEventListener("click", function() {
        if (!measuring) {
            measuring = true;
            startTime = new Date();
            avgBtn.textContent = "Stop & Calculate";
            avgResult.innerText = "Measuring started at: " + startTime.toLocaleString() + "\nElapsed: 0s";

            let seconds = 0;
            timerInterval = setInterval(() => {
                seconds++;
                avgResult.innerText = "Measuring started at: " + startTime.toLocaleString() + "\nElapsed: " + seconds + "s";
            }, 1000);
        } else {
            measuring = false;
            endTime = new Date();
            avgBtn.textContent = "Start Measuring";
            clearInterval(timerInterval);
            avgResult.innerText = "Calculating average...";

            const startISO = startTime.toISOString();
            const endISO = endTime.toISOString();

            fetch(`/data/lux/average?user_id=${user_id}&start_time=${startISO}&end_time=${endISO}`)
                .then(r => r.json())
                .then(data => {
                    avgResult.innerText =
                        data.average_lux !== null
                            ? `Average: ${data.average_lux.toFixed(2)}`
                            : "No data";
                });
        }
    });

    // live lux warning
    function updateLuxWarning() {
        const user_id = document.getElementById("user-id").value;
        fetch(`/warnings/check_warning?user_id=${user_id}`)
            .then(r => r.json())
            .then(data => {
                const warningDiv = document.getElementById("lux-warning-live");
                if (data.warning) {
                    warningDiv.innerText = data.warning;
                    if (data.warning.includes("too low") || data.warning.includes("too high")) {
                        warningDiv.style.color = "red";
                    } else {
                        warningDiv.style.color = "green";
                    }
                } else {
                    warningDiv.innerText = "No warning data.";
                    warningDiv.style.color = "black";
                }
            });
    }

    setInterval(updateLuxWarning, 5000);
    updateLuxWarning();

    // show thresholds values
    fetch(`/warnings/api/thresholds?user_id=${user_id}`)
        .then(r => r.json())
        .then(data => {
            document.getElementById("current-low-threshold").innerText =
                `Current: ${data.low_threshold !== null ? data.low_threshold : 'Not set'}`;
            document.getElementById("current-high-threshold").innerText =
                `Current: ${data.high_threshold !== null ? data.high_threshold : 'Not set'}`;
        });
});