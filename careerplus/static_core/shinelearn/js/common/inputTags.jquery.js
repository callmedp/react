(function ($) {

    $.fn.inputTags = function (options) {
        if (!('inputTags' in window)) {
            window.inputTags = {
                instances: []
            };
        }
        ;

        window.inputTags.methods = {
            tags: function (element, callback) {
                if (element) {
                    switch (typeof element) {
                        case 'string':
                            switch (element) {
                                case '_toString':
                                    var str = _instance.tags.toString();

                                    if (callback) {
                                        return callback(str);
                                    }
                                    return str;
                                    break;
                                case '_toObject':
                                    var obj = _instance._toObject(_instance.tags);

                                    if (callback) {
                                        return callback(obj);
                                    }
                                    return obj;
                                    break;
                                case '_toJSON':
                                    var obj = _instance._toObject(_instance.tags);
                                    var json = JSON.stringify(obj);

                                    if (callback) {
                                        return callback(json);
                                    }
                                    return json;
                                    break;
                                case '_toArray':
                                    if (callback) {
                                        return callback(_instance.tags);
                                    }
                                    return _instance.tags;
                                    break;
                            }

                            var partials = element.split(',');

                            if (partials.length > 1) {
                                var current = _instance.tags;
                                _instance.tags = current.concat(partials);
                            } else {
                                _instance.tags.push(partials[0]);
                            }
                            break;
                        case 'object':
                            var current = _instance.tags;

                            if ('[object Object]' === Object.prototype.toString.call(element)) {
                                element = Object.keys(element).map(function (k) {
                                    return element[k];
                                });
                            }

                            _instance.tags = current.concat(element);
                            break;
                        case 'function':
                            return element(_instance.tags);
                            break;
                    }

                    _instance._clean();
                    _instance._fill();
                    _instance._updateValue();

                    _instance.destroy();

                    _instance._setInstance(_instance);

                    if (callback) {
                        return callback(_instance.tags);
                    }
                }

                return _instance.tags;
            },
            event: function (method, callback) {
                _instance.options[method] = callback;
                _instance._setInstance(_instance);
            },
            options: function (key, value) {
                if (!key && !value) {
                    return _instance.options;
                }

                if (value) {
                    _instance.options[key] = value;
                    _instance._setInstance(_instance);
                } else {
                    return _instance.options[key];
                }
            },
            destroy: function () {
                var id = $(this).attr('data-uniqid');
                delete window.inputTags.instances[id];
            }
        };

        if ('object' === typeof options || !options) {
            var options = $.extend(true, {}, $.fn.inputTags.defaults, options);

            var obj = this.each(function () {
                var self = $(this);

                /* Constantes */
                self.UNIQID = Math.round(Date.now() / (Math.random() * (548 - 54) - 54));
                self.DEFAULT_CLASS = 'inputTags';
                self.ELEMENT_CLASS = self.DEFAULT_CLASS + '-' + self.UNIQID;
                self.LIST_CLASS = self.DEFAULT_CLASS + '-list';
                self.ITEM_CLASS = self.DEFAULT_CLASS + '-item';
                self.ITEM_CONTENT = '<span class="value">%s</span><i class="close-item">&times</i>';
                self.FIELD_CLASS = self.DEFAULT_CLASS + '-field';
                self.ERROR_CLASS = self.DEFAULT_CLASS + '-error';
                self.ERROR_CONTENT = '<p class="' + self.ERROR_CLASS + '">%s</p>';

                self.AUTOCOMPLETE_LIST_CLASS = self.DEFAULT_CLASS + '-autocomplete-list';
                self.AUTOCOMPLETE_ITEM_CLASS = self.DEFAULT_CLASS + '-autocomplete-item';
                self.AUTOCOMPLETE_ITEM_CONTENT = '<li class="' + self.AUTOCOMPLETE_ITEM_CLASS + '">%s</li>';

                /* Variables */
                self.options = options;
                self.keys = [13, 188, 27];
                self.tags = [];

                if (self.options.keys.length > 0) {
                    self.keys = self.keys.concat(self.options.keys);
                }

                self.init = function () {
                    self.addClass(self.ELEMENT_CLASS).attr('data-uniqid', self.UNIQID);

                    self.$element = $('.' + self.ELEMENT_CLASS);
                    self.$element.hide();

                    /* initialization */
                    self.build();
                    self.fill();
                    self.save();
                    self.edit();
                    self.destroy();
                    self._autocomplete()._init();
                    self._focus();
                };

                /*
                 * COnstruit le squelette HTML du plugin
                 */
                self.build = function () {
                    self.$html = $('<div>').addClass(self.LIST_CLASS);
                    self.$input = $('<input>').attr({
                        'type': 'text',
                        'class': self.FIELD_CLASS,
                        'placeholder' : self.options.placeholder
                    });

                    self.$html.insertAfter(self.$element).prepend(self.$input);

                    self.$list = self.$element.next('.' + self.LIST_CLASS);

                    self.$list.on('click', function (e) {
                        if ($(e.target).hasClass('inputTags-field')) {
                            return false;
                        }
                        self.$input.focus();
                    });
                };

                /*
                 * Initialise la liste des tags si des tags ont été passé en option, return false sinon
                 */
                self.fill = function () {
                    self._getDefaultValues();

                    if (0 === self.options.tags) {
                        return false;
                    }

                    self._concatenate();
                    self._updateValue();

                    self._fill();
                };

                /*
                 * Appelle la fonction _buildItem() si le tag est conforme
                 */
                self._fill = function () {
                    self.tags.forEach(function (value, i) {
                        var validate = self._validate(value, false);

                        if (true === validate || ('max' === validate && i + 1 <= self.options.max)) {
                            self._buildItem(value);
                        }
                    });
                };

                /*
                 * Supprime tous les éléments HTML représentant un tag
                 */
                self._clean = function () {
                    $('.' + self.ITEM_CLASS, self.$list).remove();
                };

                /*
                 * Adds or edits a tag based on which key the user is pressing
                 */
                self.save = function () {
                    self.$input.on('keyup', function (e) {
                        e.preventDefault();

                        var key = e.keyCode || e.which;
                        var value = self.$input.val().trim();

                        if ($.inArray(key, self.keys) < 0) {
                           if (self._autocomplete()._isSet()) {
                                self.options.autocomplete['values'] = $.grep(self.options.autocomplete['actualValues'], function(v) {
                                     return v.toLowerCase().indexOf(value.toLowerCase()) >= 0;
                                 });
                                 self._autocomplete()._build();
                                 if (self.options.autocomplete['values'].length){
                                     self._autocomplete()._show();
                                 }

                             }
                            return;
                        }

                        if (27 === key) {
                            self._cancel();

                            return false;
                        }

                        value = 188 === key ? value.slice(0, -1) : value;

                        if (!self._validate(value, true)) {
                            return false;
                        }

                        if (self.options.only && self._exists(value)) {
                            self._errors('exists');

                            return false;
                        }

                        if (self.$input.hasClass('is-edit')) {
                            var old_value = self.$input.attr('data-old-value');

                            if (old_value === value) {
                                self._cancel();
                                return true;
                            }

                            self._update(old_value, value);
                            self._clean();
                            self._fill();
                        } else {
                            if (self._autocomplete()._isSet() && self._autocomplete()._get('only')) {
                                if ($.inArray(value, self._autocomplete()._get('values')) < 0) {
                                    self._autocomplete()._hide();
                                    self._errors('autocomplete_only');
                                    return false;
                                }
                            }

                            if (self._exists(value)) {
                                self.$input.removeClass('is-autocomplete');
                                self._errors('exists');

                                var $tag = $('[data-tag="' + value + '"]', self.$list);

                                $tag.addClass('is-exists');

                                setTimeout(function () {
                                    $tag.removeClass('is-exists');
                                }, 300);
                                return false;
                            }

                            self._buildItem(value);
                            self._insert(value);
                        }

                        self._cancel();
                        self._updateValue();
                        self.destroy();
                        self._autocomplete()._build();

                        self._setInstance(self);
                        if (self._autocomplete()._isSet()) {
                            self.options.autocomplete['values'] = self.options.autocomplete['actualValues'];
                        }
                        self.$input.focus();

                        return false;
                    });
                };

                /*
                 * Initializes the edit field when clicking on the HTML element representing a tag
                 */
                self.edit = function () {
                    self.$list.on('click', '.' + self.ITEM_CLASS, function (e) {
                        if ($(e.target).hasClass('close-item') || false === self.options.editable || (self._autocomplete()._isSet() && self._autocomplete()._get('only'))) {
                            self._cancel();
                            return true;
                        }

                        var $item = $(this).addClass('is-edit');
                        var value = $('.value', $item).text();

                        self.$input.width($item.outerWidth()).insertAfter($item).addClass('is-edit').attr('data-old-value', value).val(value).focus();

                        self._bindEvent('selected');

                        self.$input.on('blur', function () {
                            self._cancel();
                            self._bindEvent('unselected');
                        });
                    });
                };

                /*
                 * Deletes a tag when clicking on the HTML element representing a tag
                 */
                self.destroy = function () {
                    $('.' + self.ITEM_CLASS, self.$list).off('click').on('click', '.close-item', function () {

                        var $item = $(this).parent('.' + self.ITEM_CLASS);
                        var value = $('.value', $item).text();

                        $item.addClass('is-closed');

                        setTimeout(function () {
                            self._pop(value);
                            self._updateValue();
                            $item.remove();

                            self._autocomplete()._build();

                            self.$input.focus();

                            self._setInstance(self);
                            self.ismaxLength();
                        }, 200);
                    });
                };

                /*
                 * Constructs the jQuery object representing a tag and injects it into the HTML list
                 */
                self._buildItem = function (value) {
                    var $content = $(self.ITEM_CONTENT.replace('%s', value));
                    var $item = $('<span>').addClass(self.ITEM_CLASS + ' is-closed').attr('data-tag', value).html($content);

                    $item.insertBefore(self.$input).delay(100).queue(function () {
                        $(this).removeClass('is-closed');
                    });
                };

                /*
                 * Returns the index according to the tag if it is present in the array self.tags, false otherwise
                 */
                self._getIndex = function (value) {
                    return self.tags.indexOf(value);
                };

                /*
                 * Removes excess tags if self.options.tags.length> self.options.max
                 * Concatenates tags passed as parameters by the user.
                 */
                self._concatenate = function () {
                    if (!'boolean' === typeof self.options.max || self.options.max > 0) {
                        if (self.options.tags.length > self.options.max) {
                            self.options.tags.splice(-Math.abs(self.options.tags.length - self.options.max));
                        }
                    }

                    self.tags = self.tags.concat(self.options.tags);
                };

                self._getDefaultValues = function () {
                    if (self.$element.val().length > 0) {
                        self.tags = self.tags.concat(self.$element.val().split(','));
                    } else {
                        self.$element.attr('value', '');
                    }
                };

                /*
                 * Insert item in array self.tags
                 */
                self._insert = function (item) {
                    self.tags.push(item);

                    self._bindEvent(['change', 'create']);
                };

                self.ismaxLength = function(){
                    if(self.tags.length >= self.options.max) {
                        self.$input.hide();
                    } else {
                        self.$input.show();
                    }
                };
                /*
                 * Replace old value with new value in array self.tags
                 */
                self._update = function (old_value, new_value) {
                    var index = self._getIndex(old_value);
                    self.tags[index] = new_value;
                    self._bindEvent(['change', 'update']);
                };

                /*
                 * Removes the corresponding value element from the self.tags array
                 */
                self._pop = function (value) {
                    var index = self._getIndex(value);

                    if (index < 0) {
                        return false;
                    }

                    self.tags.splice(index, 1);

                    self._bindEvent(['change', 'destroy']);
                };

                /*
                 * Resets the input field
                 */
                self._cancel = function () {
                    $('.' + self.ITEM_CLASS).removeClass('is-edit');

                    self.$input
                        .removeClass('is-edit is-autocomplete')
                        .removeAttr('data-old-value style')
                        .val('')
                        .appendTo(self.$list);
                    self.ismaxLength();    
                };

                /*
                 * returns an object with different methods for autocompletion
                 */
                self._autocomplete = function () {
                    var values = self.options.autocomplete.values;

                    return {
                        _isSet: function () {
                            return self.options.autocomplete.actualValues.length > 0;
                        },
                        _init: function () {
                            if (!self._autocomplete()._isSet()) {
                                return false;
                            }

                            self._autocomplete()._build();
                        },
                        _build: function () {
                            if (self._autocomplete()._exists()) {
                                self.$autocomplete.remove();
                            }

                            self.$autocomplete = $('<ul>').addClass(self.AUTOCOMPLETE_LIST_CLASS);

                            self._autocomplete()._get('values').forEach(function (v, k) {
                                var li = self.AUTOCOMPLETE_ITEM_CONTENT.replace('%s', v);
                                var $item = $.inArray(v, self.tags) >= 0 ? $(li).addClass('is-disabled') : $(li);
                                $item.appendTo(self.$autocomplete);
                            });

                            self._autocomplete()._bindClick();

                            $(document)
                                .not(self.$autocomplete)
                                .on('click', function () {
                                    self._autocomplete()._hide();
                                });
                            self.$input
                                .on('keydown', function (e) {
                                    if(e.originalEvent.code == 'Tab') {
                                        self._autocomplete()._hide();    
                                    }
                                    
                                });    

                        },
                        _bindClick: function () {
                            $(self.$autocomplete).off('click').on('click', '.' + self.AUTOCOMPLETE_ITEM_CLASS, function (e) {
                                if ($(e.target).hasClass('is-disabled')) {
                                    return false;
                                }
                                self.$input.addClass('is-autocomplete').val($(this).text());
                                self._autocomplete()._hide();
                                self._bindEvent('autocompleteTagSelect');

                                var e = $.Event("keyup");
                                e.which = 13;
                                self.$input.trigger(e);
                            });
                        },
                        _show: function () {
                            if (!self._autocomplete()._isSet()) {
                                return false;
                            }

                            self.$autocomplete
                                .css({
                                    'left': self.$input[0].offsetLeft,
                                    'minWidth': self.$input.width()
                                })
                                .insertAfter(self.$input);
                            setTimeout(function () {
                                self._autocomplete()._bindClick();
                                self.$autocomplete.addClass('is-active');
                            }, 100);

                        },
                        _hide: function () {
                            self.$autocomplete.removeClass('is-active');
                        },
                        _get: function (key) {
                            return self.options.autocomplete[key];
                        },
                        _exists: function () {
                            return undefined !== self.$autocomplete;
                        }
                    };
                };

                /*
                 * Updates the value attribute of the input on which the plugin is binded
                 */
                self._updateValue = function () {
                    self.$element.attr('value', self.tags.join(','));
                };

                /*
                 * Sets the events attached to focus on the input field of a tag
                 */
                self._focus = function () {
                    self.$input.on('focus', function () {
                        /*if(self.tags.length >= self.options.max) {
                            self.$input.hide();
                            return;
                        } else {
                            self.$input.show();
                        }*/

                        self._bindEvent('focus');


                        if (self._autocomplete()._isSet() && !self.$input.hasClass('is-autocomplete')  && !self.$input.hasClass('is-edit')) {
                            // if(self.tags.length < self.options.max) {
                                self._autocomplete()._show();
                            // }
                        }
                    });
                };

                /*
                 * return arr converted to object
                 */
                self._toObject = function (arr) {
                    return arr.reduce(function (o, v, i) {
                        o[i] = v;
                        return o;
                    }, {});
                };

                /*
                 * Enables user input based on various optional settings
                 */
                self._validate = function (value, alert) {
                    var type = '', re;

                    switch (true) {
                        case !value:
                        case undefined === value:
                        case 0 === value.length:
                            self._cancel();
                            type = 'empty';
                            break;
                        case value.length > 0 && value.length < self.options.minLength:
                            type = 'minLength';
                            break;
                        case value.length > self.options.maxLength:
                            type = 'maxLength';
                            break;
                        case self.options.max > 0 && self.tags.length >= self.options.max:
                            if (!self.$input.hasClass('is-edit')) {
                                type = 'max';
                            }
                            break;
                        case self.options.email:
                            re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

                            if (!re.test(value)) {
                                type = 'email';
                            }
                            break;
                    }

                    if (type.length > 0) {
                        return alert ? self._errors(type) : type;
                    }

                    return true;
                };

                /*
                 * return true if value is in the self.tags array, false otherwise
                 */
                self._exists = function (value) {
                    return $.inArray(value, self.tags) >= 0;
                }

                /*
                 * Retrieves the message according to the type passed in parameters
                 */
                self._errors = function (type) {
                    if (0 === type.length) {
                        return false;
                    }

                    if (self._autocomplete()._exists()) {
                        self.$autocomplete.remove();
                    }

                    self._displayErrors(self.options.errors[type].replace('%s', self.options[type]), type);

                    return false;
                };

                /*
                 * Displays the error (s) if any
                 */
                self._displayErrors = function (error, type) {
                    var $error = $(self.ERROR_CONTENT.replace('%s', error)).attr('data-error', type);
                    var timeout = self.options.errors.timeout;

                    if ($('.' + self.ERROR_CLASS + '[data-error="' + type + '"]').length) {
                        return false;
                    }

                    $error.hide().insertAfter(self.$list).slideDown();

                    if (!timeout || timeout <= 0) {
                        return false;
                    }

                    $('.' + self.ERROR_CLASS).on('click', function () {
                        self._collapseErrors($(this));
                    });

                    setTimeout(function () {
                        self._collapseErrors();
                    }, timeout);
                };

                /*
                 * Clears the error (s) if any
                 */
                self._collapseErrors = function ($elem) {

                    var $obj = $elem ? $elem : $('.' + self.ERROR_CLASS);

                    $obj.slideUp(300, function () {
                        $obj.remove();
                    });
                };

                /*
                 * Returns an instance of inputTags () according to its ID
                 */
                self._getInstance = function () {
                    return window.inputTags.instances[self.UNIQID];
                };

                /*
                 * Push the value instance in the array window.inputTags.instances
                 */
                self._setInstance = function (value) {
                    window.inputTags.instances[self.UNIQID] = self;
                };

                /*
                 * Return true if elem is set in self.options, false otherwise
                 */
                self._isSet = function (elem) {
                    return undefined === self.options[elem] || false === self.options[elem] || self.options[elem].length <= 0 ? false : true;
                };

                /*
                 * Call method_name if it is set in self.options, return false otherwise
                 */
                self._callMethod = function (method_name, self) {
                    if (undefined === self.options[method_name] || 'function' !== typeof self.options[method_name]) {
                        return false;
                    }

                    self.options[method_name].apply(this, Array.prototype.slice.call(arguments, 1));
                };

                self._initEvent = function (method, callback) {
                    if (!method) {
                        return false;
                    }

                    switch (typeof method) {
                        case 'string':
                            callback(method, self);
                            break;
                        case 'object':
                            method.forEach(function (m, i) {
                                callback(m, self);
                            });
                            break;
                    }

                    return true;
                };

                self._bindEvent = function (method) {
                    return self._initEvent(method, function (m, s) {
                        self._callMethod(m, s);
                    });
                };

                self._unbindEvent = function (method) {
                    return self._initEvent(method, function (m, s) {
                        self.options[m] = false;
                    });
                };

                self.init();

                self._bindEvent('init');

                self._setInstance(self);
            });

            return {
                on: function (method, callback) {
                    window.inputTags.methods.event(method, callback);
                }
            };

        } else if (window.inputTags.methods[options]) {
            var id = $(this).attr('data-uniqid');
            var _instance = window.inputTags.instances[id];

            if (undefined === _instance) {
                return $.error("[undefined instance] No inputTags instance found.");
            }

            return window.inputTags.methods[options].apply(this, Array.prototype.slice.call(arguments, 1));
        } else {
            $.error("[undefined method] The method [" + options + "] does not exists.");
        }
    };

    $.fn.inputTags.defaults = {
        tags: [],
        keys: [],
        minLength: 2,
        maxLength: 30,
        max: 6,
        email: false,
        only: true,
        init: false,
        create: false,
        update: false,
        destroy: false,
        focus: false,
        selected: false,
        unselected: false,
        change: false,
        autocompleteTagSelect: false,
        editable: true,
        autocomplete: {
            values: [],
            only: false
        },
        errors: {
            empty: 'Attention, vous ne pouvez pas ajouter un tag vide.',
            minLength: 'Attention, votre tag doit avoir au minimum %s caractères.',
            maxLength: 'Attention, votre tag ne doit pas dépasser %s caractères.',
            max: 'Attention, le nombre de tags ne doit pas dépasser %s.',
            email: 'Attention, l\'adresse email que vous avez entré n\'est pas valide',
            exists: 'Attention, ce tag existe déjà !',
            autocomplete_only: 'Attention, vous devez sélectionner une valeur dans la liste.',
            timeout: 8000
        }
    };

})(jQuery);