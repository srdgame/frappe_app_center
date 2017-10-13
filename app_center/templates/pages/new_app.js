frappe.ready(function() {
	$("#fileuploader").uploadFile({
		url:"/api/method/app_center/upload",
		fileName:"myfile",
		onSuccess:function(files,data,xhr,pd) {
			alert(data);
		},
	});
});