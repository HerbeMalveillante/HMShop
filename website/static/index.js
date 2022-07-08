function delete_note(note_id) {
	console.log("Deleting note " + note_id);
	fetch("/delete_note", { method: "POST", body: JSON.stringify({ note_id: note_id }) }).then((_res) => {
		window.location.href = "/";
	});
}
