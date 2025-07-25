/* ------------------------------------------------------------------------------
 *
 *  # Alpaca - Basic inputs
 *
 *  Demo JS code for alpaca_basic.html page
 *
 * ---------------------------------------------------------------------------- */


// Setup module
// ------------------------------

var AlpacaBasic = function() {


    //
    // Setup module components
    //

    // Alpaca examples
    var _componentAlpaca = function() {
        if (!$().alpaca) {
            console.warn('Warning - alpaca.min.js is not loaded.');
            return;
        }


        // Text input
        // ------------------------------

        // Basic example
        $('#alpaca-basic').alpaca({
            data: 'I Love Alpaca Ice Cream!',
            options: {
                focus: false
            }
        });

        // Display only view
        $('#alpaca-static').alpaca({
            data: 'I Love Alpaca Ice Cream!',
            schema: {
                type: 'string'
            },
            view: 'bootstrap-display'
        });

        // Input field label
        $('#alpaca-input-label').alpaca({
            data: 'I Love Alpaca Ice Cream!',
            options: {
                label: 'Input label',
                focus: false
            }
        });

        // Static input label
        $('#alpaca-static-label').alpaca({
            data: 'I Love Alpaca Ice Cream!',
            schema: {
                type: 'string'
            },
            options: {
                label: 'Input label'
            },
            view: 'bootstrap-display'
        });

        // Validation
        $('#alpaca-validation').alpaca({
            data: 'Mint',
            schema: {
                minLength: 3,
                maxLength: 5
            },
            options: {
                label: 'Ice Cream',
                helper: 'Your favorite ice cream?',
                size: 30,
                focus: false
            }
        });

        // Validation with predefined value
        $('#alpaca-validation-predefined').alpaca({
            data: 'Mint Chocolate',
            schema: {
                minLength: 3,
                maxLength: 5
            },
            options: {
                label: 'Ice Cream',
                helper: 'Please tell us the kind of ice cream you love most!',
                size: 30,
                focus: false,
                placeholder: 'Enter an ice cream flavor'
            }
        });

        // Disallow empty spaces
        $('#alpaca-disallow-empty').alpaca({
            schema: {
                type: 'string'
            },
            options: {
                type: 'lowercase',
                label: 'User Name',
                disallowEmptySpaces: true,
                helper: 'Type something with empty space',
                focus: false
            }
        });

        // Disallow values
        $('#alpaca-disallow-values').alpaca({
            data: 'Mickey Mantle',
            schema: {
                type: 'string',
                disallow: ['Mickey Mantle', 'Mickey']
            },
            options: {
                label: 'Name',
                focus: false
            }
        });

        // Typeahead integration
        $('#alpaca-typeahead').alpaca({
            schema: {
                type: 'string'
            },
            options: {
                type: 'text',
                label: 'Company Name',
                helper: 'Select the name of a computing company',
                placeholder: 'Enter "a"',
                focus: false,
                typeahead: {
                    config: {
                        highlight: true,
                        hint: true,
                        minLength: 1
                    },
                    datasets: {
                        type: 'local',
                        displayKey: 'value',
                        source: ['Google', 'Amazon', 'Microsoft', 'Apple', 'Spotify', 'Alpaca', 'Another company', 'Facebook']
                    }
                }
            }
        });

        // [RTL] Typeahead integration
        $('#alpaca-typeahead-rtl').alpaca({
            schema: {
                type: 'string'
            },
            options: {
                type: 'text',
                label: 'Company Name',
                helper: 'Select the name of a computing company',
                placeholder: 'Enter "a"',
                focus: false,
                fieldClass: 'typeahead-rtl',
                typeahead: {
                    config: {
                        highlight: true,
                        hint: true,
                        minLength: 1
                    },
                    datasets: {
                        type: 'local',
                        displayKey: 'value',
                        source: ['Google', 'Amazon', 'Microsoft', 'Apple', 'Spotify', 'Alpaca', 'Another company', 'Facebook']
                    }
                }
            },
            postRender: function() {
                $('.typeahead-rtl').find('.form-control').attr('dir', 'rtl');
            }
        });

        // Maxlength integration
        $('#alpaca-maxlength').alpaca({
            schema: {
                type: 'string',
                minLength: 3,
                maxLength: 25
            },
            options: {
                type: 'text',
                label: 'What is your name?',
                constrainMaxLength: true,
                constrainMinLength: true,
                showMaxLengthIndicator: true,
                focus: false
            },
            data: 'Jackie Robinson'
        });


        // Textareas
        // ------------------------------

        // Basic textarea
        $('#alpaca-textarea').alpaca({
            data: 'Ice cream or ice-cream is a frozen dessert usually made from dairy products, such as milk and cream, and often combined with fruits or other ingredients and flavours.',
            options: {
                type: 'textarea',
                label: 'Receipt',
                helper: 'Receipt for Best Homemade Ice Cream',
                rows: 4,
                cols: 80,
                focus: false
            }
        });

        // With placeholder
        $('#alpaca-textarea-placeholder').alpaca({
            options: {
                type: 'textarea',
                label: 'Receipt',
                helper: 'Receipt for Best Homemade Ice Cream',
                placeholder: 'Enter your favorite ice cream here...',
                rows: 4,
                cols: 80,
                focus: false
            }
        });

        // Display mode
        $('#alpaca-textarea-static').alpaca({
            data: 'Ice cream or ice-cream is a frozen dessert usually made from dairy products, such as milk and cream, and often combined with fruits or other ingredients and flavours.',
            options: {
                type: 'textarea',
                label: 'Receipt',
                rows: 6,
                cols: 80,
                focus: false
            },
            view: 'bootstrap-display'
        });

        // Single field render
        $('#alpaca-textarea-override').alpaca({
            data: 'My name is Dr. Jacobian and I am a neuroscientist from the Cornell University.  I\'ve perfected a DNA transcription process which ma$ it possible for the first time to use DNA nucleotides to store pedabytes of information in real-time.',
            schema: {
                type: 'string'
            },
            options: {
                type: 'textarea',
                label: 'Tell us about yourself',
                view: 'bootstrap-display'
            }
        });


        // Selects
        // ------------------------------

        // Basic select
        $('#alpaca-select').alpaca({
            data: 'coffee',
            schema: {
                enum: ['vanilla', 'chocolate', 'coffee', 'strawberry', 'mint']
            },
            options: {
                label: 'Ice cream',
                helper: 'What flavor of ice cream do you prefer?',
                focus: false
            }
        });

        // External data source
        $('#alpaca-select-external').alpaca({
            options: {
                label: 'Ice cream',
                helper: 'Guess my favorite ice cream?',
                type: 'select',
                focus: false,
                dataSource: '../../../../global_assets/demo_data/alpaca/selects.json'
            }
        });
    };

    // Alpaca with Select2
    var _componentAlpacaSelect2 = function() {
        if (!$().alpaca || !$().select2) {
            console.warn('Warning - alpaca.min.js and/or select2.min.js is not loaded.');
            return;
        }

        // Select2 select
        $('#alpaca-select2').alpaca({
            data: 'coffee',
            schema: {
                enum: ['vanilla', 'chocolate', 'coffee', 'strawberry', 'mint']
            },
            options: {
                label: 'Ice cream',
                helper: 'What flavor of ice cream do you prefer?',
                id: 'select2-basic',
                focus: false
            },
            postRender: function(control) {
                $('#select2-basic').select2({
                    minimumResultsForSearch: Infinity
                });
            }
        });

        // Select2 select with search
        $('#alpaca-select2-search').alpaca({
            data: 'coffee',
            schema: {
                enum: ['vanilla', 'chocolate', 'coffee', 'strawberry', 'mint']
            },
            options: {
                label: 'Ice cream',
                helper: 'What flavor of ice cream do you prefer?',
                id: 'select2-search',
                focus: false
            },
            postRender: function(control) {
                $('#select2-search').select2();
            }
        });
    };

    // Alpaca with Multiselect
    var _componentAlpacaMultiselect = function() {
        if (!$().alpaca || !$().multiselect) {
            console.warn('Warning - alpaca.min.js and/or bootstrap-multiselect.js is not loaded.');
            return;
        }

        // Multiselect
        $('#alpaca-multiselect').alpaca({
            data: ['Vanilla', 'Chocolate'],
            schema: {
                type: 'array',
                items: {
                    title: 'Ice Cream',
                    type: 'string',
                    enum: ['Vanilla', 'Chocolate', 'Strawberry', 'Mint'],
                    minItems: 2,
                    maxItems: 3
                }
            },
            options: {
                label: 'Ice cream',
                helper: 'Guess my favorite ice cream?',
                type: 'select',
                size: 5,
                id: 'multiselect',
                focus: false
            }
        });

        // Multiselect with remote data
        $('#alpaca-multiselect-remote').alpaca({
            options: {
                label: 'Select your favorite flavor of ice cream',
                type: 'select',
                multiple: true,
                helper: 'Guess my favorite ice cream?',
                size: 3,
                focus: false,
                id: 'multiselect-remote',
                dataSource: '../../../../global_assets/demo_data/alpaca/selects.json'
            }
        });
    };


    //
    // Return objects assigned to module
    //

    return {
        init: function() {
            _componentAlpaca();
            _componentAlpacaSelect2();
            _componentAlpacaMultiselect();
        }
    }
}();


// Initialize module
// ------------------------------

document.addEventListener('DOMContentLoaded', function() {
    AlpacaBasic.init();
});
