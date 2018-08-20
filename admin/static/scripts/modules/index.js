loader.executeModule('indexAdminModule',
'B', 'config' , (B, config) => {
	var fileCatcher = document.getElementById('file-catcher');
	var fileInput = document.getElementById('file-input');
	var fileListDisplay = document.getElementById('file-list-display');
	var errorField = document.getElementById('upload-error');

	var fileList = [];

	B.Template.init({
		pictureProgress: {html: B.$id('picture-progress').innerHTML}
	});

	function renderFileList() {
		fileListDisplay.innerHTML = '';
		fileList.forEach(function (file, index) {
			const picHTML = B.Template.compile(
				'pictureProgress',
				{imgName: file.name, imgIndex: index}
			);
			fileListDisplay.innerHTML += picHTML;
		});
	}

	function sendFile(file, fileIndex) {
		// progress on transfers from the server to the client (downloads)
		function updateProgress (oEvent) {
			if (oEvent.lengthComputable) {
				var percentComplete = oEvent.loaded / oEvent.total * 100;
				percentComplete = parseInt(percentComplete / 10) * 10;
				B.replaceClass(
					'upload-progress-img-' + fileIndex,
					'upload-progress-' + (percentComplete - 10),
					'upload-progress-' + percentComplete,
					true
				);
			}
		}

		function transferComplete(event) {
			const status = event.target.status;
			B.addClass('img-wait-' + fileIndex, 'hidden');
			if (200 <= status && status <= 299) {
				B.removeClass('img-sent-' + fileIndex, 'hidden');
			}
			else {
				B.removeClass('img-error-' + fileIndex, 'hidden');
				let response;
				try {
					response = JSON.parse(event.target.response);
				}
				catch {
					if (event.target.status == 413) {
						response = {"message": "Fichier trop volumineux"};
					}
					else {
						response = {"message": "Erreur inconnue"};
					}
				}
				B.$id("img-error-message-" + fileIndex).innerHTML = response.message || "Erreur inconnue";
			}
		}

		B.removeClass('img-wait-' + fileIndex, 'hidden');
		var formData = new FormData();
		var request = new XMLHttpRequest();
		request.open("POST", config.api_host + '/picture');

		request.addEventListener("progress", updateProgress);
		request.addEventListener("load", transferComplete);

		formData.set('file', file);
		request.send(formData);
	};

	function submitEvent(e) {
		e.preventDefault();
		if (!fileList.length) {
			errorField.innerHTML = "Aucun fichier détecté"
			return;
		}
		fileList.forEach(function (file, index) {
			sendFile(file, index);
		});
	}

	function selectFiles() {
		fileList = [];
		for (var i = 0; i < fileInput.files.length; i++) {
			fileList.push(fileInput.files[i]);
		}
		renderFileList();
	}
	fileCatcher.addEventListener('submit', submitEvent);
	fileInput.addEventListener('change', selectFiles);
});
