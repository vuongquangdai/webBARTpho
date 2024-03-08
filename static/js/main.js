$(document).ready(function () {
    var searchButton = $('#search-button');
    var suggestionList = $('#suggestion-list');
    var searchInput = $('#search-input');

    $('#search-input').on('input', function () {
        var keyword = $(this).val();
        if (keyword.length >= 1) {
            $.get('/suggest', { keyword: keyword }, function (data) {
                var suggestions = data.suggestions.slice(0, 10);
                searchButton.addClass("zindex-0");
                searchButton.addClass("border-rad-right");
                searchInput.addClass("border-rad-left");
                suggestionList.empty();
                for (var i = 0; i < suggestions.length; i++) {
                    suggestionList.append('<li> <a href="/detail/'+suggestions[i][0]+'">' + suggestions[i][3].toLowerCase() + '</a> </li>');
                }
            });
        } else {
            $('#suggestion-list').empty();
            searchButton.removeClass("border-rad-right");
            searchInput.removeClass("border-rad-left");
        }
    });
});

window.onload = function() {
    var currentPage = window.location.pathname.split("/").pop(); 
    var search = currentPage.slice(0,5);

    if (currentPage === '') {
        var header = document.querySelector('header');
        if (header) {
        var container = document.querySelector('.container');
            header.classList.add('none-box-shadow')
        }
    }

    if (currentPage === 'list') {
        var container = document.querySelector('.container');
        if (container) {
            container.classList.remove('container');
            container.classList.add('container-list');
        }
    }
};    

function saveFavoriteThesis(thesisId) {
    fetch('/thesis/' + thesisId + '/save', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: JSON.stringify({ thesis_id: thesisId }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Lỗi khi lưu luận văn');
        }
        return response.text();
    })
    .then(result => {
        var saveButton = document.querySelector('.saveThesisButton[data-thesis-id="' + thesisId + '"]');
        if (saveButton) {
            saveButton.innerHTML = '<i class="fa-solid fa-bookmark" style="color: #0d77fd;"></i>';
            saveButton.classList.remove('saveThesisButton');
            saveButton.classList.add('deleteThesisButton');
        }
    })
    .catch(error => {
        alert(error.message);
    });
}

document.addEventListener('click', function(event) {
    if (event.target.classList.contains('saveThesisButton')) {
        var thesisId = event.target.getAttribute('data-thesis-id');
        var loggedIn = "{{ 'username' in session }}";
        if (loggedIn == "False") {
            window.location.href = '/login';
        } else {
            saveFavoriteThesis(thesisId);
        }
    }
});

document.addEventListener('click', function(event) {
    if (event.target.classList.contains('deleteThesisButton')) {
        var thesisId = event.target.getAttribute('data-thesis-id');
        fetch('/delete-favorite-thesis/' + thesisId, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ thesisId: thesisId })
        })
        .then(response => {
            var deleteButton = document.querySelector('.deleteThesisButton[data-thesis-id="' + thesisId + '"]');
            if (deleteButton) {
                deleteButton.innerHTML = '<i class="fa-regular fa-bookmark"></i>';
                deleteButton.classList.remove('deleteThesisButton');
                deleteButton.classList.add('saveThesisButton');
            }
        })
        .catch(error => {
            console.error('Có lỗi xảy ra:', error);
        });
    }
});