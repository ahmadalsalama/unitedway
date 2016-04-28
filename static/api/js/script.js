$(document).ready(function() {
	$('.download').click(function() {
		var title = $(this)[0].title;
		$.get('/parts/', {'event':$(this)[0].id}, function(data) {
			var result = [];
			for (d in data){
				result.push(data[d]);
			}
			JSONToCSVConvertor(result, title, true);
		});
	});

	setInterval(function(){ 
    	//refresh every 5 seconds
		$.get('/update/', {}, function(response) {
			for (r in response.events) {
				var e = response.events[r];
				$('#figure-' + e.id + ' article .count:first-child').html(e.count_liked);
				$('#figure-' + e.id + ' article .count:last-child').html(e.count_joined);
			}
		});
	}, 5000);
});

function JSONToCSVConvertor(JSONData, ReportTitle, ShowLabel) {
	var arrData = typeof JSONData != 'object' ? JSON.parse(JSONData) : JSONData;
	var CSV = 'sep=,' + '\r\n';
	if (ShowLabel) {
		var row = "";
		for (var index in arrData[0]) {
			row += index + ',';
		}
		row = row.slice(0, -1);
		CSV += row + '\r\n';
	}
	for (var i = 0; i < arrData.length; i++) {
		var row = "";
		for (var index in arrData[i]) {
			row += '"' + arrData[i][index] + '",';
		}
		row.slice(0, row.length - 1);
		CSV += row + '\r\n';
	}
	if (CSV == '') {
		alert("Invalid data");
		return;
	}
	var fileName = ReportTitle.replace(/ /g, "_");
	var uri = 'data:text/csv;charset=utf-8,' + escape(CSV);
	var link = document.createElement("a");
	link.href = uri;
	link.style = "visibility:hidden";
	link.download = fileName + ".csv";
	document.body.appendChild(link);
	link.click();
	document.body.removeChild(link);
}