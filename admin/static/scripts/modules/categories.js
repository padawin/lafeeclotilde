loader.executeModule('categoriesAdminModule',
'B', 'config' , (B, config) => {
	var createCategoryForm = document.getElementById('create-category');
	var errorField = document.getElementById('error-message');
	var categories = document.getElementById('categories');
	var editCategForms = document.getElementsByClassName('edit-category');

	function _saveCategory(categoryNameField, url, method, resetForm) {
		function transferComplete(event) {
			const status = event.target.status;
			if (200 <= status && status <= 299) {
				if (resetForm) {
					categoryNameField.value = '';
				}
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
		request.open(method, config.api_host + url);

		request.addEventListener("load", transferComplete);
		request.send(JSON.stringify({'name': categoryNameField.value}));
	};

	function createCategory(categoryNameField) {
		_saveCategory(categoryNameField, '/category', 'POST', true);
	}

	function editCategory(categoryNameField, id_category) {
		_saveCategory(categoryNameField, '/category/' + id_category, 'PUT', false);
	}

	function deleteCategory(id_category) {
		var request = new XMLHttpRequest();
		request.open('DELETE', config.api_host + '/category/' + id_category);
		request.addEventListener("load", function() {
			window.location.reload();
		});
		request.send();
	}

	function clickCategory(e) {
		if (B.hasClass(e.target, 'show-edit-category')) {
			B.addClass('category-' + e.target.dataset.idCategory, 'hidden');
			B.removeClass('edit-category-' + e.target.dataset.idCategory, 'hidden');
		}
		else if (B.hasClass(e.target, 'cancel-edit-category')) {
			B.addClass('edit-category-' + e.target.dataset.idCategory, 'hidden');
			B.removeClass('category-' + e.target.dataset.idCategory, 'hidden');
		}
		else if (B.hasClass(e.target, 'edit-category')) {
			var form = document.getElementById(
				'edit-category-form-'+ e.target.dataset.idCategory
			);
			editCategory(form.name, form.id_category.value);
		}
		else if (B.hasClass(e.target, 'delete-category')) {
			if (confirm("Supprimer la categorie?")) {
				deleteCategory(e.target.dataset.idCategory);
			}
		}
	}

	createCategoryForm.addEventListener('submit', function (e) {
		e.preventDefault();
		createCategory(createCategoryForm.name);
	});
	categories.addEventListener('click', clickCategory);
	for (var form of editCategForms) {
		form.addEventListener('submit', function (e) {
			e.preventDefault();
			editCategory(e.target.name, e.target.id_category.value);
		});
	}
});
