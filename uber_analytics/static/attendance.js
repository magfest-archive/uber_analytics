// ----------------------------------------------------------------------------
// process attendance data from uber and create cool looking graphs of it
// ----------------------------------------------------------------------------

// convert our raw data to chart.js's format
function convert_raw_attendance_data(raw_data)
{
  // TODO: fake it, and we'll replace this later with the real data. it needs to be in this format.
  var chart_data = {
    labels: ["January", "February", "March", "April", "May", "June", "July"],
    datasets: [
      {
        label: "My First dataset",
        fillColor: "rgba(220,220,220,0.2)",
        strokeColor: "rgba(220,220,220,1)",
        pointColor: "rgba(220,220,220,1)",
        pointStrokeColor: "#fff",
        pointHighlightFill: "#fff",
        pointHighlightStroke: "rgba(220,220,220,1)",
        data: [65, 59, 80, 81, 56, 55, 40]
      },
      {
        label: "My Second dataset",
        fillColor: "rgba(151,187,205,0.2)",
        strokeColor: "rgba(151,187,205,1)",
        pointColor: "rgba(151,187,205,1)",
        pointStrokeColor: "#fff",
        pointHighlightFill: "#fff",
        pointHighlightStroke: "rgba(151,187,205,1)",
        data: [28, 48, 40, 19, 86, 27, 90]
      }
    ]
  };

  return chart_data;
}

function draw_attendance_chart(raw_data)
{
  var chart_data = convert_raw_attendance_data(raw_data);

  var ctx = $("#attendanceGraph").get(0).getContext("2d");

  var attendanceChart = new Chart(ctx).Line(chart_data);
}

function collect_all_attendance_data()
{
  var all_attendance_data = [];

  // add the current year information (which is live from the data)
  all_attendance_data.push(current_attendance_data);

  // TODO: get the other years' attendance data appended in here if they exist
  // we will eventually read this out of a JSON file or a datastore or similar.

  return all_attendance_data;
}

$( document ).ready(function() {

  var all_attendance_data = collect_all_attendance_data();

  draw_attendance_chart(all_attendance_data);
});