document.addEventListener("DOMContentLoaded", function () {
  load_activities();
});

function load_activities() {
  fetch(`/get_enrrolled_activities`, {
    method: "POST",
    body: JSON.stringify({
      type: "all",
    }),
  })
    .then((response) => response.json())
    .then((result) => {
      show_activities(result);
    });
}

function show_activities(result) {
  let content = document.querySelector(".activities_content");
  for (element of result) {
    let div = document.createElement("div");
    div.classList.add("card");
    div.classList.add("activity");
    div.dataset.aos = "fade-up";
    div.dataset.title = element.title;
    date = element.date.replace("-", "/");
    hour = element.start_hour.slice(0, -3);
    date = `${element.date[8]}${element.date[9]}/${element.date[5]}${element.date[6]}/${element.date[0]}${element.date[1]}${element.date[2]}${element.date[3]}`;

    div.innerHTML = `
            <img src="${element.image}" alt="activity image">
            <h4>${element.title}</h4>
            <p class="activities_date">${element.date}: ${hour}</p>
            <p class="creator">${element.creator}</p>
            <p class="location">${element.location}</p>
            <p class="category">${element.category}</p>`;

    div.addEventListener("click", function () {
      window.location.href = `/activity/${div.dataset.title}`;
    });
    content.append(div);
  }
}
