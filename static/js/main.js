var myPieChart = "";
var table = "";
async function get_data() {
  hide_table_show_loader();
  const data = get_query_data();
  res = await fetch(`${window.location.href}get_data`, {
    method: "post",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  if (res.status == 300) {
    res = await res.json();
    const loader = document.getElementById("loader");
    loader.style.display = "none";
    alert(res.message);

    return;
  }
  res = await res.json();
  console.log(res);
  let pie_data = res.pie_data;
  if (table != "") {
    table.destroy();
  }
  fill_data(res.data);
  initialize_table();
  hide_loader_show_table();
  if (myPieChart != "") {
    myPieChart.destroy();
  }
  create_pie_chart(pie_data);
}

function initialize_table() {
  $("#table").DataTable().destroy();
  table = $("#table").DataTable({
    destroy: true,
    dom: "Bfrtip",
    buttons: ["copyHtml5", "excelHtml5", "csvHtml5", "pdfHtml5"],
  });
}

function fill_data(data) {
  const tbody = document.getElementById("table-body");
  tbody.innerHTML = "";
  data.map((d) => {
    //create new row in table
    let new_row = tbody.insertRow();

    //create cell for every col
    let job_title = new_row.insertCell(0);
    let experience = new_row.insertCell(1);
    let salary = new_row.insertCell(2);
    let skill = new_row.insertCell(3);
    let company = new_row.insertCell(4);
    let location = new_row.insertCell(5);
    let link = new_row.insertCell(6);
    let applied = new_row.insertCell(7);

    //initialize value
    job_title.innerHTML = d["Job Name"];
    experience.innerHTML = d["Experience"];
    salary.innerHTML = d["Salary"];
    skill.innerHTML = d["Skill Tags"];
    company.innerHTML = d["Company"];
    location.innerHTML = d["Location"];
    link.innerHTML = `<a href=${d["Job link"]} target= "_blank">Job Link</a>`;
    applied.innerHTML = `<input type="checkbox" />`;
  });
}

function get_query_data() {
  const app_name = document.getElementById("app-name").value;
  const salary = document.getElementById("salary").value;
  const experience = document.getElementById("experience").value;
  const job_title = document.getElementById("job-title").value;

  const data = {
    salary: salary,
    app: app_name,
    experience: experience,
    "job-title": job_title,
  };
  return data;
}

function hide_table_show_loader() {
  try {
    const loader = document.getElementById("loader");
    const table = document.getElementById("table");

    table.style.display = "none";
    loader.style.display = "block";
  } catch (e) {
    console.log(e);
  }
}

function hide_loader_show_table() {
  const loader = document.getElementById("loader");
  const table = document.getElementById("table");

  table.style.display = "";
  loader.style.display = "none";
}

function create_pie_chart(pie_data) {
  var data = {
    labels: pie_data.lables,
    datasets: [
      {
        data: pie_data.size,
        backgroundColor: [
          "rgb(255, 99, 132)",
          "rgb(54, 162, 235)",
          "rgb(255, 205, 86)",
          "rgb(0, 255, 0)",
          "rgb(0, 0, 255)",
          "rgb(255, 255, 0)",
          "rgb(255, 0, 255)",
          "rgb(0, 255, 255)",
          "rgb(255, 165, 0)",
          "rgb(128, 0, 128)",
        ],
        hoverOffset: 4,
      },
    ],
  };
  const ctx = document.getElementById("skill-chart");
  myPieChart = new Chart(ctx, {
    type: "pie",
    data: data,
  });
}
