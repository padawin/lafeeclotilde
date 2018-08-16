loader.executeModule('indexAdminModule',
'B', (B) => {
	var fileCatcher = document.getElementById('file-catcher');
	var fileInput = document.getElementById('file-input');
	var fileListDisplay = document.getElementById('file-list-display');

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
	};

	function submitEvent(e) {
		e.preventDefault();
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
