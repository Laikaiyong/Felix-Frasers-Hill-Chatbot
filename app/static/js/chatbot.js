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
				const conversationDiv = document.getElementById('conversation');
				conversationDiv.scrollTop = conversationDiv.scrollHeight;
			},
		})
        clearChat();
		event.preventDefault();
	});
});

function speechToText() {
	var SpeechRecognition = SpeechRecognition || webkitSpeechRecognition;
	var recognition = new SpeechRecognition();

	recognition.onstart = function() {};

	recognition.onspeechend = function() {
		recognition.stop();
	}

	recognition.onresult = function(event) {
		var transcript = event.results[0][0].transcript;
		$('#message').val(transcript);
	};

	recognition.start();
}

function clearChat() {
    $('#message').val('');
}