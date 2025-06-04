document.addEventListener("DOMContentLoaded", () => {
  const startInput = document.getElementById("start-time");
  const endInput = document.getElementById("end-time");
  const addButton = document.getElementById("add-schedule");
  const scheduleList = document.getElementById("schedule-list");

  addButton.addEventListener("click", () => {
    const start = startInput.value;
    const end = endInput.value;

    if (start && end) {
      const listItem = document.createElement("li");
      listItem.textContent = `${start} ~ ${end}`;
      scheduleList.appendChild(listItem);

      // 입력창 초기화
      startInput.value = "";
      endInput.value = "";
    } else {
      alert("시작 시간과 종료 시간을 입력해주세요.");
    }
  });
});
