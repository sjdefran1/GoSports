function validateCreateAccount() {
    valCheck = 0;
    usersEmail = document.getElementById("email").value;
    userPassword = document.getElementById("psw").value;
    userRepeatedPassword = document.getElementById("pswRepeat").value;
    passwordCheck(userPassword, userRepeatedPassword);
    emailCheck(usersEmail);

    if(valCheck == 0) {
    //Have to comment this next line out to make selenium work
    location.href = "../HTML_Files/Account_Created.html";
	} 
    else if (valCheck == 1) {
        var labelResult=getNotificationFinalResult(true, "txtFinalResult","Passwords do not match, please try again.","Email should be in form xxx@xxx.xxx, where x is alphanumeric!");
    }
    else {
        var labelResult=getNotificationFinalResult(false, "txtFinalResult","Passwords do not match, please try again.","Email should be in form xxx@xxx.xxx, where x is alphanumeric!") ;
    }
    document.getElementById("FinalResult").appendChild(labelResult);
}

function getNotificationFinalResult(bool, ID,messageOK,messageFailed) {
    var label = document.getElementById("labelNotify" + ID);
    if (label == null) {
        label = document.createElement("LABEL");
        label.id = "labelNotify" + ID;
        label.setAttribute( 'class', 'errorMessage' );
      }

    label.innerHTML = bool ? messageOK : messageFailed;
    return label;
}

function emailCheck(email) {
    atSplit = email.split('@');
    if (atSplit.length == 2 && alphaNumCheck(atSplit[0])) {
        periodSplit = atSplit[1].split('.')
        if (periodSplit.length == 2 && alphaNumCheck(periodSplit[0] + periodSplit[1])) {
        }
        else {
            valCheck = 2;
        }
    }
    else {
        valCheck = 2;
    }
}

function passwordCheck(password, repeatedPassword) {
    if (password.localeCompare(repeatedPassword) != 0) {
        valCheck = 1;
    }
}

function alphaNumCheck(entry) {
    let regex = /^[a-z0-9]+$/i;
    if (entry != null && entry.match(regex)) {
        return true;
    } else {
        return false;
    }
}