$(document).ready(function() {
    $.fn.select2.amd.define("SearchableSingleSelection", [
        "select2/utils",
        "select2/selection/single",
        "select2/selection/eventRelay",
        "select2/dropdown/search",
        "select2/selection/placeholder",
      ],
      function (Utils, SingleSelection, EventRelay, DropdownSearch, Placeholder) {
        var adapter = Utils.Decorate(SingleSelection, DropdownSearch, Placeholder);
        adapter = Utils.Decorate(adapter, EventRelay);
      
        adapter.prototype.render = function (data) {
            var $rendered = DropdownSearch.prototype.render.call(this, SingleSelection.prototype.render);
        
            this.$searchContainer.hide();
            this.$element.siblings('.select2').find('.selection').prepend(this.$searchContainer);
            
            $rendered.empty().append(
                "<div style='width: 100%; padding: 4px; color: gray;'>" +
                (this.options.get("placeholder") || "")
                + "</div>"
                
                );
                
                $('input.select2-search__field').prop('placeholder', 'Search here...');
            return $rendered;
        };

        var bindOrigin = adapter.prototype.bind;
        adapter.prototype.bind = function (container) {
          var self = this;
      
          bindOrigin.apply(this, arguments);
      
          container.on('open', function () {
            self.$selection.hide();
            self.$searchContainer.show();
          });
      
          container.on('close', function () {
            self.$searchContainer.hide();
            self.$selection.show();
          });
        };
      
        return adapter;
      });
      
      /*
      * A select2 adapter to show simple dropdown list without a searchbox inside
      */
      $.fn.select2.amd.define("UnsearchableDropdown", [
        "select2/utils",
        "select2/dropdown",
        "select2/dropdown/attachBody",
        "select2/dropdown/closeOnSelect"
      ],
      function (Utils, Dropdown, AttachBody, CloseOnSelect) {
        var adapter = Utils.Decorate(Dropdown, AttachBody);
        adapter = Utils.Decorate(adapter, CloseOnSelect);
        return adapter;
      });
      
    $('#searchbox').select2({
        theme: "bootstrap4",
        placeholder: 'Search here...',
        searchInputPlaceholder: 'Search state...',
        allowClear: true,
        selectionAdapter: $.fn.select2.amd.require("SearchableSingleSelection"),
        dropdownAdapter: $.fn.select2.amd.require("UnsearchableDropdown")
    });
    
    $('b[role="presentation"]').hide();
    $('#searchbox').on('select2:select', function(e) {
        window.location.href = '../for/' + e.params.data['id'];
    });
});