document.addEventListener("DOMContentLoaded", function () {
  get_all_data();
  let title = document.querySelector(".activities_title");
  title.innerHTML = "LATEST ACTIVITIES";
  let filters = document.querySelector(".filters_div");
  let form = document.querySelector("form");
  form.addEventListener("keyup", function (e) {
    if (e.key != "Enter" || e.keyCode != 13) {
      if ($("#search_title").val() != "") {
        filters.style.display = "none";
      } else {
        filters.style.display = "block";
      }
      document.querySelector(".suggestions").style.display = "flex";
      show_autocomplete();
    } else {
      filters.style.display = "block";
      document.querySelectorAll(".search_filters").forEach(function (element) {
        $(element).find("option:eq(0)").prop("selected", true);
      });
    }
  });
  form.addEventListener("submit", function () {
    display_results();
  });

  document.querySelectorAll(".search_filters").forEach(function (filter) {
    filter.addEventListener("change", function () {
      let difficulty = $("#search_difficulty")
        .children("option:selected")
        .val();
      let location = $("#search_location").children("option:selected").val();
      let category = $("#search_category").children("option:selected").val();
      let date = $("#search_date").children("option:selected").val();
      let max_people = $("#search_maxPeople").children("option:selected").val();
      let query = $("#search_title").val();

      if (
        difficulty != "" ||
        category != "" ||
        location != "" ||
        date != "" ||
        max_people != ""
      ) {
        $(".activities_content").empty();
        filter_tags(difficulty, location, category, query, date, max_people);

        let title_text = `${difficulty} ${location} ${category} ${tool} ${date} ${max_people} ACTIVITIES`;
        if (query) {
          title_text = `"${query}"` + title_text;
        }

        let text = title_text.replace("undefined", "");
        title.innerHTML = text;
      } else {
        $(".activities_content").empty();
        if (query) {
          title.innerHTML = `"${query}" ACTIVITIES`;
          get_data_by_title(query);
        } else {
          get_all_data();
          title.innerHTML = "LATEST ACTIVITIES";
        }
      }
    });
  });
});

function display_results() {
  document.querySelector(".suggestions").style.display = "none";
  let title = $("#search_title").val();
  if (title == "") {
    $(".activities_content").empty();
    document.querySelector(".activities_title").innerHTML = `LATEST ACTIVITIES`;
    get_all_data();
  } else {
    document.querySelector(".activities_title").innerHTML = `"${title}" ACTIVITIES`;
    $(".activities_content").empty();
    get_data_by_title(title);
  }
}

function get_all_data() {
  fetch(`/filter_activities/1`, {
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
            <img src="${element.image}" alt="Activity Image">
            <h4>${element.title}</h4>
            <p class="activities_date">${element.date}: ${hour}</p>
            <div class="card_footer"><p class="card_footer_item">${element.creator}</p>
            <p class="card_footer_item">${element.category}</p></div>`;
    div.addEventListener("click", function () {
      window.location.href = `/activity/${div.dataset.title}`;
    });
    content.append(div);
  }
}

function show_autocomplete() {
  let text = $("#search_title").val();
  let html = "";
  let suggestions = document.querySelector(".suggestions_list");
  if (text != "") {
    fetch(`/filter_activities/1`, {
      method: "POST",
      body: JSON.stringify({
        type: "query",
        query: text,
      }),
    })
      .then((response) => response.json())
      .then((result) => {
        counter = 0;
        for (element of result) {
          if (counter < 3) {
            html += `<p class="autocomplete_p" onclick='fun("${element["title"]}")'>${element["title"]}</p>`;
            counter++;
          } else {
            break;
          }
        }
        html += `<p class="all_results" onclick="see_all()">See all results</p>`;
        suggestions.innerHTML = html;
      });
  } else {
    suggestions.innerHTML = "";
  }

  if ($(".suggestions_list > p").length <= 1) {
    document.querySelector(".suggestions").style.display = "none";
  }
}

function get_data_by_title(title) {
  fetch(`/filter_activities/1`, {
    method: "POST",
    body: JSON.stringify({
      type: "query",
      query: title,
    }),
  })
    .then((response) => response.json())
    .then((result) => {
      if (result["ERROR"] || result.length == 0) {
        $(".activities_content").empty();
        get_all_data();
        $(".activities_content").prepend(
          "<p class='no_activities'>No matching Activities, here are some other Activities you may like:</p>"
        );
      } else {
        $(".activities_content").empty();
        show_activities(result);
      }
    });
}

function filter_tags(difficulty, location, category, query, date, max_people) {
  fetch(`/filter_activities/1`, {
    method: "POST",
    body: JSON.stringify({
      type: "filter",
      difficulty: difficulty,
      location: location,
      category: category,
      query: query,
      date: date,
      max_people: max_people,
    }),
  })
    .then((response) => response.json())
    .then((result) => {
      $(".activities_content").empty();
      if (result.length === 0) {
        get_all_data();
        $(".activities_content").prepend(
          "<p class='no_activities'>No matching Activities, here are some other Activities you may like:</p>"
        );
      } else {
        show_activities(result);
      }
    });
}

function see_all() {
  document.querySelector(".filters_div").style.display = "block";
  display_results();
}

function fun(url) {
  window.location.href = `/activity/${url}`;
}
