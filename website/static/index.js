// function deleteNote(noteId) {
//     fetch('/delete-note', {
//         method: 'POST',
//         body: JSON.stringify({ noteId: noteId })
//     }).then((_res) => {
//         window.location.href = "/";
//     });

// }

function deleteNote(noteId) {
    const confirmed = confirm('Are you sure you want to delete this note?');
    if (confirmed) {
        fetch('/delete-note', {
            method: 'POST',
            body: JSON.stringify({ noteId: noteId })
        }).then((_res) => {
            window.location.href = "/";
        });
    }
}
