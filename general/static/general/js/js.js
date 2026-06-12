$('#id_sort, #id_filter').on('change', function() {
        $('#search-sort-filter').submit();
    });


$('#id_search').on('focusout', function() {
        $('#search-sort-filter').submit();
});