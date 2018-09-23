loader.executeModule('categoriesAdminModule',
'B', 'config' , (B, config) => {
	var createCategoryForm = document.getElementById('create-category');
	var errorField = document.getElementById('error-message');
	var categories = document.getElementById('categories');
	var editCategForms = document.getElementsByClassName('edit-category');

	function _saveCategory(categoryNameField) {
		function transferComplete(event) {
			const status = event.target.status;
			if (200 <= status && status <= 299) {
				categoryNameField.value = '';
				window.location.reload();
				return;
			}

			B.removeClass('error-message', 'hidden');
			let response;
			try {
				response = JSON.parse(event.target.response);
			}
			catch {
				response = {"message": "Erreur inconnue"};
			}
			B.$id("error-message").innerHTML = response.message || "Erreur inconnue";
		}

		if (!categoryNameField.value) {
			errorField.innerHTML = "Le nom de la categorie est obligatoire";
			return;
		}

		B.addClass('error-message', 'hidden');
		var request = new XMLHttpRequest();
		request.open("POST", config.api_host + '/category');

		request.addEventListener("load", transferComplete);
		request.send(JSON.stringify({'name': categoryNameField.value}));
	};

	function createCategory(categoryNameField) {
		_saveCategory(categoryNameField, 'POST');
	}

	createCategoryForm.addEventListener('submit', function (e) {
		e.preventDefault();
		createCategory(createCategoryForm.name);
	});
});
