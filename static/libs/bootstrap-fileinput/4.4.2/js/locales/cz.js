/*!
 * FileInput Czech Translations
 *
 * This file must be loaded after 'fileinput.js'. Patterns in braces '{}', or
 * any HTML markup tags in the messages must not be converted or translated.
 *
 * @see http://github.com/kartik-v/bootstrap-fileinput
 *
 * NOTE: this file must be saved in UTF-8 encoding.
 */
(function ($) {
    "use strict";

    $.fn.fileinputLocales['cz'] = {
        fileSingle: 'soubor',
        filePlural: 'soubory',
        browseLabel: 'Vybrat &hellip;',
        removeLabel: 'Odstranit',
        removeTitle: 'Vyčistit vybrané soubory',
        cancelLabel: 'Storno',
        cancelTitle: 'Přerušit  nahrávání',
        uploadLabel: 'Nahrát',
        uploadTitle: 'Nahrát vybrané soubory',
        msgNo: 'Ne',
        msgNoFilesSelected: 'Nevybrány žádné soubory',
        msgCancelled: 'Zrušeno',
        msgZoomModalHeading: 'Detailní náhled',
<<<<<<< HEAD
        msgFileRequired: 'You must select a file to upload.',
        msgSizeTooSmall: 'Soubor "{name}" (<b>{size} KB</b>) je příliš malý, musí mít velikost nejméně <b>{minSize} KB</b>.',
=======
        msgFileRequired: 'You must select a file to upload.',
        msgSizeTooSmall: 'Soubor "{name}" (<b>{size} KB</b>) je příliš malý, musí mít velikost nejméně <b>{minSize} KB</b>.',
>>>>>>> 9fe5041adb8bd46e6986e2837e2f09061ff40e0d
        msgSizeTooLarge: 'Soubor "{name}" (<b>{size} KB</b>): je příliš velký - maximální povolená velikost <b>{maxSize} KB</b>.',
        msgFilesTooLess: 'Musíte vybrat nejméně <b>{n}</b> {files} souborů.',
        msgFilesTooMany: 'Počet vybraných souborů <b>({n})</b> překročil maximální povolený limit <b>{m}</b>.',
        msgFileNotFound: 'Soubor "{name}" nebyl nalezen!',
        msgFileSecured: 'Zabezpečení souboru znemožnilo číst soubor "{name}".',
        msgFileNotReadable: 'Soubor "{name}" není čitelný.',
        msgFilePreviewAborted: 'Náhled souboru byl přerušen pro "{name}".',
        msgFilePreviewError: 'Nastala chyba při načtení souboru "{name}".',
<<<<<<< HEAD
        msgInvalidFileName: 'Neplatné nebo nepovolené znaky ve jménu souboru "{name}".',
=======
        msgInvalidFileName: 'Neplatné nebo nepovolené znaky ve jménu souboru "{name}".',
>>>>>>> 9fe5041adb8bd46e6986e2837e2f09061ff40e0d
        msgInvalidFileType: 'Neplatný typ souboru "{name}". Pouze "{types}" souborů jsou podporovány.',
        msgInvalidFileExtension: 'Neplatná extenze souboru "{name}". Pouze "{extensions}" souborů jsou podporovány.',
        msgUploadAborted: 'Nahrávání souboru bylo přerušeno',
        msgUploadThreshold: 'Zpracovávám...',
<<<<<<< HEAD
        msgUploadBegin: 'Initializing...',
        msgUploadEnd: 'Done',
=======
        msgUploadBegin: 'Initializing...',
        msgUploadEnd: 'Done',
>>>>>>> 9fe5041adb8bd46e6986e2837e2f09061ff40e0d
        msgUploadEmpty: 'No valid data available for upload.',
        msgValidationError: 'Chyba ověření',
        msgLoading: 'Nahrávání souboru {index} z {files} &hellip;',
        msgProgress: 'Nahrávání souboru {index} z {files} - {name} - {percent}% dokončeno.',
        msgSelected: '{n} {files} vybráno',
        msgFoldersNotAllowed: 'Táhni a pusť pouze soubory! Vynechané {n} pustěné složk(y).',
        msgImageWidthSmall: 'Šířka obrázku "{name}", musí být alespoň {size} px.',
        msgImageHeightSmall: 'Výška obrázku "{name}", musí být alespoň {size} px.',
        msgImageWidthLarge: 'Šířka obrázku "{name}" nesmí být větší než {size} px.',
        msgImageHeightLarge: 'Výška obrázku "{name}" nesmí být větší než {size} px.',
        msgImageResizeError: 'Nelze získat rozměry obrázku pro změnu velikosti.',
        msgImageResizeException: 'Chyba při změně velikosti obrázku.<pre>{errors}</pre>',
<<<<<<< HEAD
        msgAjaxError: 'Something went wrong with the {operation} operation. Please try again later!',
        msgAjaxProgressError: '{operation} failed',
        ajaxOperations: {
            deleteThumb: 'file delete',
            uploadThumb: 'file upload',
            uploadBatch: 'batch file upload',
            uploadExtra: 'form data upload'
        },
=======
        msgAjaxError: 'Something went wrong with the {operation} operation. Please try again later!',
        msgAjaxProgressError: '{operation} failed',
        ajaxOperations: {
            deleteThumb: 'file delete',
            uploadThumb: 'file upload',
            uploadBatch: 'batch file upload',
            uploadExtra: 'form data upload'
        },
>>>>>>> 9fe5041adb8bd46e6986e2837e2f09061ff40e0d
        dropZoneTitle: 'Přetáhni soubory sem &hellip;',
        dropZoneClickTitle: '<br>(nebo klikni sem a vyber je)',
        fileActionSettings: {
            removeTitle: 'Odstranit soubor',
            uploadTitle: 'nahrát soubor',
            zoomTitle: 'zobrazit podrobnosti',
            dragTitle: 'Posunout / Přeskládat',
            indicatorNewTitle: 'Ještě nenahrál',
            indicatorSuccessTitle: 'Nahraný',
            indicatorErrorTitle: 'Chyba nahrávání',
            indicatorLoadingTitle: 'Nahrávání ...'
        },
        previewZoomButtonTitles: {
            prev: 'Zobrazit předchozí soubor',
            next: 'Zobrazit následující soubor',
            toggleheader: 'Přepnout záhlaví',
            fullscreen: 'Přepnout celoobrazovkové zobrazení',
            borderless: 'Přepnout bezrámečkové zobrazení',
            close: 'Zavřít detailní náhled'
        }
    };
})(window.jQuery);