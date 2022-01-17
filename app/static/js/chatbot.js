$(document).ready(function() {
	$('form').on('submit', function(event) {
		$.ajax({
			data : {
				message : $('#message').val()
			},
			type : 'POST',
			url : '/chatbot'
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