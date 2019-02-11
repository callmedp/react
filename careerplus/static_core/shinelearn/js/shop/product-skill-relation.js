$(document).ready(function () {

    $("#test_id").select2();
    $('#select_skills').select2({
        allowClear: true

    });
    $('#select_products').select2({
        allowClear: true
    });

    let data = [], skills = [], products = [],
        currentSkillId = null, currentProductId = null,
        invalid_keys = [], productSkillList = [], notAvailSkills=[];

    const populate_list = (data, id, name) => {
        $(id).select2({
            placeholder: `Please Select ${name}`,
            data: data.map(el => {
                return {
                    id: el['id'], text: `${el['name']}-${el['id']}`
                };
            }),
            allowClear: true,
        });
    };

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

    const handleTagDelete = (elem) => {
        const dataElem = $(elem).siblings()[0];
        const prodId = $(dataElem).data('product');
        const skillId = $(dataElem).data('skill');
        data = data.filter(item => !(item['product_id'] === parseInt(prodId) && item['skill_id'] === parseInt(skillId)));
        if (!data.length) {
            disableSubmitButton('submit_product_skills');
        }
        elem.parentNode.parentNode.removeChild(elem.parentNode);
        return false;
    };

    const resetInitials = () => {
        resetObjects('select_skills');
        resetObjects('select_products');
        emptyList('current_product_list');
        data = [], currentSkillId = null, currentProductId = null, invalid_keys = [], productSkillList = [];
    };

    const removeSkills = function (list) {
        $.each(list, function (i, item) {
            $(`#select_skills option[value=${item}]`).remove()
        })
    };

    const enableSkills = function (productId) {

        let availProdSkills = productSkillList.map(ps => (ps['skill_id']));
        removeSkills(availProdSkills);
        $('#select_skills').prop('disabled', false);
    };

    const fetchProductSkills = function (productId) {
        $.ajax({
            type: 'GET',
            url: `${site_domain}/console/api/v1/product-skills/?product_id=${productId}`,
            success: function (response) {
                emptyList('current_product_list');
                notAvailSkills = [];
                $.each(response && response['results'], function (i, item) {
                            $('#current_product_list').append(`<li class="list-group-item" value= ${item['id']}>
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
                productSkillList = response && response['results'];
                productSkillList = productSkillList.filter(ps => notAvailSkills.indexOf(ps['skill_id']) === -1);
                enableSkills(productId)

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
    Fetch skills List
     */
    $.ajax({
        type: 'GET',
        url: `${site_domain}/console/api/v1/skills/`,
        success: function (result) {
            skills = result && result['results'];
            populate_list(skills, '#select_skills', 'Skill')
        }
    });
    /*
    * Fetch product list
    * */
    $.ajax({
        type: 'GET',
        url: `${site_domain}/console/api/v1/products/`,
        success: function (result) {
            products = result && result['results'];
            populate_list(products, '#select_products', 'Product')
        }
    });
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
        let index = productSkillList.findIndex(productSkill => parseInt(productSkill['skill_id']) === parseInt(instance['skill_id']));
        if (index > -1) {
            throwMessage(`Skill already exists in the current product.`, 'alert-warning');
            return;
        }
        if ((data || []).findIndex(obj => obj['product_id'] === instance['product_id'] && obj['skill_id'] === instance['skill_id']) > -1) {
            throwMessage('This relationship has already been added for submission.', 'alert-warning');
            return;
        }
        data.push(instance);

        resetForms('add-product-skill-form');

        let skill = skills.find(skill => skill.id === instance['skill_id']);
        let product = products.find(product => product.id === instance['product_id']);

        $('#tags_1_tagsinput').append(`
                                    <span class="tag"><span data-product=${product.id} data-skill=${skill.id}>${product.name}-${skill.name}&nbsp;&nbsp;</span><a onclick=handleTagDelete(this) href="#" title="Remove tag">x</a></span>

`)
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
            throwMessage(`${invalid_keys.join(',')} ${invalid_keys.length > 1 ? 'are' : 'is'} either invalid or not provided.`, 'alert-warning');
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
                resetForms('skill-edit-modal-form');
                $('#edit-modal').modal('toggle');
                throwMessage('Update Successfully !', 'alert-success');

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
            $('#select_skills').prop('disabled', 'disabled')
        }
    }))

});