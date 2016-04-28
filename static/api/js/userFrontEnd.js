
function showCommentBox() {
    comment.style.display='inherit';
    contact.style.display='none';
    Form.fileURL.focus();
  }

function showContact() {
    contact.style.display='inherit';
    comment.style.display='none';
    Form.fileURL.focus();
  }

function hideDiv() {
    shown.style.display='none';
    hidden.style.display='inherit';
    Form.fileURL.focus();
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
