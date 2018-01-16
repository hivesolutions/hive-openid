// Hive Solutions Openid
// Copyright (c) 2008-2018 Hive Solutions Lda.
//
// This file is part of Hive Solutions Openid.
//
// Hive Solutions Openid is confidential and property of Hive Solutions Lda.,
// its usage is constrained by the terms of the Hive Solutions
// Confidential Usage License.
//
// Hive Solutions Openid should not be distributed under any circumstances,
// violation of this may imply legal action.
//
// If you have any questions regarding the terms of this license please
// refer to <http://www.hive.pt/licenses/>.

// __author__    = João Magalhães <joamag@hive.pt>
// __version__   = 1.0.0
// __revision__  = $LastChangedRevision$
// __date__      = $LastChangedDate$
// __copyright__ = Copyright (c) 2008-2018 Hive Solutions Lda.
// __license__   = Hive Solutions Confidential Usage License (HSCUL)

var __buttonClick = function(event) {
    // retrieves the event target
    var eventTarget = event.target;

    // retrieves the event target element
    var eventTargetElement = jQuery(eventTarget);

    if (eventTargetElement.is(".button")) {
        // retrieves the parent button
        var parentButton = eventTargetElement;
    } else {
        // retrieves the parent button
        var parentButton = eventTargetElement.parents(".button");
    }

    // retrieves the target value
    var target = parentButton.attr("target");

    // sets the new location
    jQuery(location).attr("href", target);
};

var __formSubmit = function(event) {
    // retrieves the event target
    var eventTarget = event.target;

    // retrieves the event target element
    var eventTargetElement = jQuery(eventTarget);

    if (eventTargetElement.is("form")) {
        // retrieves the parent form
        var parentForm = eventTargetElement;
    } else {
        // retrieves the parent form
        var parentForm = eventTargetElement.parents("form");
    }

    // submits the form normally
    parentForm.submit();
};

jQuery(document).ready(function() {
    // binds the click event of the button to
    // the button click function
    jQuery("div.button").bind("click", __buttonClick);

    // binds the click event of the submit button to
    // the form submit function
    jQuery("form div.submit").bind("click", __formSubmit);
});
