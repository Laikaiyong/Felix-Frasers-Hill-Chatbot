// var socket;
$(document).ready(function() {
	$('form').on('submit', function(event) {
		$.ajax({
			data : {
				name: $('.username').val(),
				message : $('#message').val()
			},
			type : 'POST',
			url : '/chatbot',
			success: function(response) {
				$("body").html(response);
			},
		})
        clearChat();
		event.preventDefault();
	});
});

// function clickButton(logkey) {
//     if (logkey.code == "Enter") {
//         $('.send-btn').click();
//     }
// }

function clearChat() {
    $('#message').val('');
}