//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Event Handlers

// Click the "real" input
upload_file_buttton.addEventListener('click', () => {
    file_input.click();
});

// Read file data
file_input.addEventListener('change', function() {

    var fr = new FileReader();
    fr.onload = function(){
        console.log("Got file!");

        resLen = fr.result.length

        // Check proper file length
        if (resLen < 20 || resLen > 5000) {
            alertStr = "Input length cannot be less than 20 or more than 5000 characters. Current length: " + fr.result.length;
            showAlert(article_alert, alertStr, "red", "fa-exclamation-triangle")
        }
        else{
            // Make sure this is NOT a binary file
            if (fr.result.match(/[^\u0000-\u007f]/)){
                showAlert(article_alert, "File must be plain text!", "red", "fa-exclamation-triangle")
            }
            else{
                // Create new article
                setArticle(String(+ new Date()), fr.result);
            }
        }
    }

    // Reads as plain text
    fr.readAsText(this.files[0]);
})