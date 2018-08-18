loader.executeModule('indexAdminModule',
'B', 'config' , (B, config) => {
	var fileCatcher = document.getElementById('file-catcher');
	var fileInput = document.getElementById('file-input');
	var fileListDisplay = document.getElementById('file-list-display');
	var errorField = document.getElementById('upload-error');

	var fileList = [];


	function renderFileList() {
		fileListDisplay.innerHTML = '';
		fileList.forEach(function (file, index) {
			var fileDisplayEl = document.createElement('p');
			fileDisplayEl.innerHTML = (index + 1) + ': ' + file.name;
			fileListDisplay.appendChild(fileDisplayEl);
		});
	}

	function sendFile(file) {
		var formData = new FormData();
		var request = new XMLHttpRequest();

		formData.set('file', file);
		request.open("POST", config.api_host + '/picture');
		request.send(formData);
	};

	function submitEvent(e) {
		e.preventDefault();
		if (!fileList.length) {
			errorField.innerHTML = "Aucun fichier détecté"
			return;
		}
		fileList.forEach(function (file) {
			sendFile(file);
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
