$(document).ready(function(){
	"use strict";

    $("#main-form").validate();
   
    $(document).on('submit','#main-form',function(e){
        e.preventDefault();
        $('#loading').show();
        $('#estimate').hide();
        $('#estimate-error').hide();
        $.ajax({
            type:'POST',
            url:'/api/estimate_request/',
            data: {
                full_name:$('#id_full_name').val(),
                email:$('#id_email').val(),
                url:$('#id_url').val(),

                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(response){
                handleResponse(response)
            }
        })
    });

    let handleResponse = function(response) {
        $('#loading').hide();
        if (response.currency && response.price) {
            console.log('sucesso')
            setField('price', getCurrency(response.currency, response.price))
            setField('condominium', getCurrency(response.currency, response.condominium))
            setField('iptu', getCurrency(response.currency, response.iptu))
            setField('savings', response.savings)

            $('#estimate').show();
            $('#estimate-error').hide();
        } else {
            console.log('error')
            $('#estimate').hide();
            $('#estimate-error').show();
        }
    }

    let setField = function(key, value) {
        if (value) {
            $('#' + key + '-line').show();
            $('#' + key).text(value)
        } else {
            $('#' + key + '-line').hide();
        }
    }

    let getCurrency = function(currency, value) {
        let formater = Intl.NumberFormat("pt-BR", {
            minimumFractionDigits: 2
        });
        if (value) {
            return currency + ' ' + formater.format(value)
        }
        return null
    }

    jQuery.validator.addMethod("fullName", function(value, element) {
        return value.indexOf(" ") != -1;
    }, "Informe seu nome completo.");

    jQuery.validator.addMethod("zapUrl", function(value, element) {
        return this.optional(element) || /^https:\/\/(.*)zapimoveis.com.br/.test(value);
    }, "Apenas URLs do Zap Imoveis são permitidas.");
    
    $( "#id_full_name" ).rules( "add", "fullName");
    $( "#id_url" ).rules( "add", "zapUrl");

    jQuery.extend(jQuery.validator.messages, {
        required: "Este campo &eacute; obrigatório.",
        remote: "Por favor, corrija este campo.",
        email: "Por favor, forne&ccedil;a um endere&ccedil;o eletr&ocirc;nico v&aacute;lido.",
        url: "Por favor, forne&ccedil;a uma URL v&aacute;lida.",
        date: "Por favor, forne&ccedil;a uma data v&aacute;lida.",
        dateISO: "Por favor, forne&ccedil;a uma data v&aacute;lida (ISO).",
        number: "Por favor, forne&ccedil;a um n&uacute;mero v&aacute;lido.",
        digits: "Por favor, forne&ccedil;a somente d&iacute;gitos.",
        creditcard: "Por favor, forne&ccedil;a um cart&atilde;o de cr&eacute;dito v&aacute;lido.",
        equalTo: "Por favor, forne&ccedil;a o mesmo valor novamente.",
        accept: "Por favor, forne&ccedil;a um valor com uma extens&atilde;o v&aacute;lida.",
        maxlength: jQuery.validator.format("Por favor, forne&ccedil;a n&atilde;o mais que {0} caracteres."),
        minlength: jQuery.validator.format("Por favor, forne&ccedil;a ao menos {0} caracteres."),
        rangelength: jQuery.validator.format("Por favor, forne&ccedil;a um valor entre {0} e {1} caracteres de comprimento."),
        range: jQuery.validator.format("Por favor, forne&ccedil;a um valor entre {0} e {1}."),
        max: jQuery.validator.format("Por favor, forne&ccedil;a um valor menor ou igual a {0}."),
        min: jQuery.validator.format("Por favor, forne&ccedil;a um valor maior ou igual a {0}.")
    });

});