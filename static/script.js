document.getElementById("add-schedule").addEventListener("click", function() {
  const date = document.getElementById("date").value;
  const start = document.getElementById("start-time").value;
  const end = document.getElementById("end-time").value;

  if (date && start && end) {
    const li = document.createElement("li");
    li.textContent = `${date} | ${start} - ${end}`;
    document.getElementById("schedule-list").appendChild(li);
  }
});
