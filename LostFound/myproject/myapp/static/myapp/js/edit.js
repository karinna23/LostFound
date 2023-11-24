document.addEventListener('DOMContentLoaded', function () {
    // Function to handle file input change event
    function handleFileInputChange(event) {
        const input = event.target;
        if (input.files && input.files[0]) {
            const reader = new FileReader();

            reader.onload = function (e) {
                const imagePreview = document.getElementById('image-preview');
                imagePreview.src = e.target.result;
                imagePreview.style.display = 'block';
            };

            reader.readAsDataURL(input.files[0]);
        }
    }

    // Attach the event listener to the file input element
    const fileInput = document.querySelector('#id_profile_pic');
    fileInput.addEventListener('change', handleFileInputChange);
});