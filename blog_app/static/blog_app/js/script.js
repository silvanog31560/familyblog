// MediumEditor
const elements = document.querySelectorAll('.editable'),
    editor = new MediumEditor(elements);

// convert UTC time to local
const utcDate = '2022-01-15T11:02:17Z';

const date = new Date(utcDate);

console.log(date.toLocaleString());
// long date and time?
