$(document).ready(function () {

    let data = [], currentSkillId = null, currentProductId = null,
        invalid_keys = [], productSkillList = [];

    const throwMessage = (message, message_class) => {
        const el = $('#warn_message');
        el.removeClass('alert-success alert-error alert-warning').addClass(message_class).show();
        el.text(message);
        el.fadeOut(2500, 'linear');
    };

    const disableSubmitButton = (elemId) => {
        $(`#${elemId}`).attr('disabled', 'disabled');
    };

    const enableSubmitButton = (elemId) => {
        $(`#${elemId}`).removeAttr('disabled', 'disabled');
    }

    const resetObjects = (elemId) => {
        $(`#${elemId}`).val('').trigger('change');

    };

    const emptyList = (elemId) => {
        document.getElementById(elemId).innerHTML = ``;

    };

    const resetForms = (elemId) => {
        $(`#${elemId}`).trigger('reset');
    }

    const resetPriority = (elemId) => {
        $(`#${elemId}`).val('1');
    }

    const resetActiveSwitch = (elemId) => {
        if (!$(`#${elemId}`).prop('checked')) {
            $(`#${elemId}`).trigger('click');
        }

    }

    const resetInitials = () => {
        resetObjects('select_skills');
        resetObjects('select_products');
        emptyList('current_product_list');
        resetPriority('priority');
        resetActiveSwitch('active');
        data = [], currentSkillId = null, currentProductId = null, invalid_keys = [], productSkillList = [];
    };

    const enableSkills = function () {
        $('#select_skills').prop('disabled', false);
    };

    const fetchProductSkills = function (productId) {
        let filter = $('#product-skill-choice option:selected').val();
        $.ajax({
            type: 'GET',
            url: `${site_domain}/console/api/v1/product-skills/?product_id=${productId}&active=${filter === "1" ? 'False' : 'True'}`,
            success: function (response) {
                emptyList('current_product_list');
                $.each(response, function (i, item) {
                        $('#current_product_list').append(`<li class="list-group-item" value="${item['id']}">
                                    <div>
                                        <label class="list-appearence">
                                          ${item['skill_name']}-${item['skill_id']}
                                        </label>
                                    </div>
                                    <div class="pull-right action-buttons float-edit ">
                                        <a href="#" data-toggle="modal"  data-target="#edit-modal" class="edit-anchor"><span
                                                class="glyphicon glyphicon-pencil edit-span"></span></a>
                                    </div>
                                </li>`)
                    }
                );
                productSkillList = response;
                enableSkills();
            }
        });
    };

    if (!data.length) {
        disableSubmitButton('submit_product_skills');
    }

    if (!currentProductId) {
        disableSubmitButton('select_skills');
    }

    /*
    * Fetch Skills
    * */

    const fetchSkillList = () => {
        $('#select_skills').select2({
            placeholder: 'Please Select Skill',
            allowClear: true,
            ajax: {
                delay: 300,
                url: `${site_domain}/console/api/v1/skills/`,
                data: function (params) {

                    let query = {
                        page: params.page || 1,
                        page_size: 10,
                        search: (params.term || '').trim()
                    };
                    if (currentProductId) query['exel_prd_skill'] = currentProductId;
                    return query;
                },
                processResults: function (data, params) {
                    params.page = params.page || 1;
                    return {
                        results: data.results.map(skill => ({
                            id: skill['id'], text: `${skill['name']}-${skill['id']}`
                        })),
                        pagination: {
                            more: (params.page * 10) < data.count
                        }
                    };
                }
            }
        });
    };
    fetchSkillList();

    /*
    * Fetch Product List 
    * */
    const fetchProductList = () => {
        $('#select_products').select2({
            placeholder: 'Please Select Product',
            allowClear: true,
            ajax: {
                delay: 300,
                url: `${site_domain}/console/api/v1/products/`,
                data: function (params) {
                    let query = {
                        page: params.page || 1,
                        page_size: 10,
                        courses: "True",
                        search: (params.term || '').trim()
                    };
                    return query;
                },
                processResults: function (data, params) {
                    params.page = params.page || 1;
                    return {
                        results: data.results.map(product => ({
                            id: product['id'], text: `${product['name']}-${product['id']}`
                        })),
                        pagination: {
                            more: (params.page * 10) < data.count
                        }
                    };
                }
            }
        });
    };

    fetchProductList();


    /*
    * Add Skills
    * */
    $('#add-product-skill-form').submit(function (event) {
        event.preventDefault();
        let instance = $(this).serializeArray().reduce((obj, item) => {
            obj['active'] = $('#active').prop('checked');
            if (item.name === 'skill_id' || item.name === 'product_id') {
                let id = item.value;
                obj[item.name] = parseInt(id)
            } else obj[item.name] = parseInt(item.value)
            return obj;
        }, {});
        invalid_keys = [];
        for (const key in instance) {
            if (isNaN(instance[key])) {
                invalid_keys.push(key);
            }
        }
        if (invalid_keys.length) {
            throwMessage(`${invalid_keys.join(',')} ${invalid_keys.length > 1 ? 'are' : 'is'} either invalid or not provided.`, 'alert-warning');
            return;
        }
        let index = (productSkillList || []).findIndex(productSkill => parseInt(productSkill['skill_id']) === parseInt(instance['skill_id']));
        if (index > -1) {
            throwMessage(`Skill already exists in the current product.`, 'alert-warning');
            return;
        }
        if ((data || []).findIndex(obj => obj['product_id'] === instance['product_id'] && obj['skill_id'] === instance['skill_id']) > -1) {
            throwMessage('This relationship has already been added for submission.', 'alert-warning');
            return;
        }
        data.push(instance);
        resetActiveSwitch('active');
        resetForms('add-product-skill-form');
        resetObjects('select_skills');
        resetPriority('priority');

        let skill = $(`#select_skills option[value=${instance['skill_id']}]`).text();
        let product = $(`#select_products option[value=${instance['product_id']}]`).text();

        $('#tags_1_tagsinput').append(`
                                    <span class="tag"><span data-product="${instance['product_id']}" data-skill="${instance['skill_id']}">${product}-${skill}&nbsp;&nbsp;</span><a class="remove-tags-input"  href="#" title="Remove tag">x</a></span>
`);
        enableSubmitButton('submit_product_skills');
    });
    /*
    * Update Product_Skill Record
    * */
    $('#skill-edit-modal-form').submit(function (event) {
        event.preventDefault();
        let instance = $(this).serializeArray().reduce((obj, item) => {
            obj['active'] = $('#ps_active').prop('checked');
            if (item.name === 'skill_id' || item.name === 'product_id') {
                let id = item.value;
                obj[item.name] = parseInt(id)
            } else obj[item.name] = parseInt(item.value)
            return obj;
        }, {});
        const ps_id = instance['ps_id'];
        delete instance['ps_id'];
        invalid_keys = [];
        for (const key in instance) {
            if (isNaN(instance[key])) {
                invalid_keys.push(key);
            }
        }
        if (invalid_keys.length) {
            throwMessage(`${invalid_keys.join(',')} ${invalid_keys.length > 1 ? ' are ' : ' is '} either invalid or not provided.`, 'alert-warning');
            return;
        }
        $.ajax({
            type: "PUT",
            url: `${site_domain}/console/api/v1/product-skills/${ps_id}/`,
            dataType: 'json',
            data: JSON.stringify(instance),
            contentType: 'application/json',
            success: function (response) {
                fetchProductSkills(instance['product_id']);
                $('#edit-modal').modal('toggle');
                throwMessage('Updated Successfully!', 'alert-success');
            }
        })
    });

    /*
    * Skills of the Current Product
    * */
    $('#current_product_list').click(function (event) {
        let elem, psId;

        if ($(event.target).hasClass('edit-anchor')) {
            elem = event.target.parentNode.parentNode;
            psId = parseInt($(elem).attr('value'))
        } else if ($(event.target).hasClass('edit-span')) {
            elem = event.target.parentNode.parentNode.parentNode;
            psId = $(elem).attr('value');
        } else return;

        // populate model with product skill items
        let psObj = (productSkillList || []).find(ps => ps.id === parseInt(psId));
        $('#ps_priority').val(psObj['priority']);

        if ((psObj['active'] === false && $('#ps_active').prop('checked')) || (psObj['active'] === true && !$('#ps_active').prop('checked'))) {
            $('#ps_active').trigger('click');
        }

        $('#ps_product_id').val(psObj['product_id']);
        $('#ps_skill_id').val(psObj['skill_id']);
        $('#ps_id').val(psObj['id']);
    });

    /*
    * Submit New product Skills Relations
    * */
    $('#submit_product_skills').click(function () {
        if (this.hasAttribute('disabled')) {
            return;
        }
        $.ajax({
            type: 'POST',
            url: `${site_domain}/console/api/v1/product-skills/`,
            data: JSON.stringify(data),
            contentType: 'application/json',
            dataType: 'json',
            success: function (response) {
                emptyList('tags_1_tagsinput');
                disableSubmitButton('submit_product_skills');
                throwMessage('Successful!', 'alert-success');
                resetInitials();
            }
        })
    });

    /*
    * On Skill Selected
    * */
    $('#select_skills').on('change', (function (el) {
        $('#skill_id').val(el.target.value);
    }));

    /*
    *  On product selected
    * */
    $('#select_products').on('change', (function (el) {
        $('#product_id').val(el.target.value);
        if (el.target.value) {
            fetchProductSkills(el.target.value);
            currentProductId = el.target.value
        } else {
            // freeze skills
            resetObjects('select_skills');
            currentProductId = null;
            emptyList('current_product_list');
            $('#select_skills').prop('disabled', 'disabled')
        }
    }));

    /*
    * remove dynamic added tags
    * */
    $(document).on("click", 'a.remove-tags-input', function () {
        const dataElem = $(this).siblings()[0];
        const prodId = $(dataElem).data('product');
        const skillId = $(dataElem).data('skill');
        data = data.filter(item => !(item['product_id'] === parseInt(prodId) && item['skill_id'] === parseInt(skillId)));
        if (!data.length) {
            disableSubmitButton('submit_product_skills');
        }
        this.parentNode.parentNode.removeChild(this.parentNode);
        return false;
    });
    /*
    * select only active or bring all given product
    * */
    $('#product-skill-choice').on('change', function () {
        if (currentProductId) {
            fetchProductSkills(currentProductId);
        }
    })


});