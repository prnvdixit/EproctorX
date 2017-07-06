
Function EproctoringXBlock(runtime, element) {


var saveUrl = runtime.handlerUrl(element, 'save_eproc');


function save() {
        var view = this;
        view.runtime.notify('save', {state: 'start'});

        var data = {};
        $(element).find('input').each(function(index, input) {
            data[input.name] = input.value;
        });

        $.ajax({
            type: 'POST',
            url: saveUrl,
            data: JSON.stringify(data),
            success: function() {
                view.runtime.notify('save', {state: 'end'});
            }
        });
    }

    return {
        save: save
    };


