function confirmDelete() {
		    alert("Are you sure you want to delete this event?");
		}

function confirmUpdate() {
		    alert("Your event has been updated!");
		}

function showEdit() {
    hidden.style.display='inherit';
    Form.fileURL.focus();
  }

function showAttendance() {
	attendance.style.display='inherit';
	Form.fileURL.focus();
	}

function setFocus(id) {
    document.getElementById(id).focus();
}

function hideDiv() {
    shown.style.display='none';
    hidden.style.display='inherit';
    Form.fileURL.focus();
  }

function ltrim(str) {
  var chr = '15E0'
  var rgxtrim = (!chr) ? new RegExp('^\\s+') : new RegExp('^'+chr+'+');
  var leftString = str.replace(rgxtrim, '');
  /*console.log(str);
  console.log(leftString);*/
  var decString = parseInt(leftString, 16);
  console.log(decString);
}

/*
function changeActive() {
	var button = document.getElementById('edit-submit');
		button.onclick= function() {
    // this adds the 'active' class to the classes that the element already has
    var maptab = document.getElementById('maptab');
    maptab.className = maptab.className + ' active';
};
	
	var appID = document.enterAppForm.appID.value;
	if (appID>30000){
		document.getElementById("appID").innerHTML = 'List of applicable ISO controls for: ' + appID;		
	}
	//else if(appID=''){
	//	document.getElementById("appID").innerHTML = 'Please enter an application ID';		
	//}
	else{
		document.getElementById("appID").innerHTML = appID +' is not an active CMDB application';
	}
}
*/
